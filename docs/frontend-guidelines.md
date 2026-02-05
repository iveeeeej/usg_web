# Frontend Guidelines & CSS Rules

This project uses **multiple CSS systems**:
- Manual Internal & External CSS
- Bootstrap (via CDN)
- Tailwind CSS (via NPM build process)

These systems are intentionally separated.  
**Violating these rules will break the UI.**

---

## 1. General Rules (APPLIES TO ALL DEVELOPERS & AI TOOLS)

- Any change to frontend behavior or styling MUST be communicated to the team.
- Do NOT make silent changes to CSS architecture.
- Do NOT assume files are safe to edit without checking this document.

---

## 2. Internal & External CSS Rules

Files under:
- `assets/css/style.css`
- Inline `<style>` blocks

### Rules
- ✅ Allowed for landing pages and non-module pages
- ❌ Do NOT mix Tailwind utilities here
- ❌ Do NOT add Tailwind directives (`@tailwind`, `@apply`) here

---

## 3. Bootstrap Rules (CDN-Based Pages)

Bootstrap is used ONLY in:
- `index.html`
- legacy dashboard pages

### Rules
- ❌ Do NOT use Tailwind CSS on Bootstrap pages
- ❌ Do NOT load Tailwind CSS together with Bootstrap
- ❌ Do NOT refactor Bootstrap pages into Tailwind without approval

Bootstrap pages are considered **stable / legacy UI**.

---

## 4. Tailwind CSS Rules (STRICT)

Tailwind CSS is used ONLY inside the `modules/` directory.

### File Responsibility

- `modules/css/input.css`
  → **SOURCE FILE (EDIT THIS)**

- `assets/css/app.css`
  → **COMPILED OUTPUT (DO NOT EDIT)**

### Rules

- ❌ NEVER edit `assets/css/app.css`
- ❌ NEVER add Tailwind CDN (`@tailwindcss/browser`)
- ❌ NEVER mix CDN Tailwind with compiled Tailwind
- ✅ ALWAYS edit `modules/css/input.css`
- ✅ ALWAYS run Tailwind in watch mode while developing: [```bash -> npx tailwindcss -i ./modules/css/input.css -o ./assets/css/app.css --watch]

---

## 5. Logo Images (IMPORTANT EXCEPTION)

Some UI logos (e.g., sidebar headers and brand marks) intentionally use **inline `width` and `height` styles**.

This is required to override Tailwind’s base preflight rule:

```css
img,
video {
  max-width: 100%;
  height: auto;
}
