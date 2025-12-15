# Vercel Deployment - Quick Reference

## 🎯 TL;DR

Deploy **ONLY** the Docusaurus frontend to Vercel. Backend runs separately on Render/Railway.

---

## 1️⃣ Vercel Project Settings

**Go to**: Vercel Dashboard → Your Project → Settings

| Setting | Value |
|---------|-------|
| **Root Directory** | `.` (or leave blank for root) |
| **Framework** | Docusaurus (or "Other") |
| **Build Command** | `npm run build` |
| **Output Directory** | `build` |
| **Node Version** | 20.x or 18.x |

---

## 2️⃣ Environment Variables (Production)

**Go to**: Vercel Dashboard → Settings → Environment Variables

| Name | Value | Scope |
|------|-------|-------|
| `REACT_APP_BACKEND_URL` | `https://your-backend.render.com` | Production, Preview |

**Note**: Replace `your-backend.render.com` with your actual backend URL.

---

## 3️⃣ Local Development

Create `.env.local` in root:

```bash
REACT_APP_BACKEND_URL=http://localhost:8000
```

Then test locally:

```bash
npm run build
npm run serve
```

---

## 4️⃣ Deploy to Vercel

### Option A: Via Vercel Dashboard
1. Connect GitHub repo to Vercel
2. Vercel auto-detects settings
3. Click "Deploy"

### Option B: Via CLI
```bash
vercel login
vercel deploy --prod
```

---

## 5️⃣ Files to Update/Create

| File | Action | Key Change |
|------|--------|-----------|
| `vercel.json` | ✏️ Update | Add `REACT_APP_BACKEND_URL` env var |
| `docusaurus.config.js` | ✏️ Update | Read `REACT_APP_BACKEND_URL` env var |
| `src/components/ChatbotWidget.jsx` | ✏️ Update | Use `process.env.REACT_APP_BACKEND_URL` |
| `.env.example` | ✅ Create | Template for backend URL |
| `.env.local` | ✅ Create | Local dev values |

---

## 6️⃣ Verify Deployment

### ✅ Frontend Loads
```bash
curl https://mybook-username.vercel.app
```
Should return HTML.

### ✅ Chatbot Widget Visible
1. Visit `https://mybook-username.vercel.app`
2. Look for 💬 button in bottom-right
3. Click to open chat

### ✅ Backend Connected
1. Open DevTools → Console
2. Type message in chatbot
3. Check Network tab
4. POST to backend URL should succeed

### ✅ No CORS Errors
Console should NOT show:
```
Access to XMLHttpRequest at 'https://...' from origin 'https://...' has been blocked by CORS policy
```

---

## 7️⃣ Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Build fails | Missing dependencies | `npm install` → `git push` → redeploy |
| Chatbot shows error | Backend URL not set | Add `REACT_APP_BACKEND_URL` in Vercel settings |
| CORS error | Backend doesn't allow Vercel domain | Add to FastAPI: `allow_origins=["https://mybook-...vercel.app"]` |
| Pages load but blank | `docusaurus.config.js` broken | Rebuild locally: `npm run build` |
| i18n pages (Urdu) missing | i18n config missing | Check `docusaurus.config.js` has `i18n` section |

---

## 8️⃣ Architecture

```
GitHub Repo (Frontend only)
        ↓
   Vercel (Docusaurus)
        ↓
   Browser loads https://mybook-...vercel.app
        ↓
   User clicks chatbot
        ↓
   ChatbotWidget.jsx fetches:
   POST ${REACT_APP_BACKEND_URL}/api/rag/query
        ↓
   Backend (Render/Railway/AWS)
        ↓
   Returns JSON response
        ↓
   Chatbot displays answer + sources
```

---

## 9️⃣ Deployment Checklist

### Before Deploying
- [ ] `npm run build` succeeds locally
- [ ] `npm run serve` shows correct site
- [ ] `.env.local` has backend URL
- [ ] Backend running and accessible
- [ ] CORS enabled on backend for Vercel domain

### Vercel Settings
- [ ] Root: `.`
- [ ] Build: `npm run build`
- [ ] Output: `build`
- [ ] `REACT_APP_BACKEND_URL` env var set
- [ ] `vercel.json` in root

### After Deploying
- [ ] Site loads at Vercel URL
- [ ] All pages render (English + Urdu)
- [ ] Chatbot widget visible
- [ ] Chatbot connects to backend
- [ ] No console errors

---

## 🔟 Useful Commands

```bash
# Local testing
npm run build          # Build statically
npm run serve          # Serve build/ locally

# Vercel CLI
vercel login           # Authenticate
vercel deploy --prod   # Deploy to production
vercel env pull        # Get env vars from Vercel
vercel logs            # View deployment logs

# Git workflow
git add .
git commit -m "fix: Vercel deployment config"
git push origin main   # Triggers auto-deploy
```

---

## Configuration Files Quick Look

### `vercel.json`
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "build",
  "env": {
    "REACT_APP_BACKEND_URL": "@react_app_backend_url"
  }
}
```

### `docusaurus.config.js` (top)
```javascript
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
```

### `src/components/ChatbotWidget.jsx` (line 6)
```javascript
const CHAT_API_ENDPOINT = process.env.REACT_APP_BACKEND_URL
  ? `${process.env.REACT_APP_BACKEND_URL}/api/rag/query`
  : '/api/rag/query';
```

### `.env.local` (for local dev)
```bash
REACT_APP_BACKEND_URL=http://localhost:8000
```

---

## Need Help?

1. **Build fails** → Check `npm run build` locally first
2. **Chatbot not working** → Verify `REACT_APP_BACKEND_URL` in Vercel settings
3. **CORS errors** → Add Vercel domain to backend CORS allow_origins
4. **Pages not rendering** → Check `docusaurus.config.js` is valid
5. **i18n issues** → Verify `/i18n/` directory structure

See `VERCEL_DEPLOYMENT_GUIDE.md` for detailed troubleshooting.

