# Skill invocation

Every skill is either user-invoked or model-invoked. Keep both invocation
controls synchronized so each supported harness sees the same contract.

## User-invoked skills

Use this mode when the caller must deliberately choose the workflow. It suits
expensive, judgment-heavy, or orchestration skills.

- Set `disable-model-invocation: true` in `SKILL.md` frontmatter.
- Set `policy.allow_implicit_invocation: false` in `agents/openai.yaml`.
- Write a short, human-facing description without trigger phrases.

Only the caller can invoke these skills by name. Other skills cannot depend on
them as automatic subroutines.

## Model-invoked skills

Use this mode when an agent can usefully discover the skill from the task or
when another skill must reach it.

- Omit `disable-model-invocation` from `SKILL.md` frontmatter.
- Omit `policy.allow_implicit_invocation` from `agents/openai.yaml`.
- Write a model-facing description with one distinct trigger per branch.

Model-invoked skills remain available for explicit invocation.

## Package metadata

Every skill includes `agents/openai.yaml` with these required fields:

```yaml
interface:
  display_name: "Human-facing name"
  short_description: "Human-facing summary between 25 and 64 characters"
```

Add the `policy` block only for user-invoked skills. Treat `agents/` as machine
metadata, not supporting material: it does not need a link from `SKILL.md`.
