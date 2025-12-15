# RAG Chatbot Backend - Physical AI & Humanoid Robotics Textbook

FastAPI backend for a Retrieval-Augmented Generation (RAG) chatbot powered by BGE embeddings and Qdrant vector search.

## Quick Start

### Local Development

1. **Create virtual environment**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Qdrant** (Docker):
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run tests**:
   ```bash
   pytest tests/ -v
   ```

6. **Start server**:
   ```bash
   python -m uvicorn src.main:app --reload
   ```

   API will be available at: `http://localhost:8000`

## API Endpoints

### Query RAG Chatbot
```http
POST /api/rag/query
Content-Type: application/x-www-form-urlencoded

query_text=What is embodied intelligence?&student_id=optional-uuid
```

**Response**:
```json
{
  "id": "response-uuid",
  "query_id": "query-uuid",
  "query_text": "What is embodied intelligence?",
  "response_text": "Embodied intelligence refers to...\n\n**Sources:**\n- Chapter 1: Introduction to Physical AI",
  "sources": [
    {
      "chunk_id": "chunk-1",
      "chapter_name": "Chapter 1: Introduction to Physical AI",
      "section_name": "Embodied Intelligence",
      "section_number": "1.2",
      "page_number": 5,
      "link_anchor": "ch1-embodied-intelligence"
    }
  ],
  "confidence_score": 0.87,
  "hallucination_detected": false,
  "latency_ms": 340,
  "embedding_model": "bge-small-en-v1.5"
}
```

### Check System Status
```http
GET /api/rag/status
```

Returns system health, model info, and Qdrant connection status.

### Log Quality Metrics
```http
POST /api/rag/metrics

{
  "response_id": "response-uuid",
  "actual_source_correct": true,
  "relevance_feedback": 4.5,
  "hallucination_detected": false
}
```

## Architecture

### Core Modules

- **`src/config.py`** (T002): Configuration management with model switching support
- **`src/logger.py`** (T003, T014): Quality metrics logging and monitoring
- **`src/models.py`** (T035, T040, T041): Data models (Citation, IndexedChunk, RagResponse)
- **`src/qdrant_client.py`** (T004, T012): Qdrant wrapper with collection aliases
- **`src/rag/embeddings.py`** (T007-T010): Embedding model loader and encoder
- **`src/rag/retrieval.py`** (T011, T021, T024-T025): Vector search and ranking
- **`src/rag/quality.py`** (T014, T023): Hallucination detection and quality monitoring
- **`src/rag/answer_generation.py`** (T020, T022, T024, T038-T043): Response formatting with citations
- **`src/main.py`** (T029): FastAPI application and endpoints

### Data Flow

```
User Query (T029)
  ↓
[Encode with BGE embedding] (T009)
  ↓
[Retrieve similar chunks from Qdrant] (T011, T021)
  ↓
[Validate source-only constraint] (T020)
  ↓
[Detect hallucinations] (T023)
  ↓
[Format answer with citations] (T024, T038-T043)
  ↓
[Log quality metrics] (T028)
  ↓
Return RagResponse
```

## Configuration

All settings can be configured via environment variables (`.env`):

```env
# Embedding Model (T002)
EMBEDDING_MODEL=bge-small-en-v1.5  # Options: all-MiniLM-L6-v2, bge-small-en-v1.5, e5-small-v2
EMBEDDING_DIMENSION=384

# Retrieval
TOP_K_RETRIEVAL=5
MIN_RELEVANCE_THRESHOLD=0.70

# Qdrant
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION_NAME=documents

# Quality Monitoring (T014)
LOG_QUALITY_METRICS=true
HALLUCINATION_DETECTION_ENABLED=true
```

## Testing

### Unit Tests (T015-T017)
```bash
pytest tests/unit/ -v
```

Tests for:
- Accurate answer retrieval
- Hallucination detection
- Semantic similarity validation

### Integration Tests (T018)
```bash
pytest tests/integration/ -v
```

Tests for:
- End-to-end RAG pipeline
- Response formatting
- Citation accuracy

### Test Data
Sample test queries and chunks in `tests/fixtures/rag_test_data.json`:
- 10 in-scope queries (expected to return relevant chunks)
- 10 out-of-scope queries (expected to be rejected)
- 5 sample textbook chunks for testing

## Quality Metrics

The system logs comprehensive metrics for monitoring:

```json
{
  "event": "response_generated",
  "query_id": "uuid",
  "confidence_score": 0.87,
  "hallucination_detected": false,
  "latency_ms": 340,
  "response_length": 450
}
```

### Success Criteria (Spec Requirements)
- **Accuracy**: >95% pass rate on test suite
- **Hallucination Rate**: <5% on out-of-scope queries
- **Retrieval Recall**: >90% of in-scope queries return relevant chunks
- **Semantic Similarity**: >0.80 average
- **Latency**: <1s p95

## Embedding Models Supported

| Model | Size | Dimension | Latency | Accuracy | License |
|-------|------|-----------|---------|----------|---------|
| **bge-small-en-v1.5** | 133MB | 384 | 25-45ms | 87-88% | Apache 2.0 |
| all-MiniLM-L6-v2 | 80MB | 384 | 15-30ms | 84-85% | Apache 2.0 |
| e5-small-v2 | 130MB | 384 | 20-40ms | 86-87% | MIT |

**Recommended**: BGE-small-en-v1.5 (best quality/speed balance)

## Hallucination Detection

The quality monitor detects hallucinations using:

1. **Low confidence threshold** (<0.5)
2. **External knowledge patterns** (keywords like "according to", "in my knowledge")
3. **Response length anomalies** (2x longer than sources)
4. **Multiple indicator validation** (requires 2+ signals)

## Future Enhancements (Post-MVP)

- User Story 2: Enhanced citations with clickable links
- User Story 3: Re-embed with BGE model using zero-downtime migration
- Phase 6: Monitoring dashboard and performance optimization

## Implementation Tasks Completed

Phase 1 (Setup):
- ✅ T001: Python testing infrastructure with pytest
- ✅ T002: Embedding model configuration system
- ✅ T003: Logging and metrics infrastructure
- ✅ T004: Qdrant client utilities
- ✅ T005: Test fixtures and sample data
- ✅ T006: Benchmark suite structure

Phase 2 (Foundation):
- ✅ T007: Model downloading and validation (scaffolding)
- ✅ T008: Embedding model loader and switcher
- ✅ T009: Query encoding function
- ✅ T010: Chunk preprocessing and batching
- ✅ T011: Retrieval score normalization
- ✅ T012: Qdrant collection alias utilities
- ✅ T013: Zero-downtime migration script skeleton
- ✅ T014: Quality metrics logging

Phase 3 (User Story 1 - Accurate Answers):
- ✅ T015: Unit tests for accurate answer retrieval
- ✅ T016: Unit tests for hallucination detection
- ✅ T017: Semantic similarity helpers
- ✅ T018: Integration test for RAG pipeline
- ✅ T020: Source-only answer filter
- ✅ T021: Relevance threshold checker
- ✅ T022: "Not in textbook" response handler
- ✅ T023: Hallucination detection logic
- ✅ T024: Answer formatting from chunks
- ✅ T025: Confidence score calculation
- ✅ T026: Query latency tracking
- ✅ T027: Response validation
- ✅ T028: Accuracy metrics logging
- ✅ T029: FastAPI /query endpoint

## Documentation

- `README.md` (this file): Overview and quick start
- `specs/002-rag-accuracy/spec.md`: Feature specification
- `specs/002-rag-accuracy/plan.md`: Architecture and design
- `specs/002-rag-accuracy/research.md`: Model selection and research
- `specs/002-rag-accuracy/tasks.md`: Task breakdown

## Support

For issues or questions:
1. Check test fixtures in `tests/fixtures/rag_test_data.json`
2. Review logs in console output
3. Check API status: `GET /api/rag/status`
4. Run tests: `pytest tests/ -v`
