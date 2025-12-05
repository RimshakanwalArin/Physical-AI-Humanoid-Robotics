# Development Guide

This guide covers how to set up, develop, and deploy the Physical AI Robotics Textbook project.

## Project Structure

```
mybook/
├── docs/                          # Docusaurus markdown chapters
│   ├── 01-introduction-to-physical-ai.md
│   ├── 02-basics-of-humanoid-robotics.md
│   ├── 03-ros2-fundamentals.md
│   ├── 04-digital-twin-simulation.md
│   ├── 05-vision-language-action-systems.md
│   └── 06-capstone-project.md
├── src/                           # Frontend React components
│   ├── components/
│   │   ├── ChatBot.jsx            # Chat interface component
│   │   └── SelectTextHandler.jsx  # Text selection handler
│   ├── css/
│   │   └── custom.css             # Custom styling
│   └── pages/
├── backend/                       # FastAPI backend
│   ├── src/
│   │   ├── main.py               # FastAPI application
│   │   ├── config.py             # Configuration
│   │   ├── api/
│   │   │   ├── models.py         # Pydantic schemas
│   │   │   └── routes.py         # API endpoints
│   │   ├── rag/
│   │   │   ├── embeddings.py     # Embedding service
│   │   │   ├── retrieval.py      # Qdrant search
│   │   │   └── answer_generation.py # LLM-free synthesis
│   │   └── db/
│   │       ├── models.py         # SQLAlchemy models
│   │       ├── neon.py           # Database connection
│   │       └── init_db.py        # Database initialization
│   ├── tests/
│   │   ├── test_api.py
│   │   └── test_embeddings.py
│   └── requirements.txt
├── indexing/                      # Indexing pipeline
│   ├── extract_chapters.py        # Extract chapters from markdown
│   ├── embed.py                   # Generate embeddings
│   └── load_to_qdrant.py          # Load to vector database
├── .github/
│   └── workflows/
│       └── build-deploy.yml       # CI/CD pipeline
├── docusaurus.config.js           # Docusaurus configuration
├── sidebars.js                    # Sidebar structure
└── README.md
```

## Quick Start

### 1. Clone and Setup

```bash
git clone <repo-url>
cd mybook
```

### 2. Frontend Setup (Docusaurus)

```bash
# Install dependencies
npm install

# Development server
npm run start

# Build for production
npm run build
```

The frontend will be available at `http://localhost:3000`

### 3. Backend Setup (FastAPI)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 4. Vector Database Setup (Qdrant)

```bash
# Using Docker (recommended)
docker run -p 6333:6333 qdrant/qdrant

# Or install locally from https://qdrant.tech/documentation/quick_start/
```

Qdrant will be available at `http://localhost:6333`

## Indexing Pipeline

The RAG system requires embeddings to be indexed in Qdrant:

```bash
# 1. Extract chapters from markdown
python indexing/extract_chapters.py

# 2. Generate embeddings
python indexing/embed.py

# 3. Load to Qdrant
python indexing/load_to_qdrant.py
```

This creates:
- `indexing/extracted_chapters.json` - Structured chapter data
- `indexing/embeddings.json` - Embeddings with metadata
- Vector collection in Qdrant

## Database Setup

For persistent storage of queries and user preferences:

```bash
# Set DATABASE_URL environment variable
export DATABASE_URL="postgresql://user:password@localhost:5432/robotics_textbook"

# Initialize database
python backend/src/db/init_db.py
```

For development without a database, the system gracefully degrades to in-memory storage.

## Environment Variables

Create a `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Frontend
REACT_APP_API_URL=http://localhost:8000

# Backend
FASTAPI_ENV=development
QDRANT_URL=http://localhost:6333
DATABASE_URL=postgresql://...

# CORS
CORS_ORIGINS=["http://localhost:3000"]
```

## Testing

### Frontend Tests

```bash
# Run Jest tests
npm test

# Run linting
npm run lint
```

### Backend Tests

```bash
cd backend

# Run pytest
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src

# Run linting
pylint src/
```

## API Documentation

### Interactive API Docs

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### POST /api/chat

Send a query and get an answer with sources.

**Request:**
```json
{
  "query": "What is robotics?",
  "session_id": "user-session-123"
}
```

**Response:**
```json
{
  "status": "success",
  "answer": "Robotics is the study of designing, building, and operating robots...",
  "sources": [
    {
      "chapter_id": "intro-physical-ai",
      "chapter_title": "Introduction to Physical AI",
      "section_id": "intro-physical-ai-basics",
      "section_title": "Embodied Intelligence",
      "excerpt": "..."
    }
  ],
  "latency_ms": 145
}
```

#### GET /api/health

Check system health status.

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2024-01-15T10:30:00Z",
  "components": {
    "embeddings": "ok",
    "retrieval": "ok",
    "answer_generation": "ok"
  }
}
```

## Development Workflow

### Adding New Chapters

1. Create markdown file in `docs/` with front matter:

```yaml
---
id: chapter-id
title: Chapter Title
sidebar_position: 7
---
```

2. Re-run indexing pipeline
3. Test in development

### Modifying the RAG Pipeline

The RAG pipeline has three stages:

1. **Embedding**: `backend/src/rag/embeddings.py`
   - Uses Sentence Transformers
   - Singleton pattern for efficiency

2. **Retrieval**: `backend/src/rag/retrieval.py`
   - Semantic search in Qdrant
   - Top-k document retrieval

3. **Answer Synthesis**: `backend/src/rag/answer_generation.py`
   - LLM-free synthesis from retrieved text
   - Citation generation

### Adding API Endpoints

Edit `backend/src/api/routes.py` to add new endpoints:

```python
@router.get("/api/new-endpoint")
async def new_endpoint():
    """Endpoint documentation."""
    return {"result": "data"}
```

## Deployment

### Frontend Deployment (GitHub Pages)

The CI/CD pipeline automatically deploys to GitHub Pages on push to `main`:

```bash
git push origin main
```

Visit: https://your-username.github.io/mybook/

### Backend Deployment

Configure deployment in `.github/workflows/build-deploy.yml`:

- **Vercel**: Serverless platform (recommended for free tier)
- **Railway**: Modern deployment platform
- **Heroku**: Traditional hosting (limited free tier)

## Debugging

### Frontend Debugging

```bash
# Run with debug output
npm run start -- --debug

# Chrome DevTools: Press F12
```

### Backend Debugging

```bash
# Run with verbose logging
LOGLEVEL=DEBUG uvicorn src.main:app --reload

# VSCode debugging: Add to .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["src.main:app", "--reload"],
      "jinja": true
    }
  ]
}
```

## Common Issues

### "Cannot find module '@theme'"

```bash
npm install
npm run docusaurus clear
npm run start
```

### Vector Database Connection Error

```bash
# Check if Qdrant is running
curl http://localhost:6333/health

# Or start with Docker
docker run -p 6333:6333 qdrant/qdrant
```

### Python ImportError

```bash
# Make sure you're in the virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

## Performance Optimization

### Frontend
- Code splitting with dynamic imports
- Image optimization
- Caching strategies

### Backend
- Singleton pattern for embeddings (loaded once)
- Batch embedding processing
- Connection pooling for database

### Vector Search
- Top-k optimization (typically 3-5 results)
- Cosine similarity (fast on CPU)
- Index optimization in Qdrant

## Monitoring

### Logs

```bash
# Backend logs
tail -f backend_logs.txt

# Frontend build logs
npm run build > build_logs.txt 2>&1
```

### Metrics

The `/api/health` endpoint provides component status. Monitor:
- Embedding service availability
- Qdrant connection status
- Database availability

## Contributing

1. Create a feature branch
2. Make changes
3. Run tests
4. Submit pull request

## References

- [Docusaurus 3 Documentation](https://docusaurus.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [Qdrant Documentation](https://qdrant.tech/)
