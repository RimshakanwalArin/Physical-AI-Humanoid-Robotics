<!-- Sync Impact Report: Version 0.1.0 (new) | Stage: constitution | Date: 2025-12-06 -->
<!-- Initial constitution ratified for Physical AI & Humanoid Robotics textbook project -->
<!-- Principles: 6 core principles covering content accuracy, build minimalism, free-tier deployment, AI integration, documentation, and testing -->
<!-- Sections: Scope, Architecture, Constraints; Governance: amendment & compliance rules -->

# Physical AI & Humanoid Robotics – Essentials Constitution

A professional AI-native textbook built with Docusaurus, emphasizing accuracy, simplicity, and free-tier accessibility.

## Core Principles

### I. Content Accuracy & Source Integrity

All RAG chatbot answers MUST be strictly sourced from book content. No hallucinations, no external knowledge injection. Every answer includes source references (chapter, section) for verification. Test coverage includes: (1) Off-topic rejection, (2) Partial-match refinement, (3) Multi-source synthesis when appropriate.

### II. Minimalism & Lightweight Architecture

No unnecessary dependencies. Embeddings use free-tier models (e.g., Sentence Transformers). Builds remain <30s. Deployments stay under 100MB static assets. YAGNI principle: only add features when explicitly requested. Optimize for fast page loads and smooth navigation on low-bandwidth connections.

### III. Free-Tier Friendly Deployment

No GPU required. No expensive cloud services. Stack: Docusaurus (static) + Qdrant (self-hosted or free tier) + Neon PostgreSQL (free tier) + FastAPI + GitHub Pages/Vercel. All tools must offer genuine free-tier options with no surprise costs.

### IV. Integrated AI – Content-Centric RAG

Chatbot powered by vector embeddings + semantic search. Select-text Q&A capability. Voice-to-action when applicable (chapters 5–6). RAG system must degrade gracefully (no answer = "Not found in textbook" vs. hallucination).

### V. Comprehensive Documentation & Personalization

Clear code examples and tutorials (Chapters 1–6). Optional: personalized chapter variants based on user background (beginner/intermediate/advanced). Optional: Urdu translation for select chapters. All features remain optional; core book is always complete and standalone.

### VI. Test-First Development & Quality Gates

Spec → Plan → Tasks → Tests → Implementation. Unit tests for RAG retrieval, integration tests for end-to-end Q&A. Chapter content validated for accuracy and completeness before merge. Build pipeline enforces spell-check, link validation, and content audit.

## Technical Architecture & Stack

**Frontend**: Docusaurus 3.x, React, Markdown/MDX
**Backend**: FastAPI (Python 3.11+)
**Database**: Qdrant (embeddings), Neon PostgreSQL (metadata/usage)
**Embeddings**: Sentence Transformers (open-source, free-tier compatible)
**Deployment**: GitHub Pages (static) + Vercel/Render (API), Docker for local dev
**Testing**: pytest (backend), E2E tests for critical chat flows
**CI/CD**: GitHub Actions (build, test, deploy on push to main)

## Constraints & Non-Negotiables

- **Budget**: Zero hard costs (free-tier only, no paid services)
- **Performance**: Page load <2s, API response <1s (p95)
- **Scope**: 6 core chapters, no out-of-scope features until MVP is complete
- **Data**: No user PII stored without explicit consent; usage analytics optional
- **Content Quality**: No external LLM as source of truth; book is authoritative
- **Accessibility**: WCAG 2.1 AA compliance for all text, images, interactive elements
- **Browser Support**: Modern evergreen browsers (Chrome 90+, Firefox 88+, Safari 14+)

## Development Workflow

1. **Specify**: User describes feature/chapter; team clarifies acceptance criteria
2. **Plan**: Architect solution; identify dependencies; estimate effort
3. **Task Breakdown**: Generate testable tasks with P1/P2/P3 priorities
4. **Red-Green-Refactor**: Tests first, implementation second, no unrelated cleanup
5. **Review & Merge**: Content accuracy + code quality gates; all tests pass
6. **Deploy**: Main branch auto-deploys to staging; manual promotion to production

**Mandatory Gates**:
- ✅ All tests pass (unit + integration)
- ✅ Content review: accuracy & relevance confirmed
- ✅ Link check: no broken references
- ✅ Spell & grammar check: passed

## Governance

### Amendment Procedure

Amendments to this constitution require:

1. **Proposal**: Issue or PR describing the change (why, what, impact)
2. **Discussion**: Team reviews; implications for specs, plans, tasks noted
3. **Ratification**: Consensus from core team (no veto unless security/compliance)
4. **Sync**: Update specs, plans, and templates; run `/sp.analyze` to validate consistency
5. **Commit**: Record amendment with reason and version bump in git

### Version Policy

- **MAJOR** (e.g., 1.0.0 → 2.0.0): Principle removed, renamed, or fundamentally redefined
- **MINOR** (e.g., 1.0.0 → 1.1.0): New principle added, section expanded, or guidance materially changed
- **PATCH** (e.g., 1.0.0 → 1.0.1): Clarification, wording, typo, or non-semantic refinement

### Compliance & Auditing

- **Constitution Check** (in all plans): Verify adherence to principles I–VI before Phase 1
- **PHR Review**: Every major task/feature has a Prompt History Record under `history/prompts/`
- **ADR Tracking**: Architectural decisions (framework choice, API design, major refactor) documented in `history/adr/`
- **Quarterly Review**: Constitution adequacy assessed; amendments proposed if needed

### Success Metrics

- ✅ Book deployed and live on GitHub Pages/Vercel
- ✅ RAG chatbot returns >95% accurate answers (sourced strictly from book)
- ✅ Page load time <2s; API response <1s (p95)
- ✅ Zero broken links in final build
- ✅ All 6 chapters complete and reviewed
- ✅ Optional features (personalization, Urdu) functional if implemented

---

**Version**: 0.1.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-06
