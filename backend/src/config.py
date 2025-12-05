import os
from dotenv import load_dotenv

load_dotenv()

# Qdrant Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)

# Neon PostgreSQL Configuration
DATABASE_URL = os.getenv("DATABASE_URL", None)
NEON_DATABASE_URL = os.getenv("NEON_DATABASE_URL", None)

# Server Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,https://localhost:3000").split(",")

# Authentication
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production-1234567890")

# Gemini LLM Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", None)
USE_GEMINI = os.getenv("USE_GEMINI", "true").lower() == "true"
