---
name: google-slides-update
description: "Reviews and updates the Google Slides of a workshops.de lesson (slides_type: google_slides) when its content changed: finds the affected slides via the Google Slides MCP, links them for a scope check, asks about the 4-MAT principle and, on request, edits or creates slides with the workshop layouts (incl. the Code Window layout with syntax highlighting). Use when someone says \"update the slides\", \"check the slide update\", \"Slides aktualisieren\", \"Folien absichern\", \"Google Slides Review\" or asks whether slides are affected by a lesson change."
---

# Google Slides update

Review and update workflow for lessons whose slides live in Google Slides. Uses only the Google Slides MCP tools
(`get_presentation`, `summarize_presentation`, `get_page`, `batchUpdate` requests), e.g. from the
`google-slides-mcp` plugin. If those tools are missing, stop and tell the user which MCP server is needed.

Talk to the user in their language. The slides themselves are always in **English**: every new slide, suggestion or
text change for a slide is written in English.

## Preparation

- If the repository has a code submodule with the sample solution, update it first
  (`git submodule update --init <submodule>`) and make sure its solution branch is up to date, so slides match the
  current solution.
- Read `lessons/<lesson>/lesson.yml`. `google_slide_id` is the ID of the presentation to work on:

```yml
slides_type: google_slides
google_slide_id: 1fCXthDv9hMFrTPhfDUAkKd3BgmNsiVe_eOwgSkhsU30
```

- If the lesson is unclear, ask for it (`AskUserQuestion`, options = lessons with `slides_type: google_slides`).
  Stop if the lesson has no `google_slide_id`.

## Review (steps 1–6 change nothing)

1. **Clarify the change.** Ask briefly what changed in the lesson content (topic, keywords, new or removed
   section). Without a description, there is no sensible scope search.

2. **Search the slides.** Call `summarize_presentation(presentationId, include_notes: true)`. It returns
   `slideNumber`, `slideId` and the full text (incl. speaker notes) per slide. Match the user's keywords against
   titles, bullet points and notes and build a list of candidate slides: rather too broad than too narrow, the user
   narrows it down in step 3.

3. **Present candidates with links.** For every candidate give slide number, a short excerpt (title or first line)
   and a deep link `https://docs.google.com/presentation/d/<presentationId>/edit#slide=id.<slideId>`. Ask which
   candidates are really in scope (`AskUserQuestion`, `multiSelect: true`).

4. **4-MAT check.** For the confirmed slides, ask whether the update follows the 4-MAT learning principle:
   - **Why**: motivation and context, why it matters
   - **What**: the facts and concepts
   - **How**: practical application, exercise
   - **What if**: transfer, variants, edge cases, open questions

   This is a reflective question (Yes / No / Partly), not an automatic check: 4-MAT cannot be derived from slide
   text alone. If you notice yourself that a phase is missing, suggest useful additions.

5. **Summary.** In 2–3 sentences: which slides are confirmed in scope (with links) and the result of the 4-MAT
   question.

6. **Ask before changing.** Only edit the presentation when the user explicitly asks for it.

## Implementation (on request)

Adapt existing slides and/or create new ones. Pick the layout by the slide's didactic function:

| Layout          | Use for                                                                          |
| --------------- | -------------------------------------------------------------------------------- |
| Title Slide     | a new main topic in the deck                                                     |
| Section header  | a subtopic of a title slide                                                      |
| Main Point      | one important statement or rule (one sentence max.)                              |
| Little What     | a short explanation, one sentence that sums up the topic                         |
| Why             | why we need this feature                                                         |
| How             | how we use it                                                                    |
| What            | examples of how we use it                                                        |
| Task            | tells participants to work on a task now (title as in the task's `task.yml`)     |
| What If?        | sparks curiosity for upcoming questions and topics (edge cases, transfer)        |
| Lessons Learned | sums up what was learned in the section                                          |
| Code Window     | a code example, see [references/code-window.md](references/code-window.md)       |
| Code Window Explanation | code plus an explanation card, see [references/code-window-explanation.md](references/code-window-explanation.md) |

- Slide titles are short and fit on one line.
- Bullet lists: at most 4 items, each at most 70 characters, otherwise they do not fit on the slide.
- Code always uses the Code Window layouts and the syntax highlighting from
  [references/code-highlight-theme.md](references/code-highlight-theme.md). Read the references before building a
  code slide instead of guessing values.
- Look up layouts by display name in the target presentation
  (`get_presentation(presentationId, fields: "layouts(objectId,layoutProperties)")`, match
  `layoutProperties.displayName`). Layout IDs differ between decks and can change. If a layout is missing, tell the
  user it has to be added to the deck's master first.

## Bulk migration (e.g. changing the layout of many slides)

Do **not** compute `insertionIndex` for `createSlide` per slide in advance: every create or delete shifts the
following indices, so they go stale across batches (once, 28 new slides all ended up at the start instead of their
original positions).

Instead:

1. Save the original order first
   (`get_presentation(fields: "slides(objectId,slideProperties(layoutObjectId))")` into the scratchpad).
2. Build the new slides regardless of position (appending at the end is fine).
3. Compare actual and target order with a script and apply the difference as `updateSlidesPosition` requests in one
   `batchUpdate`.
4. Verify with `get_presentation(fields: "slides.objectId")`.

## Notes

- `get_page(presentationId, pageObjectId)` returns the details of one slide when the summary is not enough.
- The slide IDs from `summarize_presentation` are the `pageObjectId` values for `get_page` and the `id.<slideId>`
  part of the deep link.
