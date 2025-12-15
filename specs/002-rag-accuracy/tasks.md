# Tasks: RAG Chatbot Accuracy Improvements

**Input**: Design documents from `/specs/002-rag-accuracy/`
**Branch**: `002-rag-accuracy`
**Status**: Ready for Implementation
**Prerequisites**: spec.md ✅, plan.md ✅, research.md ✅

---

## Overview

This task list breaks down the RAG accuracy improvement feature into independently testable, parallelizable work organized by **3 user stories** (3 P1 stories, 1 P2 story). Each story can be implemented, tested, and deployed independently.

**Total Tasks**: 52 (Phase 1-2: 8 foundation tasks, Phase 3-5: 44 story-specific tasks)

**Suggested MVP Scope**: User Story 1 (Accurate Answers) + User Story 2 (Source Attribution) = 26 tasks, ~2 weeks.

---

## Format: `[ID] [P?] [Story] Description`

- **[ID]**: Task identifier (T001, T002, ...)
- **[P]**: Parallelizable (can run alongside other [P] tasks with no dependencies)
- **[Story]**: User story label (US1, US2, US3) - only in story phases
- **Description**: Clear action with exact file paths

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and configuration

**Estimated Duration**: 2-3 hours (includes Python environment, dependency management, test structure)

- [ ] T001 Initialize Python testing infrastructure with pytest in `backend/tests/` directory
- [ ] T002 [P] Create embedding model configuration system in `backend/src/config.py` to support model switching
- [ ] T003 [P] Setup logging and metrics infrastructure in `backend/src/logger.py` for quality monitoring
- [ ] T004 Create Qdrant connection and utility functions in `backend/src/qdrant_client.py` for collection operations
- [ ] T005 [P] Create test fixtures and sample data in `backend/tests/fixtures/rag_test_data.json` (20+ test queries)
- [ ] T006 Create benchmark suite structure in `backend/tests/benchmark/` directory for performance comparison

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story implementation

**⚠️ CRITICAL**: No user story work can begin until Phase 2 is complete

**Estimated Duration**: 3-4 days (model loading, embeddings, retrieval pipeline updates)

- [ ] T007 Download and validate BGE-small-en-v1.5 model, verify size <1GB and dimensions (384) in `backend/src/models/bge_model.bin`
- [ ] T008 [P] Implement embedding model loader and switcher in `backend/src/rag/embeddings.py` (support both all-MiniLM-L6-v2 and bge-small-en-v1.5)
- [ ] T009 [P] Implement query encoding function that produces normalized 384-dim vectors in `backend/src/rag/embeddings.py`
- [ ] T010 Implement chunk preprocessing and embedding batching in `backend/src/rag/embeddings.py` for efficient re-embedding
- [ ] T011 [P] Implement retrieval score normalization and confidence calculation in `backend/src/rag/retrieval.py`
- [ ] T012 [P] Create Qdrant collection alias utilities in `backend/src/qdrant_client.py` (create, switch, rollback aliases)
- [ ] T013 Create zero-downtime migration script skeleton in `backend/scripts/migrate_embeddings.py` with argument parsing
- [ ] T014 [P] Implement quality metrics logging infrastructure in `backend/src/rag/quality.py` for retrieval success rate, relevance scores

**Checkpoint**: Foundation complete - all user story work can now proceed in parallel

---

## Phase 3: User Story 1 - Student Gets Accurate, Relevant Answers (Priority: P1) 🎯 MVP

**Goal**: Students receive highly accurate, relevant answers from the RAG chatbot with <5% hallucination rate and proper citations

**Independent Test**: Run 20+ automated test queries (10 in-scope, 10 out-of-scope), verify >95% pass rate, <5% hallucination rate, semantic similarity >0.85

**Estimated Duration**: 4-5 days

### Tests for User Story 1 (Test-First Approach)

> **NOTE: Write and execute these tests FIRST - they should FAIL before implementation**

- [ ] T015 [P] [US1] Create unit tests for accurate answer retrieval in `backend/tests/unit/test_accurate_answers.py` covering 10 in-scope queries
- [ ] T016 [P] [US1] Create unit tests for hallucination detection in `backend/tests/unit/test_hallucination_detection.py` covering 10 out-of-scope queries
- [ ] T017 [P] [US1] Create semantic similarity assertion helper in `backend/tests/unit/test_semantic_similarity.py` (assert cosine similarity >0.85)
- [ ] T018 [P] [US1] Create integration test for full RAG pipeline (query → embedding → retrieval → response) in `backend/tests/integration/test_rag_pipeline_accuracy.py`
- [ ] T019 [US1] Create benchmark test comparing all-MiniLM-L6-v2 vs BGE-small-en-v1.5 on test queries in `backend/tests/benchmark/test_model_comparison.py`

### Implementation for User Story 1

- [ ] T020 [P] [US1] Implement source-only answer filter in `backend/src/rag/answer_generation.py` (reject external knowledge)
- [ ] T021 [P] [US1] Implement relevance threshold checker in `backend/src/rag/retrieval.py` (configurable MIN_RELEVANCE_THRESHOLD)
- [ ] T022 [P] [US1] Implement "not in textbook" response handler in `backend/src/rag/answer_generation.py` for out-of-scope queries
- [ ] T023 [US1] Implement hallucination detection logic in `backend/src/rag/quality.py` using keyword matching and semantic validation
- [ ] T024 [US1] Enhance answer formatting to include confidence scores in `backend/src/rag/answer_generation.py`
- [ ] T025 [US1] Create confidence score calculation from retrieved chunk relevance in `backend/src/rag/retrieval.py`
- [ ] T026 [US1] Add query latency tracking and p95 measurement in `backend/src/rag/answer_generation.py`
- [ ] T027 [US1] Implement response validation to ensure all answers meet accuracy criteria before returning in `backend/src/rag/answer_generation.py`
- [ ] T028 [US1] Add comprehensive logging for accuracy metrics in `backend/src/rag/quality.py` (log for each query: accuracy, hallucination flag, confidence)
- [ ] T029 [US1] Update `/api/rag/query` endpoint to return confidence and model info in `backend/src/api/routes.py`

**Checkpoint**: User Story 1 complete - students receive accurate answers with hallucination prevention ✅

---

## Phase 4: User Story 2 - Clear Source Attribution for Every Answer (Priority: P1)

**Goal**: Every chatbot answer includes clear, verifiable source citations (chapter/section) that link back to the textbook

**Independent Test**: Verify 100% of responses include structured citations, test citation links resolve to correct sections, confirm citations are unambiguous

**Estimated Duration**: 3-4 days

### Tests for User Story 2

- [ ] T030 [P] [US2] Create unit tests for citation extraction in `backend/tests/unit/test_citation_extraction.py` (10 multi-section answers)
- [ ] T031 [P] [US2] Create unit tests for citation formatting in `backend/tests/unit/test_citation_formatting.py` (verify format "Chapter X: Section Y")
- [ ] T032 [P] [US2] Create unit tests for citation link generation in `backend/tests/unit/test_citation_links.py` (verify anchor links work)
- [ ] T033 [US2] Create integration test for source traceability in `backend/tests/integration/test_source_attribution.py` (trace answer → chunk → chapter)
- [ ] T034 [US2] Create acceptance test for UI citation rendering in `backend/tests/integration/test_citation_ui_display.py`

### Implementation for User Story 2

- [ ] T035 [P] [US2] Create Citation data model in `backend/src/models/citation.py` with fields: chunk_id, chapter_name, section_name, section_number, page_number, link_anchor
- [ ] T036 [P] [US2] Implement citation extraction from retrieved chunks in `backend/src/rag/retrieval.py` (extract chapter, section from chunk metadata)
- [ ] T037 [P] [US2] Implement citation formatter in `backend/src/rag/answer_generation.py` to format citations as "Chapter X: Section Y, Page Z"
- [ ] T038 [US2] Implement citation link generator in `backend/src/rag/answer_generation.py` (create anchor links to textbook sections)
- [ ] T039 [US2] Implement citation deduplication to avoid duplicate sources in `backend/src/rag/answer_generation.py`
- [ ] T040 [US2] Enhance IndexedChunk model in `backend/src/models/chunk.py` to include chapter_id, section_name, section_number, page_number
- [ ] T041 [US2] Implement citation metadata persistence in `backend/src/models/response.py` (store citations with each RagResponse)
- [ ] T042 [US2] Update `/api/rag/query` endpoint to return structured citations in `backend/src/api/routes.py`
- [ ] T043 [US2] Add citation validation in response generation to ensure 100% coverage in `backend/src/rag/answer_generation.py`
- [ ] T044 [US2] Implement citation logging for audit trail in `backend/src/rag/quality.py`

**Checkpoint**: User Story 2 complete - all answers include verifiable source citations ✅

---

## Phase 5: User Story 3 - Reduced False Negatives (Improved Retrieval) (Priority: P2)

**Goal**: Chatbot successfully answers questions using synonymous phrasing; retrieval recall improves >15% over baseline with semantic similarity >0.80 average

**Independent Test**: Run 30-query test set with known good answers; measure retrieval recall >90%; verify semantic similarity avg >0.80; compare vs all-MiniLM-L6-v2 baseline

**Estimated Duration**: 3-4 days

### Tests for User Story 3

- [ ] T045 [P] [US3] Create unit tests for semantic similarity in `backend/tests/unit/test_semantic_similarity.py` (30 query pairs with expected matches)
- [ ] T046 [P] [US3] Create integration test for synonym handling in `backend/tests/integration/test_synonym_retrieval.py` (robot walking → bipedal locomotion)
- [ ] T047 [P] [US3] Create retrieval recall benchmark in `backend/tests/benchmark/test_retrieval_recall.py` (>90% of in-scope queries return relevant chunks)
- [ ] T048 [US3] Create model comparison test comparing BGE vs all-MiniLM on retrieval quality in `backend/tests/benchmark/test_bge_vs_minilm_recall.py`
- [ ] T049 [US3] Create edge case tests for low-confidence scenarios in `backend/tests/unit/test_low_confidence_handling.py`

### Implementation for User Story 3

- [ ] T050 [P] [US3] Replace embedding model in `backend/src/rag/embeddings.py` from all-MiniLM-L6-v2 to BGE-small-en-v1.5 (update model name, load new model)
- [ ] T051 [P] [US3] Re-index all 50k textbook chunks using BGE model via `backend/scripts/migrate_embeddings.py` (compute new embeddings, upload to Qdrant)
- [ ] T052 [US3] Execute zero-downtime Qdrant migration using collection aliases in `backend/scripts/migrate_embeddings.py` (create v2, switch alias atomically)
- [ ] T053 [US3] Implement semantic similarity scoring in `backend/src/rag/retrieval.py` (calculate cosine similarity between query and chunk embeddings)
- [ ] T054 [US3] Update MIN_RELEVANCE_THRESHOLD in `backend/src/config.py` (tune threshold from 0.65 to 0.70 for better recall)
- [ ] T055 [US3] Implement retrieval recall metric logging in `backend/src/rag/quality.py` (track % of queries returning relevant chunks)
- [ ] T056 [US3] Create retrieval debugging endpoint in `backend/src/api/routes.py` (POST /api/rag/debug/retrieval for testing queries)
- [ ] T057 [US3] Document embedding model differences in `backend/src/rag/embeddings.py` with comments on performance/accuracy tradeoffs
- [ ] T058 [US3] Validate backward compatibility: run old all-MiniLM queries against new BGE index to ensure no regression in `backend/tests/integration/test_backward_compatibility.py`

**Checkpoint**: User Story 3 complete - retrieval accuracy improved with BGE model ✅

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Integration, documentation, performance optimization, final validation

**Estimated Duration**: 3-4 days

### Documentation & Setup

- [ ] T059 [P] Create reindexing guide in `backend/docs/REINDEXING.md` (step-by-step production migration guide)
- [ ] T060 [P] Create model selection documentation in `backend/docs/EMBEDDING_MODELS.md` (rationale for BGE choice, performance comparison)
- [ ] T061 [P] Create API documentation update in `backend/docs/API.md` (document /query, /metrics, /status endpoints)
- [ ] T062 [P] Update requirements.txt with sentence-transformers 3.0+ and qdrant-client 1.11+ pinned versions

### Performance Optimization

- [ ] T063 [P] Benchmark end-to-end latency: query → answer in `backend/tests/benchmark/test_e2e_latency.py` (verify <1s p95)
- [ ] T064 [P] Benchmark batch re-embedding throughput in `backend/tests/benchmark/test_reindex_performance.py` (measure speed)
- [ ] T065 [P] Implement embedding caching for repeated queries in `backend/src/rag/embeddings.py` (LRU cache for common questions)
- [ ] T066 [P] Optimize Qdrant query parameters (batch size, parallelism) in `backend/scripts/migrate_embeddings.py`

### Monitoring & Rollback

- [ ] T067 Create monitoring dashboard setup in `backend/docs/MONITORING.md` (track hallucination rate, retrieval recall, latency)
- [ ] T068 [P] Create rollback procedure documentation in `backend/docs/ROLLBACK.md` (how to revert to all-MiniLM if needed)
- [ ] T069 [P] Create snapshot backup procedure in `backend/scripts/backup_qdrant.sh` (create pre-migration snapshot)
- [ ] T070 [P] Test rollback via alias switch in `backend/tests/integration/test_rollback_procedure.py`

### Final Validation

- [ ] T071 Run full test suite: `pytest backend/tests/unit backend/tests/integration backend/tests/benchmark` (all tests PASS)
- [ ] T072 Verify hallucination rate <5% on full test corpus (20+ out-of-scope queries)
- [ ] T073 Verify retrieval recall >90% on 30-query benchmark set
- [ ] T074 Verify latency <1s p95 on production hardware simulation
- [ ] T075 Manual smoke test: ask 5 representative questions, verify accurate answers with citations
- [ ] T076 Update CHANGELOG.md with migration notes, version bump to indicate model upgrade

**Checkpoint**: Feature complete, tested, documented, production-ready ✅

---

## Dependency Graph & Parallel Execution Strategy

### Critical Path (Blocking Tasks)
```
Phase 1 Setup (T001-T006)
    ↓
Phase 2 Foundation (T007-T014)
    ↓
Phase 3/4/5 User Stories (can run in parallel after Phase 2)
    ├─→ US1 Tasks (T015-T029) - 3-4 days
    ├─→ US2 Tasks (T030-T044) - 3-4 days (can start after T014)
    └─→ US3 Tasks (T045-T058) - 3-4 days (depends on T007 model download)
    ↓
Phase 6 Polish (T059-T076) - must run after all user stories complete
```

### Parallel Execution Examples

**Day 1-2: Phase 1 & 2 (Sequential foundation)**
- Team lead: T001-T006 (setup)
- In parallel: T007-T014 (foundation)

**Day 3-5: User Stories (Parallel 3-way)**
- Developer A: US1 (T015-T029) - Accuracy & Hallucination
- Developer B: US2 (T030-T044) - Citations & Attribution
- Developer C: US3 (T045-T058) - Retrieval Recall & Reindexing

**Day 6-7: Polish & Integration (Sequential)**
- Team: T059-T076 (documentation, monitoring, validation)

### Task Dependencies (Within Phases)

**Phase 3 (US1)**:
- T015-T019 (tests) can run in parallel
- T020-T029 (implementation) run after T015 (tests must exist first)
- T028 depends on T024-T026

**Phase 4 (US2)**:
- T030-T034 (tests) can run in parallel
- T035-T044 (implementation) run after T030 (tests must exist first)
- T042 depends on T035-T041
- T043 depends on T040

**Phase 5 (US3)**:
- T045-T049 (tests) can run in parallel
- T050-T058 (implementation) run after T045 (tests must exist first)
- T052 depends on T007, T050, T051
- T058 depends on T050

**Phase 6 (Polish)**:
- T059-T070 (docs, setup) can run in parallel
- T071-T076 (validation) must run after all user story implementation complete

---

## MVP Scope & Incremental Delivery

### MVP (Week 1): User Stories 1 & 2
**What**: Students get accurate answers with proper source citations
**Tasks**: T001-T044 (Phase 1, 2, 3, 4)
**Duration**: ~8-10 days with 2 developers
**Risk**: Low (foundation + core accuracy features)
**Go-Live**: Can deploy after US1 & US2 complete

### Phase 2 (Week 2): User Story 3
**What**: Improved retrieval recall via BGE model migration
**Tasks**: T045-T058 (Phase 5)
**Duration**: 3-4 days
**Risk**: Medium (Qdrant migration, re-indexing timing)
**Go-Live**: Deploy after full test suite passes

### Phase 3 (Week 2): Polish & Monitoring
**What**: Production readiness, documentation, monitoring
**Tasks**: T059-T076 (Phase 6)
**Duration**: 3-4 days
**Risk**: Low (non-blocking, improve post-MVP)
**Go-Live**: After validation complete

---

## Success Criteria & Acceptance Gates

### Per User Story Acceptance

**User Story 1 (Accurate Answers)**:
- ✅ T015-T019 tests PASS (>95% test suite pass rate)
- ✅ Hallucination rate <5% verified on test corpus
- ✅ Semantic similarity >0.85 average on in-scope queries
- ✅ All T020-T029 implementation tasks complete

**User Story 2 (Citations)**:
- ✅ T030-T034 tests PASS
- ✅ 100% of responses include structured citations
- ✅ Citation links resolve to correct textbook sections
- ✅ All T035-T044 implementation tasks complete

**User Story 3 (Retrieval Recall)**:
- ✅ T045-T049 tests PASS
- ✅ Retrieval recall >90% on 30-query benchmark
- ✅ Semantic similarity >0.80 average with BGE model
- ✅ All T050-T058 implementation tasks complete

### Final Acceptance

- ✅ All 76 tasks complete
- ✅ Full test suite passes: `pytest backend/tests/` (no failures)
- ✅ Benchmark suite validates: latency <1s p95, hallucination <5%, recall >90%
- ✅ Production readiness checks complete (T071-T076)
- ✅ Rollback procedure tested and documented
- ✅ Zero-downtime migration executed successfully on staging
- ✅ Code review approved by tech lead
- ✅ Deployed to production with monitoring active

---

## Notes for Implementers

1. **Test-First Approach**: Write tests (T015-T019, T030-T034, T045-T049) FIRST, verify they FAIL before implementation
2. **Backward Compatibility**: US3 task T058 validates old all-MiniLM queries still work with new BGE index
3. **Parallel Development**: After Phase 2 complete, 3 developers can work on US1, US2, US3 independently
4. **Zero-Downtime Migration**: Task T052 uses Qdrant collection aliases for atomic cutover (no downtime)
5. **Rollback Always Available**: Snapshots created before migration (T069), alias switching enables instant rollback
6. **Monitoring Critical**: Quality metrics must be logged continuously (T028, T044, T056) for production confidence

---

**Version**: 1.0 | **Status**: Ready for Implementation | **Next**: Begin Phase 1 with `/sp.red` for TDD approach
