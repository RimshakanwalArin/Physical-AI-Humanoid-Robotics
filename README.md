# Physical AI & Humanoid Robotics Textbook

An interactive, AI-powered textbook for learning about Physical AI, humanoid robotics, and robot programming.

## Features

- 📚 **6 Comprehensive Chapters**: From Physical AI fundamentals to capstone projects
- 🤖 **RAG Chatbot**: Ask questions about the textbook and get instant answers with citations
- 🎯 **Text Selection**: Select any text in the textbook to ask the AI about it
- 🌍 **Multi-language**: English and Urdu support with internationalization
- 🔍 **Semantic Search**: Powered by Sentence Transformers embeddings
- 📝 **Open Source**: Full source code available on GitHub

## Quick Links

- 📖 [View Textbook](https://your-username.github.io/mybook/)
- 🚀 [Development Guide](./DEVELOPMENT.md)
- 🏗️ [Architecture Documentation](./specs/textbook-generation/plan.md)
- 📋 [Feature Specification](./specs/textbook-generation/spec.md)

## Table of Contents

### Chapter 1: Introduction to Physical AI
- Embodied intelligence
- Principles of Physical AI
- Real-world constraints and opportunities

### Chapter 2: Basics of Humanoid Robotics
- Robot anatomy and joint structure
- Sensor systems (vision, proprioception, touch, hearing)
- Bipedal locomotion and kinematics

### Chapter 3: ROS 2 Fundamentals
- Nodes, topics, and services
- Actions and the computation graph
- Robot Description Format (URDF)

### Chapter 4: Digital Twin Simulation
- Gazebo and Isaac Sim
- Physics simulation
- Sim-to-real gap and domain randomization

### Chapter 5: Vision-Language-Action Systems
- Multimodal learning and perception
- Action prediction and control
- Learning from demonstrations

### Chapter 6: Capstone Project
- End-to-end system design
- Household task robotics
- Evaluation metrics and deployment

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.10+
- Docker (for Qdrant)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/physical-ai-textbook.git
   cd physical-ai-textbook
   ```

2. **Setup frontend**
   ```bash
   npm install
   npm start
   ```

3. **Setup backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn src.main:app --reload
   ```

4. **Setup vector database**
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```

5. **Index the textbook**
   ```bash
   python indexing/extract_chapters.py
   python indexing/embed.py
   python indexing/load_to_qdrant.py
   ```

6. **Visit the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Architecture

### Frontend (Docusaurus 3 + React)
- Static site generation with Docusaurus
- Interactive chatbot component
- Text selection handler for in-context queries
- Responsive design for mobile devices

### Backend (FastAPI + RAG)
- Embedding service using Sentence Transformers
- Semantic search with Qdrant
- LLM-free answer synthesis
- RESTful API with OpenAPI/Swagger docs

### Data Pipeline
- Chapter extraction from markdown
- Embedding generation and batch processing
- Vector indexing in Qdrant
- Session-based query logging

## API Endpoints

### POST /api/chat
Send a natural language query about the textbook.

**Request:**
```json
{
  "query": "What is bipedal locomotion?",
  "session_id": "user-12345"
}
```

**Response:**
```json
{
  "status": "success",
  "answer": "Bipedal locomotion refers to movement on two legs...",
  "sources": [
    {
      "chapter_title": "Basics of Humanoid Robotics",
      "section_title": "Bipedal Locomotion and Kinematics",
      "excerpt": "..."
    }
  ],
  "latency_ms": 145
}
```

### GET /api/health
Check system health and component status.

**Response:**
```json
{
  "status": "ok",
  "components": {
    "embeddings": "ok",
    "retrieval": "ok",
    "answer_generation": "ok"
  }
}
```

## Project Structure

```
.
├── docs/                       # Markdown chapters
├── src/                        # React components
├── backend/                    # FastAPI application
│   ├── src/
│   │   ├── api/               # API endpoints
│   │   ├── rag/               # RAG pipeline
│   │   └── db/                # Database models
│   └── tests/                 # Unit tests
├── indexing/                  # Data pipeline scripts
├── .github/workflows/         # CI/CD configuration
├── docusaurus.config.js       # Docusaurus config
└── DEVELOPMENT.md             # Development guide
```

## Testing

### Frontend
```bash
npm test
npm run lint
```

### Backend
```bash
cd backend
python -m pytest tests/ -v
pylint src/
```

## Deployment

### Frontend Deployment (GitHub Pages)
```bash
npm run build
npm run deploy
```

### Backend Deployment
Configure in `.github/workflows/build-deploy.yml` for your chosen platform:
- Vercel (recommended for free tier)
- Railway
- Heroku
- Your own server

## Technology Stack

### Frontend
- **Docusaurus 3**: Static site generation
- **React 18**: Interactive components
- **TypeScript**: Type safety (optional)
- **CSS**: Custom styling and animations

### Backend
- **FastAPI**: Modern web framework
- **Uvicorn**: ASGI server
- **SQLAlchemy**: ORM
- **Sentence Transformers**: Embeddings
- **Qdrant**: Vector database

### Infrastructure
- **PostgreSQL/Neon**: Persistent storage
- **Docker**: Containerization
- **GitHub Actions**: CI/CD

## Learning Outcomes

By the end of this course, you will understand:

✅ Fundamentals of Physical AI and embodied intelligence
✅ Humanoid robot anatomy, sensors, and locomotion
✅ ROS 2 middleware for robot programming
✅ Digital twin simulation and sim-to-real transfer
✅ Vision-language-action systems for robotic control
✅ End-to-end pipeline design for intelligent robots

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes and write tests
4. Commit with clear messages: `git commit -m 'Add feature: description'`
5. Push and create a Pull Request

### Adding Content

To add new chapters or sections:
1. Create markdown file in `docs/`
2. Add front matter with `id`, `title`, and `sidebar_position`
3. Run indexing pipeline to update embeddings
4. Test with the chatbot

### Bug Reports

Please use GitHub Issues with:
- Clear description of the problem
- Steps to reproduce
- Expected vs. actual behavior
- Screenshots if applicable

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Citation

If you use this textbook in your research or teaching, please cite:

```bibtex
@book{physical_ai_robotics_2024,
  title={Physical AI & Humanoid Robotics Textbook},
  author={Your Name},
  year={2024},
  url={https://github.com/your-username/physical-ai-textbook}
}
```

## Acknowledgments

- ROS 2 Community for the middleware framework
- Hugging Face for Sentence Transformers
- Qdrant for vector database
- Docusaurus team for static site generation

## Support

- 📚 Read the [Development Guide](./DEVELOPMENT.md)
- 📖 Check the [Architecture Plan](./specs/textbook-generation/plan.md)
- 💬 Open an [Issue](https://github.com/your-username/physical-ai-textbook/issues)
- 🔗 See [Project Specification](./specs/textbook-generation/spec.md)

## Roadmap

- [ ] Urdu language translation
- [ ] Personalization based on user progress
- [ ] Advanced visualization tools
- [ ] Interactive 3D robot simulator
- [ ] Mobile app (React Native)
- [ ] Certification program
- [ ] Community forums

## Contact

- **Author**: Your Name
- **Email**: your.email@example.com
- **Twitter**: [@yourhandle](https://twitter.com/yourhandle)
- **GitHub**: [@your-username](https://github.com/your-username)

---

**Built with ❤️ for the robotics community**
