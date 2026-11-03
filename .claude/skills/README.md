# Project skills

Skills vendored into this repo so every Claude Code session on it (including
ephemeral cloud sessions) picks them up automatically from `.claude/skills/`.

| Skill | Source | License |
|---|---|---|
| `frontend-slides` | github.com/zarazhangrui/frontend-slides | see `frontend-slides/LICENSE` |
| `ui-ux-pro-max` + `design`, `design-system`, `brand`, `slides`, `banner-design`, `ui-styling` | github.com/nextlevelbuilder/ui-ux-pro-max-skill | see each `LICENSE` |
| `impeccable` | github.com/pbakaus/impeccable (`plugin/skills/impeccable`) | Apache-2.0, `impeccable/LICENSE` |
| `humanizer` | github.com/blader/humanizer | MIT, `humanizer/LICENSE` |
| `diagram-design` | github.com/cathrynlavery/diagram-design (`skills/diagram-design`) | MIT, `diagram-design/LICENSE` |

Not vendored: `pptx` — already provided account-wide (`anthropic-skills:pptx`)
and at `/mnt/skills/public/pptx`, so a copy here would only shadow it.

## Updating

Re-clone the upstream repo and copy the skill folder over the one here; each
folder is a verbatim copy of the upstream skill directory plus its LICENSE.

## Notes

- `impeccable/scripts/impeccable` is a launcher that downloads a self-contained
  binary on first run; it needs outbound network access.
- `design`, `brand`, `slides` and `ui-styling` have generic names and overlap in
  scope with `impeccable`, `frontend-slides` and the built-in `dataviz` /
  `artifact-design` skills. Delete the folders you do not want if skill
  selection gets noisy.
