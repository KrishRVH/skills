---
name: demo-html
description: Single-file before/after HTML demo of UI changes, with screenshots captured from the running app and a technical vs non-technical language toggle for mixed stakeholder audiences.
disable-model-invocation: true
---

# Demo HTML

Produce one self-contained HTML file that shows each UI change as labeled
before/after screenshots of the real running application, with plain-language
and technical versions of every explanatory text block behind a page-level
audience toggle. The file must survive being emailed or forwarded: no external
assets, no server, safe to open in stakeholder mode by default.

## Steps

1. **Scope.** List the changes to demonstrate and, for each, the page URL and
   the on-screen element that shows the difference. Done when every change has
   a URL, a target element, and data known to exist that exercises it.
2. **Capture "after".** Launch the real app (use the project's run skill or
   launch procedure if one exists) and screenshot each target element with a
   headless browser. Use element-level screenshots, a viewport wide enough
   that no relevant column is cropped, and hide debug toolbars. Look at every
   image: a shot that crops out the changed element, or hides it behind a
   lazy-rendered header, is a failed capture — reshoot, don't narrate around
   it. Done when each "after" image visibly contains the change.
3. **Capture "before".** Save the index tree (`index_tree=$(git write-tree)`),
   then stash only the changed paths, including untracked additions, with
   pathspecs that cover deletions, usually their parent directories:
   `git stash push --include-untracked -- <pathspecs>`. Proceed only if both
   commands succeed and Git reports a new stash. If a failed push still creates
   a stash entry, reconcile it before stopping. Do not create another stash
   until restoration. Clear any compiled-view/template caches and reshoot the
   same targets. In a guaranteed cleanup path, even after capture failure, run
   `git stash pop` without `--index`, then restore the scoped index state with
   `git restore --source="$index_tree" --staged -- <pathspecs>` and clear caches
   again. If restoration fails, stop and recover from the stash or saved index
   tree before making further changes. If you added any temporary access shim
   (login route, auth bypass) for capture, remove it and prove it is gone
   (request it, expect 404) before finishing. Done when each before-image visibly
   shows the prior behavior in the same framing as its after-shot, the working
   tree and index are back to their pre-capture state, and no shim responds.
4. **Write dual copy.** For every text block (page intro, per-change summary,
   where-to-look pointer), write both audience variants per the copy contract
   below. Done when each variant reads complete on its own — neither refers to
   the other, and neither is a stub.
5. **Build the page.** Start from [templates/DEMO-HTML.html](templates/DEMO-HTML.html):
   one section per change, BEFORE and AFTER labels on every image, all images
   embedded as base64 data URIs. Keep the audience toggle, the plain-language
   default, and the fit-to-width / full-resolution image toggle. Done when the
   file opens from disk with no network access and both toggles work.
6. **Verify and deliver.** Open the page and read it once in each audience
   mode. Review every screenshot for data the audience must not see
   (credentials, keys, personal data, records from a non-demo environment) —
   recapture with safer data rather than editing images. Report the file path,
   which environment and data the screenshots came from, and any capture
   limitation (stale seed data, unreachable page, change not demonstrable).
   Done when both modes read correctly and the report is delivered.

## Copy contract

|                 | Plain (default mode)                                      | Technical                                                        |
| --------------- | --------------------------------------------------------- | ---------------------------------------------------------------- |
| Names things by | what the user sees: screen names, column headers, buttons | routes, files, columns, helpers, format strings                  |
| Explains        | what changed and why it helps, in one or two sentences    | what was edited and the edge cases handled                       |
| Never contains  | file paths, code identifiers, format strings, jargon      | filler — if it repeats the plain copy, add the missing specifics |

Both variants live in the DOM; the toggle switches a class on `<body>`. The
page defaults to plain mode so an unmodified forward is stakeholder-safe.
Shared copy, including headings, controls, capture metadata, and image
alternative text, uses plain, audience-neutral language.

## Common mistakes

- A collapsible "technical notes" footnote is not the toggle: plain readers
  still see engineering clutter, and the sender cannot set a mode for the page.
- Scaling wide screenshots to container width makes table text unreadable —
  keep full resolution available via the image toggle.
- Screenshotting only the "after" state and describing the "before" in prose.
  The comparison is the demo; capture both.
