# Feature Specification: AI-Native Textbook with RAG Chatbot

**Feature Branch**: `001-textbook-generation`
**Created**: 2025-12-06
**Status**: Draft
**Input**: Generate a feature specification for textbook-generation with an AI-native textbook and a RAG chatbot. Feature includes Docusaurus, auto-generated sidebar, RAG backend (Qdrant + Neon), free-tier embeddings, optional Urdu translation, and personalized chapters.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Student Reads Textbook Chapters (Priority: P1)

A student accesses the published textbook online and reads one of the six core chapters: Introduction to Physical AI, Basics of Humanoid Robotics, ROS 2 Fundamentals, Digital Twin Simulation, Vision-Language-Action Systems, or the Capstone project. The site loads quickly with a clean, modern layout; navigation is intuitive with an auto-generated sidebar reflecting the full chapter structure.

**Why this priority**: Core product delivery; students cannot learn without the textbook being published and readable. This is the foundation for all other features.

**Independent Test**: Can be fully tested by deploying the built static site (Docusaurus output) to GitHub Pages and verifying all 6 chapters render correctly with working internal links, no broken images, and <2s page load times.

**Acceptance Scenarios**:

1. **Given** the textbook is deployed, **When** a student navigates to a chapter URL, **Then** the page loads in <2 seconds and displays formatted Markdown content (text, code blocks, images).
2. **Given** a student is on Chapter 3 (ROS 2), **When** they click a sidebar link to Chapter 4 (Digital Twin), **Then** navigation is instant and the new chapter displays correctly.
3. **Given** the student is on a chapter page, **When** they select text, **Then** selection works normally (no UI breaks).

---

### User Story 2 - Student Asks RAG Chatbot Questions (Priority: P1)

A student reads Chapter 1 and has a question: "What is embodied intelligence?" They either (a) select text in the chapter and click "Ask AI" or (b) open the chatbot sidebar and type a question. The chatbot searches the vector database for relevant chapter content and responds with an accurate answer sourced strictly from the book, including chapter/section references.

**Why this priority**: RAG chatbot is a core product differentiator; ensures accurate, on-topic answers. This enables interactive learning and is a primary user engagement mechanism.

**Independent Test**: Can be fully tested by:
   - Indexing all 6 chapters into Qdrant
   - Submitting 10 test queries (in-scope and out-of-scope)
   - Validating responses: in-scope queries return answers with source citations; out-of-scope queries return "Not found in textbook"
   - Measuring latency (<1s p95 for API response)

**Acceptance Scenarios**:

1. **Given** a student selects "bipedal locomotion" text in Chapter 2, **When** they click "Ask AI", **Then** a chatbot pops open with the selected text pre-filled and ready to submit.
2. **Given** the chatbot is open, **When** the student submits "Explain bipedal locomotion", **Then** the chatbot responds within 1 second with an answer sourced from Chapter 2, including a citation (e.g., "Chapter 2: Basics of Humanoid Robotics, Section 2.2").
3. **Given** a student asks "What is machine learning?", **When** the chatbot processes this, **Then** it responds "This topic is not covered in the textbook" (graceful degradation; no hallucination).

---

### User Story 3 - Reader Chooses Personalized Chapter Variant (Priority: P2)

An intermediate-level reader wants to deepen their ROS 2 knowledge. They select "Intermediate" when prompted about their background. The system serves a variant of Chapter 3 with more advanced code examples, additional references, and deeper theoretical context—while the baseline chapter remains beginner-friendly.

**Why this priority**: Optional personalization enhances user experience and increases engagement. Defers non-critical scope; core textbook works without it.

**Independent Test**: Can be fully tested by creating two Chapter 3 variants (beginner/intermediate) and verifying:
   - System correctly detects user preference (cookie or session)
   - Correct variant is served based on preference
   - Baseline chapter remains unaffected if personalization is disabled

**Acceptance Scenarios**:

1. **Given** a reader visits the site for the first time, **When** they navigate to Chapter 3, **Then** they are prompted to select their background (Beginner / Intermediate / Advanced) with a clear explanation of what each level includes.
2. **Given** a reader has selected "Intermediate", **When** they reload Chapter 3, **Then** the intermediate variant is served (more advanced code, deeper theory).
3. **Given** a reader chooses "Beginner", **When** they later change their preference to "Advanced", **Then** the site switches to serving the advanced variant.

---

### User Story 4 - Reader Accesses Urdu Translation (Priority: P3)

A reader whose primary language is Urdu wants to access a translated version of Chapter 1. They click a language toggle and see the chapter title, key terms, and explanations in Urdu, while code examples and technical diagrams remain in English (not translated).

**Why this priority**: Expands accessibility and market reach. Optional; core book always works in English. Defers to post-MVP if resource-constrained.

**Independent Test**: Can be fully tested by:
   - Creating Urdu translation files for Chapter 1
   - Verifying language toggle switches between English and Urdu
   - Checking that code blocks and diagrams remain in English
   - Validating no layout breaks occur with right-to-left text

**Acceptance Scenarios**:

1. **Given** a reader is viewing Chapter 1 in English, **When** they click the language toggle, **Then** the page switches to Urdu and displays translated content (title, body text) while code blocks remain in English.
2. **Given** the page is in Urdu, **When** the reader reloads, **Then** the browser remembers the preference and serves Urdu by default.

---

### Edge Cases

- What happens when the Qdrant vector database is offline? (Chatbot responds: "Chat service is temporarily unavailable.")
- How does the system handle a malformed embed request from the frontend? (API returns 400 with clear error message; no 500 errors leak to user.)
- What if a chapter file is deleted or corrupted before build? (Build process fails with clear error; prevents deployment of incomplete textbook.)
- What if a user asks a question before any chapters are indexed? (Chatbot responds: "Textbook is still being prepared; please try again in a moment.")

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST build and deploy the complete 6-chapter textbook as a static site (Docusaurus) to GitHub Pages or Vercel with zero setup cost.
- **FR-002**: System MUST auto-generate a sidebar navigation tree reflecting all chapters and sections based on Markdown file structure.
- **FR-003**: System MUST serve the textbook frontend with page load times <2 seconds (p95) and support modern browsers (Chrome 90+, Firefox 88+, Safari 14+).
- **FR-004**: System MUST provide a RAG chatbot backend that:
  - Indexes all 6 chapters into a Qdrant vector database using free-tier embeddings (Sentence Transformers)
  - Accepts user queries and returns answers sourced strictly from chapter content
  - Includes source citations (chapter, section) with every answer
  - Returns "Not found in textbook" for out-of-scope queries (no hallucinations)
  - Responds to queries in <1 second (p95)
- **FR-005**: System MUST support select-text-to-ask-AI: users can highlight text in a chapter and trigger the chatbot with that text pre-filled.
- **FR-006**: System MUST persist user preferences (background level, language) in the browser (localStorage or session cookie) with no server-side user tracking required.
- **FR-007**: System MUST expose optional personalized chapter variants (Beginner / Intermediate / Advanced) selectable by user, while maintaining a single authoritative baseline chapter.
- **FR-008**: System MUST support optional Urdu translation for select chapters (Chapter 1 minimum), with right-to-left text handling and language toggle UI.
- **FR-009**: System MUST validate all links (internal and external) in the final build and fail the build if any link is broken.
- **FR-010**: System MUST run spell-check and grammar validation on all chapter content as part of the build pipeline; flag issues without blocking (warnings, not errors).

### Key Entities

- **Chapter**: A core unit of the textbook (6 total). Attributes: title, slug, path to Markdown file, version, language (EN/UR), optional personalization variants, publish status.
- **Section**: A subdivision within a chapter (heading + body). Attributes: heading level, title, anchor link, content hash for change detection.
- **ChatbotQuery**: A user question submitted to the RAG system. Attributes: query text, timestamp, user session ID (anonymous), embedding vector, top-k retrieved chapters/sections, response text, latency.
- **Variant**: An optional personalization of a chapter. Attributes: base chapter, level (Beginner/Intermediate/Advanced), content overrides (code examples, explanations), creation date.
- **Translation**: An optional language variant of a chapter. Attributes: base chapter, target language, translated sections (title, body), non-translated sections (code, diagrams), last updated.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Textbook successfully builds and deploys to GitHub Pages/Vercel in <30 seconds; build artifact is <100MB; zero deployment cost (free-tier services only).
- **SC-002**: All 6 chapters are complete, error-free, and render correctly in the final build with <2 second page load time (p95 measured in browser DevTools).
- **SC-003**: RAG chatbot returns accurate, sourced answers for 95%+ of in-scope queries (queries about content in the textbook). Accuracy validated by manual review of 50+ test queries.
- **SC-004**: RAG chatbot responds to queries in <1 second (p95), measured at API level. Zero hallucinations on out-of-scope queries; all off-topic responses return "Not found in textbook".
- **SC-005**: Select-text-to-ask-AI works end-to-end: users can highlight any text in a chapter and open the chatbot with that text pre-populated (latency <500ms).
- **SC-006**: User preferences (background level, language) persist across sessions with 100% reliability (browser storage validation).
- **SC-007**: All internal links (chapter references, sidebar navigation) are valid and tested; 100% link check pass rate in final build.
- **SC-008**: Textbook meets WCAG 2.1 AA accessibility standards for text, images, and interactive elements; verified with automated accessibility scanner (Axe or similar).
- **SC-009**: (Optional) Personalized chapter variants for at least one chapter are functional and correctly served based on user preference.
- **SC-010**: (Optional) Urdu translation for Chapter 1 is complete and renders correctly (no layout breaks, RTL text handling works).

## Assumptions

- Docusaurus 3.x is the frontend framework; builds output static HTML/CSS/JS suitable for GitHub Pages.
- Sentence Transformers (open-source, Python-based) is used for embeddings; free-tier compatible (<100MB memory).
- Qdrant vector database is self-hosted (Docker) or free-tier cloud; no monthly cost.
- Neon PostgreSQL is used for optional metadata storage (e.g., query logs, usage analytics); free tier supports 3GB storage.
- FastAPI backend runs on Vercel (free tier) or similar serverless platform; cold starts acceptable for this use case.
- No authentication required; textbook is fully public. User preferences are anonymous (no PII).
- Initial deployment targets GitHub Pages; future deployments may move to Vercel or similar.

## Out of Scope

- Live collaboration (multiple editors working on chapters simultaneously).
- Advanced personalization beyond Beginner/Intermediate/Advanced (e.g., role-based filtering).
- Multi-language support beyond optional Urdu translation; core textbook is English.
- Video content or interactive simulations (embedded links to external resources are acceptable).
- Real-time notifications or user accounts.
- Monetization or premium features.
- Search indexing for external search engines (Google, Bing) beyond Docusaurus default sitemap.
