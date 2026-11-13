# Code Window Explanation layout

Use this layout when the code needs additional explanation. It is the [Code Window](code-window.md) layout with an
extra card on the right for the explanation. Look it up by display name in the target deck like the Code Window
layout. Building the slide, line breaks (`\x0b`) and syntax highlighting work exactly as described in
[code-window.md](code-window.md); this file only covers the differences.

| Placeholder | Use                                       | Font (default)           |
| ----------- | ----------------------------------------- | ------------------------ |
| `TITLE`     | slide title                               | Arial 23pt               |
| `SUBTITLE`  | slide category                            | Helvetica 10pt, #2563eb  |
| `BODY`      | code (see code-window.md)                 | Fira Mono 13pt           |
| `BODY`      | explanation (see below)                   | Helvetica 12pt           |

`get_page` returns two `BODY` placeholders: tell them apart by position (code left, explanation right).

## Explanation card

### Card container

| Property             | Value                            | RGB (0–1)           | Hex      |
| :------------------- | :------------------------------- | :------------------ | :------- |
| Background fill      | light warning surface            | 0.996, 0.973, 0.965 | \#FEFAF6 |
| Border (outer)       | 1px solid neutral                | 0.898, 0.906, 0.922 | \#E5E7EB |
| Accent border (left) | 4px solid alert red              | 0.851, 0.188, 0.145 | \#D93025 |
| Corner radius        | 8px                              | -                   | -        |
| Padding              | 16px top/bottom, 20px left/right | -                   | -        |

### Typography and colours

| Element                                             | Font family                           | Size  | Weight        | Hex      | RGB (0–1)           | Special styling                                                                               |
| :-------------------------------------------------- | :------------------------------------ | :---- | :------------ | :------- | :------------------ | :-------------------------------------------------------------------------------------------- |
| Badge label ("LIMITATION")                          | Sans-serif (Roboto / Google Sans)     | 11 pt | Bold (700)    | \#D93025 | 0.851, 0.188, 0.145 | UPPERCASE; pill fill \#FCE8E6 (0.988, 0.910, 0.902); padding 3px 8px; radius 4px              |
| Section title ("Constructor Injection")             | Sans-serif (Roboto / Google Sans)     | 18 pt | Bold (700)    | \#1F2937 | 0.122, 0.161, 0.216 | margin-bottom 8px                                                                             |
| Body description text                               | Sans-serif (Roboto / Google Sans)     | 13 pt | Regular (400) | \#4B5563 | 0.294, 0.333, 0.388 | line height 1.45                                                                              |
| Inline code (`@Service()`)                          | Monospace (Roboto Mono / Courier New) | 12 pt | Regular (400) | \#0080A0 | 0, 0.502, 0.627     | decorator colour from the code palette                                                        |
| Fix section header ("💡 Recommended Fix")           | Sans-serif (Roboto / Google Sans)     | 14 pt | Bold (700)    | \#137333 | 0.075, 0.451, 0.200 | lightbulb prefix (U+1F4A1); margin-top 12px                                                   |
| Fix description text                                | Sans-serif (Roboto / Google Sans)     | 13 pt | Regular (400) | \#1F2937 | 0.122, 0.161, 0.216 | line height 1.45                                                                              |
| Fix inline code (`@Injectable({ providedIn: 'root' })`) | Monospace (Roboto Mono / Courier New) | 12 pt | mixed     | mixed    | mixed               | colours from the code palette, e.g. `@Injectable` \#0080A0, `providedIn` \#2D60CA, `'root'` \#0077AA |

### Hierarchy

1. Badge pill ("LIMITATION") at the top left of the card.
2. Title ("Constructor Injection") directly below the badge.
3. Problem description below the title.
4. Recommended fix, separated by a subtle divider or spacing, with the green header.
