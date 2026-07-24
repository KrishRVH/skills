import { createHash } from "node:crypto";
import {
  existsSync,
  lstatSync,
  readFileSync,
  readdirSync,
  realpathSync,
} from "node:fs";
import {
  basename,
  extname,
  join,
  posix,
  resolve,
} from "node:path";

import { decodeHTML } from "entities";
import { parseTree } from "jsonc-parser";
import { load as parseYaml } from "js-yaml";
import MarkdownIt from "markdown-it";

const ALLOWED_FRONTMATTER_KEYS = new Set([
  "description",
  "disable-model-invocation",
  "name",
]);
const SUPPORT_DIRECTORIES = new Set([
  "assets",
  "examples",
  "helpers",
  "references",
  "templates",
]);
const KEBAB_CASE = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const SHA256 = /^[a-f0-9]{64}$/;
const MAX_NAME_CHARACTERS = 64;
const MAX_DESCRIPTION_CHARACTERS = 1024;
const MAX_SKILL_LINES = 500;
const MAX_SKILL_BYTES = 50_000;
const MAX_SUPPORT_MARKDOWN_BYTES = 100_000;
const MAX_REFERENCE_LINES_WITHOUT_CONTENTS = 100;
const markdownParser = new MarkdownIt({
  html: true,
  linkify: false,
  typographer: false,
});
const defaultLinkValidator =
  markdownParser.validateLink.bind(markdownParser);
markdownParser.validateLink = (destination) => {
  return (
    /^file:/i.test(destination) ||
    /^[A-Za-z]:(?:[\\/]|%5[cC]|%2[fF])/.test(destination) ||
    defaultLinkValidator(destination)
  );
};

export function validateRepository(rootDirectory, options = {}) {
  const root = realpathSync(resolve(rootDirectory));
  const errors = [];
  const add = (code, path, message) => {
    errors.push({ code, message, path });
  };
  const config = normalizeConfig(
    options.config ?? readConfig(root, add),
    add,
  );
  const git = gitContext(root, add);
  const repositoryFiles = listRepositoryFiles(root, git, add);
  const rootEntries = listRootEntries(root, git, add);
  const topLevelSymlinks = new Set(
    rootEntries
      .filter(({ symlink }) => symlink)
      .map(({ name }) => name),
  );
  const foldersWithFiles = new Set(
    repositoryFiles
      .filter((path) => path.includes("/"))
      .map((path) => path.split("/", 1)[0]),
  );
  const skillFolders = rootEntries
    .filter(({ ignored, name, portableDirectory }) => {
      return (
        !name.startsWith(".") &&
        portableDirectory &&
        (!ignored || foldersWithFiles.has(name))
      );
    })
    .map(({ name }) => name)
    .sort();
  const skillFolderSet = new Set(skillFolders);
  const metadataByFolder = new Map();

  for (const configuredFolder of Object.keys(config.frozenSkills)) {
    if (!skillFolderSet.has(configuredFolder)) {
      add(
        "frozen.files",
        configuredFolder,
        "The configured frozen package is missing.",
      );
    }
  }

  for (const folder of skillFolders) {
    const packagePrefix = `${folder}/`;
    const packageFiles = repositoryFiles
      .filter((path) => path.startsWith(packagePrefix))
      .map((path) => path.slice(packagePrefix.length))
      .sort();
    const frozen = Object.hasOwn(config.frozenSkills, folder)
      ? config.frozenSkills[folder]
      : undefined;

    if (topLevelSymlinks.has(folder)) {
      add(
        "package.symlink",
        folder,
        "A skill package must be a real directory, not a symlink.",
      );
      if (frozen) {
        validateFrozenPackage(root, folder, packageFiles, frozen, add, {
          hashFiles: false,
        });
      }
      continue;
    }

    if (!packageFiles.includes("SKILL.md")) {
      add(
        "repository.skill-entry",
        folder,
        "Every visible, non-ignored top-level directory must contain SKILL.md.",
      );
    }

    validatePackageLayout(root, folder, packageFiles, add);

    if (frozen) {
      validateFrozenPackage(root, folder, packageFiles, frozen, add);
    }

    const skillPath = join(root, folder, "SKILL.md");
    if (!existsSync(skillPath)) {
      continue;
    }
    const skillStat = lstatSync(skillPath);
    if (skillStat.isSymbolicLink() || !skillStat.isFile()) {
      continue;
    }
    if (!frozen && skillStat.size > MAX_SKILL_BYTES) {
      add(
        "skill.size",
        `${folder}/SKILL.md`,
        `SKILL.md has ${skillStat.size} UTF-8 bytes; the maximum is ${MAX_SKILL_BYTES}.`,
      );
      continue;
    }

    const skillText = readFileSync(skillPath, "utf8");
    const metadata = validateFrontmatter(
      skillText,
      `${folder}/SKILL.md`,
      add,
    );
    if (metadata) {
      metadataByFolder.set(folder, metadata);
      const expectedName = frozen?.name ?? folder;
      if (metadata.name !== expectedName) {
        add(
          "package.name",
          `${folder}/SKILL.md`,
          `Frontmatter name must be "${expectedName}".`,
        );
      }
    }

    if (frozen) {
      continue;
    }

    validateSkillContent(skillText, `${folder}/SKILL.md`, add);
    validateReferenceContent(root, folder, packageFiles, add);
    validateSupportGraph(root, folder, packageFiles, add);
    validateVendorNeutrality(
      root,
      folder,
      packageFiles,
      config.forbiddenTerms,
      add,
    );
  }

  validateUniqueNames(metadataByFolder, add);
  validateReadme(root, skillFolders, add);

  return uniqueSortedErrors(errors);
}

function normalizeConfig(rawConfig, add) {
  const normalized = {
    forbiddenTerms: [],
    frozenSkills: Object.create(null),
  };

  if (
    rawConfig === null ||
    typeof rawConfig !== "object" ||
    Array.isArray(rawConfig)
  ) {
    add(
      "config.format",
      ".config/skills/validation.json",
      "Validation configuration must be a JSON object.",
    );
    return normalized;
  }

  for (const key of Object.keys(rawConfig)) {
    if (key !== "forbiddenTerms" && key !== "frozenSkills") {
      add(
        "config.format",
        ".config/skills/validation.json",
        `Unsupported validation configuration key "${key}".`,
      );
    }
  }

  if (!Array.isArray(rawConfig.forbiddenTerms)) {
    add(
      "config.format",
      ".config/skills/validation.json",
      "forbiddenTerms must be an array.",
    );
  } else {
    for (const term of rawConfig.forbiddenTerms) {
      if (typeof term !== "string" || term.trim() === "") {
        add(
          "config.format",
          ".config/skills/validation.json",
          "Each forbidden term must be a nonempty string.",
        );
        continue;
      }
      normalized.forbiddenTerms.push(term);
    }
  }

  if (
    rawConfig.frozenSkills === null ||
    typeof rawConfig.frozenSkills !== "object" ||
    Array.isArray(rawConfig.frozenSkills)
  ) {
    add(
      "config.format",
      ".config/skills/validation.json",
      "frozenSkills must be an object.",
    );
    return normalized;
  }

  for (const [folder, frozen] of Object.entries(rawConfig.frozenSkills)) {
    if (!KEBAB_CASE.test(folder)) {
      add(
        "config.format",
        ".config/skills/validation.json",
        `Frozen skill folder "${folder}" is not lowercase kebab-case.`,
      );
      continue;
    }
    if (
      frozen === null ||
      typeof frozen !== "object" ||
      Array.isArray(frozen) ||
      typeof frozen.name !== "string" ||
      !KEBAB_CASE.test(frozen.name) ||
      frozen.files === null ||
      typeof frozen.files !== "object" ||
      Array.isArray(frozen.files)
    ) {
      add(
        "config.format",
        ".config/skills/validation.json",
        `Frozen skill "${folder}" must define a portable name and file hashes.`,
      );
      continue;
    }

    for (const key of Object.keys(frozen)) {
      if (key !== "files" && key !== "name") {
        add(
          "config.format",
          ".config/skills/validation.json",
          `Unsupported frozen-skill key "${folder}.${key}".`,
        );
      }
    }

    const files = {};
    for (const [path, digest] of Object.entries(frozen.files)) {
      const normalizedPath = posix.normalize(path);
      if (
        path !== normalizedPath ||
        posix.isAbsolute(path) ||
        normalizedPath === ".." ||
        normalizedPath.startsWith("../") ||
        typeof digest !== "string" ||
        !SHA256.test(digest)
      ) {
        add(
          "config.format",
          ".config/skills/validation.json",
          `Frozen file entry "${folder}/${path}" is invalid.`,
        );
        continue;
      }
      files[path] = digest;
    }
    if (!Object.hasOwn(files, "SKILL.md")) {
      add(
        "config.format",
        ".config/skills/validation.json",
        `Frozen skill "${folder}" must include a SKILL.md hash.`,
      );
    }
    normalized.frozenSkills[folder] = { files, name: frozen.name };
  }

  return normalized;
}

function readConfig(root, add) {
  const relativePath = ".config/skills/validation.json";
  const path = join(root, relativePath);
  try {
    const source = readFileSync(path, "utf8");
    validateJsonDuplicates(source, relativePath, add);
    return JSON.parse(source);
  } catch (error) {
    add(
      "config.format",
      relativePath,
      `Could not read valid JSON: ${error.message}`,
    );
    return { forbiddenTerms: [], frozenSkills: {} };
  }
}

function validateJsonDuplicates(source, path, add) {
  const parseErrors = [];
  const tree = parseTree(source, parseErrors, {
    allowTrailingComma: false,
    disallowComments: true,
  });
  if (tree === undefined || parseErrors.length > 0) {
    return;
  }

  const visit = (node, segments) => {
    if (node.type === "object") {
      const seen = new Set();
      for (const property of node.children ?? []) {
        const key = property.children?.[0]?.value;
        const value = property.children?.[1];
        if (seen.has(key)) {
          add(
            "config.format",
            path,
            `Duplicate JSON key "${[...segments, key].join(".")}".`,
          );
        }
        seen.add(key);
        if (value) {
          visit(value, [...segments, key]);
        }
      }
    } else if (node.type === "array") {
      for (const child of node.children ?? []) {
        visit(child, segments);
      }
    }
  };
  visit(tree, []);
}

function gitContext(root, add) {
  const result = Bun.spawnSync(
    ["git", "rev-parse", "--show-toplevel"],
    { cwd: root, stderr: "ignore", stdout: "pipe" },
  );
  if (result.exitCode !== 0) {
    return null;
  }

  const topLevel = result.stdout.toString().replace(/\r?\n$/, "");
  try {
    return realpathSync(resolve(topLevel)) === root ? { root } : null;
  } catch (error) {
    add(
      "repository.git",
      ".",
      `Could not resolve Git's repository root: ${error.message}`,
    );
    return null;
  }
}

function listRepositoryFiles(root, git, add) {
  if (git) {
    const result = Bun.spawnSync(
      [
        "git",
        "ls-files",
        "--cached",
        "--others",
        "--exclude-standard",
        "-z",
        "--",
        ".",
      ],
      { cwd: root, stderr: "ignore", stdout: "pipe" },
    );
    if (result.exitCode === 0) {
      return splitGitPaths(result.stdout, add)
        .filter((path) => {
          try {
            lstatSync(join(root, path));
            return true;
          } catch (error) {
            if (error.code !== "ENOENT") {
              add(
                "repository.path",
                path,
                `Could not inspect repository path: ${error.message}`,
              );
            }
            return false;
          }
        })
        .sort();
    }
  }

  const files = [];
  walk(root, "", files, add);
  return files.sort();
}

function splitGitPaths(stdout, add) {
  const bytes = Buffer.from(stdout);
  const paths = [];
  let start = 0;

  for (let index = 0; index <= bytes.length; index += 1) {
    if (index !== bytes.length && bytes[index] !== 0) {
      continue;
    }
    const encodedPath = bytes.subarray(start, index);
    start = index + 1;
    if (encodedPath.length === 0) {
      continue;
    }
    const path = decodePath(encodedPath, add);
    if (path !== null) {
      paths.push(path);
    }
  }
  return paths;
}

function decodePath(encodedPath, add) {
  try {
    return new TextDecoder("utf-8", { fatal: true }).decode(encodedPath);
  } catch {
    const preview = Buffer.from(encodedPath)
      .toString("hex")
      .slice(0, 128);
    add(
      "repository.path",
      ".",
      `Repository contains a non-UTF-8 path (hex prefix: ${preview}).`,
    );
    return null;
  }
}

function walk(root, relativeDirectory, files, add) {
  const absoluteDirectory = join(root, relativeDirectory);
  for (const encodedName of readdirSync(absoluteDirectory, {
    encoding: "buffer",
  })) {
    const name = decodePath(encodedName, add);
    if (name === null) {
      continue;
    }
    if (relativeDirectory === "" && name.startsWith(".")) {
      continue;
    }
    const relativePath = relativeDirectory
      ? `${relativeDirectory}/${name}`
      : name;
    const stat = lstatSync(join(root, relativePath));
    if (stat.isDirectory()) {
      walk(root, relativePath, files, add);
    } else if (stat.isFile() || stat.isSymbolicLink()) {
      files.push(relativePath);
    }
  }
}

function listRootEntries(root, git, add) {
  const entries = [];
  for (const encodedName of readdirSync(root, { encoding: "buffer" })) {
    const name = decodePath(encodedName, add);
    if (name === null) {
      continue;
    }
    const stat = lstatSync(join(root, name));
    const ignored = git ? gitIgnores(root, name) : false;
    entries.push({
      ignored,
      name,
      portableDirectory: stat.isDirectory() || stat.isSymbolicLink(),
      symlink: stat.isSymbolicLink(),
    });
  }
  return entries;
}

function gitIgnores(root, path) {
  const result = Bun.spawnSync(
    ["git", "check-ignore", "--quiet", "--", path],
    { cwd: root, stderr: "ignore", stdout: "ignore" },
  );
  return result.exitCode === 0;
}

function validatePackageLayout(root, folder, packageFiles, add) {
  for (const relativePath of packageFiles) {
    const path = `${folder}/${relativePath}`;
    const absolutePath = join(root, path);
    const stat = lstatSync(absolutePath);

    if (stat.isSymbolicLink()) {
      add(
        "package.symlink",
        path,
        "Skill packages must not contain symlinks.",
      );
      continue;
    }

    if (relativePath === "SKILL.md") {
      continue;
    }

    const segments = relativePath.split("/");
    if (segments.length < 2 || !SUPPORT_DIRECTORIES.has(segments[0])) {
      add(
        "package.layout",
        path,
        "Supporting files must live in an allowed support directory.",
      );
      continue;
    }

    if (segments[0] === "templates") {
      const extension = extname(relativePath);
      const expectedName = `${folder.toUpperCase()}${extension}`;
      if (extension === "" || basename(relativePath) !== expectedName) {
        add(
          "package.template-name",
          path,
          `Template filename must be "${expectedName}".`,
        );
      }
    }
  }
}

function validateFrozenPackage(
  root,
  folder,
  packageFiles,
  frozen,
  add,
  options = {},
) {
  const expectedFiles = Object.keys(frozen.files).sort();
  if (
    expectedFiles.length !== packageFiles.length ||
    expectedFiles.some((path, index) => path !== packageFiles[index])
  ) {
    add(
      "frozen.files",
      folder,
      `Frozen file set must be exactly: ${expectedFiles.join(", ")}.`,
    );
  }

  if (options.hashFiles === false) {
    return;
  }

  for (const [relativePath, expectedDigest] of Object.entries(frozen.files)) {
    const path = join(root, folder, relativePath);
    if (
      !existsSync(path) ||
      lstatSync(path).isSymbolicLink() ||
      !lstatSync(path).isFile()
    ) {
      continue;
    }
    const actualDigest = createHash("sha256")
      .update(readFileSync(path))
      .digest("hex");
    if (actualDigest !== expectedDigest) {
      add(
        "frozen.hash",
        `${folder}/${relativePath}`,
        `Frozen SHA-256 must remain ${expectedDigest}.`,
      );
    }
  }
}

function validateFrontmatter(text, path, add) {
  const match = text.match(
    /^---[ \t]*\r?\n([\s\S]*?)\r?\n---[ \t]*(?:\r?\n|$)/,
  );
  if (!match) {
    add(
      "frontmatter.format",
      path,
      "SKILL.md must begin with a closed YAML frontmatter block.",
    );
    return null;
  }

  const source = match[1];
  let metadata;
  try {
    metadata = parseYaml(source);
  } catch (error) {
    const duplicate = /duplicated mapping key/i.test(error.message);
    add(
      duplicate ? "frontmatter.duplicate" : "frontmatter.format",
      path,
      `Frontmatter is not valid YAML: ${error.message}`,
    );
    return null;
  }

  if (
    metadata === null ||
    typeof metadata !== "object" ||
    Array.isArray(metadata)
  ) {
    add(
      "frontmatter.format",
      path,
      "Frontmatter must be a YAML mapping.",
    );
    return null;
  }

  for (const key of Object.keys(metadata)) {
    if (!ALLOWED_FRONTMATTER_KEYS.has(key)) {
      add(
        "frontmatter.key",
        path,
        `Unsupported frontmatter key "${key}".`,
      );
    }
  }

  const name = metadata.name;
  if (
    typeof name !== "string" ||
    !KEBAB_CASE.test(name) ||
    Array.from(name).length > MAX_NAME_CHARACTERS
  ) {
    add(
      "frontmatter.name",
      path,
      `name must be lowercase kebab-case and at most ${MAX_NAME_CHARACTERS} characters.`,
    );
  }

  const description = metadata.description;
  if (
    typeof description !== "string" ||
    description.trim() === "" ||
    Array.from(description).length > MAX_DESCRIPTION_CHARACTERS
  ) {
    add(
      "frontmatter.description",
      path,
      `description must be a nonempty string of at most ${MAX_DESCRIPTION_CHARACTERS} characters.`,
    );
  }

  if (
    Object.hasOwn(metadata, "disable-model-invocation") &&
    typeof metadata["disable-model-invocation"] !== "boolean"
  ) {
    add(
      "frontmatter.invocation",
      path,
      "disable-model-invocation must be a boolean when present.",
    );
  }

  return typeof name === "string" ? { name } : null;
}

function validateUniqueNames(metadataByFolder, add) {
  const foldersByName = new Map();
  for (const [folder, { name }] of metadataByFolder) {
    const folders = foldersByName.get(name) ?? [];
    folders.push(folder);
    foldersByName.set(name, folders);
  }

  for (const [name, folders] of foldersByName) {
    if (folders.length > 1) {
      for (const folder of folders) {
        add(
          "frontmatter.name",
          `${folder}/SKILL.md`,
          `Portable skill name "${name}" is also used by ${folders
            .filter((candidate) => candidate !== folder)
            .join(", ")}.`,
        );
      }
    }
  }
}

function validateSkillContent(text, path, add) {
  const lines = countLines(text);
  if (lines > MAX_SKILL_LINES) {
    add(
      "skill.length",
      path,
      `SKILL.md has ${lines} lines; the maximum is ${MAX_SKILL_LINES}.`,
    );
  }
}

function validateReferenceContent(root, folder, packageFiles, add) {
  for (const relativePath of packageFiles) {
    if (
      extname(relativePath).toLowerCase() !== ".md" ||
      !SUPPORT_DIRECTORIES.has(relativePath.split("/")[0])
    ) {
      continue;
    }
    const path = join(root, folder, relativePath);
    const stat = lstatSync(path);
    if (stat.isSymbolicLink() || !stat.isFile()) {
      continue;
    }
    if (stat.size > MAX_SUPPORT_MARKDOWN_BYTES) {
      add(
        "support.size",
        `${folder}/${relativePath}`,
        `Support Markdown has ${stat.size} UTF-8 bytes; the maximum is ${MAX_SUPPORT_MARKDOWN_BYTES}.`,
      );
      continue;
    }
    if (!relativePath.startsWith("references/")) {
      continue;
    }
    const text = readFileSync(path, "utf8");
    const lines = countLines(text);
    if (
      lines > MAX_REFERENCE_LINES_WITHOUT_CONTENTS &&
      !hasContentsNavigation(text)
    ) {
      add(
        "reference.contents",
        `${folder}/${relativePath}`,
        `Reference Markdown over ${MAX_REFERENCE_LINES_WITHOUT_CONTENTS} lines needs a Contents section with a same-document link.`,
      );
    }
  }
}

function hasContentsNavigation(markdown) {
  const tokens = markdownParser.parse(markdown, {});
  let inContents = false;

  for (let index = 0; index < tokens.length; index += 1) {
    const token = tokens[index];
    if (token.type === "heading_open" && token.tag === "h2") {
      const title = tokens[index + 1]?.content?.trim().toLowerCase();
      inContents =
        title === "contents" || title === "table of contents";
      continue;
    }
    if (!inContents || token.type !== "inline") {
      continue;
    }
    for (const child of token.children ?? []) {
      if (
        child.type === "link_open" &&
        child.attrGet("href")?.startsWith("#")
      ) {
        return true;
      }
    }
  }
  return false;
}

function validateSupportGraph(root, folder, packageFiles, add) {
  const regularFiles = new Set(
    packageFiles.filter((relativePath) => {
      const path = join(root, folder, relativePath);
      const stat = lstatSync(path);
      return stat.isFile() && !stat.isSymbolicLink();
    }),
  );
  const supportFiles = [...regularFiles].filter(
    (relativePath) =>
      relativePath !== "SKILL.md" &&
      SUPPORT_DIRECTORIES.has(relativePath.split("/")[0]),
  );
  const visited = new Set();
  const queue = regularFiles.has("SKILL.md") ? ["SKILL.md"] : [];

  while (queue.length > 0) {
    const sourcePath = queue.shift();
    if (visited.has(sourcePath)) {
      continue;
    }
    visited.add(sourcePath);
    if (extname(sourcePath).toLowerCase() !== ".md") {
      continue;
    }

    const sourceFile = join(root, folder, sourcePath);
    if (
      sourcePath !== "SKILL.md" &&
      lstatSync(sourceFile).size > MAX_SUPPORT_MARKDOWN_BYTES
    ) {
      continue;
    }
    const source = readFileSync(sourceFile, "utf8");
    for (const destination of markdownDestinations(source)) {
      const resolved = resolvePackageLink(sourcePath, destination);
      if (resolved === null) {
        continue;
      }
      if (resolved.escape) {
        add(
          "package.link-escape",
          `${folder}/${sourcePath}`,
          `Local link "${destination}" escapes the skill package.`,
        );
        continue;
      }
      if (regularFiles.has(resolved.path) && !visited.has(resolved.path)) {
        queue.push(resolved.path);
      }
    }
  }

  for (const relativePath of supportFiles) {
    if (!visited.has(relativePath)) {
      add(
        "package.orphan",
        `${folder}/${relativePath}`,
        "Support file is not reachable from SKILL.md through Markdown links.",
      );
    }
  }
}

function markdownDestinations(markdown) {
  const destinations = [];
  const queue = [...markdownParser.parse(markdown, {})];
  while (queue.length > 0) {
    const token = queue.shift();
    if (token.type === "link_open") {
      const destination = token.attrGet("href");
      if (destination !== null) {
        destinations.push(destination);
      }
    } else if (token.type === "image") {
      const destination = token.attrGet("src");
      if (destination !== null) {
        destinations.push(destination);
      }
    }
    if (token.children) {
      queue.push(...token.children);
    }
  }
  return destinations;
}

function resolvePackageLink(sourcePath, destination) {
  if (
    destination === "" ||
    destination.startsWith("#")
  ) {
    return null;
  }

  const pathOnly = destination.split("#", 1)[0].split("?", 1)[0];
  let decoded;
  try {
    decoded = decodeURIComponent(pathOnly);
  } catch {
    decoded = pathOnly;
  }
  const leadingSeparators = decoded.slice(0, 2);
  const windowsUnc =
    /^[\\/]{2}$/.test(leadingSeparators) &&
    leadingSeparators.includes("\\");
  decoded = decoded.replaceAll("\\", "/");
  if (decoded.startsWith("//")) {
    return windowsUnc ? { escape: true } : null;
  }
  if (
    /^file:/i.test(decoded) ||
    /^[A-Za-z]:/.test(decoded) ||
    decoded.startsWith("/")
  ) {
    return { escape: true };
  }
  if (/^[A-Za-z][A-Za-z0-9+.-]*:/.test(decoded)) {
    return null;
  }

  const path = posix.normalize(
    posix.join(posix.dirname(sourcePath), decoded),
  );
  if (path === ".." || path.startsWith("../")) {
    return { escape: true };
  }
  return { escape: false, path };
}

function validateVendorNeutrality(
  root,
  folder,
  packageFiles,
  forbiddenTerms,
  add,
) {
  for (const relativePath of packageFiles) {
    if (extname(relativePath).toLowerCase() !== ".md") {
      continue;
    }
    const path = join(root, folder, relativePath);
    const stat = lstatSync(path);
    if (!stat.isFile() || stat.isSymbolicLink()) {
      continue;
    }
    if (
      relativePath !== "SKILL.md" &&
      stat.size > MAX_SUPPORT_MARKDOWN_BYTES
    ) {
      continue;
    }
    const text = markdownProse(readFileSync(path, "utf8"));
    for (const term of forbiddenTerms) {
      const escaped = term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      const pattern = new RegExp(
        `(?:^|[^A-Za-z0-9])${escaped}(?=$|[^A-Za-z0-9])`,
        "i",
      );
      if (pattern.test(text)) {
        add(
          "language.vendor",
          `${folder}/${relativePath}`,
          `Maintained skill Markdown contains configured vendor term "${term}".`,
        );
      }
    }
  }
}

function markdownProse(markdown) {
  const parts = [];
  for (const token of markdownParser.parse(markdown, {})) {
    if (token.type === "fence" || token.type === "code_block") {
      for (const line of token.content.split(/\r\n|\r|\n/)) {
        if (!isInstallationCommand(line)) {
          parts.push(line, "\n");
        }
      }
      continue;
    }
    if (token.type === "html_block") {
      parts.push(htmlVisibleText(token.content), "\n");
      continue;
    }
    if (token.type !== "inline") {
      continue;
    }
    for (const child of token.children ?? []) {
      if (child.type === "text" || child.type === "code_inline") {
        parts.push(child.content);
      } else if (
        child.type === "softbreak" ||
        child.type === "hardbreak"
      ) {
        parts.push(" ");
      } else if (child.type === "image") {
        parts.push(child.content);
      } else if (child.type === "html_inline") {
        parts.push(htmlVisibleText(child.content));
      }
    }
    parts.push("\n");
  }
  return parts.join("");
}

function htmlVisibleText(html) {
  const attributes = [];
  const attributePattern =
    /\b(?:alt|aria-label|placeholder|title)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))/gi;
  for (const match of html.matchAll(attributePattern)) {
    attributes.push(match[1] ?? match[2] ?? match[3]);
  }

  const body = html
    .replace(/<!--[\s\S]*?-->/g, "")
    .replace(
      /<\/?(?:address|article|aside|blockquote|br|dd|div|dl|dt|fieldset|figcaption|figure|footer|form|h[1-6]|header|hr|li|main|nav|ol|p|pre|section|table|tbody|td|tfoot|th|thead|tr|ul)\b[^>]*>/gi,
      "\n",
    )
    .replace(/<[^>]*>/g, "");
  return decodeHTML(`${attributes.join("\n")}\n${body}`);
}

function isInstallationCommand(line) {
  const command = line.trim().replace(/^(?:[$>]\s*)/, "");
  if (/[;&|`<>]|\$\(|\s#/.test(command)) {
    return false;
  }
  return [
    /^(?:npm|pnpm|yarn|bun)\s+(?:add|install)\s+\S+(?:\s+\S+)*$/i,
    /^(?:pip|pip3|pipx)\s+install\s+\S+(?:\s+\S+)*$/i,
    /^python(?:3)?\s+-m\s+pip\s+install\s+\S+(?:\s+\S+)*$/i,
    /^uv\s+(?:add|tool\s+install)\s+\S+(?:\s+\S+)*$/i,
    /^cargo\s+install\s+\S+(?:\s+\S+)*$/i,
    /^dotnet\s+tool\s+install\s+\S+(?:\s+\S+)*$/i,
    /^go\s+install\s+\S+(?:\s+\S+)*$/i,
    /^npx\s+skills@latest\s+add\s+\S+(?:\s+\S+)*$/i,
  ].some((pattern) => pattern.test(command));
}

function validateReadme(root, skillFolders, add) {
  const path = join(root, "README.md");
  if (!existsSync(path)) {
    add("readme.missing", "README.md", "README.md is required.");
    return;
  }

  const text = readFileSync(path, "utf8");
  const installs = [];
  const shellLanguages = new Set(["bash", "sh", "shell", "zsh"]);
  for (const token of markdownParser.parse(text, {})) {
    const language = token.info?.trim().split(/\s+/, 1)[0].toLowerCase();
    if (token.type !== "fence" || !shellLanguages.has(language)) {
      continue;
    }
    const matches = [];
    let unexpectedLine = false;
    for (const line of token.content.split(/\r\n|\r|\n/)) {
      const trimmed = line.trim();
      if (trimmed === "" || trimmed.startsWith("#")) {
        continue;
      }
      const match = trimmed.match(
        /^npx skills@latest add KrishRVH\/skills\/([a-z0-9]+(?:-[a-z0-9]+)*)$/,
      );
      if (match) {
        matches.push(match[1]);
      } else {
        unexpectedLine = true;
      }
    }
    if (matches.length > 0 && unexpectedLine) {
      add(
        "readme.command",
        "README.md",
        "A skill-install fence may contain only install commands, blank lines, and comments.",
      );
    } else {
      installs.push(...matches);
    }
  }
  const counts = new Map();
  for (const folder of installs) {
    counts.set(folder, (counts.get(folder) ?? 0) + 1);
  }

  const skillSet = new Set(skillFolders);
  for (const folder of skillFolders) {
    const count = counts.get(folder) ?? 0;
    if (count === 0) {
      add(
        "readme.missing",
        "README.md",
        `Missing install command for "${folder}".`,
      );
    } else if (count > 1) {
      add(
        "readme.duplicate",
        "README.md",
        `Install command for "${folder}" appears ${count} times.`,
      );
    }
  }
  for (const folder of counts.keys()) {
    if (!skillSet.has(folder)) {
      add(
        "readme.unknown",
        "README.md",
        `Install command names unknown skill folder "${folder}".`,
      );
    }
  }
}

function countLines(text) {
  if (text === "") {
    return 0;
  }
  return text
    .replace(/(?:\r\n|\r|\n)$/, "")
    .split(/\r\n|\r|\n/).length;
}

function uniqueSortedErrors(errors) {
  const byIdentity = new Map();
  for (const error of errors) {
    byIdentity.set(
      `${error.path}\0${error.code}\0${error.message}`,
      error,
    );
  }
  return [...byIdentity.values()].sort((left, right) => {
    return (
      left.path.localeCompare(right.path) ||
      left.code.localeCompare(right.code) ||
      left.message.localeCompare(right.message)
    );
  });
}

if (import.meta.main) {
  const root = process.argv[2] ? resolve(process.argv[2]) : process.cwd();
  const errors = validateRepository(root);
  if (errors.length === 0) {
    process.stdout.write("Skill package validation passed.\n");
  } else {
    for (const error of errors) {
      process.stderr.write(
        `${error.path}: [${error.code}] ${error.message}\n`,
      );
    }
    process.exitCode = 1;
  }
}
