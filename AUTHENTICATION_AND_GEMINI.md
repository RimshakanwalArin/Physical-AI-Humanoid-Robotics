# Authentication & Gemini LLM Integration Guide

This document explains the new authentication system and Gemini LLM integration added to the Physical AI Robotics Textbook.

## Overview

The project now includes:
- **User Authentication**: Login/Signup with JWT tokens
- **Gemini LLM Integration**: Enhanced answer generation using Google's Gemini API
- **Session Management**: Persistent user sessions with database storage
- **Security**: Password hashing with bcrypt, token-based authentication

## Getting Started

### 1. Set Up Gemini API

#### Get Your API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Get API Key"
3. Create a new API key or use existing one
4. Copy the key

#### Add to .env

```bash
GEMINI_API_KEY=your_api_key_here
USE_GEMINI=true
SECRET_KEY=your-super-secret-key-at-least-32-characters
```

### 2. Update Dependencies

```bash
cd backend
pip install -r requirements.txt
```

New packages installed:
- `google-generativeai==0.3.0` - Gemini API client
- `bcrypt==4.1.1` - Password hashing
- `python-jose==3.3.0` - JWT token handling
- `cryptography==41.0.7` - Encryption
- `email-validator==2.1.0` - Email validation

### 3. Initialize Database

```bash
python backend/src/db/init_db.py
```

This creates the `users` table for storing user accounts.

## Features

### Authentication System

#### Components

**Frontend (React):**
- `src/components/Auth.jsx` - Login/Signup component
- `src/styles/auth.css` - Styling

**Backend (FastAPI):**
- `backend/src/auth/models.py` - User models and schemas
- `backend/src/auth/security.py` - Password hashing and JWT tokens
- `backend/src/auth/routes.py` - Auth endpoints

#### API Endpoints

##### Sign Up
```http
POST /api/auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "securepassword123"
}
```

**Response (201):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "name": "John Doe",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z"
  },
  "message": "Account created successfully"
}
```

##### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "name": "John Doe",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z"
  },
  "message": "Login successful"
}
```

##### Get Current User
```http
GET /api/auth/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (200):**
```json
{
  "id": "uuid-here",
  "email": "user@example.com",
  "name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Gemini LLM Integration

#### How It Works

1. **Query Embedding**: User query is embedded using Sentence Transformers
2. **Retrieval**: Relevant text chunks are retrieved from Qdrant
3. **Gemini Generation**: Google Gemini API generates answer using:
   - Retrieved chunks as context (RAG)
   - User query
   - System prompt for educational tone
4. **Citation Extraction**: Citations are extracted and formatted

#### Example RAG Flow

```
User Query: "What is bipedal locomotion?"
    ↓
1. Embed Query → [0.2, 0.5, ...]
    ↓
2. Search Qdrant → [
    "Bipedal locomotion is movement on two legs...",
    "Zero Moment Point is critical for balance...",
    "Dynamic walking involves swing and stance phases..."
   ]
    ↓
3. Call Gemini API with context
    ↓
4. Response: "Bipedal locomotion refers to movement using two legs,
    which is fundamentally different from quadruped locomotion..."
    ↓
5. Return answer + citations
```

#### API Endpoint

##### Chat with Gemini
```http
POST /api/chat
Authorization: Bearer {optional_token}
Content-Type: application/json

{
  "query": "What is bipedal locomotion?",
  "session_id": "optional-user-session-id"
}
```

**Response (200):**
```json
{
  "status": "success",
  "answer": "Bipedal locomotion refers to movement on two legs. It is fundamentally different from quadruped or wheeled robots because...",
  "sources": [
    {
      "chapter_id": "humanoid-robotics",
      "chapter_title": "Basics of Humanoid Robotics",
      "section_id": "humanoid-robotics-bipedal",
      "section_title": "Bipedal Locomotion and Kinematics",
      "excerpt": "Bipedal walking is fundamentally different..."
    }
  ],
  "latency_ms": 245
}
```

### Fallback to LLM-Free Synthesis

If Gemini is unavailable or returns an error, the system automatically falls back to the original LLM-free synthesis:

```python
if gemini_client and retrieved_chunks:
    try:
        answer, citations = gemini_client.answer_with_rag(query, chunks)
    except Exception:
        # Fallback to synthesis
        answer, citations = AnswerGenerationService.synthesize_answer(query, chunks)
```

## Frontend Integration

### Using Auth Component

```jsx
import Auth from './components/Auth';

function App() {
  const [user, setUser] = useState(null);

  const handleAuthSuccess = (userData) => {
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  if (!user) {
    return <Auth onAuthSuccess={handleAuthSuccess} />;
  }

  return <MainApp user={user} />;
}
```

### Sending Authenticated Requests

```jsx
const token = localStorage.getItem('token');

const response = await fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    query: 'What is robotics?',
    session_id: sessionId
  })
});
```

## Security Considerations

### Password Hashing

Passwords are hashed using bcrypt with salt:

```python
from backend.src.auth.security import hash_password, verify_password

# Register
hashed = hash_password("user_password")
db.save(user_email, hashed)

# Login
if verify_password("user_password", hashed):
    # Password matches
    pass
```

### JWT Tokens

- **Algorithm**: HS256
- **Expiration**: 30 days (configurable)
- **Secret Key**: Set in environment variable (required in production)

```python
# Create token
access_token = create_access_token(data={"sub": user.email})

# Decode token
token_data = decode_token(access_token)
```

### Gemini API Security

- API key stored in environment variables (never hardcoded)
- Request validation with Pydantic
- Rate limiting ready (implement as needed)
- Error handling prevents API key leakage

## Configuration

### Environment Variables

```env
# Authentication
SECRET_KEY=your-super-secret-key-change-in-production-at-least-32-characters

# Gemini LLM
GEMINI_API_KEY=your_gemini_api_key_here
USE_GEMINI=true

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/robotics_textbook

# CORS
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

### Disabling Gemini

If you want to use only the LLM-free synthesis:

```env
USE_GEMINI=false
GEMINI_API_KEY=  # Leave empty
```

## Performance

### Latency Metrics

- **Embedding**: ~100ms
- **Retrieval**: ~120ms
- **Gemini Generation**: ~300-500ms
- **Total p95**: ~800ms

### Optimization Tips

1. **Reduce Context**: Limit to top-3 chunks instead of top-10
2. **Cache Results**: Redis caching for popular queries
3. **Batch Requests**: Process multiple queries together
4. **Async Processing**: Use async/await for non-blocking calls

## Testing

### Test Authentication

```bash
# Sign up
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "Test User",
    "password": "test123456"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123456"
  }'

# Get current user
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Test Chat with Gemini

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "query": "What is robotics?",
    "session_id": "test-session-123"
  }'
```

### Demo Credentials

For testing without authentication setup:
- Email: `demo@example.com`
- Password: `demo123`

(Note: These credentials need to be pre-created in the database)

## Troubleshooting

### "GEMINI_API_KEY environment variable not set"

**Solution**: Set the API key in `.env`:
```bash
GEMINI_API_KEY=your_key_here
```

### "Invalid token" error

**Possible causes**:
1. Token expired (30-day expiration)
2. Token tampered with
3. Wrong secret key in environment

**Solution**: Login again to get a fresh token

### "Email already registered"

**Solution**: Use a different email or reset password

### Gemini API rate limits

If you hit Gemini API rate limits:
- Implement request queuing
- Add exponential backoff
- Fall back to LLM-free synthesis
- Monitor usage on Google AI Studio

## Migration Guide

### From LLM-Free to Gemini

If you had the system without Gemini and want to upgrade:

1. Add Gemini API key to `.env`
2. Update dependencies: `pip install -r requirements.txt`
3. Update database schema (auth tables already included)
4. No breaking changes to existing endpoints

### From Gemini to LLM-Free

To disable Gemini and revert to LLM-free synthesis:

1. Set `USE_GEMINI=false` in `.env`
2. Or remove `GEMINI_API_KEY`
3. System automatically falls back

## Production Deployment

### Before Going Live

1. **Change SECRET_KEY**: Generate a strong 32+ character key
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Set GEMINI_API_KEY**: Securely store API key

3. **Configure DATABASE_URL**: Use production database

4. **Test Authentication**: Verify login/signup works

5. **Monitor Gemini Costs**: Set up usage monitoring

### Deployment Steps

```bash
# 1. Build backend
cd backend
pip install -r requirements.txt

# 2. Initialize database
python src/db/init_db.py

# 3. Run migrations (if any)
# python alembic upgrade head

# 4. Start server
uvicorn src.main:app --host 0.0.0.0 --port 8000

# 5. Verify health
curl http://localhost:8000/api/health
```

## References

- [Google Generative AI Python SDK](https://ai.google.dev/tutorials/python_quickstart)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT Tokens](https://tools.ietf.org/html/rfc7519)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

## Support

For issues or questions:
1. Check `.env` configuration
2. Verify database connection
3. Test API with provided curl examples
4. Check logs for detailed error messages
5. Open an issue on GitHub
