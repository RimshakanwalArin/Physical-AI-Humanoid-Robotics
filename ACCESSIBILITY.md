# Accessibility Guidelines

This document outlines the accessibility standards and practices for the Physical AI Robotics Textbook.

## Overview

We are committed to making this textbook accessible to all learners, including those with disabilities. We follow WCAG 2.1 Level AA standards.

## WCAG 2.1 Compliance

### Perceivable
Content must be perceivable to all users regardless of sensory abilities.

#### Color Contrast
- All text has a contrast ratio of at least 4.5:1 (normal text)
- All interactive elements have a contrast ratio of at least 3:1
- Color is not the only means of conveying information

#### Images and Diagrams
- All images have descriptive alt text
- Complex diagrams include long descriptions
- Code syntax highlighting is not the only visual cue

#### Text Size and Spacing
- Default font size is 16px (readable by default)
- Line height is at least 1.5x the font size
- Letter spacing is at least 0.12x the font size
- Paragraph spacing is at least 2x the font size

### Operable
Users must be able to interact with content using any input method.

#### Keyboard Navigation
- All interactive elements are keyboard accessible
- Tab order is logical and visible
- No keyboard traps
- Chatbot can be used entirely with keyboard

#### Focus Management
- Focus indicator is visible at all times
- Focus order is logical
- Modal dialogs manage focus appropriately

#### Motion and Animation
- Animations respect `prefers-reduced-motion` setting
- No auto-playing videos with audio
- Animations do not cause seizures (no flashing more than 3x per second)

### Understandable
Content and interfaces must be understandable to users.

#### Language
- Page language is declared in HTML
- Language changes are marked with `lang` attribute
- Technical terms are defined or linked to glossaries

#### Text Clarity
- Simple, clear language (grade 8 level when possible)
- Active voice preferred
- Code examples are well-commented
- Abbreviations are expanded on first use

#### Readability
- Readable fonts (sans-serif preferred)
- Justified text is avoided
- Line length is between 45-75 characters

#### Predictability
- Consistent navigation patterns
- Consistent component behavior
- No unexpected context changes

### Robust
Content must work with current and future assistive technologies.

#### HTML Semantics
```html
<!-- Use semantic HTML -->
<button>Click me</button>      <!-- Not <div onClick> -->
<nav>...</nav>                  <!-- Not <div class="nav"> -->
<main>...</main>                <!-- Main content -->
<article>...</article>          <!-- Blog posts, chapters -->
<section>...</section>          <!-- Sections of content -->
<aside>...</aside>              <!-- Sidebars -->
<header>...</header>            <!-- Page header -->
<footer>...</footer>            <!-- Page footer -->
```

#### ARIA Labels
```jsx
// For icons without text
<button aria-label="Close menu">
  <IconX />
</button>

// For complex regions
<div aria-label="Chat messages" role="log">
  {messages.map(msg => ...)}
</div>

// For form fields
<input
  id="search-query"
  type="text"
  aria-label="Search textbook"
/>
<label htmlFor="search-query">Search</label>
```

#### Screen Reader Support
- All images have meaningful alt text
- Links have descriptive text (avoid "click here")
- Form labels are associated with inputs
- Error messages are announced
- Loading states are announced

## Implementation Guidelines

### Frontend Components

#### ChatBot Component
```jsx
<div
  className="chatbot-container"
  role="complementary"
  aria-label="Chatbot assistant"
>
  <form onSubmit={handleSubmit}>
    <label htmlFor="chat-input">Ask about the textbook:</label>
    <input
      id="chat-input"
      type="text"
      placeholder="Your question..."
      aria-describedby="chat-help"
    />
    <span id="chat-help">
      Type your question and press Enter or click Send
    </span>
    <button type="submit">Send</button>
  </form>

  {loading && <div role="status" aria-live="polite">
    Processing your question...
  </div>}

  {answer && (
    <article aria-label="Chat response">
      <h2>Answer</h2>
      <p>{answer}</p>
      {sources.length > 0 && (
        <section aria-label="Sources">
          <h3>Sources</h3>
          <ul>
            {sources.map(src => (
              <li key={src.id}>
                <a href={`#${src.id}`}>
                  {src.chapter_title}: {src.section_title}
                </a>
              </li>
            ))}
          </ul>
        </section>
      )}
    </article>
  )}
</div>
```

#### Text Selection Handler
```jsx
<button
  className="ask-ai-button"
  onClick={handleAskAI}
  aria-label={`Ask about selected text: ${selectedText}`}
>
  Ask AI about this
</button>
```

### Keyboard Support

#### Expected Shortcuts
- `Tab` - Navigate to next focusable element
- `Shift+Tab` - Navigate to previous focusable element
- `Enter` - Activate button or submit form
- `Escape` - Close modals or exit focus modes
- `/` - Focus search input (optional)

### Testing for Accessibility

#### Manual Testing Checklist
- [ ] Keyboard-only navigation works
- [ ] Screen reader announces all content
- [ ] Tab order is logical
- [ ] Color contrast meets requirements
- [ ] Images have alt text
- [ ] Form labels are present
- [ ] Error messages are clear
- [ ] Focus indicator is visible

#### Automated Tools
```bash
# Install accessibility testing tools
npm install -D axe-core jest-axe

# Run accessibility tests
npm test -- --testPathPattern=accessibility
```

#### Browser Extensions
- [axe DevTools](https://www.deque.com/axe/devtools/)
- [WAVE](https://wave.webaim.org/extension/)
- [Lighthouse](https://developer.chrome.com/docs/lighthouse/)

#### Screen Reader Testing
- **Windows**: NVDA (free), JAWS (paid)
- **macOS**: VoiceOver (built-in)
- **iOS**: VoiceOver (built-in)
- **Android**: TalkBack (built-in)

### CSS Accessibility

```css
/* High contrast mode support */
@media (prefers-contrast: more) {
  .button {
    border: 2px solid currentColor;
  }
}

/* Respect motion preferences */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  :root {
    --bg-color: #1a1a1a;
    --text-color: #e0e0e0;
  }
}

/* Focus styles */
button:focus-visible {
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}

/* Skip link for keyboard users */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #000;
  color: #fff;
  padding: 8px;
  text-decoration: none;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
```

## Content Guidelines

### Writing for Accessibility

#### Use Clear Headings
```markdown
# Main Topic (H1)
## Subtopic (H2)
### Sub-subtopic (H3)

<!-- Don't skip heading levels -->
<!-- Bad: H1 → H3 -->
<!-- Good: H1 → H2 → H3 -->
```

#### Alt Text for Images
```html
<!-- Bad -->
<img src="robot.jpg" alt="robot" />

<!-- Good -->
<img
  src="robot.jpg"
  alt="Humanoid robot standing in stable posture with legs apart at 30cm"
/>

<!-- For decorative images -->
<img src="decoration.jpg" alt="" aria-hidden="true" />
```

#### Code Examples
```jsx
// Good - clear variable names
const calculateBalance = (centerOfMass, supportBase) => {
  const margin = centerOfMass.distance(supportBase);
  return margin > STABILITY_THRESHOLD;
};

// Bad - unclear notation
const cb = (cm, sb) => cm.d(sb) > ST;
```

#### Lists and Navigation
```markdown
- Use bullet points for non-sequential lists
  - Organize hierarchically
  - Keep items parallel in structure

1. Number for sequential lists
2. Like steps in a procedure
3. Or ranking of items
```

## Links and Navigation

### Link Text
```html
<!-- Bad -->
<a href="/docs">Click here</a> to learn more about robotics.

<!-- Good -->
<a href="/docs">Learn more about humanoid robotics fundamentals</a>

<!-- Bad -->
<a href="/api">→</a>

<!-- Good -->
<a href="/api">Go to API documentation</a>
```

## Forms and Inputs

### Form Accessibility
```jsx
<form>
  <div>
    <label htmlFor="email">Email Address:</label>
    <input
      id="email"
      type="email"
      name="email"
      required
      aria-required="true"
      aria-describedby="email-help"
    />
    <span id="email-help">
      We'll never share your email address
    </span>
  </div>

  <div>
    <label htmlFor="message">Message:</label>
    <textarea
      id="message"
      name="message"
      aria-describedby="message-error"
      aria-invalid={hasError}
    />
    {hasError && (
      <span id="message-error" role="alert">
        Message is required
      </span>
    )}
  </div>

  <button type="submit">Submit</button>
</form>
```

## Internationalization for Accessibility

### Language Attributes
```jsx
// English
<html lang="en">

// Urdu
<html lang="ur">

// Code in English with comments
<div lang="en">
  {englishContent}
</div>

// Urdu content
<div lang="ur">
  {urduContent}
</div>
```

## Multimedia Accessibility

### Videos and Captions
- All videos include closed captions (CC)
- Transcripts available for all audio content
- Audio descriptions for important visual information

### Images and Diagrams
- Code architecture diagrams have text descriptions
- Robot anatomy images include labeled parts
- Charts have accessible data tables as alternatives

## Performance and Accessibility

### Page Load Time
- Accessibility should not sacrifice performance
- Lazy load non-critical images
- Minify CSS and JavaScript
- Use CDN for static assets

### Color and Vision
```css
/* Sufficient contrast */
body {
  color: #333; /* Dark gray on light background */
  background: #fff; /* White */
}

/* Color-blind friendly palette */
:root {
  --primary: #0173B2; /* Blue - color-blind safe */
  --success: #029E73; /* Green - color-blind safe */
  --danger: #D55E00; /* Orange - color-blind safe */
}
```

## Accessibility Testing Schedule

- **During development**: Use tools like axe during development
- **Code review**: Check accessibility in PRs
- **Pre-release**: Full accessibility audit
- **Quarterly**: Re-test with assistive technologies
- **User feedback**: Monitor and fix accessibility issues

## Resources

- [WebAIM](https://webaim.org/) - Web Accessibility Resources
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Inclusive Components](https://inclusive-components.design/)
- [A11y Project](https://www.a11yproject.com/)

## Reporting Accessibility Issues

Found an accessibility issue? Please report it:

1. **GitHub Issues**: File a detailed issue
2. **Email**: accessibility@example.com
3. **Include**:
   - What issue you encountered
   - Which assistive technology you used
   - Steps to reproduce
   - Expected vs. actual behavior

We take accessibility seriously and will respond within 48 hours.

---

Last updated: 2024
Accessibility standards: WCAG 2.1 Level AA
