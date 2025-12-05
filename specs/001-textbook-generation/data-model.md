# Data Model: AI-Native Textbook

**Phase**: 1 (Design) | **Status**: Final
**Date**: 2025-12-06

## Overview

The system manages chapters, sections, personalization variants, translations, and chatbot queries. All entities are designed for minimal complexity and free-tier compatibility.

## Core Entities

### Chapter

A complete chapter in the textbook. Serves as the primary unit for content organization, RAG indexing, and personalization.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `id` | UUID | Yes | Primary key; format: `ch-001`, `ch-002`, etc. |
| `title` | String | Yes | e.g., "Introduction to Physical AI" |
| `slug` | String | Yes | URL-safe name; e.g., `intro-physical-ai` |
| `markdown_path` | String | Yes | Path to source file; e.g., `docs/01-introduction-to-physical-ai/index.md` |
| `language` | Enum (EN, UR) | Yes | Primary language; EN default, UR optional |
| `version` | String | Yes | Semantic version; e.g., `1.0.0` |
| `publish_status` | Enum (DRAFT, PUBLISHED, ARCHIVED) | Yes | Publication state |
| `sections` | Relationship → Section[] | Yes | Heading-based sections within chapter |
| `variants` | Relationship → Variant[] | No | Optional personalization variants (Beginner/Intermediate/Advanced) |
| `translations` | Relationship → Translation[] | No | Optional language translations |
| `created_at` | DateTime | Yes | Timestamp |
| `updated_at` | DateTime | Yes | Last modified timestamp |

**Validation Rules**:
- `title` length: 3-200 characters
- `slug` format: `^[a-z0-9-]+$`
- `markdown_path` must exist in repository
- `publish_status` transitions: DRAFT → PUBLISHED → ARCHIVED (no reverse)

---

### Section

A subsection within a chapter, identified by heading level and content.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `id` | UUID | Yes | Primary key; generated from chapter_id + heading hash |
| `chapter_id` | UUID | Yes | Foreign key → Chapter |
| `heading_level` | Int (1-6) | Yes | Markdown heading level (H1-H6) |
| `title` | String | Yes | Section title; e.g., "Embodied Intelligence" |
| `anchor` | String | Yes | URL anchor; e.g., `#embodied-intelligence` |
| `content_hash` | String | Yes | SHA256 of content; used for change detection |
| `created_at` | DateTime | Yes | Timestamp |

**Validation Rules**:
- `anchor` format: `^[a-z0-9-]+$`
- `content_hash` updated whenever section body changes

---

### Variant

Optional personalization: separate content for Beginner/Intermediate/Advanced levels.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `id` | UUID | Yes | Primary key |
| `chapter_id` | UUID | Yes | Foreign key → Chapter |
| `level` | Enum (BEGINNER, INTERMEDIATE, ADVANCED) | Yes | Personalization level |
| `markdown_path` | String | Yes | Path to variant file; e.g., `docs/variants/03-ros2-intermediate.md` |
| `content_overrides` | JSON | Yes | Delta: code examples, explanations, additional references |
| `created_at` | DateTime | Yes | Timestamp |
| `updated_at` | DateTime | Yes | Last modified |

**Validation Rules**:
- One variant per chapter per level (unique constraint on chapter_id + level)
- Variant content must be superset of baseline chapter content (no deletions)

---

### Translation

Optional language translation of a chapter.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `id` | UUID | Yes | Primary key |
| `chapter_id` | UUID | Yes | Foreign key → Chapter |
| `language` | Enum (UR) | Yes | Target language (Urdu only for MVP) |
| `markdown_path` | String | Yes | Path to translated file; e.g., `docs/01-introduction-ur/index.md` |
| `translated_sections` | JSON | Yes | {section_id: translated_title_and_body} |
| `non_translated_sections` | JSON | Yes | {section_id: "not translated"} for code blocks, diagrams |
| `last_updated` | DateTime | Yes | Last translation update |

**Validation Rules**:
- One translation per chapter per language
- All sections must be explicitly marked as translated or not

---

### ChatbotQuery

A user question submitted to the RAG system. Used for analytics and accuracy validation.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `id` | UUID | Yes | Primary key |
| `query_text` | String | Yes | User question; e.g., "What is embodied intelligence?" |
| `session_id` | UUID | Yes | Anonymous session ID (no user tracking) |
| `timestamp` | DateTime | Yes | Query submission time |
| `embedding_vector` | Vector (384-dim) | Yes | Sentence Transformer embedding of query |
| `retrieved_sections` | String[] | Yes | IDs of top-3 retrieved sections |
| `response_text` | String | Yes | Generated answer or "Not found in textbook" |
| `source_citations` | JSON | Yes | [{chapter_id, section_id, excerpt}] |
| `latency_ms` | Int | Yes | API response time |
| `accuracy_label` | Enum (ACCURATE, PARTIAL, IRRELEVANT) | No | Manual review result |

**Validation Rules**:
- `query_text` length: 1-500 characters
- `latency_ms` must be <1000 (1 second p95 target)
- `retrieved_sections` length: 0-3

---

### UserPreference

Browser-stored user preferences (no server-side user tracking).

| Field | Type | Stored Where | Notes |
|-------|------|--------------|-------|
| `personalization_level` | Enum (BEGINNER, INTERMEDIATE, ADVANCED) | localStorage | User's selected chapter difficulty |
| `language` | Enum (EN, UR) | localStorage | Preferred language |
| `last_chapter_viewed` | UUID | localStorage | Last visited chapter (for UX) |

**Validation Rules**:
- All fields optional (defaults: BEGINNER, EN)
- No PII stored
- Cleared on browser data clear

---

## State Diagrams

### Chapter Publication Flow

```
┌─────┐    publish()    ┌───────────┐    archive()    ┌──────────┐
│DRAFT├──────────────→ │PUBLISHED  ├──────────────→  │ARCHIVED  │
└─────┘                └───────────┘                  └──────────┘
```

### RAG Query Lifecycle

```
┌──────────┐   retrieve()   ┌──────────────┐   synthesize()   ┌─────────┐
│Query Text├──────────────→ │Retrieved Chunks├──────────────→  │Answer   │
└──────────┘                └──────────────┘                   └─────────┘
         ↓                            ↓                              ↓
    embedding()                 metadata filter           include citations
```

---

## Relationships

```
Chapter
  ├── 1:N → Section (a chapter has many sections)
  ├── 1:N → Variant (a chapter has 0-3 variants: Beginner/Intermediate/Advanced)
  └── 1:N → Translation (a chapter has 0-N translations)

ChatbotQuery
  └── N:M → Section (a query retrieves top-3 sections)

UserPreference
  └── stored in browser localStorage (no server-side persistence)
```

---

## Free-Tier Design Decisions

1. **No user authentication**: UserPreference stored client-side (localStorage). No user table needed.
2. **Minimal database schema**: Neon PostgreSQL used for optional analytics only (ChatbotQuery logs). Not required for core functionality.
3. **Embeddings in memory**: Sentence Transformers loaded once at startup. No external API calls.
4. **Static chapter files**: Variants and translations are Markdown files, not database rows. Leverages Docusaurus static generation.

---

## Migration & Versioning

- **Initial version**: 1.0.0 (6 chapters, RAG chatbot, optional personalization, optional Urdu translation)
- **Schema migrations**: None required for MVP (all data is Markdown + in-memory embeddings)
- **Future versioning**: If adding user accounts or advanced analytics, versions will increment

