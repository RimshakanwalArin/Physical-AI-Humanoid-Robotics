# Implementation Plan: AI-Native Textbook with RAG Chatbot

**Branch**: `001-textbook-generation` | **Date**: 2025-12-06 | **Spec**: [specs/001-textbook-generation/spec.md](spec.md)
**Input**: Feature specification from `/specs/001-textbook-generation/spec.md`

## Summary

Build an AI-native textbook with 6 chapters (Physical AI, Humanoid Robotics, ROS 2, Digital Twin, VLA Systems, Capstone) using Docusaurus for the frontend and a RAG chatbot backend. The chatbot indexes chapters in Qdrant, answers user questions with source citations, and prevents hallucinations. Optional personalization (Beginner/Intermediate/Advanced) and Urdu translation enhance accessibility. All infrastructure must be free-tier compatible with zero hard costs. Core deliverables: fast-loading static site (<2s, <100MB), accurate RAG responses (<1s, 95% accuracy), graceful degradation for off-topic queries, and full WCAG 2.1 AA accessibility.

## Technical Context

**Language/Version**: JavaScript (frontend, Node.js 18+), Python 3.11+ (backend)
**Primary Dependencies**:
  - Frontend: Docusaurus 3.x, React, MDX
  - Backend: FastAPI, Sentence Transformers, Qdrant client, Neon PostgreSQL client
  - Indexing: Qdrant (vector DB), Neon PostgreSQL (metadata)

**Storage**:
  - Qdrant (embeddings, semantic search)
  - Neon PostgreSQL (query logs, user preferences, analytics metadata)
  - Static files: GitHub Pages / Vercel (build artifacts)

**Testing**:
  - Frontend: Jest/React Testing Library (Docusaurus integration)
  - Backend: pytest (RAG logic, embeddings, API contracts)
  - E2E: Playwright or Cypress (chatbot interaction, select-text-to-ask)

**Target Platform**: Web (cross-browser: Chrome 90+, Firefox 88+, Safari 14+)
**Project Type**: Web (frontend static + backend API)
**Performance Goals**:
  - Page load: <2s p95 (frontend metrics)
  - API response: <1s p95 (RAG queries)
  - Build time: <30s
  - Deployment artifact: <100MB static assets

**Constraints**:
  - Zero hard costs (free-tier services only)
  - No GPU required
  - Minimal memory footprint (Sentence Transformers <100MB)
  - Browser-compatible API (CORS, standard REST/JSON)

**Scale/Scope**:
  - 6 chapters (estimated 200-400 pages total)
  - ~50-100 KB vectors per chapter (Sentence Transformers embeddings)
  - <1000 daily active users (MVP)
  - ~10-50 chatbot queries per user session

## Constitution Check ✅

*GATE: Verify adherence to principles I–VI before Phase 0. Re-check after Phase 1.*

| Principle | Adherence | Notes |
|-----------|-----------|-------|
| **I. Content Accuracy & Source Integrity** | ✅ PASS | RAG system enforces sourced-only answers with citations; graceful degradation for off-topic queries |
| **II. Minimalism & Lightweight Architecture** | ✅ PASS | Docusaurus static build, free-tier embeddings (Sentence Transformers), <30s build, <100MB deployment |
| **III. Free-Tier Friendly Deployment** | ✅ PASS | GitHub Pages (static), Qdrant (self-hosted Docker or free-tier cloud), Neon PostgreSQL (free tier), FastAPI on Vercel (free) |
| **IV. Integrated AI – Content-Centric RAG** | ✅ PASS | Vector embeddings + semantic search, select-text Q&A, graceful degradation (no hallucinations) |
| **V. Comprehensive Documentation & Personalization** | ✅ PASS | 6 chapters with tutorials, optional Beginner/Intermediate/Advanced variants, optional Urdu translation (Chapter 1) |
| **VI. Test-First Development & Quality Gates** | ✅ PASS | Build pipeline includes link validation, spell-check, grammar checks; RAG tested for accuracy and latency |

**Gate Result**: ✅ **PASS** — Design adheres to all 6 constitutional principles. No violations or tradeoffs needed.

## Project Structure

### Documentation (this feature)

```text
specs/001-textbook-generation/
├── plan.md                          # This file
├── data-model.md                    # Phase 1: Entities & relationships
├── quickstart.md                    # Phase 1: Developer guide
├── contracts/
│   ├── rag-api.openapi.yaml        # RAG chatbot API (OpenAPI 3.0)
│   └── frontend-api-contract.json  # Frontend ↔ Backend contract
├── checklists/
│   └── requirements.md             # Quality checklist
└── tasks.md                        # Phase 2: Testable tasks (/sp.tasks)
```

### Source Code (repository root)

**Frontend** (Docusaurus static site):
```text
docs/
├── 01-introduction-to-physical-ai/
│   ├── index.md
│   ├── embodied-intelligence.md
│   └── principles.md
├── 02-basics-of-humanoid-robotics/
├── 03-ros2-fundamentals/
├── 04-digital-twin-simulation/
├── 05-vision-language-action-systems/
├── 06-capstone/
└── variants/                       # Optional personalization
    ├── 03-ros2-intermediate.md
    ├── 03-ros2-advanced.md
    └── ...

docusaurus.config.js               # Docusaurus config
sidebars.js                        # Auto-generated sidebar
src/
├── components/
│   ├── ChatBot.jsx               # Chatbot widget
│   ├── SelectTextHandler.jsx     # Select-to-ask functionality
│   ├── LanguageToggle.jsx        # Language switcher (EN/UR)
│   └── PersonalizeModal.jsx      # Level selector (Beginner/Intermediate/Advanced)
├── pages/
│   └── index.js                  # Homepage
└── styles/
    ├── globals.css
    └── chatbot.css

i18n/
├── en/
│   └── docusaurus-plugin-content-docs/
│       └── current.json
└── ur/                           # Urdu translations (optional)
    └── docusaurus-plugin-content-docs/
        └── current.json

scripts/
├── validate-links.js             # Link validation
├── spellcheck.js                 # Spell-check
└── build-sidebar.js              # Auto-generate sidebar

package.json
.github/workflows/build-deploy.yml # CI/CD
```

**Backend** (FastAPI RAG service):
```text
backend/
├── src/
│   ├── main.py                       # FastAPI app entry
│   ├── api/
│   │   ├── routes.py                # Chat endpoint, health check
│   │   └── models.py                # Request/response schemas
│   ├── rag/
│   │   ├── embeddings.py            # Sentence Transformers wrapper
│   │   ├── indexing.py              # Qdrant indexing (batch, incremental)
│   │   ├── retrieval.py             # Semantic search (top-k retrieval)
│   │   └── answer_generation.py     # Prompt + LLM-free synthesis from retrieved chunks
│   ├── db/
│   │   ├── models.py                # SQLAlchemy: ChatbotQuery, UserPreference
│   │   └── neon.py                  # Neon PostgreSQL client
│   └── config.py                    # Environment, free-tier API keys
├── tests/
│   ├── unit/
│   │   ├── test_embeddings.py
│   │   ├── test_retrieval.py
│   │   └── test_answer_gen.py
│   ├── integration/
│   │   ├── test_rag_pipeline.py    # End-to-end: embed → retrieve → answer
│   │   └── test_api_contract.py    # API input/output validation
│   └── conftest.py                  # pytest fixtures
├── scripts/
│   ├── index_chapters.py            # Batch index all 6 chapters
│   ├── validate_accuracy.py         # Test 50+ queries for accuracy
│   └── load_test.py                 # Simulate concurrent requests
└── requirements.txt
```

**Indexing & Data Pipeline** (one-time + periodic):
```text
indexing/
├── chapters.json                    # Manifest: {chapter_id, path, language, variants}
├── extract_chapters.py              # Extract chapters → chunks (300-500 tokens each)
├── embed.py                         # Sentence Transformers → embeddings
├── load_to_qdrant.py               # Insert/update Qdrant vectors
└── validation/
    ├── check_completeness.py       # Verify all chapters indexed
    └── test_queries.json           # 50+ test queries (ground truth answers)
```

**Structure Decision**:
- **Frontend**: Docusaurus (static generator) + React components for chatbot & personalization. Variants stored as separate markdown files per level. i18n for Urdu.
- **Backend**: FastAPI microservice (stateless, scales on Vercel) for RAG queries. Qdrant for vectors, Neon PostgreSQL for metadata. No authentication (public textbook).
- **Separation rationale**: Static frontend decouples from backend; fast loads via CDN (GitHub Pages). Backend scales independently for chatbot workload.

## Phase 0: Research & Technical Decisions

**All decisions are clarified; no NEEDS CLARIFICATION markers remain.**

### Resolved Decisions:

1. **RAG Answer Generation**: Use retrieval + prompt synthesis (no LLM call). Backend retrieves top-3 relevant chunks from Qdrant, synthesizes answer by combining facts from chunks, includes citations.
   - **Why**: Avoids hallucinations (no LLM inventing facts), respects free-tier constraint (no OpenAI API costs).

2. **Embedding Model**: Sentence Transformers (`sentence-transformers/all-MiniLM-L6-v2`).
   - **Why**: Open-source, <100MB memory, free-tier compatible, good semantic performance for QA.

3. **Vector Store**: Qdrant (self-hosted Docker or free-tier cloud).
   - **Why**: Lightweight, supports metadata filtering, free-tier option available.

4. **Chunking Strategy**: 300-500 token chunks per section; preserve section boundaries.
   - **Why**: Balances context window with retrieval relevance; includes source metadata (chapter, section).

5. **Personalization Strategy**: Separate markdown files per variant (Ch3-beginner.md, Ch3-intermediate.md, Ch3-advanced.md). Frontend detects preference (localStorage), serves correct file.
   - **Why**: Minimal complexity, no database needed, leverages Docusaurus static generation.

6. **Urdu Translation**: Markdown i18n plugin; translated body/title, code blocks untranslated.
   - **Why**: Docusaurus i18n native support, avoids translating code.

7. **Deployment**: GitHub Pages (static) + Vercel (backend API, free tier).
   - **Why**: Zero cost, GitHub Pages for site CDN, Vercel for serverless API (cold starts acceptable).

## Phase 1: Design Artifacts

### Data Model (data-model.md)
*To be generated: Entities (Chapter, Section, ChatbotQuery, Variant, Translation), relationships, validation rules.*

### API Contracts (contracts/)
*To be generated:*
- **RAG API** (rag-api.openapi.yaml): POST /api/chat, GET /api/health
- **Frontend Contract**: Select-text event → chatbot pre-fill, preference persistence

### Quickstart (quickstart.md)
*To be generated: Developer setup (Docusaurus, FastAPI local dev, Qdrant Docker), chapter authoring, personalization, translation.*

## Complexity Tracking

**No violations detected**. Design adheres to all constitutional principles without justification needed.
