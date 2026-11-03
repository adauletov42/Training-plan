# Project skills

Skills vendored into this repo so every Claude Code session on it (including
ephemeral cloud sessions) picks them up automatically from `.claude/skills/`.

| Skill | Source | License |
|---|---|---|
| `frontend-slides` | github.com/zarazhangrui/frontend-slides | see `frontend-slides/LICENSE` |
| `ui-ux-pro-max` | github.com/nextlevelbuilder/ui-ux-pro-max-skill | see `ui-ux-pro-max/LICENSE` |
| `impeccable` | github.com/pbakaus/impeccable (`plugin/skills/impeccable`) | Apache-2.0, `impeccable/LICENSE` |
| `humanizer` | github.com/blader/humanizer | MIT, `humanizer/LICENSE` |
| `diagram-design` | github.com/cathrynlavery/diagram-design (`skills/diagram-design`) | MIT, `diagram-design/LICENSE` |

Not vendored:

- `pptx` — already provided account-wide (`anthropic-skills:pptx`) and at
  `/mnt/skills/public/pptx`, so a copy here would only shadow it.
- `design`, `design-system`, `brand`, `slides`, `banner-design`, `ui-styling`
  from the ui-ux-pro-max-skill repo — dropped on purpose. Their scope overlaps
  `impeccable`, `frontend-slides` and the built-in `dataviz` / `artifact-design`
  skills, and the generic names made skill selection noisy. Copy them back from
  upstream `.claude/skills/` if you want them.

## Updating

Re-clone the upstream repo and copy the skill folder over the one here; each
folder is a verbatim copy of the upstream skill directory plus its LICENSE.

## Notes

- `impeccable/scripts/impeccable` is a launcher that downloads a self-contained
  binary on first run; it needs outbound network access.
- `.claude/settings.json` pre-approves that launcher so it runs without a
  permission prompt. Permission rules are prefix matches on the command text,
  so the allow list carries the relative spelling and this repo's cloud-session
  absolute path. On a different checkout path, add that path's spelling or
  invoke the launcher by its relative path from the repo root. Note that
  pre-approving it means every session in this repo will run a binary the
  launcher downloads, without asking first.
