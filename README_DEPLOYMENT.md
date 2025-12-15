# Vercel Deployment Guide Index

Welcome! This folder contains comprehensive documentation for deploying the Physical AI & Robotics textbook to Vercel with a separate backend.

## 📚 Documentation Overview

### For Quick Setup (5 minutes)
👉 **Start here**: [`VERCEL_QUICK_REFERENCE.md`](./VERCEL_QUICK_REFERENCE.md)
- TL;DR configuration settings
- Copy-paste values for Vercel dashboard
- Common issues and quick fixes
- Deployment checklist

### For Complete Understanding (30 minutes)
👉 **Read this**: [`VERCEL_DEPLOYMENT_GUIDE.md`](./VERCEL_DEPLOYMENT_GUIDE.md)
- Detailed repository structure analysis
- Exact Vercel configuration explained
- Environment variable setup
- 8 common errors with solutions
- Verification checklist
- Architecture diagrams

### For Project Overview (10 minutes)
👉 **Understand this**: [`DEPLOYMENT_SUMMARY.md`](./DEPLOYMENT_SUMMARY.md)
- Architecture overview
- Configuration files explained
- Step-by-step deployment instructions
- Production readiness checklist
- Troubleshooting guide

---

## 🚀 Quick Start (TL;DR)

### 1. Update Vercel Settings
```
Root Directory: .
Build Command: npm run build
Output Directory: build
```

### 2. Set Environment Variable
```
Name: REACT_APP_BACKEND_URL
Value: https://your-backend-domain.render.com
```

### 3. Deploy
```bash
vercel deploy --prod
```

### 4. Verify
Visit `https://mybook-...vercel.app` → Click chatbot → Send message

---

## 📋 Key Files Updated/Created

| File | Action | Purpose |
|------|--------|---------|
| `vercel.json` | ✏️ Updated | Tells Vercel how to build |
| `docusaurus.config.js` | ✏️ Updated | Docusaurus configuration |
| `src/components/ChatbotWidget.jsx` | ✅ Ready | Chatbot component |
| `.env.example` | ✅ Created | Environment template |
| `.env.local` | ⚠️ Create | Local dev setup |

---

## 🎯 What's Happening

Your project has **two deployment targets**:

```
┌─────────────────────┐
│  Your Code (GitHub) │
└──────────┬──────────┘
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌─────────┐   ┌──────────┐
│ Vercel  │   │ Render/  │
│Frontend │   │ Railway  │
└────┬────┘   │ Backend  │
     │        └──────────┘
     │             ▲
     └─────fetch───┘
```

- **Vercel** (Frontend): Serves your Docusaurus textbook site
- **Render/Railway** (Backend): Runs your FastAPI RAG chatbot API

---

## ⚡ Installation Steps

### Step 1: Prepare Your Repository
```bash
git status
git add .
git commit -m "Vercel deployment configuration"
git push origin main
```

### Step 2: Deploy Backend (Choose One)

**Option A: Render.com**
```bash
# 1. Go to render.com
# 2. New Web Service → GitHub
# 3. Select your repo
# 4. Runtime: Python 3.12
# 5. Start Command: uvicorn backend.src.main:app --host 0.0.0.0
# 6. Deploy
# 7. Copy your Render URL
```

**Option B: Railway.app**
```bash
# 1. Go to railway.app
# 2. New Project → GitHub
# 3. Select your repo
# 4. Railway auto-detects Python
# 5. Deploy
# 6. Copy your Railway URL
```

### Step 3: Deploy Frontend (Vercel)

**Via CLI:**
```bash
npm install -g vercel
vercel login
vercel deploy --prod
```

**Via Web:**
1. Go to https://vercel.com
2. Import GitHub repository
3. Set `REACT_APP_BACKEND_URL` environment variable
4. Click Deploy

### Step 4: Connect Frontend to Backend

1. In Vercel Dashboard
2. Settings → Environment Variables
3. Add:
   - **Name**: `REACT_APP_BACKEND_URL`
   - **Value**: `https://your-backend-domain.render.com`
4. Redeploy: `vercel deploy --prod`

### Step 5: Test Everything
1. Visit your Vercel URL
2. Click chatbot widget (💬)
3. Type a question
4. Verify response appears

---

## 🧪 Local Testing Before Deployment

```bash
# Create local env file
echo "REACT_APP_BACKEND_URL=http://localhost:8000" > .env.local

# Test build locally
npm run build

# Serve and test
npm run serve
```

Then:
1. Open http://localhost:3000
2. Test all pages load
3. Test chatbot (if backend running at localhost:8000)

---

## ❌ Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Build fails on Vercel | Run `npm run build` locally to debug |
| Chatbot shows error | Check `REACT_APP_BACKEND_URL` in Vercel settings |
| CORS errors | Add Vercel domain to backend `allow_origins` |
| Pages blank | Verify `docusaurus.config.js` is correct |
| Urdu pages missing | Check i18n configuration in `docusaurus.config.js` |

See [`VERCEL_DEPLOYMENT_GUIDE.md`](./VERCEL_DEPLOYMENT_GUIDE.md#6-common-vercel--docusaurus-errors--solutions) for detailed solutions.

---

## 📞 Need Help?

1. **For quick setup**: Read [`VERCEL_QUICK_REFERENCE.md`](./VERCEL_QUICK_REFERENCE.md)
2. **For detailed help**: Read [`VERCEL_DEPLOYMENT_GUIDE.md`](./VERCEL_DEPLOYMENT_GUIDE.md)
3. **For overview**: Read [`DEPLOYMENT_SUMMARY.md`](./DEPLOYMENT_SUMMARY.md)

---

## ✅ Deployment Verification Checklist

- [ ] Backend deployed to Render/Railway
- [ ] Backend URL available (e.g., `https://mybook-backend-abc.render.com`)
- [ ] `REACT_APP_BACKEND_URL` set in Vercel
- [ ] Frontend deployed to Vercel
- [ ] Frontend loads at Vercel URL
- [ ] Chatbot widget visible
- [ ] Can send message to chatbot
- [ ] Response received from backend
- [ ] No CORS errors in console
- [ ] Performance acceptable (< 3s load time)

---

## 🔐 Security Best Practices

✅ **Do**:
- Use `.env.example` template (committed to Git)
- Use `.env.local` for secrets (NOT committed to Git)
- Set environment variables in Vercel Dashboard
- Enable CORS only for your domain

❌ **Don't**:
- Hardcode backend URL in code
- Commit `.env` or secrets to Git
- Use `allow_origins=["*"]` in production
- Store API keys in React code

---

## 📖 Configuration Reference

### `vercel.json`
Controls how Vercel builds your project.

### `docusaurus.config.js`
Configures Docusaurus and reads backend URL.

### `src/components/ChatbotWidget.jsx`
React component that calls the backend API.

### `.env.example`
Template showing available environment variables.

### `.env.local` (Local Dev Only)
Your local development environment variables.

See [`VERCEL_DEPLOYMENT_GUIDE.md`](./VERCEL_DEPLOYMENT_GUIDE.md#3-complete-verceljson-configuration) for detailed file contents.

---

## 🌐 Architecture Overview

```
┌─────────────────────────────────────────┐
│         Your Users' Browsers             │
└────────────────┬────────────────────────┘
                 │
        ┌────────▼────────┐
        │  VERCEL (CDN)   │
        │ ────────────    │
        │ • Docusaurus    │
        │ • React         │
        │ • Chatbot UI    │
        │ • Static Assets │
        └────────┬────────┘
                 │ (REST API)
        ┌────────▼──────────────┐
        │ RENDER / RAILWAY      │
        │ ──────────────────    │
        │ • FastAPI Backend     │
        │ • RAG Pipeline        │
        │ • Vector Database     │
        │ • AI/ML Services      │
        └───────────────────────┘
```

**Frontend**: Vercel (scales globally, fast CDN)
**Backend**: Render/Railway (persistent compute, can handle long requests)

---

## 📊 Deployment Timeline

| Step | Time | Task |
|------|------|------|
| 1 | 5 min | Prepare Git repository |
| 2 | 10 min | Deploy backend to Render/Railway |
| 3 | 5 min | Set Vercel environment variable |
| 4 | 5 min | Deploy frontend to Vercel |
| 5 | 5 min | Verify everything works |
| **Total** | **30 min** | **Complete deployment** |

---

## 🎓 Learning Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Docusaurus 3 Guide](https://docusaurus.io/docs)
- [Render Deployment Guide](https://render.com/docs)
- [Railway Documentation](https://docs.railway.app/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

## 📝 Notes

- Your Vercel deployment is **static** (fast, scalable, cheap)
- Your backend is **serverless** (on-demand, auto-scaling, easy to manage)
- You can swap backend services anytime (Render → Railway, etc.)
- Chatbot uses env var, so no code changes needed to switch backends
- All costs are pay-as-you-go

---

## ✨ Next Steps

1. **Read** [`VERCEL_QUICK_REFERENCE.md`](./VERCEL_QUICK_REFERENCE.md)
2. **Follow** the deployment steps in [`DEPLOYMENT_SUMMARY.md`](./DEPLOYMENT_SUMMARY.md)
3. **Troubleshoot** using [`VERCEL_DEPLOYMENT_GUIDE.md`](./VERCEL_DEPLOYMENT_GUIDE.md)
4. **Monitor** your live site at Vercel Dashboard

---

## 📬 Support

If something isn't working:

1. Check the relevant guide (quick ref, deployment guide, or summary)
2. Verify environment variables are set correctly
3. Check build logs in Vercel Dashboard
4. Run `npm run build` locally to test
5. Consult the troubleshooting section

---

**Happy deploying! 🚀**

Created: December 15, 2025
Branch: `001-textbook-generation`
Repository: https://github.com/RimshakanwalArin/Physical-AI-Humanoid-Robotics

