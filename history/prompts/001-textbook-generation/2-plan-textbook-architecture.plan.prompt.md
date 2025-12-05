---
id: 2
title: Plan Textbook-Generation Architecture
stage: plan
date: 2025-12-06
surface: agent
model: claude-haiku-4-5-20251001
feature: 001-textbook-generation
branch: 001-textbook-generation
user: user
command: /sp.plan
labels: ["architecture","rag","docusaurus","fastapi","data-model","api-contract"]
links:
  spec: specs/001-textbook-generation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-textbook-generation/plan.md
  - specs/001-textbook-generation/data-model.md
  - specs/001-textbook-generation/contracts/rag-api.openapi.yaml
  - specs/001-textbook-generation/contracts/frontend-api-contract.md
  - specs/001-textbook-generation/quickstart.md
tests:
  - Constitution Check (all 6 principles PASS)
  - Data Model validation (entity relationships, free-tier design)
  - API Contract validation (OpenAPI 3.0 spec compliance)
  - Project structure validation (directory layout, separation of concerns)
---

## Prompt

```
[Execute /sp.plan for feature 001-textbook-generation]

Task: Create comprehensive implementation plan for AI-native textbook with RAG chatbot.
- Specify technical context (languages, frameworks, databases)
- Perform constitution check (verify adherence to project principles)
- Design data model (Chapter, Section, ChatbotQuery, Variant, Translation entities)
- Generate API contracts (RAG API OpenAPI spec + frontend-backend contract)
- Create quickstart guide (setup, authoring, deployment, testing)
```

## Response snapshot

Comprehensive implementation plan created for 001-textbook-generation with Phase 0 (research) and Phase 1 (design) complete.

**Technical Context**:
- Frontend: Docusaurus 3.x + React (Node.js 18+)
- Backend: FastAPI (Python 3.11+), deployed on Vercel (free tier)
- Embeddings: Sentence Transformers (all-MiniLM-L6-v2, <100MB)
- Vector DB: Qdrant (self-hosted Docker or free-tier cloud)
- Metadata: Neon PostgreSQL (free tier, optional)

**Constitution Check**: ✅ **PASS** — All 6 principles verified:
1. Content Accuracy: RAG enforces sourced-only answers + citations; graceful degradation
2. Minimalism: <30s builds, <100MB deployments, free-tier stack only
3. Free-Tier: GitHub Pages + Qdrant + Neon + FastAPI/Vercel (zero hard costs)
4. AI Integration: Vector embeddings + semantic search + no hallucinations
5. Documentation: 6 chapters + optional personalization + optional Urdu translation
6. Test-First: Build pipeline includes link validation, spell-check, RAG accuracy tests

**Phase 0 Research** (7 key decisions):
1. RAG answer generation: retrieval + prompt synthesis (no LLM calls, avoids hallucinations & costs)
2. Embedding model: Sentence Transformers (open-source, <100MB memory, good QA performance)
3. Vector store: Qdrant (lightweight, metadata filtering support, free-tier option)
4. Chunking strategy: 300-500 token chunks per section (balances context + relevance)
5. Personalization: Separate markdown files per level (Beginner/Intermediate/Advanced)
6. Translation: Docusaurus i18n plugin (code blocks remain English)
7. Deployment: GitHub Pages (static) + Vercel (backend API, free tier)

**Data Model** (Phase 1):
- Entities: Chapter (6 total), Section (heading-based), ChatbotQuery (analytics), Variant (personalization), Translation (language), UserPreference (localStorage)
- Key design: No user authentication, client-side preferences only, markdown files as primary storage, free-tier optimized
- Relationships: Chapter 1:N→ Sections/Variants/Translations, ChatbotQuery N:M→ Sections

**API Contracts** (Phase 1):
- RAG API (OpenAPI 3.0): POST /api/chat (query + session_id → answer + citations), GET /api/health
- Frontend ↔ Backend: Select-text-to-ask flow, localStorage preference persistence, 8-item testing contract
- CORS: No authentication; public textbook
- Performance: <1s API response (p95), <2s page load, <500ms select-text latency

**Project Structure** (Phase 1):
- Frontend: docs/ (6 chapters), src/ (chatbot/i18n/personalization components), scripts/ (validation)
- Backend: src/ (API routes, RAG pipeline, DB), tests/ (unit/integration/contract)
- Indexing: extract chapters → embed → load to Qdrant pipeline
- Deployment: GitHub Actions CI/CD

**Quickstart Guide** (Phase 1):
- Frontend: Docusaurus init, chapter authoring markdown format, chatbot component integration
- Backend: FastAPI setup, RAG pipeline outline (embeddings.py, retrieval.py, answer_gen.py)
- Indexing: Extract chapters script, Sentence Transformers embedding, Qdrant batch load
- Deployment: GitHub Pages (npm run deploy), Vercel (backend), Qdrant Cloud (free tier)
- Personalization: Create chapter variants (optional, post-MVP if needed)
- Translation: Urdu i18n setup (optional, post-MVP if needed)
- CI/CD: GitHub Actions workflow for build, test, deploy
- Testing: 9-item pre-launch checklist

## Outcome

- ✅ Impact: Architecture designed; all constitutional principles verified; Phase 0-1 complete; ready for task breakdown
- 🧪 Tests: Constitution Check (PASS), Entity model validation (PASS), API contract validation (PASS), Structure validation (PASS)
- 📁 Files: plan.md, data-model.md, rag-api.openapi.yaml, frontend-api-contract.md, quickstart.md (5 artifacts)
- 🔁 Next prompts: `/sp.tasks` to break down work into testable tasks; `/sp.analyze` to validate consistency
- 🧠 Reflection: Design balances free-tier constraints with robust architecture. RAG approach (no LLM calls) prevents hallucinations and costs. Separation of frontend (static Docusaurus) and backend (FastAPI microservice) enables independent scaling. All optional features (personalization, Urdu) are additive and don't block MVP. Ready to implement.

## Evaluation notes (flywheel)

- Failure modes observed: None; all technical decisions justified and traceable
- Graders run and results (PASS/FAIL): Constitution adherence (PASS), free-tier compatibility (PASS), API contract completeness (PASS), project structure clarity (PASS)
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): `/sp.tasks` to generate task list and task IDs; begin implementation with P1 tasks (Docusaurus + FastAPI setup + RAG indexing)

