---
description: "Task list for AI-Native Textbook with RAG Chatbot implementation"
---

# Tasks: AI-Native Textbook with RAG Chatbot

**Input**: Design documents from `/specs/001-textbook-generation/`
**Prerequisites**: plan.md (required), spec.md (user stories), data-model.md, contracts/
**Organization**: Tasks are grouped by user story (US1, US2, US3, US4) to enable independent implementation and testing.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and core tooling setup

### Frontend Setup

- [ ] T001 Initialize Docusaurus 3.x project with package.json at repository root
- [ ] T002 Create directory structure: `docs/`, `src/components/`, `src/styles/`, `scripts/`, `i18n/`
- [ ] T003 [P] Install dependencies: docusaurus, react, @docusaurus plugins (MDX, i18n, search)
- [ ] T004 [P] Configure docusaurus.config.js with sidebar auto-generation, i18n settings, and GitHub Pages/Vercel deployment
- [ ] T005 [P] Setup Eslint + Prettier for frontend code quality and formatting
- [ ] T006 Create `.github/workflows/build-deploy.yml` CI/CD pipeline (build → test → deploy to GitHub Pages)

### Backend Setup

- [ ] T007 Create Python project structure: `backend/src/`, `backend/tests/`, `backend/scripts/`, `backend/requirements.txt`
- [ ] T008 [P] Create `backend/src/main.py` FastAPI application entry point with CORS configuration
- [ ] T009 [P] Create `backend/src/config.py` for environment variables, free-tier API keys, Qdrant/Neon URLs
- [ ] T010 [P] Create `backend/src/api/models.py` with Pydantic schemas: ChatRequest, ChatResponse, Citation, HealthResponse, ErrorResponse
- [ ] T011 [P] Install backend dependencies: fastapi, uvicorn, sentence-transformers, qdrant-client, sqlalchemy, python-dotenv, pytest
- [ ] T012 [P] Setup pytest configuration: `backend/tests/conftest.py` with fixtures for embeddings, Qdrant client, mock data

### Indexing Pipeline Setup

- [ ] T013 Create `indexing/` directory with `chapters.json` manifest (placeholder with chapter IDs, paths, languages)
- [ ] T014 [P] Create `indexing/extract_chapters.py` skeleton that reads Markdown files and outputs chunk structure

**Checkpoint**: Project structure ready - both frontend and backend can be developed in parallel

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure required by ALL user stories

**⚠️ CRITICAL**: All tasks in this phase MUST complete before ANY user story implementation begins

### RAG Core Components

- [ ] T015 Implement `backend/src/rag/embeddings.py` with SentenceTransformer wrapper:
  - Load model: `sentence-transformers/all-MiniLM-L6-v2`
  - Expose `embed_text(text: str) -> List[float]` method
  - Cache loaded model (singleton pattern)

- [ ] T016 [P] Implement `backend/src/rag/retrieval.py` with Qdrant semantic search:
  - `search_chapters(query_vector: List[float], top_k: int = 3) -> List[dict]` returning section IDs, chapter info, text excerpts
  - Handle Qdrant connection errors gracefully
  - Support metadata filtering by chapter_id, section_id

- [ ] T017 [P] Implement `backend/src/rag/answer_generation.py` (LLM-free synthesis):
  - `synthesize_answer(query: str, retrieved_chunks: List[dict]) -> (str, List[Citation])`
  - Combine facts from top-k chunks into coherent answer
  - Extract source citations (chapter, section, excerpt) from retrieved chunks
  - Handle empty retrieval: return "Not found in textbook" message

### Database & Storage

- [ ] T018 Implement `backend/src/db/models.py` with SQLAlchemy:
  - ChatbotQuery model: query_text, session_id, embedding_vector, retrieved_sections, response_text, latency_ms, timestamp
  - No UserPreference model (stored client-side in localStorage)

- [ ] T019 [P] Implement `backend/src/db/neon.py` with Neon PostgreSQL connection:
  - Initialize database on startup (optional for MVP)
  - Provide `save_query(chatbot_query: ChatbotQuery)` method
  - Handle connection errors (non-blocking for MVP)

### API Routing

- [ ] T020 Implement `backend/src/api/routes.py` with two endpoints:
  - `POST /api/chat` (ChatRequest → ChatResponse pipeline using embeddings → retrieval → synthesis)
  - `GET /api/health` (check embeddings, Qdrant, database availability)
  - Include latency measurement (time from request to response)
  - Proper HTTP status codes: 200 (success), 400 (bad request), 503 (service unavailable)

- [ ] T021 [P] Add error handling middleware in `main.py`:
  - Catch and format exceptions (no stack traces to client)
  - Log errors to stderr for debugging
  - Graceful fallback responses

### Docusaurus Configuration

- [ ] T022 Configure `sidebars.js` for auto-generated sidebar from `docs/` directory structure
- [ ] T023 [P] Create `src/components/SelectTextHandler.jsx` that:
  - Detects text selection in chapter pages
  - Shows floating "Ask AI" button near selection
  - Passes selected text to ChatBot component

- [ ] T024 [P] Create `src/components/ChatBot.jsx` chatbot widget that:
  - Accepts pre-filled query from SelectTextHandler
  - Submits POST requests to `/api/chat`
  - Displays answer + citations with latency
  - Handles errors gracefully (service unavailable message)

### Indexing Pipeline Core

- [ ] T025 Implement `indexing/extract_chapters.py`:
  - Read all chapter Markdown files from `docs/*/index.md`
  - Parse sections by heading (H2/H3 as section boundaries)
  - Create chunks: 300-500 tokens per chunk, preserve section metadata
  - Output: list of {section_id, chapter_id, text, heading_level, title}

- [ ] T026 [P] Implement `indexing/embed.py`:
  - Load all chapters using extract_chapters.py
  - Embed each chunk using Sentence Transformers
  - Cache embeddings to avoid re-computation

- [ ] T027 [P] Implement `indexing/load_to_qdrant.py`:
  - Connect to Qdrant (self-hosted Docker or cloud)
  - Create collection if not exists: `textbook_chunks` with vector dimension 384
  - Upsert chunks as points with embeddings + metadata payload
  - Verify all chapters indexed before returning success

**Checkpoint**: RAG pipeline complete and testable in isolation. All user stories can now be implemented independently.

---

## Phase 3: User Story 1 - Student Reads Textbook Chapters (Priority: P1) 🎯 MVP

**Goal**: Publish a fully formatted, fast-loading textbook with all 6 chapters visible and navigable

**Independent Test**: Deploy Docusaurus build to GitHub Pages; verify all 6 chapters load <2s, sidebar works, links valid, WCAG 2.1 AA compliant

### Implementation for User Story 1

#### Chapter Content Creation

- [ ] T028 [P] Create `docs/01-introduction-to-physical-ai/index.md` with:
  - Frontmatter: id, title, sidebar_position
  - 3-5 sections (H2) covering embodied intelligence, principles, definitions
  - Include code examples, diagrams (placeholder paths), internal links to other chapters

- [ ] T029 [P] Create `docs/02-basics-of-humanoid-robotics/index.md`:
  - Sections: robot anatomy, sensor systems, bipedal locomotion kinematics
  - Code examples (Python pseudocode for kinematics calculations)

- [ ] T030 [P] Create `docs/03-ros2-fundamentals/index.md`:
  - Sections: nodes, topics, services, actions, rclpy integration, URDF
  - ROS 2 code snippets and configuration examples

- [ ] T031 [P] Create `docs/04-digital-twin-simulation/index.md`:
  - Sections: Gazebo overview, Isaac Sim, physics simulation, synthetic data generation

- [ ] T032 [P] Create `docs/05-vision-language-action-systems/index.md`:
  - Sections: VLA architecture, Whisper voice-to-action, language models, task planning

- [ ] T033 [P] Create `docs/06-capstone/index.md`:
  - Sections: end-to-end AI-robot pipeline, voice commands, navigation, object recognition
  - Reference to all 5 previous chapters

#### Frontend Components & Styling

- [ ] T034 [P] Create `src/components/LanguageToggle.jsx` that:
  - Shows EN/UR language selector (functional stub for P1; full i18n in US4)
  - Stores preference in localStorage
  - Triggers page layout update (dir="rtl" if Urdu)

- [ ] T035 [P] Create `src/components/PersonalizeModal.jsx` (functional stub for P1):
  - Shows Beginner/Intermediate/Advanced level selector (full impl in US3)
  - Stores preference in localStorage

- [ ] T036 [P] Create `src/styles/globals.css` with:
  - Clean, modern typography
  - Sidebar styling
  - Responsive layout (mobile, tablet, desktop)
  - Code block styling

- [ ] T037 [P] Create `src/styles/chatbot.css` with:
  - Chatbot panel positioning (bottom-right)
  - Input field and button styling
  - Citation collapsible styling
  - Accessibility: focus states, ARIA labels

- [ ] T038 Create `src/pages/index.js` homepage with:
  - Project title, brief description
  - Links to all 6 chapters
  - Overview of RAG chatbot feature (coming soon for P1)

#### Build & Link Validation

- [ ] T039 Create `scripts/validate-links.js`:
  - Parse all Markdown files in `docs/`
  - Extract internal links (references to other chapters)
  - Verify all linked files exist
  - Fail build if any links broken
  - Output: report of validated/broken links

- [ ] T040 Create `scripts/spellcheck.js`:
  - Run spell-check on all chapter Markdown files
  - Flag common misspellings (warnings, not errors)
  - Allow custom dictionary for robotics/AI terms

- [ ] T041 Create `scripts/build-sidebar.js`:
  - Auto-generate sidebar from `docs/*/index.md` structure
  - Include all H2/H3 headings as sidebar items
  - Output to `sidebars.js` (consumed by Docusaurus)

#### Build & Deployment

- [ ] T042 Configure GitHub Pages deployment:
  - Update `.github/workflows/build-deploy.yml`:
    - Run: `npm run build`
    - Run: `scripts/validate-links.js` (fail if broken links)
    - Run: `scripts/spellcheck.js` (warn but don't fail)
    - Deploy: push `build/` to `gh-pages` branch
  - Enable GitHub Pages in repo settings (gh-pages branch)
  - Verify site lives at `https://username.github.io/mybook`

#### Accessibility & Performance

- [ ] T043 Add accessibility features:
  - Run Axe accessibility scanner on built pages
  - Verify WCAG 2.1 AA compliance
  - Add skip-to-content link
  - Ensure keyboard navigation works (Tab through sidebar, chapters, links)

- [ ] T044 Measure and optimize page load time:
  - Run Lighthouse on each chapter page
  - Target: <2s p95 load time (measured with DevTools)
  - Optimize images (compress, lazy-load)
  - Analyze bundle size; identify and remove unused dependencies

**Checkpoint**: User Story 1 COMPLETE ✅ — All 6 chapters published, <2s load time, links validated, WCAG 2.1 AA compliant

---

## Phase 4: User Story 2 - Student Asks RAG Chatbot Questions (Priority: P1)

**Goal**: Deploy fully functional RAG chatbot that answers questions sourced strictly from textbook content with citations

**Independent Test**: Index all 6 chapters in Qdrant; submit 50 test queries (25 in-scope, 25 out-of-scope); verify 95%+ accuracy, <1s latency, zero hallucinations

### RAG Indexing & Testing

- [ ] T045 Run indexing pipeline (end-to-end):
  - Execute `python indexing/extract_chapters.py` (extract all chapters into chunks)
  - Execute `python indexing/embed.py` (embed each chunk with Sentence Transformers)
  - Execute `python indexing/load_to_qdrant.py` (load vectors to Qdrant)
  - Verify all 6 chapters indexed: count total chunks, verify no duplicates

- [ ] T046 [P] Create `indexing/validation/test_queries.json` with 50 test queries:
  - 25 in-scope queries (answerable from textbook):
    - "What is embodied intelligence?" (Chapter 1)
    - "Explain bipedal locomotion" (Chapter 2)
    - "What is a ROS 2 topic?" (Chapter 3)
    - ... (2 per chapter)
  - 25 out-of-scope queries (not in textbook):
    - "How do I bake a cake?"
    - "What is machine learning?" (not covered)
    - ... (generic, off-topic questions)
  - Include ground-truth answers for in-scope queries

- [ ] T047 Implement `indexing/validation/check_completeness.py`:
  - Verify all 6 chapters present in Qdrant
  - Verify embedding dimension (384 for all-MiniLM-L6-v2)
  - Verify metadata: chapter_id, section_id, text present on all points
  - Output: completeness report

- [ ] T048 [P] Implement `indexing/validation/test_accuracy.py`:
  - Load test_queries.json
  - For each query:
    - Embed query using Sentence Transformers
    - Retrieve top-3 chunks from Qdrant
    - Synthesize answer using answer_generation.py
    - Compare against ground-truth answer
    - Record: query, result (correct/incorrect/partial), latency
  - Output: accuracy report (target: 95%+ on in-scope, 100% "not found" on out-of-scope)

### Backend API Verification

- [ ] T049 [P] Create `backend/tests/contract/test_chat_api.py` (contract tests):
  - Test POST /api/chat with valid in-scope query → verify response schema (status, answer, sources, latency_ms)
  - Test POST /api/chat with out-of-scope query → verify "not found" response
  - Test POST /api/chat with missing query field → 400 Bad Request
  - Test GET /api/health → verify all components healthy
  - Test API latency: measure p95 response time (target <1000ms)

- [ ] T050 [P] Create `backend/tests/integration/test_rag_pipeline.py` (integration tests):
  - Full pipeline test: query → embed → retrieve → synthesize
  - Verify citations include correct chapter/section info
  - Verify no hallucinations in responses
  - Test graceful degradation when Qdrant offline

### Frontend Chatbot Integration

- [ ] T051 Update `src/components/ChatBot.jsx` to call backend:
  - Implement submit handler: POST to `${API_URL}/api/chat`
  - Display response: answer text + collapsible citations
  - Show latency: "Answered in 245ms"
  - Handle error: display "Chat service temporarily unavailable"
  - Add loading state during API call

- [ ] T052 [P] Implement `src/components/CitationExpander.jsx`:
  - Render citation list (Chapter, Section, Excerpt)
  - Click to expand/collapse excerpt
  - Link to specific section in chapter (if applicable)

- [ ] T053 [P] Update `src/styles/chatbot.css`:
  - Style citation cards with chapter/section headers
  - Collapsible excerpt display
  - Loading spinner animation

### Local Backend Development

- [ ] T054 Create `backend/.env.example` with:
  - `QDRANT_URL=http://localhost:6333` (local Docker)
  - `NEON_URL=postgres://...` (optional)
  - `LOG_LEVEL=DEBUG`

- [ ] T055 Create `backend/docker-compose.yml` for local development:
  - Qdrant service (port 6333)
  - Optional PostgreSQL service (for Neon testing)
  - Allow developers to run `docker-compose up` and have full backend environment

### Performance & Scaling

- [ ] T056 Implement `backend/scripts/load_test.py`:
  - Simulate 10 concurrent users, each submitting 5 queries
  - Measure latency percentiles (p50, p95, p99)
  - Target: p95 <1000ms
  - Output: load test report

- [ ] T057 Deploy backend to Vercel (free tier):
  - Create `vercel.json` with build config
  - Deploy: `vercel deploy`
  - Verify API endpoints accessible: `https://your-project.vercel.app/v1/api/chat`
  - Test latency from production (may include cold start)

- [ ] T058 Deploy Qdrant (choose one):
  - Option A: Self-hosted Docker (on server/droplet)
  - Option B: Qdrant Cloud (free-tier cluster)
  - Verify connection from Vercel backend to Qdrant
  - Test indexing and retrieval in production environment

### Documentation & Examples

- [ ] T059 Create `backend/README.md` with:
  - Setup instructions (Python 3.11+, dependencies)
  - Local development with `docker-compose up`
  - RAG indexing pipeline walkthrough
  - API endpoint examples (curl commands)
  - Accuracy testing instructions

- [ ] T060 Create `docs/chatbot-guide.md`:
  - User guide: how to ask questions in the chatbot
  - Examples of good vs. poor questions
  - How citations work
  - FAQ: "Why doesn't it know X?" (out-of-scope clarification)

**Checkpoint**: User Story 2 COMPLETE ✅ — Chatbot deployed, 95%+ accurate, <1s latency, zero hallucinations, integration tests passing

---

## Phase 5: User Story 3 - Reader Chooses Personalized Chapter Variant (Priority: P2)

**Goal**: Enable readers to select Beginner/Intermediate/Advanced level and serve appropriate chapter variants

**Independent Test**: Create Ch3 variants (beginner/intermediate/advanced); verify correct variant served based on localStorage preference; baseline chapter unaffected if personalization disabled

### Chapter Variant Creation

- [ ] T061 [P] Create `docs/variants/03-ros2-intermediate.md`:
  - Copy baseline Chapter 3 as starting point
  - Add advanced sections: custom message types, parameter servers, advanced debugging
  - Keep H2/H3 structure consistent with baseline (for sidebar)
  - All code examples more complex/comprehensive

- [ ] T062 [P] Create `docs/variants/03-ros2-advanced.md`:
  - Even deeper technical content
  - ROS 2 internals, performance tuning, distributed systems patterns
  - Advanced Python/C++ integration examples

### Frontend Personalization Components

- [ ] T063 Update `src/components/PersonalizeModal.jsx` (now functional):
  - Show three buttons: Beginner / Intermediate / Advanced
  - Explain each level (short description)
  - Store selection in localStorage: `personalization_level`
  - Trigger page reload to fetch correct variant

- [ ] T064 [P] Implement variant routing in Docusaurus config:
  - Detect `localStorage.personalization_level`
  - On navigation to Chapter 3, serve appropriate file:
    - BEGINNER → `docs/03-ros2-fundamentals/index.md` (baseline)
    - INTERMEDIATE → `docs/variants/03-ros2-intermediate.md`
    - ADVANCED → `docs/variants/03-ros2-advanced.md`

- [ ] T065 [P] Create `src/components/VariantSelector.jsx`:
  - Shows level selector on first visit to Chapter 3
  - Saves preference
  - Shows current level and option to change
  - Persists across sessions

### Testing & Validation

- [ ] T066 Create test data:
  - Verify personalization_level saved to localStorage
  - Verify correct variant file served when preference changes
  - Verify baseline works if preference not set (defaults to BEGINNER)

- [ ] T067 [P] Update CI/CD to validate variants:
  - Check that variant files exist and are valid Markdown
  - Verify variant files don't have broken internal links
  - Ensure all variants have same section structure (same H2/H3 headings)

### Documentation

- [ ] T068 Create `docs/personalization-guide.md`:
  - Explain personalization feature
  - How to select level
  - How variant content differs per level
  - How to add variants to other chapters (for future expansion)

**Checkpoint**: User Story 3 COMPLETE ✅ — Personalization working; correct variants served; baseline unaffected

---

## Phase 6: User Story 4 - Reader Accesses Urdu Translation (Priority: P3)

**Goal**: Provide Urdu translation of Chapter 1 with RTL text support and language toggle

**Independent Test**: Create Chapter 1 Urdu translation; toggle language EN ↔ UR; verify RTL rendering, code blocks untranslated, no layout breaks

### Urdu Translation & i18n Setup

- [ ] T069 Setup Docusaurus i18n plugin:
  - Configure `docusaurus.config.js` for multi-language support
  - Create `i18n/` directory structure:
    - `i18n/en/docusaurus-plugin-content-docs/current.json` (English strings)
    - `i18n/ur/docusaurus-plugin-content-docs/current.json` (Urdu strings)

- [ ] T070 [P] Translate `docs/01-introduction-to-physical-ai/index.md` to Urdu:
  - Create `docs/variants/01-introduction-ur/index.md` with Urdu content
  - Translate: title, section headings, body text
  - DO NOT translate: code blocks, technical diagrams, links, code variable names
  - Mark non-translated sections clearly

- [ ] T071 [P] Create Urdu translation file:
  - Translate UI strings to Urdu: "Ask AI", "Chat", "Chapters", etc.
  - Store in `i18n/ur/docusaurus-plugin-content-docs/current.json`
  - Verify all UI strings covered

### Language Toggle Implementation

- [ ] T072 Update `src/components/LanguageToggle.jsx` (now functional):
  - Show EN/UR toggle button in header
  - Click EN → set `localStorage.language = 'EN'`; reload page
  - Click UR → set `localStorage.language = 'UR'`; reload page
  - Docusaurus i18n plugin handles page rendering in selected language

- [ ] T073 [P] Update layout component to apply RTL:
  - Detect `localStorage.language === 'UR'`
  - Apply `dir="rtl"` to document root and relevant containers
  - Test that layout flips correctly: sidebar on right, text right-aligned

### Testing & Validation

- [ ] T074 [P] Test Urdu rendering:
  - Manual visual inspection: Urdu text displays correctly
  - No layout breaks with RTL text
  - Code blocks remain LTR (left-to-right)
  - Links and buttons work correctly

- [ ] T075 [P] Verify code blocks untranslated:
  - Scan Chapter 1 Urdu translation
  - Confirm all code blocks, examples, variable names in English
  - Confirm only prose/explanatory text is translated

- [ ] T076 Create `docs/urdu-translation-guide.md`:
  - Guidelines for translating chapters to Urdu
  - What to translate (prose, headings) vs. not (code, links)
  - How to manage translations in i18n/ directory
  - How to add more languages in future

### Documentation & Accessibility

- [ ] T077 Verify accessibility for RTL:
  - Run Axe scanner on Urdu pages
  - Verify WCAG 2.1 AA compliance still met with RTL layout
  - Test keyboard navigation in RTL mode

- [ ] T078 Create language selector documentation:
  - User guide: how to switch languages
  - Note: Urdu translation available for Chapter 1 only (MVP)
  - Roadmap: future translations for other chapters

**Checkpoint**: User Story 4 COMPLETE ✅ — Urdu translation functional, RTL rendering correct, language toggle working, WCAG 2.1 AA maintained

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final quality, optimization, and operational readiness

### Performance Optimization

- [ ] T079 Optimize Docusaurus build:
  - Minify CSS/JS
  - Compress images (JPEG, PNG, WebP formats)
  - Lazy-load images below fold
  - Verify final build artifact <100MB

- [ ] T080 [P] Optimize RAG latency:
  - Profile embeddings model loading time
  - Consider caching embeddings in-memory vs. loading on-demand
  - Profile Qdrant retrieval: target <100ms for top-3 retrieval
  - Profile answer synthesis: target <100ms for text combination

- [ ] T081 [P] Monitor production performance:
  - Setup logging in FastAPI backend (timestamp, latency, error count)
  - Collect metrics: queries/min, avg latency, error rate
  - Create dashboard or export logs for analysis

### Documentation & Guides

- [ ] T082 Create comprehensive `README.md` at project root:
  - Project overview
  - Architecture diagram (text or image)
  - Quick start: run locally, deploy to GitHub Pages/Vercel
  - Contributing guidelines
  - License

- [ ] T083 [P] Create deployment guide `docs/deployment.md`:
  - GitHub Pages setup (DNS, custom domain if applicable)
  - Vercel backend deployment (environment variables, secrets)
  - Qdrant deployment options (Docker, cloud, self-hosted)
  - Monitoring & troubleshooting

- [ ] T084 [P] Create developer guide `docs/developer-guide.md`:
  - Local development setup
  - Project structure walkthrough
  - How to add a new chapter
  - How to run tests
  - How to debug RAG issues

### Quality Assurance & Testing

- [ ] T085 Full end-to-end testing:
  - User journey 1: Load textbook → read chapter → navigate between chapters (manual)
  - User journey 2: Ask chatbot question → get answer with citation (manual + automated)
  - User journey 3: Change personalization level → verify correct variant served (manual)
  - User journey 4: Toggle language EN ↔ UR → verify RTL, no layout breaks (manual)

- [ ] T086 [P] Create automated test suite:
  - Run all backend unit tests: `pytest backend/tests/unit/`
  - Run all backend integration tests: `pytest backend/tests/integration/`
  - Run all backend contract tests: `pytest backend/tests/contract/`
  - Run Docusaurus build: `npm run build` (no errors/warnings)

- [ ] T087 [P] Accessibility audit (final):
  - Run Axe accessibility scanner on all pages (English & Urdu)
  - Fix any WCAG 2.1 AA violations found
  - Test with keyboard navigation (no mouse)
  - Test with screen reader (if possible)

- [ ] T088 [P] SEO & metadata:
  - Verify each chapter page has meta description
  - Setup Open Graph tags (og:title, og:description, og:image)
  - Generate sitemap.xml (Docusaurus default)
  - Verify robots.txt allows indexing (if desired)

### Monitoring & Maintenance

- [ ] T089 Setup error alerting:
  - Configure Vercel to email on backend errors
  - Setup CloudWatch or similar for production logs
  - Create runbook: "How to respond to chat service errors"

- [ ] T090 [P] Create maintenance checklist:
  - Monthly: review RAG accuracy (sample 50 queries)
  - Quarterly: update chapter content as course evolves
  - Quarterly: review and optimize RAG latency
  - Annually: audit Qdrant and Neon usage (free tier compliance)

---

## Summary

**Total Tasks**: 90

**Task Breakdown by Phase**:
- Phase 1 (Setup): 14 tasks
- Phase 2 (Foundational): 27 tasks
- Phase 3 (User Story 1): 18 tasks
- Phase 4 (User Story 2): 16 tasks
- Phase 5 (User Story 3): 8 tasks
- Phase 6 (User Story 4): 10 tasks
- Phase 7 (Polish): 10 tasks

**Task Breakdown by User Story**:
- US1 (Read Chapters): 18 tasks
- US2 (RAG Chatbot): 16 tasks
- US3 (Personalization): 8 tasks
- US4 (Urdu Translation): 10 tasks

**Parallelization Opportunities**:
- Phase 1: All setup tasks can run in parallel (T003-T006, T007-T012)
- Phase 2: RAG components can be built in parallel (T015-T017, T018-T019, T024-T027)
- Phase 3: All chapter content creation can run in parallel (T028-T033)
- Phase 4: Testing and backend work can run in parallel (T049-T050)
- Phase 7: All optimization and documentation tasks can run in parallel (T079-T090)

**MVP Scope** (Recommended for First Release):
- Phase 1: Setup (COMPLETE)
- Phase 2: Foundational (COMPLETE)
- Phase 3: User Story 1 (COMPLETE)
- Phase 4: User Story 2 (COMPLETE)
- Phase 7 (subset): Performance optimization, core documentation

**Post-MVP Features**:
- Phase 5: User Story 3 (Personalization)
- Phase 6: User Story 4 (Urdu Translation)
- Phase 7 (remainder): Advanced monitoring, full documentation

---

## Dependencies & Execution Order

```
Phase 1 (Setup) [parallel tasks: T003-T006, T007-T012]
    ↓
Phase 2 (Foundational) [parallel tasks: T015-T017, T018-T019, T024-T027]
    ├─→ Phase 3 (US1) [parallel: T028-T033, T036-T037]
    ├─→ Phase 4 (US2) [parallel: T049-T050, T051-T053, T056] (after T045-T048)
    ├─→ Phase 5 (US3) [parallel: T061-T062, T063-T064] (independent after Phase 2)
    └─→ Phase 6 (US4) [parallel: T070-T071, T072-T073] (independent after Phase 2)
            ↓
Phase 7 (Polish) [parallel: T079-T090]
```

**Critical Path**: Phase 1 → Phase 2 → Phase 3 → Phase 7 (MVP launch)

---

