---
name: translate-task-de
description: "Translate workshops.de tasks into German: body.md, hint.md, bonus.md and trainer_hint.md as *.de.md files next to the English ones, plus translations.de.title in task.yml. Use when asked to translate tasks to German, to update stale German translations, or to find tasks whose German translation is missing or outdated."
argument-hint: "[task folder, e.g. 120-hooks | --todo | all]"
---

# Translate tasks to German

English is the source of truth. German lives next to it and the platform imports it as
`translations.de.*`.

## Target format

| English source       | German file / field                  | Platform field                          |
| -------------------- | ------------------------------------ | --------------------------------------- |
| `body.md`            | `body.de.md`                         | `translations.de.body_markdown`         |
| `hint.md`            | `hint.de.md`                         | `translations.de.hint_markdown`         |
| `bonus.md`           | `bonus.de.md`                        | `translations.de.bonus_markdown`        |
| `trainer_hint.md`    | `trainer_hint.de.md`                 | `translations.de.trainer_hint_markdown` |
| `task.yml` → `title` | `task.yml` → `translations.de.title` | `translations.de.title`                 |

Only translate files that exist in English. Never touch the English files, `position`, `category`,
timing or flags: they are shared by both languages.

`task.yml` gets this block at the end (keep everything else as is):

```yaml
translations:
  de:
    title: 'Hooks: Den Leselisten-Flow absichern'
```

## Repository rules first

Look for a translation guide in the repository, usually `docs/translation-de.md` (otherwise search
for `translation` in `docs/` and the repository's `CLAUDE.md`). If it exists, read it completely
before translating: its glossary, address, typography and heading rules are binding and override
the defaults below. If the repository has a status script (e.g. `scripts/translation-status.sh`),
use it to find and check tasks.

## Which tasks

Tasks live in `lessons/*/tasks/<NN-slug>/`.

- `$ARGUMENTS` is a folder name (`120-hooks`) → that task.
- `--todo` or no argument → find tasks that need work (see below) and work through them, one task
  at a time.
- `all` → every task, one at a time.

A German file is **missing** if it does not exist, and **stale** if the English file was committed
after it. Without a status script, compare the last commits:

```bash
git log -1 --format=%ct -- path/to/body.md      # English
git log -1 --format=%ct -- path/to/body.de.md   # German: stale if older than English
```

For a stale file, diff the English file since the German one was last committed
(`git log -1 --format=%H -- <file>.de.md`, then `git diff <hash> -- <file>.md`) and update only the
changed passages instead of re-translating everything.

## Before translating

1. Read the repository's translation guide (see above).
2. Read all English files of the task, so terms stay consistent between body, hints and trainer
   notes.
3. If German slides already exist for this task (e.g. a German slide deck or `*.de.md` slide files),
   reuse their phrasing for the title and key terms.

## Default rules (the repository guide wins where it differs)

- Address participants as **„ihr/euch“**. Trainer notes stay neutral unless the English addresses
  the trainer directly.
- Keep the **Markdown structure 1:1**: same headings (translated), lists, order, tables and
  `<details>`/`<summary>` blocks (translate the summary text, keep emoji).
- Common section headings: Overview → Überblick, Prerequisites → Voraussetzungen, Steps → Schritte,
  Success Criteria → Erfolgskriterien, References → Referenzen, Background → Hintergrund,
  Learning goals → Lernziele, Facilitation notes → Hinweise zur Durchführung, Going further →
  Weiterführend. If the repository has a glossary, add new headings there.
- **Code stays code**: commands, flags, file names, paths, JSON/YAML keys and identifiers stay
  unchanged. Translate comments and natural-language prompts (`> …`) inside code blocks.
- Inline code (`` `…` ``) is never translated.
- Links keep their URLs; links to English documentation stay English.
- Bold and italic emphasis moves to the corresponding German words.
- Product and feature names stay English unless the repository glossary says otherwise.
- Prefer natural German over literal translation, and keep it as concise as the original.
- Typography: German quotation marks „…“.

## After translating

1. Self-check each German file against its English source:
   - same number of headings, list items, code blocks and `<details>` blocks
   - code blocks identical except comments and prompts
   - no English sentences left (product names and fixed English phrases excepted)
2. Check the status again (status script or the git comparison above): every file of the task is
   up to date.
3. Commit one task per commit, following the repository's commit conventions, e.g.
   `docs(tasks): translate <folder> to german` or `docs(tasks): update german translation of <folder>`.
