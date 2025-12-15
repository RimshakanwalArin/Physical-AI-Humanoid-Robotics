# Feature Specification: RAG Chatbot Accuracy Improvements

**Feature Branch**: `002-rag-accuracy`
**Created**: 2025-12-15
**Status**: Draft
**Input**: User request to improve RAG chatbot accuracy by switching to a more sophisticated embedding model, reducing hallucinations, and improving source attribution. Success measured via automated tests.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Student Gets Accurate, Relevant Answers (Priority: P1)

A student asks the RAG chatbot a question about a topic covered in the textbook. The chatbot returns a highly relevant, accurate answer sourced strictly from the book chapters. When the student asks a question outside the scope of the textbook, the chatbot gracefully responds "This topic is not covered in the textbook" instead of hallucinating external knowledge.

**Why this priority**: Core product quality; accuracy directly impacts student trust and learning outcomes. Hallucinations destroy credibility and violate Constitution Principle I (Content Accuracy & Source Integrity).

**Independent Test**: Can be fully tested by:
   - Running automated test suite with 20+ known questions (in-scope and out-of-scope)
   - Measuring hallucination rate (<5% of responses contain external knowledge)
   - Verifying relevant answers match query intent (semantic similarity >0.85)
   - Confirming all answers include chapter/section citations

**Acceptance Scenarios**:

1. **Given** a student asks "What is embodied intelligence?", **When** the chatbot processes this, **Then** it returns an answer from Chapter 1 with proper citation within 1 second.
2. **Given** a student asks "What is machine learning?", **When** the chatbot processes this, **Then** it responds "This topic is not covered in the textbook" (no hallucination).
3. **Given** a student asks "How does bipedal locomotion work?", **When** the chatbot processes this, **Then** it retrieves the correct section from Chapter 2 (not unrelated robotics content).

---

### User Story 2 - Clear Source Attribution for Every Answer (Priority: P1)

Every chatbot answer includes clear, verifiable source attribution. The student can see exactly which chapter and section the answer came from, and click through to read the original context if desired.

**Why this priority**: Transparency and traceability are core to the RAG system design. Students must be able to verify sources and trust the system.

**Independent Test**: Can be fully tested by:
   - Verifying all responses include structured citation (chapter name, section number, or heading)
   - Testing that citations link to correct document sections
   - Confirming citations are unambiguous and prevent misattribution

**Acceptance Scenarios**:

1. **Given** the chatbot returns an answer, **When** the student reads the response, **Then** a citation footer appears with format "Chapter X: Section Title" or "Chapter X, Section Y, Page Z".
2. **Given** the student sees a citation, **When** they click it, **Then** the textbook opens to that exact section.
3. **Given** an answer spans multiple source sections, **When** the student reads it, **Then** multiple citations are listed with clear section labels.

---

### User Story 3 - Reduced False Negatives (Improved Retrieval) (Priority: P2)

The chatbot successfully answers legitimate questions that it previously failed to answer due to poor semantic matching. For example, synonymous phrasing ("robot walking" vs. "bipedal locomotion") now retrieves relevant content.

**Why this priority**: Improves user experience and confidence. Students should get help when the answer exists in the book, even if they use different terminology.

**Independent Test**: Can be fully tested by:
   - Creating a test set of 30 questions with known good answers in the textbook
   - Running same questions against old and new embedding models
   - Measuring retrieval recall (% of queries returning relevant content)
   - Target: >90% of in-scope queries retrieve at least one relevant chunk

**Acceptance Scenarios**:

1. **Given** a student asks "How do robots walk?", **When** the chatbot searches the vector database, **Then** it finds Chapter 2 sections on bipedal locomotion (even though the student didn't use exact terminology).
2. **Given** a student asks "Explain ROS components", **When** the chatbot processes this, **Then** it retrieves relevant ROS 2 content from Chapter 3 (not unrelated robotics content).

---

### Edge Cases

- What happens when embedding model returns very low confidence scores for all chunks?
- How does system handle queries that partially match multiple chapters (ambiguous scope)?
- What occurs if embedding model changes and historical cached embeddings become stale?
- How should the system behave if a student asks a follow-up question requiring context from previous exchanges?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support switching embedding models without reindexing all documents (or with automatic reindexing if needed).
- **FR-002**: RAG pipeline MUST enforce that no answer is generated without first retrieving relevant chunks from the vector database.
- **FR-003**: Every generated answer MUST include explicit source citations (chapter/section identifiers).
- **FR-004**: System MUST filter and reject answers that contain knowledge not found in the indexed textbook chapters.
- **FR-005**: System MUST return "This topic is not covered in the textbook" when no chunks exceed a minimum relevance threshold (configurable).
- **FR-006**: Embedding model MUST support free-tier deployment (no GPU, <1s inference on CPU for a single query).
- **FR-007**: System MUST maintain backward compatibility: existing indexed content must be queryable after model switch (with reindexing if necessary).
- **FR-008**: System MUST log embedding quality metrics (retrieval success rate, relevance scores) for monitoring.

### Key Entities *(include if feature involves data)*

- **Embedding Model**: A pre-trained model that converts text to dense vectors. Attributes: model name, vector dimension, license, inference cost/speed, domain suitability.
- **Indexed Chunk**: A segment of textbook content (paragraph or section). Attributes: chapter ID, section name, content text, embedding vector, metadata (page, heading).
- **Query**: A student question. Attributes: text, timestamp, student ID (optional), model version used.
- **RAG Response**: A generated answer. Attributes: query ID, retrieved chunks, generated text, citations, confidence score, timestamp.

### Non-Functional Requirements

- **NFR-001**: Embedding inference latency MUST be <100ms for a single query vector on CPU.
- **NFR-002**: Reindexing all 6 chapters MUST complete in <5 minutes on standard hardware.
- **NFR-003**: Model size MUST be <1GB for easy local development and deployment.
- **NFR-004**: System MUST remain free-tier compatible (no paid APIs, no GPU required).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Automated test suite MUST achieve >95% pass rate for in-scope questions (correct source retrieval and citation).
- **SC-002**: Hallucination rate MUST be <5% (verified by test cases asking out-of-scope questions).
- **SC-003**: Retrieval recall MUST improve by >15% compared to baseline (measured on controlled test set of 30+ questions).
- **SC-004**: Semantic similarity of retrieved chunks to query MUST average >0.80 (vector cosine similarity).
- **SC-005**: API response latency (query to answer) MUST remain <1 second p95.
- **SC-006**: New embedding model MUST be free-tier compatible and deployable without GPU.

### Quality Gates

- ✅ All automated accuracy tests pass
- ✅ Hallucination test suite shows <5% external knowledge injection
- ✅ Source attribution verification passes for 100% of test cases
- ✅ No performance regression (p95 latency <1s maintained)
- ✅ Backward compatibility: all existing indexed chapters remain queryable
- ✅ Documentation updated with new model details, reindexing instructions

## Constraints & Non-Goals

### In Scope
- Switching embedding model to improve semantic matching
- Enhancing retrieval accuracy and reducing false negatives
- Improving source attribution clarity
- Adding automated tests for accuracy validation

### Out of Scope (Post-MVP)
- Fine-tuning embedding model on domain-specific data (future iteration if needed)
- Re-ranking retrieved chunks with cross-encoders (nice-to-have)
- Multi-turn conversation memory and context tracking (separate feature)
- Hybrid search (semantic + keyword-based retrieval)

### Constraints
- **Budget**: Must use only free-tier models and services
- **Deployment**: No GPU required; must run on CPU infrastructure
- **Data**: Cannot store user queries for fine-tuning without explicit consent
- **Scope**: Only improve embedding model and retrieval; generation LLM unchanged for now

## Architecture & Integration Points

### Current State
- **Embedding Model**: Sentence Transformers (`sentence-transformers/all-MiniLM-L6-v2`)
- **Vector Database**: Qdrant
- **Retrieval**: Top-K semantic search (default K=5)
- **Answer Generation**: FastAPI endpoint that formats retrieved chunks into markdown response
- **Evaluation**: Manual testing; no automated accuracy tests

### Proposed Changes
1. **Evaluate & Select New Embedding Model**: Test candidates (e.g., `all-MiniLM-L12-v2`, `all-mpnet-base-v2`, `instructor-base`) against test queries.
2. **Implement Model Switching Infrastructure**: Allow config-driven embedding model selection.
3. **Add Automated Test Suite**: 20+ test cases covering in-scope, out-of-scope, edge cases.
4. **Reindex Chapters**: Convert all textbook chapters with new embedding model.
5. **Enhance Source Attribution**: Ensure every response includes chapter/section metadata.
6. **Monitor & Log Metrics**: Track retrieval success, relevance scores, and hallucination patterns.

## Dependencies & Risks

### External Dependencies
- Embedding model availability and license (must be free and open-source)
- Qdrant API stability (no breaking changes assumed)
- FastAPI response generation logic (existing code, minimal changes)

### Risks
1. **Reindexing Time**: Large model may take longer to embed all chapters; risk of bottleneck during deployment.
   - **Mitigation**: Pre-compute embeddings in advance; run reindex in background; provide clear deployment instructions.

2. **Model Size & Inference Cost**: Larger models may exceed CPU performance budget.
   - **Mitigation**: Benchmark candidate models on target hardware; prioritize models <500MB with <200ms inference.

3. **Backward Compatibility**: Changing embedding model invalidates old indices; existing searches will fail until reindexing.
   - **Mitigation**: Plan reindex as part of deployment; version embeddings; provide rollback mechanism.

4. **Overfitting to Test Queries**: Test suite may not generalize to real student questions.
   - **Mitigation**: Use diverse, representative test set; randomize test order; monitor real-world metrics post-deployment.

---

## Follow-up & Next Steps

1. **Plan Phase**: Architecture design, model selection criteria, reindexing strategy
2. **Tasks**: Enumerate specific implementation, testing, and deployment tasks
3. **Red-Green-Refactor**: Implement tests first, then embedding model integration
4. **Review & Deploy**: Accuracy tests pass, performance metrics validated, reindex successful
5. **Post-Launch Monitoring**: Track hallucination rate, retrieval success, user feedback over time

---

**Version**: 1.0 | **Status**: Ready for Planning | **Next Step**: Run `/sp.plan 002-rag-accuracy`
