# Vercel Deployment Guide - Physical AI Textbook

## Executive Summary

This guide explains how to deploy **ONLY the Docusaurus frontend** to Vercel while keeping the FastAPI backend on a separate platform (Render, Railway, or similar). This is the recommended architecture for scalability and cost optimization.

---

## 1. Repository Structure Analysis

```
mybook/ (root)
├── docs/                          # Docusaurus markdown content
│   ├── intro.md
│   ├── ch1-intro-physical-ai.md
│   └── ... (all chapter files)
├── i18n/                          # Internationalization (English + Urdu)
│   ├── en/docusaurus-plugin-content-docs/current/
│   └── ur/docusaurus-plugin-content-docs/current/
├── src/
│   ├── components/
│   │   ├── ChatbotWidget.jsx      # React chatbot component (calls backend API)
│   │   └── ChatbotWidget.module.css
│   ├── css/
│   │   └── custom.css
│   └── theme/                     # Docusaurus theme overrides
├── static/                         # Static assets (images, favicon, etc.)
│   ├── img/
│   └── favicon.ico
├── backend/                        # FastAPI backend (NOT deployed on Vercel)
│   ├── src/
│   └── requirements.txt
├── api/                            # Serverless functions (should be REMOVED for Vercel)
│   └── rag/query.py              # ⚠️ Should NOT exist if backend is separate
├── package.json                    # Node.js dependencies (Docusaurus + React)
├── docusaurus.config.js            # Docusaurus configuration
├── vercel.json                     # Vercel deployment settings
├── sidebars.js                     # Documentation sidebar structure
└── .env.example                    # Environment variables template
```

### Key Points:
- **Frontend only**: Docusaurus + React lives in root
- **Backend separate**: FastAPI runs independently on Render/Railway
- **No Python on Vercel**: Remove `/backend` and `/api` from Vercel deployment
- **Environment variables**: Frontend calls backend via URL from `.env`

---

## 2. Exact Vercel Configuration

### 2.1 Root Directory Setting
```
./
```
**Why**: Your root `package.json` defines the Docusaurus project. Vercel should build from the repository root.

### 2.2 Framework Preset
```
Docusaurus 3 (or "Other" and manually specify below)
```
**If manually selecting**:
- Select **"Docusaurus"** if available in the preset dropdown
- If not, select **"Other"** and manually configure

### 2.3 Build Command
```bash
npm run build
```
**Why**: This runs `docusaurus build` which generates the static HTML in the `build/` directory.

### 2.4 Output Directory
```
build/
```
**Why**: Docusaurus outputs to `build/` by default. Vercel serves this as your site.

### 2.5 Install Command (Optional, explicit)
```bash
npm install
```
**Note**: Vercel auto-detects this, but you can make it explicit.

---

## 3. Complete `vercel.json` Configuration

Replace your current `vercel.json` with:

```json
{
  "version": 2,
  "buildCommand": "npm run build",
  "outputDirectory": "build",
  "installCommand": "npm install",
  "env": {
    "REACT_APP_BACKEND_URL": "@react_app_backend_url"
  },
  "build": {
    "env": {
      "REACT_APP_BACKEND_URL": "@react_app_backend_url"
    }
  },
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=3600, s-maxage=3600"
        }
      ]
    }
  ],
  "redirects": [],
  "rewrites": []
}
```

**Explanation**:
- `buildCommand`: Tells Vercel to run `npm run build`
- `outputDirectory`: Points to the built static files
- `env`: Injects backend URL as environment variable during build
- `headers`: Caches static assets for 1 hour (adjust as needed)
- No `rewrites` or `api/` routing (you'll handle this in ChatbotWidget.jsx)

---

## 4. Updated `docusaurus.config.js` for Vercel

Update your `docusaurus.config.js` to use environment variables:

```javascript
// @ts-check
const { themes } = require('prism-react-renderer');

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics – Essentials',
  tagline: 'Professional AI-native textbook with integrated RAG chatbot',
  favicon: 'img/favicon.ico',

  // ✅ Update for Vercel
  url: 'https://mybook-username.vercel.app', // Change to your actual Vercel domain
  baseUrl: '/',
  organizationName: 'RimshakanwalArin',
  projectName: 'mybook',

  onBrokenLinks: 'warn',
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
    localeConfigs: {
      en: { label: 'English', direction: 'ltr' },
      ur: { label: 'اردو', direction: 'rtl' },
    },
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/RimshakanwalArin/Physical-AI-Humanoid-Robotics/tree/main/',
          routeBasePath: '/',
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],

  // ✅ Make BACKEND_URL available to client-side code
  clientModules: [
    require.resolve('./src/theme/ChatbotSetup.js'),
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Physical AI Textbook',
      logo: {
        alt: 'Physical AI Logo',
        src: 'img/logo.svg',
      },
      hideOnScroll: true,
      items: [
        {
          label: 'Chapters',
          position: 'left',
          items: [
            { label: 'Introduction', to: '/intro' },
            { label: 'Physical AI', to: '/intro-physical-ai' },
            { label: 'Humanoid Robotics', to: '/humanoid-robotics' },
            { label: 'ROS2 Fundamentals', to: '/ros2-fundamentals' },
          ],
        },
        {
          type: 'localeDropdown',
          position: 'right',
        },
        {
          href: 'https://github.com/RimshakanwalArin/Physical-AI-Humanoid-Robotics',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Courses',
          items: [
            { label: 'Physical AI Fundamentals', to: '/intro-physical-ai' },
            { label: 'Humanoid Robotics', to: '/humanoid-robotics' },
            { label: 'ROS 2 Programming', to: '/ros2-fundamentals' },
          ],
        },
        {
          title: 'Resources',
          items: [
            { label: 'GitHub', href: 'https://github.com/RimshakanwalArin/Physical-AI-Humanoid-Robotics' },
            { label: 'Documentation', to: '/' },
          ],
        },
      ],
      copyright: `Copyright © 2024-2025 Physical AI Course. Built with ❤️ using Docusaurus.`,
    },
    prism: {
      theme: themes.github,
      darkTheme: themes.dracula,
      additionalLanguages: ['python', 'bash', 'javascript', 'typescript', 'yaml', 'sql'],
    },
  },
};

module.exports = config;
```

---

## 5. Environment Variables in Vercel

### 5.1 Set Backend URL in Vercel Dashboard

1. **Go to Vercel Dashboard** → Select your project
2. **Settings** → **Environment Variables**
3. **Add new variable**:
   - **Name**: `REACT_APP_BACKEND_URL`
   - **Value**: `https://your-backend-domain.render.com` (or Railway URL)
   - **Environments**: Check `Production` and `Preview`
4. **Save** and **Redeploy**

### 5.2 Local Development (.env.local)

Create `.env.local` in your root directory:

```bash
REACT_APP_BACKEND_URL=http://localhost:8000
```

This allows you to test locally with your FastAPI backend running on `localhost:8000`.

### 5.3 Updated ChatbotWidget.jsx

Ensure your `ChatbotWidget.jsx` uses the environment variable:

```jsx
import React, { useState, useRef, useEffect } from 'react';
import styles from './ChatbotWidget.module.css';

export default function ChatbotWidget() {
  // Get backend URL from environment, fallback to relative path
  const CHAT_API_ENDPOINT = process.env.REACT_APP_BACKEND_URL
    ? `${process.env.REACT_APP_BACKEND_URL}/api/rag/query`
    : '/api/rag/query'; // Fallback for local development

  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      text: 'Hi! 👋 I\'m your AI assistant. Ask me anything about the Physical AI & Robotics textbook!',
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Focus input when chat opens
  useEffect(() => {
    if (isOpen && inputRef.current) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [isOpen]);

  const sendMessage = async (e) => {
    e.preventDefault();

    if (!inputValue.trim()) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      type: 'user',
      text: inputValue,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call backend API with query as URL parameter
      const queryParams = new URLSearchParams({
        query_text: inputValue,
        student_id: sessionStorage.getItem('chatSessionId') || 'guest',
      });

      const response = await fetch(`${CHAT_API_ENDPOINT}?${queryParams.toString()}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();

      // Add bot response
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: data.response_text || 'No response from backend',
        sources: data.sources || [],
        latency_ms: data.latency_ms,
        confidence_score: data.confidence_score,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Chat error:', error);

      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: `Error: ${error.message}. Make sure the backend is running at: ${CHAT_API_ENDPOINT}`,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(e);
    }
  };

  return (
    <>
      {/* Floating Chat Button */}
      <button
        className={styles.chatButton}
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Open chatbot"
        title="Ask me anything!"
      >
        <span className={styles.icon}>
          {isOpen ? '✕' : '💬'}
        </span>
      </button>

      {/* Chat Modal/Drawer */}
      {isOpen && (
        <>
          {/* Backdrop */}
          <div
            className={styles.backdrop}
            onClick={() => setIsOpen(false)}
          />

          {/* Chat Panel */}
          <div className={styles.chatPanel}>
            {/* Header */}
            <div className={styles.header}>
              <div className={styles.headerContent}>
                <h3 className={styles.title}>🤖 AI Assistant</h3>
                <p className={styles.subtitle}>
                  Powered by Claude
                </p>
              </div>
              <button
                className={styles.closeButton}
                onClick={() => setIsOpen(false)}
                aria-label="Close chatbot"
              >
                ✕
              </button>
            </div>

            {/* Messages Container */}
            <div className={styles.messagesContainer}>
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`${styles.message} ${styles[message.type]}`}
                >
                  <div className={styles.messageContent}>
                    <p className={styles.messageText}>{message.text}</p>

                    {/* Sources for bot messages */}
                    {message.type === 'bot' && message.sources && message.sources.length > 0 && (
                      <div className={styles.sources}>
                        <p className={styles.sourcesTitle}>📚 Sources:</p>
                        {message.sources.map((source, idx) => (
                          <div key={idx} className={styles.sourceItem}>
                            <strong>{source.section_name}</strong>
                            <br />
                            <small>
                              {source.chapter_name} - Page {source.page_number}
                            </small>
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Latency info */}
                    {message.type === 'bot' && message.latency_ms && (
                      <div className={styles.latency}>
                        ⏱️ {message.latency_ms.toFixed(0)}ms
                      </div>
                    )}

                    {/* Confidence score */}
                    {message.type === 'bot' && message.confidence_score && (
                      <div className={styles.confidence}>
                        🎯 Confidence: {(message.confidence_score * 100).toFixed(0)}%
                      </div>
                    )}
                  </div>

                  <span className={styles.timestamp}>
                    {message.timestamp.toLocaleTimeString([], {
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </span>
                </div>
              ))}

              {/* Loading indicator */}
              {isLoading && (
                <div className={`${styles.message} ${styles.bot}`}>
                  <div className={styles.messageContent}>
                    <div className={styles.typingIndicator}>
                      <span />
                      <span />
                      <span />
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <form className={styles.inputArea} onSubmit={sendMessage}>
              <input
                ref={inputRef}
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask a question..."
                className={styles.input}
                disabled={isLoading}
              />
              <button
                type="submit"
                className={styles.sendButton}
                disabled={isLoading || !inputValue.trim()}
                title="Send message (Enter)"
              >
                📤
              </button>
            </form>
          </div>
        </>
      )}
    </>
  );
}
```

---

## 6. Common Vercel + Docusaurus Errors & Solutions

### Error 1: "Build failed: Cannot find module 'docusaurus'"

**Cause**: Missing `node_modules` or incorrect `package.json` dependencies.

**Solution**:
```bash
# Ensure package.json has Docusaurus:
npm install @docusaurus/core@3.9.2 @docusaurus/preset-classic@3.9.2

# Push and redeploy:
git add package.json package-lock.json
git commit -m "fix: Ensure Docusaurus dependencies"
git push origin main
```

---

### Error 2: "The Root directory '.' doesn't contain a valid Docusaurus project"

**Cause**:
- Wrong root directory selected in Vercel settings
- Missing `docusaurus.config.js` in root
- `package.json` missing Docusaurus

**Solution**:
1. **Verify file structure**:
   ```bash
   ls -la docusaurus.config.js package.json
   ```
2. **In Vercel dashboard**, ensure:
   - Root Directory: `.` (default)
   - Framework: Docusaurus (or Other)
   - Build: `npm run build`
   - Output: `build`

---

### Error 3: "Error: ENOENT: no such file or directory, scandir '/vercel/output/static'"

**Cause**: `build/` directory doesn't exist after build fails.

**Solution**:
```bash
# Test local build:
npm run build

# Check build output:
ls -la build/

# If build fails, check:
npm run clear
npm install
npm run build
```

---

### Error 4: "Broken links detected"

**Cause**: Markdown files reference non-existent pages.

**Solution**:
```javascript
// In docusaurus.config.js, set to 'warn' instead of 'throw':
onBrokenLinks: 'warn',  // ✅ Allows build to continue
```

---

### Error 5: "React App is undefined" or chatbot shows errors

**Cause**: Environment variables not injected at build time.

**Solution**:
```bash
# In Vercel Dashboard:
1. Settings → Environment Variables
2. Add: REACT_APP_BACKEND_URL = https://your-backend.render.com
3. Redeploy with: Vercel → Redeploy

# Verify in browser:
1. Open DevTools → Console
2. Check: process.env.REACT_APP_BACKEND_URL
```

---

### Error 6: "CORS error when calling backend"

**Cause**: Backend doesn't allow requests from Vercel domain.

**Solution** (add to your FastAPI backend):
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://mybook-username.vercel.app",  # Your Vercel domain
        "http://localhost:3000",                # Local dev
        "http://localhost:8000",                # Local backend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### Error 7: "i18n pages not building (Urdu pages missing)"

**Cause**: i18n structure incorrect or missing locale configuration.

**Solution**:
```javascript
// In docusaurus.config.js, verify:
i18n: {
  defaultLocale: 'en',
  locales: ['en', 'ur'],
  localeConfigs: {
    en: { label: 'English', direction: 'ltr' },
    ur: { label: 'اردو', direction: 'rtl' },
  },
},

// Rebuild:
npm run build
```

---

### Error 8: "Vercel deployment protection blocking API requests"

**Cause**: Vercel has enabled "Deployment Protection" and your backend IP isn't whitelisted.

**Solution**:
```bash
# Option 1: Disable deployment protection (if safe)
# Vercel Dashboard → Settings → Deployment Protection → Disable

# Option 2: Use Vercel CLI with auth token
vercel env pull
vercel deploy --prod
```

---

## 7. Deployment Verification Checklist

### Pre-Deployment (Local Testing)

- [ ] **Build succeeds locally**:
  ```bash
  npm run build
  npm run serve  # Test production build
  ```

- [ ] **Docusaurus renders correctly**:
  - All chapters visible
  - Navigation works
  - Urdu pages accessible at `/ur/`

- [ ] **Chatbot widget loads**:
  - Button visible in bottom-right
  - Can type messages
  - Receives responses (if backend running locally)

- [ ] **Environment variable set locally** (`.env.local`):
  ```bash
  REACT_APP_BACKEND_URL=http://localhost:8000
  ```

- [ ] **Backend running on separate service**:
  - Render.com OR Railway OR local `localhost:8000`
  - CORS enabled for Vercel domain

### Vercel Configuration

- [ ] **Project settings correct**:
  - Root Directory: `.`
  - Framework: Docusaurus
  - Build Command: `npm run build`
  - Output Directory: `build`

- [ ] **Environment variables set**:
  - `REACT_APP_BACKEND_URL` set to backend domain
  - Applied to Production and Preview

- [ ] **`vercel.json` in root**:
  - `buildCommand`: `npm run build`
  - `outputDirectory`: `build`
  - No `/api/` rewrites (backend is separate)

- [ ] **`docusaurus.config.js` updated**:
  - `url` set to Vercel domain
  - `baseUrl: '/'`
  - Uses `REACT_APP_BACKEND_URL` env var

### Post-Deployment (Testing)

- [ ] **Frontend loads at Vercel URL**:
  ```bash
  curl https://mybook-username.vercel.app
  ```

- [ ] **All pages render**:
  - English chapters: ✓
  - Urdu pages: ✓ (check `/ur/intro`, `/ur/humanoid-robotics`)
  - Navigation: ✓

- [ ] **Chatbot widget visible and functional**:
  - Button visible: ✓
  - Can open/close: ✓
  - Can send message: ✓

- [ ] **Chatbot connects to backend**:
  - Check DevTools → Network tab
  - POST to backend URL (not `/api/...`)
  - Receives JSON response with `response_text` and `sources`

- [ ] **No CORS errors**:
  - DevTools → Console shows no CORS blocks
  - Network response shows `Access-Control-Allow-Origin: *`

- [ ] **Performance acceptable**:
  - Page load < 3 seconds
  - Chatbot response < 2 seconds
  - No 404s on static assets

### Error Troubleshooting

If deployment fails:

1. **Check build logs**:
   ```bash
   # In Vercel Dashboard: Deployments → [Latest] → Logs
   ```

2. **Redeploy with fresh build**:
   ```bash
   vercel deploy --prod --force
   ```

3. **Test backend connectivity**:
   ```bash
   curl https://your-backend-domain.render.com/api/health
   # Should return: {"status": "healthy"}
   ```

4. **Check environment variables**:
   ```bash
   # In Vercel Dashboard:
   Settings → Environment Variables → Verify REACT_APP_BACKEND_URL
   ```

---

## 8. Recommended Next Steps

### 1. **Deploy Backend First**
- Use Render.com or Railway
- Test API at its URL
- Configure CORS for your Vercel domain

### 2. **Set Vercel Environment Variables**
- `REACT_APP_BACKEND_URL` = your backend URL
- Test in Preview deployment first

### 3. **Deploy Frontend to Vercel**
- Connect GitHub repo
- Select root directory: `.`
- Build: `npm run build` / Output: `build`
- Set env vars
- Deploy!

### 4. **Test Everything**
- Load frontend at Vercel URL
- Click chatbot, send query
- Verify response + sources appear

### 5. **Monitor**
- Vercel Analytics for performance
- Check backend logs for errors
- Set up alerts for 5xx errors

---

## 9. Quick Reference: File Checklist

| File | Purpose | Status |
|------|---------|--------|
| `package.json` | Node deps + build scripts | ✅ |
| `docusaurus.config.js` | Docusaurus config | ⚠️ Needs `REACT_APP_BACKEND_URL` |
| `vercel.json` | Vercel build settings | ✅ Updated |
| `src/components/ChatbotWidget.jsx` | Frontend chatbot | ✅ Uses env var |
| `.env.local` | Local dev env vars | ⚠️ Create for local testing |
| `backend/` | FastAPI code | ❌ Remove from Vercel (deploy separately) |
| `api/` | Python serverless funcs | ❌ Remove if not using Vercel for backend |

---

## 10. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER'S BROWSER                            │
│                  (mybook-username.vercel.app)                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                   ┌─────────▼──────────┐
                   │   VERCEL (CDN)     │
                   │ ────────────────   │
                   │ • Docusaurus HTML  │
                   │ • React components │
                   │ • Assets (CSS/JS)  │
                   │ • Urdu i18n pages  │
                   │ • ChatbotWidget    │
                   └────────┬───────────┘
                            │
                    ┌──────────────────┐
                    │  ChatbotWidget   │
                    │  (React.jsx)     │
                    └────────┬─────────┘
                             │
                    Fetch API call
                  process.env.REACT_APP_BACKEND_URL
                             │
                   ┌─────────▼──────────────┐
                   │ RENDER / RAILWAY / AWS │
                   │ ────────────────────   │
                   │ • FastAPI backend      │
                   │ • RAG pipeline         │
                   │ • Vector DB (Qdrant)   │
                   │ • CORS enabled         │
                   └────────────────────────┘
```

---

## Summary

✅ **Vercel Configuration**:
- Root: `.`
- Build: `npm run build`
- Output: `build`
- Framework: Docusaurus

✅ **Environment Setup**:
- `REACT_APP_BACKEND_URL` → Backend domain
- Injected at build time
- Used by ChatbotWidget.jsx

✅ **Separation of Concerns**:
- Frontend (Vercel) handles UI + routing
- Backend (Render/Railway) handles API + AI logic
- Both communicate via HTTPS

✅ **Best Practices**:
- No Python/serverless on Vercel
- Backend hosted independently
- CORS properly configured
- Environment variables managed securely

This setup ensures **scalability**, **cost efficiency**, and **production readiness**.

