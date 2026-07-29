# Evidence note for shallow object type guards

Date: 2026-07-28

## Bottom line

The common TypeScript helper named `isRecord` is not inherently incorrect, but
it is a useful review signal. Its name often promises more than its runtime
check proves, and coding agents frequently emit it as repetitive defensive
boilerplate.

Judge the helper by its contract and placement:

- Keep trust-boundary validation.
- Prefer domain-specific predicates when the expected shape is known.
- Use a semantically exact name such as `isNonArrayObject` when that shallow
  condition is genuinely reused.
- Inline a one-use check when a helper adds no clarity.
- Do not add a schema library solely to replace a few small local checks.

## What the common implementation proves

The usual implementation is:

```ts
function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}
```

TypeScript defines `Record<Keys, Type>` as an object type mapping keys to value
types. It does not define a runtime category named “record.”
([TypeScript utility types](https://www.typescriptlang.org/docs/handbook/utility-types.html#recordkeys-type))

The runtime expression proves only that the value is:

1. reported as an object by JavaScript;
2. not `null`; and
3. not an array.

It still accepts dates, regular expressions, maps, sets, class instances,
proxies, and objects with unusual prototypes. It proves no required fields,
field types, own-property status, or domain invariants.
([MDN `typeof`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/typeof#custom_method_that_gets_a_more_specific_type))

The explicit `value is ...` return type is a programmer promise. TypeScript
does not verify that the body proves the declared predicate and says explicit
type predicates are no safer than type assertions.
([TypeScript 5.5 release notes](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-5.html#inferred-type-predicates))

## Why it became an agent-code smell

A July 2026 tldraw post documented the helper becoming a recognizable coding
agent meme and speculated that an older tldraw implementation influenced model
output.
([tldraw discussion](https://tldraw.dev/blog/is-record-sorry))

The attribution is not established provenance. The same generic guard was
discussed publicly in 2021, before tldraw says it wrote its version in 2022.
([earlier TypeScript discussion](https://www.reddit.com/r/typescript/comments/ns6595/is_there_a_way_to_narrow_an_unknown_type_to/))

The pattern looks mechanically generated when it appears as:

- a private helper with one caller;
- duplicate copies across unrelated files;
- the same generic name for different intended meanings;
- a defensive check on a value already guaranteed by a typed internal API; or
- a shallow object check presented as complete schema validation.

These are maintainability signals, not proof of authorship.

## Better alternatives

### Known property

Modern TypeScript can narrow an unknown object and an individual property
directly:

```ts
if (
  typeof value === "object" &&
  value !== null &&
  "name" in value &&
  typeof value.name === "string"
) {
  useName(value.name);
}
```

TypeScript 4.9 added unlisted-property narrowing for this pattern.
([TypeScript 4.9 release notes](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html#unlisted-property-narrowing-with-the-in-operator))

### Known domain shape

Use a domain predicate such as `isProgressState` or
`isTrainerSettingsInput`. Check every consumed field and invariant inside it.
A shallow object check may remain as an implementation step, but should not be
mistaken for the validation itself.

### Reused shallow condition

If several dynamic property reads need exactly “non-null, non-array object,”
name that condition directly:

```ts
function isNonArrayObject(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}
```

This remains a shallow guard. The more precise name prevents readers from
mistaking it for proof of a plain object or valid domain record.

### Substantial external schema

For a reusable nested external schema, a runtime schema validator can define
the shape once and return typed data. Zod, for example, distinguishes object
schemas from record schemas and validates their contents.
([Zod objects](https://zod.dev/api#objects),
[Zod records](https://zod.dev/api#records))

A dependency is justified only when it removes enough repeated validation to
offset its API, bundle, and maintenance cost.

## Review checklist

When this helper appears, ask:

1. Is the input genuinely `unknown` at a storage, network, file, plugin, or
   process boundary?
2. Does the code validate every property it later consumes?
3. Does the predicate name describe exactly what the body proves?
4. Is the condition reused enough to deserve a helper?
5. Would direct `typeof` and `in` narrowing be clearer?
6. Is a schema validator already present and appropriate?

Delete or inline the helper when it merely placates the compiler. Preserve it
under an exact name when it supports complete boundary validation.

## Applied conclusion for GeoTrainer

The repository had four local definitions:

- Persisted progress validation: justified boundary staging; renamed the
  shallow condition to `isNonArrayObject`.
- Wikidata response parsing: justified repeated boundary staging; renamed the
  shallow condition to `isNonArrayObject`.
- Package manifest parsing: necessary check but unnecessary one-use helper;
  inlined.
- Trainer settings normalization: misleading generic name and arrays were
  accepted; renamed to `isTrainerSettingsInput` and arrays are rejected.

No shared utility or validation dependency was added.
