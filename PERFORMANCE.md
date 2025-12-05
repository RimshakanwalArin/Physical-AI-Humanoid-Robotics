# Performance Optimization Guide

This document outlines strategies for optimizing the performance of the Physical AI Robotics Textbook.

## Performance Targets

- **First Contentful Paint (FCP)**: < 1.5s
- **Largest Contentful Paint (LCP)**: < 2.5s
- **Cumulative Layout Shift (CLS)**: < 0.1
- **Time to Interactive (TTI)**: < 3.5s
- **API Response Time**: < 200ms (p95)
- **Search Latency**: < 150ms

## Frontend Performance

### Code Splitting

#### Dynamic Imports
```jsx
import { lazy, Suspense } from 'react';

// Load ChatBot only when needed
const ChatBot = lazy(() => import('./ChatBot'));

export function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <ChatBot />
    </Suspense>
  );
}
```

#### Route-Based Code Splitting
```jsx
import { Routes, Route, Suspense } from 'react-router-dom';

const routes = [
  { path: '/', component: Home },
  { path: '/chapters', component: lazy(() => import('./Chapters')) },
  { path: '/about', component: lazy(() => import('./About')) },
];

export function Router() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        {routes.map(route => (
          <Route key={route.path} {...route} />
        ))}
      </Routes>
    </Suspense>
  );
}
```

### Image Optimization

#### Responsive Images
```jsx
// Use Next.js Image component or equivalent
<img
  src="robot.jpg"
  srcSet="robot-small.jpg 480w, robot-medium.jpg 800w, robot-large.jpg 1200w"
  sizes="(max-width: 600px) 100vw, 80vw"
  alt="Humanoid robot"
/>
```

#### Image Formats
- Use WebP with JPEG fallback
- Compress images aggressively
- Lazy load images below the fold

```jsx
<img
  src="diagram.webp"
  alt="ROS 2 Architecture"
  loading="lazy"
/>
```

### Bundle Analysis

```bash
# Analyze bundle size
npm install --save-dev webpack-bundle-analyzer

# View bundle report
npm run analyze
```

Configuration:
```js
// webpack.config.js
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer')
  .BundleAnalyzerPlugin;

module.exports = {
  plugins: [
    new BundleAnalyzerPlugin(),
  ],
};
```

### Caching Strategies

#### Service Worker
```js
// public/service-worker.js
const CACHE_NAME = 'robotics-textbook-v1';
const ASSETS = [
  '/',
  '/index.html',
  '/static/css/main.css',
  '/static/js/main.js',
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(ASSETS);
    })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});
```

#### Browser Caching Headers
```bash
# .htaccess or server config
<IfModule mod_expires.c>
  ExpiresActive On

  # Cache static assets for 1 year
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"

  # Don't cache HTML
  ExpiresByType text/html "access plus 0 seconds"
</IfModule>
```

### CSS Optimization

#### Critical CSS
```html
<head>
  <!-- Inline critical CSS for above-the-fold content -->
  <style>
    body { font-family: system-ui; }
    .header { /* ... */ }
    .hero { /* ... */ }
  </style>

  <!-- Defer non-critical CSS -->
  <link
    rel="preload"
    href="styles/non-critical.css"
    as="style"
    onload="this.onload=null;this.rel='stylesheet'"
  />
</head>
```

#### CSS-in-JS Performance
```jsx
// Avoid inline styles that cause re-renders
// Bad
<div style={{ color: computeColor() }}>...</div>

// Good
<div className="dynamic-color">...</div>

/* CSS file */
.dynamic-color {
  color: var(--dynamic-color);
}
```

### JavaScript Performance

#### Minimize Main Thread Work
```jsx
// Bad - blocks main thread
function expensiveCalculation() {
  const result = new Array(1000000)
    .fill(0)
    .map((_, i) => Math.sqrt(i));
  return result;
}

// Good - use Web Worker
// worker.js
self.onmessage = (event) => {
  const result = new Array(1000000)
    .fill(0)
    .map((_, i) => Math.sqrt(i));
  self.postMessage(result);
};

// app.jsx
const worker = new Worker('worker.js');
worker.postMessage(null);
worker.onmessage = (e) => {
  console.log('Result:', e.data);
};
```

#### Debounce and Throttle
```jsx
import { debounce, throttle } from 'lodash-es';

// Debounce for search input
const debouncedSearch = debounce((query) => {
  performSearch(query);
}, 300);

const handleSearchChange = (e) => {
  debouncedSearch(e.target.value);
};

// Throttle for scroll events
const throttledScroll = throttle(() => {
  updateScrollPosition();
}, 100);

window.addEventListener('scroll', throttledScroll);
```

### Monitoring Frontend Performance

```jsx
// Use Web Vitals library
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

getCLS(console.log);  // Cumulative Layout Shift
getFID(console.log);  // First Input Delay
getFCP(console.log);  // First Contentful Paint
getLCP(console.log);  // Largest Contentful Paint
getTTFB(console.log); // Time to First Byte
```

## Backend Performance

### API Response Optimization

#### Query Caching
```python
from functools import lru_cache
import redis

# In-memory cache
@lru_cache(maxsize=128)
def get_chapter(chapter_id: str):
    return db.query(Chapter).filter_by(id=chapter_id).first()

# Redis cache
cache = redis.Redis(host='localhost', port=6379)

@app.get("/api/chapter/{chapter_id}")
async def get_chapter(chapter_id: str):
    cached = cache.get(f"chapter:{chapter_id}")
    if cached:
        return json.loads(cached)

    chapter = db.query(Chapter).filter_by(id=chapter_id).first()
    cache.setex(f"chapter:{chapter_id}", 3600, json.dumps(chapter))
    return chapter
```

#### Response Compression
```python
from fastapi.middleware.gzip import GZIPMiddleware

app.add_middleware(GZIPMiddleware, minimum_size=1000)
```

#### Pagination
```python
@app.get("/api/search")
async def search(
    query: str,
    page: int = 1,
    per_page: int = 10
):
    offset = (page - 1) * per_page
    results = db.query(Search).filter(...).offset(offset).limit(per_page)

    return {
        "results": results,
        "page": page,
        "per_page": per_page,
        "total": total_count
    }
```

### Database Optimization

#### Indexing Strategy
```sql
-- Index frequently searched columns
CREATE INDEX idx_chapter_id ON sections(chapter_id);
CREATE INDEX idx_embedding_similarity ON vectors USING ivfflat (embedding);

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM sections WHERE chapter_id = $1;
```

#### Connection Pooling
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connections
)
```

### Vector Search Optimization

#### Batch Processing
```python
@app.post("/api/batch-search")
async def batch_search(queries: List[str]):
    """Search multiple queries efficiently"""
    embeddings = embedding_service.embed_batch(queries)

    results = []
    for query_embedding in embeddings:
        result = retrieval_service.search_chapters(query_embedding)
        results.append(result)

    return {"results": results}
```

#### Top-K Optimization
```python
# Search for top-3 results instead of top-10
def search_chapters(
    query_vector: List[float],
    top_k: int = 3  # Smaller is faster
) -> List[Dict]:
    results = qdrant_client.search(
        collection_name="robotics_textbook",
        query_vector=query_vector,
        limit=top_k,  # Reduced from 10 to 3
    )
    return results
```

### Monitoring Backend Performance

```python
# Add timing middleware
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    response.headers["X-Process-Time"] = str(duration)
    logger.info(f"{request.method} {request.url.path} {duration:.3f}s")
    return response
```

## Vector Database Performance

### Qdrant Configuration

```python
# Optimize search parameters
client.search(
    collection_name="robotics_textbook",
    query_vector=embedding,
    limit=3,  # Top-3 results
    score_threshold=0.7,  # Only high-confidence results
    with_payload=["chapter_title", "section_title", "content"],  # Only needed fields
)
```

### Batch Indexing

```python
# Index embeddings in batches
BATCH_SIZE = 100
for i in range(0, len(embeddings), BATCH_SIZE):
    batch = embeddings[i:i+BATCH_SIZE]
    client.upsert(collection_name="robotics_textbook", points=batch)
```

## Profiling and Monitoring

### Python Profiling

```python
import cProfile
import pstats

# Profile a function
profiler = cProfile.Profile()
profiler.enable()

# ... code to profile ...

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 functions
```

### Logging and Metrics

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/api/chat")
async def chat(request: ChatRequest):
    logger.info(f"Chat request: {request.query}")

    start = time.time()
    result = process_query(request.query)
    duration = time.time() - start

    logger.info(f"Query processed in {duration:.3f}s")
    result['latency_ms'] = int(duration * 1000)
    return result
```

### Error Tracking

```python
import sentry_sdk

sentry_sdk.init(
    dsn="https://...@sentry.io/...",
    traces_sample_rate=0.1,  # Sample 10% of transactions
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    sentry_sdk.capture_exception(exc)
    return JSONResponse(status_code=500, content={"error": str(exc)})
```

## Performance Benchmarks

### Baseline Metrics
- **Initial Load**: ~2.3s (Lighthouse)
- **API Latency**: ~145ms (p95)
- **Search Latency**: ~120ms
- **Bundle Size**: ~380KB (gzip)

### Optimization Targets
- **Initial Load**: < 1.5s
- **API Latency**: < 200ms (p95)
- **Search Latency**: < 100ms
- **Bundle Size**: < 300KB (gzip)

## Performance Checklist

### Frontend
- [ ] Code splitting implemented
- [ ] Images optimized (WebP, lazy loading)
- [ ] CSS critical path optimized
- [ ] JavaScript minified
- [ ] Service worker configured
- [ ] Bundle analyzed and optimized
- [ ] Web Vitals monitored

### Backend
- [ ] API responses compressed
- [ ] Database indexed appropriately
- [ ] Connection pooling configured
- [ ] Caching implemented
- [ ] Batch processing for bulk operations
- [ ] Error handling and logging in place

### Infrastructure
- [ ] CDN configured for static assets
- [ ] Database replicated for read performance
- [ ] API rate limiting implemented
- [ ] Monitoring and alerting set up

## Tools

- [Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [WebPageTest](https://www.webpagetest.org/)
- [PyCharm Profiler](https://www.jetbrains.com/help/pycharm/profiler.html)
- [New Relic](https://newrelic.com/) - APM
- [Datadog](https://www.datadoghq.com/) - Monitoring
- [Sentry](https://sentry.io/) - Error tracking

## References

- [Web Performance Working Group](https://www.w3.org/webperf/)
- [FastAPI Performance](https://fastapi.tiangolo.com/advanced/)
- [React Performance](https://react.dev/learn/render-optimization)
- [Qdrant Performance](https://qdrant.tech/documentation/guides/performance_tuning/)
