# Vercel Dashboard Configuration - Step-by-Step

Complete visual guide for configuring your project in the Vercel Dashboard.

---

## Step 1: Import Project from GitHub

### 1.1 Go to Vercel Dashboard
- **URL**: https://vercel.com/dashboard
- **Login**: Sign in with your GitHub account

### 1.2 Click "Add New Project"
```
┌─────────────────────────────────┐
│  Add New    ▼                    │
├─────────────────────────────────┤
│ ▶ Project                         │ ← Click this
│ ▶ Team                            │
│ ▶ Integration                     │
└─────────────────────────────────┘
```

### 1.3 Select "Import Git Repository"
```
┌──────────────────────────────────────┐
│ Import Git Repository                │
│                                      │
│ [Continue]                           │
└──────────────────────────────────────┘
```

### 1.4 Select Your Repository
```
┌────────────────────────────────────┐
│ Select a Git Repository            │
├────────────────────────────────────┤
│ Search for repo...                 │
├────────────────────────────────────┤
│ ☐ RimshakanwalArin/                │
│   ☑ Physical-AI-Humanoid-Robotics │
│                                    │
│          [Import]                  │
└────────────────────────────────────┘
```

---

## Step 2: Configure Build Settings

### 2.1 Project Name
```
┌─────────────────────────────────────┐
│ Project Name                        │
├─────────────────────────────────────┤
│ mybook                              │
│ (or your preferred name)            │
└─────────────────────────────────────┘
```

### 2.2 Root Directory
```
┌──────────────────────────────────────┐
│ Root Directory                       │
├──────────────────────────────────────┤
│ .                                    │
│ (select root, don't change)          │
│                                      │
│ ℹ️ Vercel auto-detects Docusaurus   │
└──────────────────────────────────────┘
```

### 2.3 Framework Preset
```
┌──────────────────────────────────────┐
│ Framework Preset                     │
├──────────────────────────────────────┤
│ ▼ (dropdown)                         │
│                                      │
│ Options:                             │
│ • Docusaurus ← SELECT THIS           │
│ • Next.js                            │
│ • Nuxt.js                            │
│ • Other                              │
└──────────────────────────────────────┘
```

### 2.4 Build and Output Settings
```
┌──────────────────────────────────────┐
│ Build Command                        │
├──────────────────────────────────────┤
│ npm run build                        │
│                                      │
├──────────────────────────────────────┤
│ Output Directory                     │
├──────────────────────────────────────┤
│ build                                │
│                                      │
├──────────────────────────────────────┤
│ Install Command                      │
├──────────────────────────────────────┤
│ npm install                          │
│ (auto-detected, can leave as-is)    │
└──────────────────────────────────────┘
```

**Expected**:
```
✅ Build Command: npm run build
✅ Output Directory: build
✅ Install Command: npm install
```

---

## Step 3: Set Environment Variables

### 3.1 Click "Environment Variables"
```
┌────────────────────────────────────────┐
│ Environment Variables                  │
├────────────────────────────────────────┤
│ [Add New] [Import from .env.local]     │
├────────────────────────────────────────┤
│ NAME                 │ VALUE           │
│──────────────────────┼─────────────────│
│ (currently empty)    │                 │
└────────────────────────────────────────┘
```

### 3.2 Click "Add New"
```
┌────────────────────────────────────────┐
│ Add Environment Variable               │
├────────────────────────────────────────┤
│ NAME:                                  │
│ REACT_APP_BACKEND_URL                 │
│                                        │
│ VALUE:                                 │
│ https://mybook-backend.render.com     │
│                                        │
│ ENVIRONMENTS: ☑ Production             │
│              ☑ Preview                │
│              ☐ Development            │
│                                        │
│              [Save]                    │
└────────────────────────────────────────┘
```

**Important**: Set for BOTH Production and Preview!

### 3.3 Verify Environment Variable Added
```
┌────────────────────────────────────────┐
│ Environment Variables                  │
├────────────────────────────────────────┤
│ NAME                 │ ENVIRONMENTS     │
│──────────────────────┼──────────────────│
│ REACT_APP_BACKEND_URL│ ✓ Prod ✓ Prev  │
│                      │ Value: https://..
└────────────────────────────────────────┘
```

---

## Step 4: Deploy Project

### 4.1 Click "Deploy"
```
┌────────────────────────────────────────┐
│              [Deploy]                  │
│                                        │
│ 🔄 Deployment in progress...          │
└────────────────────────────────────────┘
```

### 4.2 Watch Build Progress
```
📦 Installing dependencies...
    npm install
    ✅ 1.2 MB

🔨 Building project...
    npm run build
    ✅ Generated 42 pages in 23s

📤 Uploading files...
    ✅ 156 files

✅ Production deployment ready!
    https://mybook-abc123.vercel.app
```

### 4.3 Deployment Complete
```
✅ Deployment succeeded!

Domain: https://mybook-abc123.vercel.app
Git Branch: main
Commit: abc1234...
Deployment Time: 35s
```

---

## Step 5: Verify Deployment Settings

### 5.1 Project Settings
**Path**: Settings → General

```
┌────────────────────────────────────────┐
│ Project Settings                       │
├────────────────────────────────────────┤
│ Name: mybook                           │
│ Domains: mybook-abc123.vercel.app      │
│ Framework: Docusaurus                  │
│ Build Command: npm run build           │
│ Output Directory: build                │
│ Root Directory: .                      │
│ Node Version: 20.x                     │
└────────────────────────────────────────┘
```

### 5.2 Environment Variables
**Path**: Settings → Environment Variables

```
┌────────────────────────────────────────┐
│ Environment Variables                  │
├────────────────────────────────────────┤
│ REACT_APP_BACKEND_URL                 │
│ Value: https://mybook-backend.render.com│
│ Environments: Production + Preview      │
└────────────────────────────────────────┘
```

### 5.3 Deployments
**Path**: Deployments

```
┌────────────────────────────────────────┐
│ Deployments                            │
├────────────────────────────────────────┤
│ Status │ Commit      │ Time    │ Domain│
│─────────┼─────────────┼─────────┤────────│
│ ✅ Ready│ abc1234 (2h)│ 35s    │ Live  │
│ ✅ Ready│ def5678 (1d)│ 42s    │       │
│ ✅ Ready│ ghi9012 (2d)│ 38s    │       │
└────────────────────────────────────────┘
```

---

## Step 6: Test Your Deployment

### 6.1 Visit Your Site
- **URL**: Click the domain link from Deployments
- **Expected**: Docusaurus homepage loads
- **Time**: Should load within 3 seconds

### 6.2 Check All Pages
```
Navigation:
├── Introduction ✅
├── Physical AI ✅
├── Humanoid Robotics ✅
├── ROS2 Fundamentals ✅
└── GitHub Link ✅

Language Switcher (top-right):
├── English ✅
└── اردو (Urdu) ✅
```

### 6.3 Test Chatbot Widget
1. **Look for** 💬 button in bottom-right corner
2. **Click** to open chat
3. **Type** a test message (e.g., "What is embodied intelligence?")
4. **Wait** for response (3-5 seconds)
5. **Verify**:
   - ✅ Response appears
   - ✅ Sources shown
   - ✅ No error messages
   - ✅ No CORS warnings in console

### 6.4 Check Browser Console
- **Open**: DevTools (F12) → Console
- **Should see**: No red errors
- **Check**: `process.env.REACT_APP_BACKEND_URL` contains correct backend URL

```javascript
// In browser console, type:
console.log(process.env.REACT_APP_BACKEND_URL)

// Output should be:
// "https://mybook-backend.render.com"
```

---

## Step 7: Configure Custom Domain (Optional)

### 7.1 Add Custom Domain
**Path**: Settings → Domains

```
┌────────────────────────────────────────┐
│ Domains                                │
├────────────────────────────────────────┤
│ [Add] mybook-abc123.vercel.app (current)│
│                                        │
│ Add custom domain:                     │
│ [textbook.mycompany.com]  [Add]        │
└────────────────────────────────────────┘
```

### 7.2 Configure DNS
1. Go to your domain registrar
2. Add DNS records (provided by Vercel)
3. Wait for DNS propagation (5-30 minutes)
4. Vercel confirms SSL certificate

---

## Step 8: Enable Analytics (Optional)

### 8.1 Go to Analytics
**Path**: Analytics

```
┌────────────────────────────────────────┐
│ Analytics                              │
├────────────────────────────────────────┤
│ [Enable Web Analytics]                 │
│ [Enable Monitoring]                    │
└────────────────────────────────────────┘
```

### 8.2 View Real-Time Data
```
┌────────────────────────────────────────┐
│ Real-time                              │
├────────────────────────────────────────┤
│ Requests (24h): 256                    │
│ Average Latency: 145ms                 │
│ Cache Hit Rate: 92%                    │
│ Top Pages:                             │
│  • / (homepage) - 128 visits           │
│  • /intro-physical-ai - 64 visits      │
│  • /humanoid-robotics - 45 visits      │
└────────────────────────────────────────┘
```

---

## Troubleshooting: Common Dashboard Issues

### Issue 1: Build Command Not Found
**Error**: `npm: command not found`

**Solution**:
1. Settings → General
2. Verify "Node Version" is set to 18.x or 20.x
3. Click "Redeploy"

### Issue 2: Output Directory Not Found
**Error**: `build directory was not found`

**Solution**:
1. Run locally: `npm run build`
2. Verify `build/` folder exists
3. Check `docusaurus.config.js` is correct
4. Push changes and redeploy

### Issue 3: Environment Variable Not Injected
**Issue**: Chatbot shows "REACT_APP_BACKEND_URL is undefined"

**Solution**:
1. Settings → Environment Variables
2. Verify `REACT_APP_BACKEND_URL` exists
3. Check "Production" is selected
4. Redeploy: Click latest deployment → Redeploy

### Issue 4: Deployment Protection Enabled
**Error**: "Authentication required" page

**Solution**:
1. Settings → Deployment Protection
2. Choose "No Protection" or "Only Production"
3. Redeploy

---

## Dashboard Navigation Map

```
Dashboard (Home)
├── Projects
│   └── mybook
│       ├── Overview
│       ├── Deployments
│       ├── Analytics
│       └── Settings
│           ├── General
│           ├── Environment Variables
│           ├── Domains
│           ├── Deployment Protection
│           └── Build & Development
└── Team Settings
```

---

## Key Dashboard Terms Explained

| Term | Meaning | Action |
|------|---------|--------|
| **Deployment** | A built version of your site | View logs, rollback, redeploy |
| **Preview** | Staging URL (not live) | Test before production |
| **Production** | Live URL (what users see) | Make sure everything works! |
| **Redeploy** | Rebuild and rehost current code | Use after env var changes |
| **Rollback** | Use an older deployment | If something broke |
| **Domains** | Your site's URL(s) | Add custom domains here |
| **Environment Variables** | Hidden settings injected at build time | Backend URL, API keys, etc. |
| **Analytics** | Traffic and performance stats | Monitor your site |

---

## Deployment Checklist

- [ ] **Root Directory**: `.`
- [ ] **Framework**: Docusaurus
- [ ] **Build Command**: `npm run build`
- [ ] **Output Directory**: `build`
- [ ] **Environment Variable**: `REACT_APP_BACKEND_URL` set
- [ ] **Deployment**: Successful (✅ Ready status)
- [ ] **Site loads**: Homepage visible
- [ ] **Pages work**: All chapters accessible
- [ ] **Chatbot visible**: 💬 button shows
- [ ] **Chatbot works**: Can send messages
- [ ] **No console errors**: DevTools clean
- [ ] **Performance**: Page loads < 3s

---

## After Successful Deployment

✅ **You now have**:
- Production-ready website on Vercel
- Global CDN distribution
- Automatic HTTPS/SSL
- Environment variables injected
- Zero-downtime deployments
- Analytics and monitoring

🎉 **Your site is live!**

Visit: `https://mybook-...vercel.app`

---

## Next Steps

1. **Share your site** → Send link to users
2. **Monitor performance** → Check Analytics dashboard
3. **Watch deployments** → Set up Slack notifications (optional)
4. **Update regularly** → Push changes to GitHub → Auto-deploys

---

## Support

For help with Vercel dashboard:
- [Vercel Dashboard Docs](https://vercel.com/docs/concepts/projects/overview)
- [Environment Variables Guide](https://vercel.com/docs/concepts/projects/environment-variables)
- [Deployment Docs](https://vercel.com/docs/concepts/deployments/overview)

