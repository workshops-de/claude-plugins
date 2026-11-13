---
name: course-content
description: "Rules for workshops.de course content: lesson folders under lessons/, lesson.yml (Slidev or Google Slides), stepped task folders, task.yml, body.md, hint.md, bonus.md, trainer_hint.md and German *.de.md translations. Use when creating or editing lessons or tasks in a workshops.de slide repository."
---

## Lesson Structure

Each lesson is a folder in `/lessons/` with a two-digit prefix for ordering (e.g., `03-angular-services-http`).
Lessons count up by one (`01`, `02`, `03` …); tasks use stepped numbers (see below).

A lesson has slides in one of two forms, set by `slides_type` in `lesson.yml`:

- **`slidev`**: the slides live in the repository, with an entry file named like the folder
- **`google_slides`**: the slides live in Google Slides (`google_slide_id`); the folder has no slide files

```
lessons/
└── 01-example-lesson/
    ├── lesson.yml              # Lesson configuration (required)
    ├── 01-example-lesson.md    # Slidev entry point (only for slides_type: slidev)
    ├── slides/                 # 4-MAT topic files (only for slides_type: slidev)
    │   └── topic-name/
    │       ├── why.md
    │       ├── what.md
    │       ├── how.md
    │       ├── what-if.md
    │       └── task.md
    └── tasks/
        ├── 10-first-task/
        └── 20-second-task/
```

### lesson.yml Configuration

```yaml
# Required
name: Lesson Title
position: 1

# Trainer (email or slug)
trainer: trainer@workshops.de

# Code repository (if the workshop has one)
github_code_url: https://github.com/org/repo
git_tag_starting: main

# Presentation type: "slidev" or "google_slides"
slides_type: slidev

# For Google Slides only
# google_slide_id: "1NmeNH96Qj9jqwrHJ4axQEH7_1ptbkZPjQlLZ4jyWWg"

# PDF sync
pdf_generation_enabled: true

# Playground options
stackblitz_enabled: true
codesandbox_enabled: false

# Status
deprecated: false
```

## Task Structure

Each task is a folder in `/lessons/{lesson}/tasks/` named `NN-task-slug`, where `NN` equals the task's
`position`. Positions are **stepped by 10** (`10`, `20`, `30` …), so a new task fits between two existing
ones without renumbering: to insert between `10-service` and `20-http`, create `15-new-task` with
`position: 15`. Only renumber when there is no gap left.

```
tasks/
└── 10-first-task/
    ├── task.yml            # Task configuration (required)
    ├── body.md             # Main task description (required)
    ├── hint.md             # Hints for participants (optional)
    ├── bonus.md            # Bonus challenges (optional)
    ├── trainer_hint.md     # Notes for trainers only (optional)
    ├── body.de.md          # German translations (optional, see below)
    ├── hint.de.md
    └── assets/             # Images and media (optional)
        └── screenshot.png
```

### task.yml Configuration

```yaml
# Required
title: "Task Title"
position: 10

# Optional metadata
category: "Basics"
preparation: false             # true only for setup tasks done before the session
estimated_time_in_minutes: 15
always_unlocked: false         # true only for setup tasks that must work before anything is unlocked

# Git integration, only for workshops with a solution repository
git_tag_completed: solution--first-task

# German title (when the task has German translations)
translations:
  de:
    title: "Aufgabentitel"
```

### German Translations

English is the source of truth. German translations sit next to the English files with a `.de.md`
suffix (`body.de.md`, `hint.de.md`, `bonus.de.md`, `trainer_hint.de.md`) plus `translations.de.title`
in `task.yml`; the platform imports them as `translations.de.*`. Translate a task completely or not at
all, and update the German files whenever the English ones change.

**Note**: Markdown content is loaded from separate `.md` files, NOT from the YAML file.

## Markdown Content Guidelines

### Markdown renderer

The eClassroom renders `body.md`, `hint.md` and `bonus.md` with [Earmark](https://earmark.hexdocs.pm/readme.html),
the Elixir Markdown parser. Earmark treats a matched pair of block-level HTML tags (e.g. `<details>...</details>`)
as a single **verbatim** node: it does not parse Markdown (code fences, inline code, bold, …) nested inside raw HTML.

- Do not use `<details>`/`<summary>` or any other raw-HTML wrapping in `body.md`, `hint.md` or `bonus.md`.
  Formatted content inside renders as flat, unstyled text in the eClassroom (confirmed live).
- If someone explicitly asks for a collapsible section, explain this limitation and suggest plain Markdown instead.
- Existing tasks may still contain `<details>` blocks; replace them when you touch the task.

### Inline code highlighting

The eClassroom highlights code with [Shiki](https://shiki.style/packages/rehype#inline-code)
(`inline: 'tailing-curly-colon'`). Highlight inline code by appending a `{:<lang>}` marker **inside** the backticks,
directly after the code:

| Write this                     | Instead of this           | Language |
| ------------------------------ | ------------------------- | -------- |
| `` `input(){:ts}` ``           | `` `input()` ``           | `ts`     |
| `` `[content]{:html}` ``       | `` `[content]` ``         | `html`   |
| `` `<input>{:html}` ``         | `_<input>_`               | `html`   |
| `` `count = signal(0){:ts}` `` | `` `count = signal(0)` `` | `ts`     |

- Applies to `body.md`, `hint.md` and `bonus.md`.
- The marker sits inside the backticks: `` `code{:ts}` `` ✅, `` `code`{:ts} `` ❌.
- Always use a marker for code (TypeScript → `ts`, templates → `html`, styles → `css`, shell → `bash`, Java → `java`,
  Python → `python`, …); a code span without marker stays unhighlighted.
- Use it for code snippets, identifiers, bindings and API calls. Plain terms, file names and paths (`src/app/app.ts`)
  and UI labels stay without a marker or in _italics_.
- When updating an existing task, add the marker to the inline code you touch; do not rewrite untouched tasks.
- Never put JS template strings (backticks, `${...}`) into inline code; the backticks break the inline marker.
  Describe the value in prose or _italics_ instead (e.g. _/books/:isbn_) and show the full snippet in a fenced block
  in `hint.md`.
- Code blocks use fenced blocks with a language (` ```ts `, ` ```html `), as in the
  [hint template](references/hint.template.md).

### body.md - Main Task Description

The description guides the participant to solve the task alone. Give every detail that is needed, but no wall of
text: include only what is really needed.

- One step per bullet with a bold heading, steps separated by `---` for readability
- Follow the [body template](references/body.template.md)

### hint.md - Hints

Hints are a safe harbour for participants who are learning a completely new area: easy to follow, no tricks,
straightforward code that makes the solution work.

- Follow the order of the steps in `body.md`, one hint per step, separated by `---`
- Give the technical details and the code snippets (with the file name as first comment) needed for each step
- Follow the [hint template](references/hint.template.md)

### bonus.md - Bonus Challenges

Bonus tasks are for fast and more experienced participants.

- When you write a new task, ask whether to add a bonus and suggest one that fits the topic
- Extend the main task, do not replace it
- Follow the [body template](references/body.template.md)

### Task titles

When the task has a solution commit (`git_tag_completed: solution--<topic>-<part>`), derive the task title from the
topic parts of the tag.

### trainer_hint.md - Trainer Notes

- Include common issues and solutions
- Add time estimates for different skill levels
- List discussion points for the group
- Note any setup requirements

## Code Examples in Tasks

### Shiki Notation Transformers

Use inline comments for syntax highlighting features:

| Notation | Description |
|----------|-------------|
| `// [!code highlight]` | Highlights a line |
| `// [!code focus]` | Focuses a line (blurs others) |
| `// [!code ++]` | Shows as added line (green) |
| `// [!code --]` | Shows as removed line (red) |
| `// [!code warning]` | Marks as warning |
| `// [!code error]` | Marks as error |

### Examples

**Line Highlighting:**
```typescript
interface User {
  id: number;        // [!code highlight]
  name: string;
  email: string;     // [!code highlight]
}
```

**Diff Highlighting:**
```typescript
function greet(name: string) {
  console.log('Hello')           // [!code --]
  console.log(`Hello, ${name}!`) // [!code ++]
}
```

**Error & Warning:**
```typescript
const config = {
  apiUrl: process.env.API_URL,  // [!code warning]
  secret: 'hardcoded-secret',   // [!code error]
};
```

### Code Example Best Practices

- Annotate each code block with the correct language
- Keep examples concise (1-15 lines preferred)
- Use comments to explain important parts
- Avoid showing irrelevant boilerplate

## Images and Assets

### Referencing Images

Store images in the task's `assets/` folder and reference them with relative paths:

```markdown
![Screenshot](./assets/screenshot.png)
```

During sync, relative paths are automatically converted to absolute GitHub Raw URLs.

### Image Guidelines

- Use descriptive filenames (e.g., `step-3-result.png` not `image1.png`)
- Optimize images for web (compress, appropriate resolution)
- Prefer PNG for screenshots, JPG for photos
- Add alt text for accessibility

## Git Integration

### Git Tags for Solutions

Use `git_tag_completed` in `task.yml` to link to the solution state:

```yaml
git_tag_completed: solution--first-task
```

This enables:
- Code diffs between starting point and solution
- StackBlitz playground with solution code
- Easy navigation for trainers

### Naming Convention

- Format: `solution--{task-slug}` (double dash, no position, so renumbering a task keeps its tag)
- Example: `solution--service`, `solution--mock-components`
- Workshops without a solution repository (participants build everything themselves) omit
  `git_tag_completed` entirely

## Quality Checklist

- [ ] All required files present (`task.yml`, `body.md`)
- [ ] Task title is clear and descriptive
- [ ] Steps have bold headings, are separated by `---` and easy to follow
- [ ] Hints follow the order of the steps and contain working code
- [ ] Code blocks have a language, inline code has a `{:lang}` marker
- [ ] No `<details>`/`<summary>` or other raw HTML in body, hint or bonus
- [ ] Images have alt text and are optimized
- [ ] Trainer notes cover common issues
