# ✅ Physical AI Robotics Chatbot - Setup Checklist

## Phase 1: Pre-Setup (Before Running Servers)

### Credentials Setup
- [ ] Visit https://neon.tech and create/get a PostgreSQL project
- [ ] Copy the CONNECTION STRING (PostgreSQL)
- [ ] Visit https://console.anthropic.com and create/get API key
- [ ] Copy the API KEY

### Configuration File
- [ ] Open project root: `E:\physical-AI-Robotics\mybook`
- [ ] Copy `.env.example` to `.env`
- [ ] Open `.env` in a text editor
- [ ] Paste DATABASE_URL from Neon
- [ ] Paste ANTHROPIC_API_KEY from Claude console
- [ ] Save `.env` file

### Python Dependencies
- [ ] Open terminal in `backend` folder
- [ ] Run: `pip install -r requirements.txt`
- [ ] Wait for installation to complete
- [ ] Verify: `python -c "import fastapi; print('OK')"`

---

## Phase 2: Database Initialization (First Time Only)

### Initialize Neon Database
- [ ] In terminal, navigate to `backend` folder
- [ ] Run: `python scripts/init_neon_db.py`
- [ ] Wait for "✓ Database initialization completed successfully!" message
- [ ] This enables pgvector extension and creates tables

### Index Your Documents
- [ ] Still in `backend` folder
- [ ] Run: `python scripts/index_documents.py --docs ../mybook/docs`
- [ ] Wait for indexing to complete
- [ ] You should see: `Successfully indexed: X/X documents`
- [ ] This indexes your textbook content into the database

---

## Phase 3: Start Servers

### Option A: Windows (Easiest)
- [ ] Navigate to project root: `E:\physical-AI-Robotics\mybook`
- [ ] Double-click: `START_CHATBOT.bat`
- [ ] Two command windows will open
- [ ] Wait for "✅ SERVERS STARTED!" message
- [ ] Do NOT close these windows while using chatbot

### Option B: Linux/Mac
- [ ] Open terminal in project root
- [ ] Run: `chmod +x start_chatbot.sh`
- [ ] Run: `bash start_chatbot.sh`
- [ ] Wait for "✅ SERVERS STARTED!" message
- [ ] Do NOT close this terminal while using chatbot

### Option C: Manual (All Platforms)
Terminal 1:
- [ ] Navigate to `backend` folder
- [ ] Run: `uvicorn src.main:app --reload --host 0.0.0.0 --port 8000`
- [ ] Wait for "Uvicorn running on http://0.0.0.0:8000"
- [ ] Keep this terminal open

Terminal 2:
- [ ] Navigate to `frontend` folder
- [ ] Run: `python server.py`
- [ ] Wait for green checkmarks
- [ ] Keep this terminal open

---

## Phase 4: Verify Everything Works

### Backend Health Check
- [ ] Open browser to: `http://localhost:8000/api/health`
- [ ] You should see JSON with "status": "healthy"
- [ ] Check that pgvector, database, embeddings, and claude are all "ok"

### Frontend Access
- [ ] Open browser to: `http://localhost:3000`
- [ ] You should see a beautiful purple chatbot login page
- [ ] Elements should be CENTERED (not right-aligned)
- [ ] You should see robot emoji logo

### API Documentation
- [ ] Visit: `http://localhost:8000/api/docs`
- [ ] You should see Swagger UI with endpoints listed
- [ ] Try "GET /api/health" to test

### Test Chatbot
- [ ] On login page, enter any email: `test@example.com`
- [ ] Enter any password (at least 6 chars)
- [ ] Click "Sign In"
- [ ] You should see chat interface
- [ ] Type a question: "What is ROS2?"
- [ ] Click "Send" or press Enter
- [ ] Wait for response (should take 1-3 seconds)
- [ ] You should see answer with sources below

---

## Phase 5: Production Verification

### Performance Check
- [ ] Responses should take 600-2150ms total
- [ ] Messages should appear smoothly
- [ ] No errors in browser console (F12)
- [ ] No errors in terminal windows

### Feature Verification
- [ ] ✓ Login page works
- [ ] ✓ Signup page works
- [ ] ✓ Chat interface works
- [ ] ✓ Send button sends messages
- [ ] ✓ Bot responds with answers
- [ ] ✓ Sources appear below answer
- [ ] ✓ Logout button works
- [ ] ✓ Mobile view works (resize browser)

### Database Verification
- [ ] Documents were indexed
- [ ] Statistics show documents: `curl http://localhost:8000/api/index/stats`
- [ ] Chat history is being saved (messages appear)

---

## Troubleshooting Checklist

### If Servers Won't Start

Server won't run on port 8000?
- [ ] Check if port 8000 is already in use
- [ ] Kill process on port 8000
- [ ] Try different port in code

Server won't run on port 3000?
- [ ] Check if port 3000 is already in use
- [ ] Kill process on port 3000
- [ ] Try different port in code

Python errors?
- [ ] Run: `pip install -r requirements.txt`
- [ ] Check Python version: `python --version` (should be 3.10+)
- [ ] Try: `pip install --upgrade pip`

### If Chatbot Doesn't Respond

No response to questions?
- [ ] Check backend is running (look for "Uvicorn running" message)
- [ ] Check ANTHROPIC_API_KEY is set correctly in .env
- [ ] Check DATABASE_URL is set correctly in .env
- [ ] Check documents were indexed: `curl http://localhost:8000/api/index/stats`
- [ ] Try a simpler question: "What is robotics?"

Database errors?
- [ ] Run: `python backend/scripts/init_neon_db.py`
- [ ] Check DATABASE_URL starts with: `postgresql://`
- [ ] Check sslmode=require is in DATABASE_URL

Embedding errors?
- [ ] Check documents are indexed: `python backend/scripts/index_documents.py --docs ../mybook/docs`
- [ ] Check stats: `curl http://localhost:8000/api/index/stats`

### If UI Doesn't Show

Can't access http://localhost:3000?
- [ ] Check frontend server is running
- [ ] Check for error in frontend terminal
- [ ] Try: `python -c "import http.server; print('OK')"`
- [ ] Try accessing from: http://127.0.0.1:3000

Can't access http://localhost:8000?
- [ ] Check backend server is running
- [ ] Check for error in backend terminal
- [ ] Try: `uvicorn --version`
- [ ] Try accessing from: http://127.0.0.1:8000

---

## Final Verification

Before considering setup complete:

- [ ] Both servers running without errors
- [ ] Can access chatbot at http://localhost:3000
- [ ] Can login/signup
- [ ] Can ask a question and get a response
- [ ] Response includes sources and relevance scores
- [ ] UI is centered (login/signup/input - not right-aligned)
- [ ] Mobile view works
- [ ] Logout button works
- [ ] No console errors (F12 in browser)

---

## You're Ready! 🎉

If all checkboxes are complete, your chatbot is fully operational.

### What to Do Now:
1. Bookmark: http://localhost:3000
2. Use the chatbot to ask questions
3. Share with others (make sure servers stay running)
4. Read the documentation for advanced features

### Keep Servers Running:
- Do NOT close the terminal windows
- The servers need to stay running to use the chatbot
- You can minimize the windows

---

## Quick Support

**Issue: Need detailed help?**
- Read: `CHATBOT_START_GUIDE.md`

**Issue: Want to understand the full system?**
- Read: `CHATBOT_IMPLEMENTATION_SUMMARY.md`

**Issue: Need production deployment?**
- Read: `backend/RAG_CHATBOT_SETUP.md`

**Issue: Need quick reference?**
- Read: `backend/QUICK_REFERENCE.md`

---

Date Completed: _______________

Notes: _______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________
