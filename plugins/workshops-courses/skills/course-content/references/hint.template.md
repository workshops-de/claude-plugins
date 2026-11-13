- **<Task step heading>** technical details about the respective step, inline code is highlighted with `input(){:ts}` or `[content]{:html}`

```ts
// <file-name.ts of the affected module>
import { Component, signal } from '@angular/core';

export class BookCard {
  customStyle = signal({ color: 'red' });
}
```

```html
<!-- <filename.html of the affected template> -->
<h4 [style]="customStyle()">{{ content().author }}</h4>
```

---

- **<Next task step heading>** ...
