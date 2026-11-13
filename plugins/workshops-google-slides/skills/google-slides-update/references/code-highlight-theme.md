# Code highlight theme

Blue-based palette matching the layout's accent. The `highlight_code.py` script uses exactly these values.

| Token type                                                                  | RGB (0–1)           | Hex      | Bold |
| :-------------------------------------------------------------------------- | :------------------ | :------- | :--- |
| Keywords (`export`, `class`, `private`, `return`, `this`, `import`, `from`) | 0, 0.0627, 0.502    | \#001080 | Yes  |
| Decorators / annotations (`@Injectable`, `@Component`, `@Input`)            | 0, 0.502, 0.627     | \#0080A0 | No   |
| Types / method names / function calls (`Book`, `getAll`, `get`, `inject`)   | 0.176, 0.376, 0.792 | \#2D60CA | No   |
| String literals                                                             | 0, 0.467, 0.667     | \#0077AA | No   |
| Comments                                                                    | 0.6, 0.6, 0.6       | \#999999 | No   |
| Standard text (punctuation, operators, remaining code)                      | 0.2, 0.2, 0.2       | \#333333 | No   |

Rules:

- Every language keyword (also `this`, `import`, `from`, `async`, `await` etc.) gets the keyword colour **and bold**.
- Every decorator or annotation (everything starting with `@`) gets the decorator colour on the name, not bold; the
  `@` itself stays standard.
- Class names, interfaces, generic type parameters AND called method/function names (also technical ones like
  `inject(...)`) get the type colour, which visually links declaration and call.
- Only real string literals get the string colour.
- Everything else (brackets, operators, property access like `.http.`) stays standard grey.
- For other languages (Java, Python, Kotlin, …) map their tokens to the same categories.

## HTML (Angular templates)

Same palette; HTML only maps its tokens:

| HTML token                                                                    | Colour                 | Bold |
| :---------------------------------------------------------------------------- | :--------------------- | :--- |
| Tag names (`div`, `app-book`, `ng-container`), also in closing tags           | Types (\#2D60CA)       | No   |
| Attribute names (`class`, `[value]`, `(click)`, `*ngFor`, `#ref`, `disabled`) | Decorators (\#0080A0)  | No   |
| Control-flow names (`@if`, `@else if`, `@for`, `@switch`, `@let`, `@defer`)   | Decorators (\#0080A0)  | No   |
| Static attribute values (`class="title"`, `type='button'`)                    | Strings (\#0077AA)     | No   |
| Keywords in expressions (`of`, `as`, `async`, `let`, `track`)                 | Keywords (\#001080)    | Yes  |
| Function calls in expressions (`select(book)`, `format(price)`)               | Types (\#2D60CA)       | No   |
| Comments `<!-- ... -->`                                                       | Grey (\#999999)        | No   |
| Angle brackets, `=`, `/`, quotes around binding values, text content          | Standard (\#333333)    | No   |

Rules:

- **Expressions vs. text:** keywords, function calls, types and strings are only highlighted inside _expressions_:
  `{{ ... }}`, binding values (`[x]="…"`, `(x)="…"`, `*x="…"`), control-flow headers (`@if (…)`, `@for (…)`) and
  `@let …;`. Text between tags stays standard grey: an "in" or "get" in text must never turn bold.
- **`class` is not a keyword in HTML** but an attribute name (decorator colour, not bold).
- **Binding values are not strings:** `[title]="book.title"` and `(click)="save()"` are coloured like TypeScript
  expressions (brackets and quotes standard grey). Only real string literals inside (`[title]="'Hello'"`) get the
  string colour.
- As with decorators, the `@` of control flow stays uncoloured; only the name (`if`, `for`, …) gets the decorator
  colour.
- Inline templates in TypeScript (`template: \`<div>…</div>\``) are a string literal and stay string colour. On
  slides, prefer showing templates as a separate HTML snippet.

The script [`highlight_code.py`](../scripts/highlight_code.py) detects HTML automatically (snippet starts with `<` or
`@if`/`@for`/…); explicitly with `highlight(code, language="html")`.
