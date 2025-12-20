# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the website for **DBBP (Društvo Bistroumnih Bitij Pan-galaksije)** - a Slovenian association inspired by The Hitchhiker's Guide to the Galaxy. The project is built with **pure HTML5 and CSS3 only** - no JavaScript, no frameworks, no external libraries.

## Core Technical Constraints

**ABSOLUTE REQUIREMENTS:**
- Pure HTML5 + CSS3 only - zero JavaScript allowed
- No frameworks (React, Vue, Bootstrap, Tailwind, etc.)
- No preprocessors (Sass, Less, etc.)
- No external libraries or dependencies
- All interactive features must use CSS-only techniques (checkbox hacks, :hover, :target, etc.)

## Project Structure

The project uses a multi-page static website structure:

```
/
├── index.html              # Homepage (English)
├── index-slo.html          # Homepage (Slovenian)
├── about.html              # About page (English)
├── about-slo.html          # About page (Slovenian)
├── events.html             # Events page (English)
├── events-slo.html         # Events page (Slovenian)
├── contact.html            # Contact page (English)
├── contact-slo.html        # Contact page (Slovenian)
├── styles.css              # Single shared stylesheet for all pages
├── 404.html                # Custom 404 page (optional)
└── Img/                    # Images directory
    ├── 42.png
    ├── Don't_Panic.svg.png
    ├── LOGO-favourite.png
    └── The_Hitchhiker's_Guide_to_the_Galaxy.svg
```

## Design System

**Hitchhiker's Guide Aesthetic:**
- Background: Pure black (`#000`)
- Body text: Terminal green (`#0f0`)
- Headers: Yellow (`#ff0`)
- Font: Monospace (`'Courier New'` or similar)
- Style: Retro-futuristic terminal/computer aesthetic
- Theme elements: "Don't Panic" / "Ne Paničari!!!" branding

**Color Palette:**
```css
--bg-black: #000;
--text-green: #0f0;
--accent-yellow: #ff0;
```

## Key Features to Implement

### 1. Language Toggle (EN/SLO)
- Small button in top-right of header
- Links to corresponding page in other language (e.g., `about.html` ↔ `about-slo.html`)
- Style: Green border, yellow text, ~30px wide
- Must be present and functional on ALL pages

### 2. Navigation Menu
- **Desktop/Tablet:** Horizontal nav bar below main title
- **Mobile:** Hamburger menu using CSS checkbox hack
  - Hide menu by default
  - Show ☰ icon as label for hidden checkbox
  - When checked, display vertical dropdown using CSS `display` and transitions
- Links: Home, About, Events, Contact (localized for Slovenian pages)
- Minimum 44px tap targets for mobile accessibility

### 3. Header (All Pages)
- `<h1>` with "Ne Paničari!!!" (SLO) or "Don't Panic!!!" (EN) in yellow
- Blinking cursor effect using CSS animation
- Association name: "Društvo Bistroumnih Bitij Pan-galaksije - DBBP"
- Language toggle button
- Main navigation

### 4. Footer Navigation
- Small horizontal nav menu at bottom of each page
- Same links as header nav (Home, About, Events, Contact)
- Enables quick navigation without scrolling
- Copyright notice: "© 2025 DBBP - Društvo Bistroumnih Bitij Pan-galaksije. Vse pravice pridržane."

### 5. Responsive Design
- Mobile-first approach
- Breakpoint: 768px for tablets/mobile
- Vertical stacking on small screens
- Sticky header using `position: sticky`

## CSS Implementation Guidelines

**Required CSS Patterns:**
- CSS Reset for consistent rendering
- Custom properties for colors and spacing
- Flexbox for component layouts
- CSS Grid for page-level layouts
- Media queries for responsive breakpoints
- CSS animations (e.g., blinking cursor):
  ```css
  @keyframes blink {
    50% { opacity: 0; }
  }
  ```

**Accessibility Requirements:**
- Semantic HTML5 elements (`<header>`, `<nav>`, `<main>`, `<footer>`, etc.)
- High contrast (green on black)
- Proper `lang` attribute on `<html>` tag (`lang="en"` or `lang="sl"`)
- Keyboard navigation support
- Focus styles for interactive elements

## Content Guidelines

**Association Context:**
DBBP is a horizontal network focused on social reforms in Slovenia, inspired by Hitchhiker's Guide themes. The association advocates for:
- Basic income (Temeljni dohodek)
- 30-hour work week
- Energy and water self-sufficiency
- Housing reform
- Substance reform and mental health
- Criminal justice reform
- Economic growth and Balkan union
- Human rights and ethics

Content should reflect this progressive, pan-galactic vision with subtle Hitchhiker's references.

## Development Workflow

1. **Structure First:** Plan semantic HTML outline before styling
2. **Single Stylesheet:** All pages share `styles.css` - maintain consistency
3. **Progressive Enhancement:** Base functionality works without advanced CSS
4. **Test Responsiveness:** Use browser dev tools to test at 768px and below
5. **Validate:** Check HTML5 and CSS3 validity with W3C validators

## Common CSS-Only Patterns to Use

- **Mobile menu:** Checkbox hack with hidden input
- **Hover effects:** Use `:hover` and `transition` for smooth color changes
- **Focus management:** Style `:focus` states for keyboard navigation
- **Smooth transitions:** Apply to color, transform, opacity changes
- **Sticky positioning:** For persistent header

## What NOT to Do

- Never add JavaScript or event handlers
- Don't use external CDNs or libraries
- Avoid inline styles (use the shared stylesheet)
- Don't create unnecessary files - maintain the clean structure
- No preprocessor syntax in CSS
- Don't add !important unless absolutely necessary
- Avoid over-engineering - keep solutions simple and focused

## Browser Compatibility

Target modern evergreen browsers (Chrome, Firefox, Safari, Edge). Use standard CSS3 features that work across these platforms without prefixes where possible.
