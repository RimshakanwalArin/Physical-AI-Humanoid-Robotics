# Testing & Validation Checklist

Complete this checklist to ensure the project is ready for production deployment.

## ✅ Pre-Testing Setup

- [ ] Clone repository successfully
- [ ] All dependencies installed (npm, Python)
- [ ] Virtual environment created and activated
- [ ] `.env` file configured with correct endpoints
- [ ] Qdrant database running (docker run -p 6333:6333 qdrant/qdrant)

## 🧪 Frontend Testing

### Component Tests
- [ ] ChatBot component renders without errors
- [ ] SelectTextHandler component detects text selection
- [ ] Send button submits queries
- [ ] Error messages display on API failure
- [ ] Loading states show during processing
- [ ] Response displays answer and sources

### React Component Specific
```bash
npm test -- ChatBot.test.jsx
npm test -- SelectTextHandler.test.jsx
```

- [ ] All ChatBot tests pass
- [ ] All SelectTextHandler tests pass
- [ ] Coverage > 80%

### Docusaurus Build
```bash
npm run build
```

- [ ] Build completes without errors
- [ ] No TypeScript errors
- [ ] No ESLint warnings (except acceptable ones)
- [ ] All chapters render correctly
- [ ] Sidebar auto-generated properly
- [ ] i18n configuration working

### Frontend Visual Testing
- [ ] Chapters load and display correctly
- [ ] Code blocks are syntax highlighted
- [ ] Images render properly
- [ ] Responsive design works on mobile
- [ ] Chatbot widget visible and accessible
- [ ] Text selection button appears on selection

## 🔙 Backend Testing

### Unit Tests
```bash
cd backend
python -m pytest tests/test_embeddings.py -v
python -m pytest tests/test_api.py -v
```

- [ ] All embedding tests pass
- [ ] All API tests pass
- [ ] Test coverage > 80%
- [ ] No warnings or deprecated functions

### API Endpoint Testing

#### Health Check
```bash
curl http://localhost:8000/api/health
```

- [ ] Returns 200 status
- [ ] Response includes status: "ok"
- [ ] Component status reported

#### Chat Endpoint
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is robotics?", "session_id": "test-123"}'
```

- [ ] Returns 200 status
- [ ] Response includes answer
- [ ] Response includes sources array
- [ ] Response includes latency_ms
- [ ] Session ID is tracked

#### Error Handling
- [ ] Missing query returns 422
- [ ] Invalid JSON returns 400
- [ ] API unavailable returns 503
- [ ] Error messages are descriptive

### Linting
```bash
cd backend
pylint src/ --disable=all --enable=C,W
```

- [ ] No critical warnings
- [ ] Code style consistent
- [ ] No obvious bugs detected

## 📊 Data Pipeline Testing

### Chapter Extraction
```bash
python indexing/extract_chapters.py
```

- [ ] Extracts all 6 chapters
- [ ] Creates extracted_chapters.json
- [ ] Chapter metadata correct
- [ ] Sections properly parsed
- [ ] Code blocks preserved

### Embedding Generation
```bash
python indexing/embed.py
```

- [ ] Generates embeddings for all sections
- [ ] Creates embeddings.json
- [ ] Embedding dimension = 384
- [ ] All embeddings normalized
- [ ] Metadata preserved

### Qdrant Indexing
```bash
python indexing/load_to_qdrant.py
```

- [ ] Collection created successfully
- [ ] All embeddings uploaded
- [ ] Can search collection
- [ ] Search returns relevant results
- [ ] Metadata searchable

## 🔗 Integration Testing

### End-to-End Flow
1. [ ] Start Docusaurus: `npm start`
2. [ ] Start FastAPI: `uvicorn backend.src.main:app --reload`
3. [ ] Select text in chapter
4. [ ] Click "Ask AI" button
5. [ ] Submit question in chatbot
6. [ ] Verify answer received
7. [ ] Verify sources displayed

### Cross-Component Communication
- [ ] Frontend can reach backend API
- [ ] Backend can access Qdrant
- [ ] Session IDs persist correctly
- [ ] Query logging works (if database configured)

### Error Scenarios
- [ ] Close backend, try to query - error message shows
- [ ] Stop Qdrant, try search - graceful error
- [ ] Invalid session ID - handled gracefully
- [ ] Very long query - processed correctly
- [ ] Special characters in query - handled properly

## 📱 Browser Compatibility

Test on these browsers:
- [ ] Chrome 90+
- [ ] Firefox 88+
- [ ] Safari 14+
- [ ] Edge 90+
- [ ] Mobile Chrome
- [ ] Mobile Safari

### Desktop Testing
- [ ] Chapters render correctly
- [ ] Chatbot functional
- [ ] No console errors
- [ ] Links work properly

### Mobile Testing
- [ ] Responsive layout works
- [ ] Touch interactions work
- [ ] Chatbot accessible
- [ ] Text selection works
- [ ] No layout shifts

## ♿ Accessibility Testing

### Keyboard Navigation
- [ ] Tab through all interactive elements
- [ ] Shift+Tab works backwards
- [ ] Enter submits forms
- [ ] Escape closes modals
- [ ] Focus visible at all times

### Screen Reader Testing
- [ ] Use NVDA (Windows) or VoiceOver (Mac)
- [ ] Page structure announced correctly
- [ ] Form labels announced
- [ ] Links have descriptive text
- [ ] Images have alt text
- [ ] Buttons announced correctly

### Color Contrast
```bash
npm install --save-dev axe-core
npm test -- --testPathPattern=accessibility
```

- [ ] All text meets WCAG AA (4.5:1)
- [ ] Interactive elements meet 3:1
- [ ] Color not only differentiator

### Focus Management
- [ ] Focus visible at all times
- [ ] Focus order is logical
- [ ] No keyboard traps

## ⚡ Performance Testing

### Frontend Performance
```bash
npm run build
npx lighthouse https://localhost:3000
```

- [ ] First Contentful Paint < 1.5s
- [ ] Largest Contentful Paint < 2.5s
- [ ] Cumulative Layout Shift < 0.1
- [ ] Time to Interactive < 3.5s
- [ ] Lighthouse score > 90

### Backend Performance
- [ ] API response < 200ms (p95)
- [ ] Search latency < 100ms
- [ ] Embedding generation < 100ms/text
- [ ] No memory leaks on sustained load

### Load Testing
```bash
# Using Apache Bench
ab -n 1000 -c 10 http://localhost:8000/api/health

# Or using hey
go install github.com/rakyll/hey@latest
hey -n 1000 -c 10 http://localhost:8000/api/health
```

- [ ] Handles 100+ concurrent requests
- [ ] No request timeouts
- [ ] Error rate < 0.1%

## 🔐 Security Testing

### Input Validation
- [ ] SQL injection attempts fail safely
- [ ] XSS attempts fail safely
- [ ] Long inputs handled properly
- [ ] Invalid JSON rejected

### CORS
- [ ] Only allowed origins can access API
- [ ] Preflight requests working
- [ ] Credentials handled correctly

### Secrets
- [ ] No API keys in code
- [ ] Environment variables used
- [ ] `.env` not committed to git
- [ ] `.env.example` present

### Headers
- [ ] Content-Type set correctly
- [ ] CORS headers present
- [ ] Security headers configured

## 📦 Deployment Readiness

### Code Quality
- [ ] No console.log statements (except warnings/errors)
- [ ] No `debugger;` statements
- [ ] No `TODO` comments without context
- [ ] No commented-out code blocks

### Dependencies
- [ ] No unused dependencies
- [ ] All versions pinned
- [ ] No security vulnerabilities: `npm audit` returns 0
- [ ] Lock files committed

### Documentation
- [ ] README.md complete
- [ ] DEVELOPMENT.md current
- [ ] Code comments clear
- [ ] API documentation accurate
- [ ] Deployment instructions clear

### Configuration
- [ ] `.env.example` has all required vars
- [ ] Defaults are sensible
- [ ] Documentation of each var
- [ ] No hardcoded values

## 🚀 Deployment Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] Code review completed
- [ ] Performance benchmarks met
- [ ] Security audit passed
- [ ] Backups configured
- [ ] Rollback plan documented

### Deployment
- [ ] Frontend deployed to GitHub Pages
- [ ] Backend deployed (Vercel/Railway/Heroku)
- [ ] Database migrations applied
- [ ] Vector database indexed
- [ ] DNS configured
- [ ] SSL certificate installed

### Post-Deployment
- [ ] Health check passes
- [ ] Monitoring alerts active
- [ ] Error tracking enabled
- [ ] Analytics working
- [ ] User communication ready
- [ ] Incident response plan activated

## 📋 Final Validation

### Content Review
- [ ] All 6 chapters complete
- [ ] Content technically accurate
- [ ] Code examples run without errors
- [ ] References and links valid
- [ ] Images display correctly

### Feature Completeness
- [ ] Chatbot fully functional
- [ ] Text selection working
- [ ] Citations accurate
- [ ] Session tracking working
- [ ] Error messages helpful

### User Experience
- [ ] Intuitive interface
- [ ] Clear error messages
- [ ] Fast response times
- [ ] Responsive design
- [ ] Accessible to all users

## ✨ Final Checklist

- [ ] All sections above completed
- [ ] No known bugs
- [ ] Performance targets met
- [ ] Accessibility standards met
- [ ] Documentation complete
- [ ] Team approval obtained
- [ ] Go/No-Go decision: **GO** 🚀

---

## Sign-Off

- **Tested By**: ________________
- **Date**: ________________
- **Status**: [ ] Ready for Production [ ] Needs Work

## Notes

```
[Add any notes, issues found, or concerns here]
```

---

**How to Use This Checklist**:
1. Print or copy this document
2. Work through each section systematically
3. Mark items as completed
4. Note any failures or issues
5. Before deployment, all items should be checked
6. Keep record for audit trail
