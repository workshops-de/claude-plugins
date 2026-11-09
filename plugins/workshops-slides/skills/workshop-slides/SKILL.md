---
name: workshop-slides
description: "Generates complete Slidev workshop slide repositories for workshops.de. Use when asked to create a new workshop, generate workshop slides, create lesson content, or build a training course. Creates all files needed for a workshops.de Slidev repository: lesson.yml metadata, Slidev slide decks following the 4-MAT teaching structure (WHY/WHAT/HOW/WHAT-IF), hands-on tasks with body.md/hint.md/bonus.md, and repository scaffolding (00-index.md, slides.md, sources.md). Output follows the workshops-de/workshop-slides-template structure and can be synced to the workshops.de platform via GitHub."
---

# Workshop Slides Generator

## Overview

You generate complete Slidev-based workshop slide repositories for workshops.de, a German IT training platform. Your output is a full set of files that follow the `workshops-de/workshop-slides-template` structure, ready to push to GitHub and sync to the platform.

## Workflow

When asked to create a workshop, follow these phases:

### Phase 1: Curriculum Planning

First, propose a structured curriculum plan:

| # | Directory | Lesson Name | Topics | Tasks |
|---|-----------|-------------|--------|-------|
| 1 | 01-getting-started | Getting Started | setup, first-steps | Setup Environment, First Project |
| 2 | 02-components | Components | basics, data-binding | Create Component, Bind Data |

Rules:
- Each lesson = roughly half a training day (3-day workshop = ~6 lessons)
- Each lesson has 1-3 topics (each following 4-MAT)
- Each lesson has 1-4 tasks (hands-on exercises)
- Tasks build progressively
- First lesson starts with environment setup
- Ask user to confirm before proceeding

### Phase 2: File Generation

Generate files in order:
1. `00-index.md` — index linking all lessons
2. `slides.md` — combined deck for presenter view
3. `sources.md` — references
4. For each lesson:
   - `lessons/NN-name/lesson.yml`
   - `lessons/NN-name/NN-name.md`
   - `lessons/NN-name/slides/topic-name/topic.md` (per topic)
   - `lessons/NN-name/tasks/NN-task/task.yml` (per task)
   - `lessons/NN-name/tasks/NN-task/body.md`
   - `lessons/NN-name/tasks/NN-task/hint.md`
   - Optionally: `bonus.md`, `trainer_hint.md`

Present each file with its full path clearly marked.

To create the repository, use the GitHub CLI (`gh`) if it is available and the user agrees:

```bash
gh repo create workshops-de/<workshop>-slides --public --template workshops-de/workshop-slides-template --clone
```

Then write the generated files into the clone, run `npm install` and `npm run build` to check the build, and commit. After the first push the user enables GitHub Pages once: Settings → Pages → Source → "GitHub Actions".

## Repository Structure

```
/
├── 00-index.md                          # Index with links to all lessons
├── slides.md                            # Combined deck for presenter view
├── sources.md                           # Sources and references
├── package.json                         # Theme + toolkit (from template, only update name)
├── lessons/
│   └── 01-lesson-name/
│       ├── lesson.yml                   # Lesson metadata
│       ├── 01-lesson-name.md            # Slidev entry point
│       ├── slides/
│       │   └── topic-name/
│       │       └── topic.md             # Slides following 4-MAT
│       └── tasks/
│           └── 01-task-name/
│               ├── task.yml             # Task metadata
│               ├── body.md              # Task description
│               └── hint.md             # Collapsible hints
```

## ⚠️ STEP 0: READ THE REFERENCE FILES FIRST ⚠️

**CRITICAL: BEFORE generating any workshop content:**

1. **Read** `reference/01-repository-structure.md` — full file tree and conventions
2. **Read** `reference/02-slidev-conventions.md` — layouts, frontmatter, code blocks
3. **Read** `reference/03-example-lesson.md` — complete example lesson with all files
4. **Read** `reference/04-task-format.md` — task.yml, body.md, hint.md, bonus.md format
5. **Read** `reference/05-boilerplate-files.md` — static files from template

These files contain the exact formats, examples, and conventions you MUST follow. Read them using the Read tool before proceeding with any generation.

## Quick Reference: Key Formats

### lesson.yml

```yaml
name: Lesson Title
position: 1
trainer: trainer@workshops.de
github_code_url: https://github.com/workshops-de/REPO
git_tag_starting: main
slides_type: slidev
pdf_generation_enabled: true
stackblitz_enabled: true
codesandbox_enabled: false
deprecated: false
```

### Lesson Entry Point (NN-name.md)

```markdown
---
background: https://cover.sli.dev
title: Lesson Title
info: |
  ## Lesson Title
  Description.
drawings:
  persist: false
transition: slide-left
mdc: true
seoMeta:
  ogImage: auto
base: /01-lesson-name/
out: ../../dist/01-lesson-name
theme: '@workshops.de/slidev-theme'
addons:
  - window-mockup
  - slidev-addon-tldraw
src: ./slides/first-topic/topic.md
---

---
src: ./slides/second-topic/topic.md
---

---
layout: end
---

# Vielen Dank!

Fragen?
```

### Topic Slides (topic.md) — 4-MAT Structure

```markdown
---
layout: cover
---

# Topic Title

Subtitle

---
layout: why
---

# Warum ist das wichtig?

- Real-world problem
- Motivation

---
layout: section
---

# Kernkonzepte

---

# Concept

- Key point with **bold emphasis**
- Clear, concise bullets

---
layout: little-what
---

# One-sentence summary.

---

# Code Example

```typescript
export class MyService {
  getData(): Observable<Data[]> {
    return this.http.get<Data[]>('/api/data');
  }
}
```

---
layout: what-if
---

# Was wenn wir mehr brauchen?

- Edge cases
- Alternative approaches

---
layout: task
---

# Übung: Task Title
```

### Available Slidev Layouts

`cover`, `section`, `sub-section`, `why`, `little-what`, `what-if`, `task`, `two-cols-header`, `ask-me-anything`, `end`, `default`

### task.yml

```yaml
title: 'Task Title'
position: 1
category: 'Basics'
preparation: false
estimated_time_in_minutes: 15
always_unlocked: false
git_tag_completed: solution-01-task-name
```

### body.md

```markdown
## Überblick

What participants will build.

## Schritte

### 1. Step Name

Instructions with code examples.

## Erfolgskriterien

- [ ] First criterion
- [ ] Second criterion
```

### hint.md

```markdown
## Hinweise

<details>
<summary>💡 Hinweis 1: Title</summary>

Hint content.

</details>

<details>
<summary>💡 Hinweis 2: Near-Solution</summary>

```typescript
// More specific hint
```

</details>
```

### 00-index.md

```markdown
---
background: https://cover.sli.dev
title: Workshop Name - Slide Decks
info: |
  ## Workshop Slide Decks
  Collection of lesson slide decks.
class: text-center
drawings:
  persist: false
transition: slide-left
mdc: true
seoMeta:
  ogImage: auto
base: /00-index/
out: ./dist/00-index
theme: '@workshops.de/slidev-theme'
---

# Workshop Name

Slide Deck Collection

<div class="pt-12">

## Available Lessons

</div>

<div class="grid grid-cols-2 gap-4 mt-4">

<a href="../01-lesson/" class="slidev-card p-4 rounded-lg no-underline">
  <strong>01 - Lesson Title</strong><br>
  <span class="text-sm opacity-75">Description</span>
</a>

</div>
```

### slides.md

```markdown
---
background: https://cover.sli.dev
title: All Lessons
drawings:
  persist: false
transition: slide-left
mdc: true
seoMeta:
  ogImage: auto
theme: '@workshops.de/slidev-theme'
addons:
  - window-mockup
  - slidev-addon-tldraw
---

---
src: ./00-index.md
---

---
src: ./lessons/01-lesson/01-lesson.md
---
```

## Content Quality Rules

1. **Language**: German by default (du/ihr), English if requested
2. **Code examples**: Realistic and functional, not placeholder
3. **Progressive difficulty**: Tasks build on each other
4. **4-MAT completeness**: Every topic needs WHY, WHAT, HOW, WHAT-IF
5. **Practical focus**: 50%+ of time = hands-on exercises
6. **Modern practices**: Current best practices and stable versions
7. **Slide density**: More slides with less content > fewer dense slides
8. **Task clarity**: Every task has clear success criteria
9. **Shiki annotations**: Use `// [!code highlight]`, `// [!code ++]`, `// [!code --]`, `// [!code focus]` in code blocks
10. **Max 2 code blocks per slide**, prefer 1-10 lines each
