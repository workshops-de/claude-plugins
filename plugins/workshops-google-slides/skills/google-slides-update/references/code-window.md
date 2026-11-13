# Code Window layout

Code examples use the slide layout **"Code Window"**. It contains the complete visual shell (card with shadow,
tab header, coloured dot, background gradient) and three placeholders:

| Placeholder | Use                 | Font (default)                    |
| ----------- | ------------------- | --------------------------------- |
| `TITLE`     | slide title         | Arial 23pt                        |
| `SUBTITLE`  | file name in the tab | Roboto Mono 11pt, bold, `#434343` |
| `BODY`      | code                | Fira Mono 13pt                    |

The shell is part of the layout, so do **not** build card, divider, dot or background per slide. Put new code slides
on this layout and only fill the placeholders and set the syntax highlighting.

The layout's `objectId` differs per deck and changes when the layout is recreated or duplicated in the master. Look it
up before building a slide:

```
get_presentation(presentationId, fields: "layouts(objectId,layoutProperties)")
→ entry with layoutProperties.displayName == "Code Window"
```

The internal name may still be `BLANK`; only the display name counts. If the deck has no "Code Window" layout, copy it
from the reference deck (see below) into the master first.

## Building a code slide

1. `createSlide` with `slideLayoutReference: { layoutId: "<Code Window objectId>" }`.
2. `get_page(presentationId, pageObjectId: "<new slide ID>")` to get the placeholder `objectId`s created on this slide
   (by `placeholder.type`: `TITLE`, `SUBTITLE`, `BODY`).
3. Per placeholder: `insertText` with the content (title, file name, the complete code in one go).
4. Set the syntax highlighting on the `BODY` placeholder: first one `updateTextStyle` with `textRange.type: ALL` for
   base colour, font and size, then one `updateTextStyle` with `textRange.type: FIXED_RANGE` per deviating token.
5. **Never count indices by hand.** Use the highlighter script in this skill's `scripts/` folder
   (next to `SKILL.md`):

   ```python
   import sys
   sys.path.insert(0, "<skill directory>/scripts")
   from highlight_code import highlight

   text, ranges = highlight(code, known_types=["BooksClient"])
   ```

   or as CLI: `python3 <skill directory>/scripts/highlight_code.py [--language ts|html|auto] < snippet.ts`

   `code` uses normal `\n` line breaks; the function returns the final text (with `\x0b` instead of `\n`, see below)
   and the highlight ranges. Pass `known_types` for class names that appear as bare references
   (e.g. `inject(BooksClient)`) so they get the type colour too. HTML and Angular templates are detected automatically
   (snippet starts with `<` or `@if`/`@for`/…), or pass `language="html"`. The script is a heuristic tagger for
   TypeScript and HTML, not a real parser. For other languages, apply the
   [theme](code-highlight-theme.md) by hand and compute ranges with a small script.

6. Read the slide again with `get_page` and spot-check that ranges and colours arrived as planned.

### ⚠️ Line breaks in code: never `\n`, always `\x0b`

A normal `\n` creates a **new paragraph** in Google Slides: every code line gets the placeholder's full paragraph
spacing (`spaceAbove`/`spaceBelow`) and the code looks stretched. Inside a code block, separate lines with a **soft
line break** (Shift+Enter in the UI, technically the vertical tab character `\x0b`), which stays in the same paragraph.

- Join every code line with `\x0b` instead of `\n`. An empty line is `\x0b\x0b`.
- `\x0b` is one character like `\n`, so range start and end indices do **not** change.
- Check after building: `get_page` should show **one** `paragraphMarker` spanning the whole `BODY` text. Several
  `paragraphMarker` entries mean `\n` was used: delete the text (`deleteText`, `textRange.type: ALL`) and insert it
  again with `\x0b`.
- `TITLE` and `SUBTITLE` are single-line and use normal `insertText`.

## Syntax highlighting

See [code-highlight-theme.md](code-highlight-theme.md).

## Reference slide

Live example with highlighting in the Angular HTTP deck: slide `wsde01_slide`
(`https://docs.google.com/presentation/d/1YQKMhSZvX_0PNBwvkUIpItLzhbrbOqXAIthOhjNKEAc/edit#slide=id.wsde01_slide`).
When unsure, read exact values there with `get_page` instead of guessing. This slide still uses the old, manually
built shell from before the "Code Window" layout existed. The deck's master also contains the "Code Window" layout to
copy into other decks.

## Layout maintenance (not part of the normal workflow)

The tab header uses the shape type `ROUND_2_SAME_RECTANGLE` (rounds only two adjacent corners), because the Slides API
does not allow one-sided rounded corners on normal rectangles. The card has a real Slides shadow
(`shadow.propertyState: RENDERED`). Change the shell in the master (_Slide → Edit theme_), not via API calls per slide.
