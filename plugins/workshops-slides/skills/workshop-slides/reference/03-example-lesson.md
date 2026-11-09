# Example Lesson — Complete Reference

This shows a complete lesson from the template repository with all its files.

## File: lessons/01-example-lesson/lesson.yml

```yaml
name: Example Lesson Title
position: 1
trainer: trainer@workshops.de
github_code_url: https://github.com/workshops-de/example-code-repo
git_tag_starting: main
slides_type: slidev
pdf_generation_enabled: true
stackblitz_enabled: true
codesandbox_enabled: false
deprecated: false
```

## File: lessons/01-example-lesson/01-example-lesson.md

```markdown
---
background: https://cover.sli.dev
title: Example Lesson
info: |
  ## Example Lesson
  This is an example lesson to demonstrate the slide structure.
drawings:
  persist: false
transition: slide-left
mdc: true
seoMeta:
  ogImage: auto
base: /01-example-lesson/
out: ../../dist/01-example-lesson
theme: '@workshops.de/slidev-theme'
addons:
  - window-mockup
  - slidev-addon-tldraw
src: ./slides/example-topic/topic.md
---

---
layout: end
---

# Thank You!

Questions?
```

Note: If a lesson has multiple topics, add more `src` blocks before the end slide:

```markdown
src: ./slides/first-topic/topic.md
---

---
src: ./slides/second-topic/topic.md
---

---
src: ./slides/third-topic/topic.md
---

---
layout: end
---

# Thank You!
```

## File: lessons/01-example-lesson/slides/example-topic/topic.md

```markdown
---
layout: cover
---

# Your Workshop

Succeed, whatever you build

---
layout: section
---

# First Section

---
layout: sub-section
---

# First Sub-Section

---

# Hallo

**Strong**, _italic_, normal

---
layout: why
---

# Explains, why this topic matters.

---
layout: little-what
---

# Explain in one sentence what the following topic is about.

---
layout: what-if
---

# What if we want to bring it to the next level?

---
layout: task
---

# Create your own solution, now.

---

# Explanation

- Work with lists
- to explain important things
- step by step
- lists are easy to follow

---
layout: section
---

# Code Examples

---

# Simple Code Example

<WindowMockup codeblock title="my-file.js" padding="2rem">

```js
export function do() {
    return 'Success 🚀';
}
```

</WindowMockup>

---

# Magic move

````md magic-move
```ts
console.log('Hello, World!');
```

```js
console.log('Hello, World!');
console.log(`Step ${1}`);
```

```js
console.log('Hello, World!');
console.log(`Step ${1 + 1}`);
```
````

---
layout: two-cols-header
layoutClass: gap-x-2
---

# Side-by-side

::left::

```html
<p>Template</p>
```

::right::

```ts {all} twoslash
// @log: Custom log message
const a = 1;
// @error: Custom error message
const b = 1;
```

::bottom::

Shikijs and twoslash rock your code samples

---
layout: ask-me-anything
---
```
