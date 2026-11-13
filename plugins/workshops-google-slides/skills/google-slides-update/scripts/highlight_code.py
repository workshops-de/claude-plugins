"""
Syntax highlighter for the "Code Window" slide layout's BODY placeholder.

Given TypeScript or Angular-template (HTML) code (lines joined with plain
"\n"), computes:
  - the text to insert, with "\n" replaced by "\x0b" (vertical tab / soft
    line break) so Slides doesn't add per-line paragraph spacing
  - a list of {start, end, color, bold} ranges matching the palette in
    references/code-highlight-theme.md, ready to feed into updateTextStyle
    FIXED_RANGE requests

Usage as a library:
    from highlight_code import highlight
    text, ranges = highlight(code, known_types=["BooksClient"])
    text, ranges = highlight(template, language="html")

Usage as a CLI (reads code from stdin, prints {"text":..., "ranges":...}):
    python3 highlight_code.py [--language ts|html|auto] < snippet.ts

language: "ts", "html" or "auto" (default). "auto" picks "html" when the
snippet starts with "<" or an Angular control-flow block (@if, @for, ...),
otherwise "ts".

HTML mode colors (see references/code-highlight-theme.md):
  - tag names                          -> TYPE
  - attribute names / bindings         -> DECORATOR  (class, [x], (x), *ngIf, #ref)
  - static attribute values            -> STRING
  - binding values ([x]="...", (x)="...", *x="...") and {{ ... }} and
    control-flow headers (@if (...), @for (...), @let ...;)
                                       -> treated as expressions: keywords,
                                          calls, strings are highlighted as in TS
  - <!-- comments -->                  -> COMMENT
  - everything else (text content)     -> DEFAULT, never keyword-bold

known_types: pass class/interface names that appear as bare references
(e.g. inside inject(...) calls) elsewhere in the snippet, so every
occurrence gets the TYPE color even where it isn't followed by "(" or
after class/extends/implements.

This covers common TypeScript/Angular syntax well but is a heuristic, not
a real parser — always spot-check the built slide with get_page afterwards.
"""

import re
import json

KEYWORD = {"red": 0, "green": 0.0627, "blue": 0.502}
DECORATOR = {"red": 0, "green": 0.502, "blue": 0.627}
TYPE = {"red": 0.176, "green": 0.376, "blue": 0.792}
STRING = {"red": 0, "green": 0.467, "blue": 0.667}
DEFAULT = {"red": 0.2, "green": 0.2, "blue": 0.2}
COMMENT = {"red": 0.6, "green": 0.6, "blue": 0.6}

KEYWORDS = set("""export class private public protected return this import from readonly
async await const let var new extends implements interface static void true false null
undefined function if else for while try catch finally throw typeof instanceof in of
get set default case switch break continue delete yield as""".split())

# Only meaningful inside Angular control-flow headers, e.g. @for (x of xs; track x.id)
HTML_KEYWORDS = {"track", "on", "when", "prefetch", "hydrate"}

CONTROL_FLOW_RE = re.compile(
    r'(?<![\w.])@(?:else\s+if|else|if|for|empty|switch|case|default|defer|'
    r'placeholder|loading|error|let)\b')
INTERPOLATION_RE = re.compile(r'\{\{.*?\}\}', re.DOTALL)
HTML_COMMENT_RE = re.compile(r'<!--.*?-->', re.DOTALL)
TAG_RE = re.compile(r'</?[A-Za-z][^\s>/]*(?:"[^"]*"|\'[^\']*\'|[^>"\'])*>')
TAG_NAME_RE = re.compile(r'</?[^\s>/]+')
TAG_TOKEN_RE = re.compile(r'"[^"]*"|\'[^\']*\'|=|[^\s=<>"\'/]+')
STRING_RE = re.compile(r"""'(?:[^'\\]|\\.)*'|"(?:[^"\\]|\\.)*"|`(?:[^`\\]|\\.)*`""")
BINDING_PREFIXES = ("[", "(", "*", "bind-", "on-")


def detect_language(code):
    stripped = code.lstrip()
    if stripped.startswith("<") or CONTROL_FLOW_RE.match(stripped):
        return "html"
    return "ts"


def _runs(flags):
    """(start, end) spans of consecutive truthy entries in flags."""
    runs = []
    i, n = 0, len(flags)
    while i < n:
        if not flags[i]:
            i += 1
            continue
        j = i
        while j < n and flags[j]:
            j += 1
        runs.append((i, j))
        i = j
    return runs


def _balanced_paren_end(text, open_idx):
    """Index of the ")" matching the "(" at open_idx, or None if unbalanced."""
    depth = 0
    for i in range(open_idx, len(text)):
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth == 0:
                return i
    return None


def _scan_html(text, style, allowed, mark):
    """Mark HTML structure and flag the spans where expression rules apply."""
    n = len(text)
    protected = []  # spans in which no tag may start (comments, expressions)

    def allow(a, b):
        for i in range(a, b):
            allowed[i] = True

    for m in HTML_COMMENT_RE.finditer(text):
        mark(m.start(), m.end(), "COMMENT")
        protected.append(m.span())

    for m in INTERPOLATION_RE.finditer(text):
        if style[m.start()] is None:
            allow(*m.span())
            protected.append(m.span())

    # Angular control flow: @if (...) {, @for (...) {, @let x = ...;
    for m in CONTROL_FLOW_RE.finditer(text):
        if style[m.start()] is not None:
            continue
        mark(m.start() + 1, m.end(), "DECORATOR")  # name only, not the @
        if m.group(0) == "@let":
            end = text.find(";", m.end())
            end = n if end == -1 else end
            allow(m.end(), end)
            protected.append((m.start(), end))
            continue
        j = m.end()
        while j < n and text[j].isspace():
            j += 1
        if j < n and text[j] == "(":
            close = _balanced_paren_end(text, j)
            if close is not None:
                allow(j + 1, close)
                protected.append((j, close + 1))

    def is_protected(pos):
        return any(a <= pos < b for a, b in protected)

    for tag in TAG_RE.finditer(text):
        if is_protected(tag.start()) or style[tag.start()] is not None:
            continue
        name = TAG_NAME_RE.match(text, tag.start())
        name_start = tag.start() + (2 if text.startswith("</", tag.start()) else 1)
        mark(name_start, name.end(), "TYPE")

        attr = None
        expect_value = False
        for t in TAG_TOKEN_RE.finditer(text, name.end(), tag.end() - 1):
            a, b = t.span()
            tok = t.group(0)
            if tok == "=":
                expect_value = attr is not None
            elif tok[0] in "\"'":
                if expect_value and attr.startswith(BINDING_PREFIXES):
                    allow(a + 1, b - 1)
                elif expect_value:
                    mark(a, b, "STRING")
                attr, expect_value = None, False
            elif expect_value:  # unquoted value: attr=value
                if attr.startswith(BINDING_PREFIXES):
                    allow(a, b)
                else:
                    mark(a, b, "STRING")
                attr, expect_value = None, False
            else:
                mark(a, b, "DECORATOR")
                attr = tok


def highlight(code_nl, known_types=None, language="auto"):
    """code_nl: text using "\\n" between lines. Returns (text_with_vt, ranges)."""
    if language == "auto":
        language = detect_language(code_nl)
    if language not in ("ts", "html"):
        raise ValueError(f"unknown language {language!r}, expected 'ts', 'html' or 'auto'")
    html = language == "html"

    text = code_nl.replace("\n", "\x0b")
    n = len(text)
    style = [None] * n
    # Where TS-style token rules may apply. Everywhere for TS; only inside
    # expressions for HTML, so prose like "Note: Angular" stays untouched.
    allowed = [not html] * n
    keywords = KEYWORDS | HTML_KEYWORDS if html else KEYWORDS

    def mark(a, b, key, bold=False):
        for i in range(a, b):
            if style[i] is None:
                style[i] = (key, bold)

    def free(i):
        return style[i] is None and allowed[i]

    if html:
        _scan_html(text, style, allowed, mark)
    else:
        # comments (// to end of physical line, i.e. until \x0b or end)
        for m in re.finditer(r'//[^\x0b]*', text):
            mark(m.start(), m.end(), "COMMENT")

    # strings (single, double, backtick) - not touching already-marked spans.
    # Scanned per allowed run, so an apostrophe in HTML prose can't open a string.
    for run_start, run_end in _runs(allowed):
        for m in STRING_RE.finditer(text, run_start, run_end):
            a, b = m.span()
            if free(a):
                mark(a, b, "STRING")

    # decorators / Angular control-flow (@Component, @for, @if, ...)
    # HTML mode handles control flow in _scan_html.
    if not html:
        for m in re.finditer(r'@[A-Za-z_][A-Za-z0-9_]*', text):
            a, b = m.span()
            if free(a):
                mark(a + 1, b, "DECORATOR")  # color the name only, not the @

    # class/interface/extends/implements NAME -> TYPE
    for m in re.finditer(r'\b(class|interface|extends|implements)\s+([A-Za-z_][A-Za-z0-9_]*)', text):
        a, b = m.span(2)
        if free(a):
            mark(a, b, "TYPE")

    # generic type params <Ident> and array types Ident[]
    for m in re.finditer(r'<([A-Za-z_][A-Za-z0-9_]*)\s*(?:\[\])?>', text):
        a, b = m.span(1)
        if free(a):
            mark(a, b, "TYPE")
    for m in re.finditer(r'\b([A-Z][A-Za-z0-9_]*)\[\]', text):
        a, b = m.span(1)
        if free(a):
            mark(a, b, "TYPE")

    # type annotations: ": Ident" (colon-space-capitalized identifier)
    for m in re.finditer(r':\s*([A-Z][A-Za-z0-9_]*)\b', text):
        a, b = m.span(1)
        if free(a):
            mark(a, b, "TYPE")

    # identifier( -> TYPE (method/function call or decl), excluding keywords
    for m in re.finditer(r'\b([A-Za-z_][A-Za-z0-9_]*)\s*(?=\()', text):
        name = m.group(1)
        a, b = m.span(1)
        if name in keywords:
            continue
        if free(a):
            mark(a, b, "TYPE")

    # known extra type names (bare references, e.g. inject(BooksClient))
    if known_types:
        for tname in known_types:
            for m in re.finditer(r'\b' + re.escape(tname) + r'\b', text):
                a, b = m.span()
                if free(a):
                    mark(a, b, "TYPE")

    # keywords (word boundary), only over unmarked spans
    for m in re.finditer(r'\b[A-Za-z_][A-Za-z0-9_]*\b', text):
        w = m.group(0)
        a, b = m.span()
        if w in keywords and free(a):
            mark(a, b, "KEYWORD", bold=True)

    colors = {"KEYWORD": KEYWORD, "DECORATOR": DECORATOR, "TYPE": TYPE, "STRING": STRING, "COMMENT": COMMENT}
    ranges = []
    i = 0
    while i < n:
        if style[i] is None:
            i += 1
            continue
        key, bold = style[i]
        j = i
        while j < n and style[j] == (key, bold):
            j += 1
        ranges.append({"start": i, "end": j, "color": colors[key], "bold": bold})
        i = j

    return text, ranges


if __name__ == "__main__":
    import sys
    lang = "auto"
    if "--language" in sys.argv:
        lang = sys.argv[sys.argv.index("--language") + 1]
    code = sys.stdin.read()
    text, ranges = highlight(code, language=lang)
    print(json.dumps({"text": text, "ranges": ranges}, indent=2))
