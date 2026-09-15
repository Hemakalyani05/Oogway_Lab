# Agent Transcripts & AI-Assisted Development Trace

This directory records the development trajectory, tool interactions, prompt engineering iterations, and technical trade-off decisions made while building **The Lenny Growth Assistant**.

---

## 1. Key Engineering Iterations & Failure Corrections

### Iteration 1: Database Driver Architecture & Zero-Config Local Execution
- **Initial Attempt**: The backend database layer was initially structured around `asyncpg` and `aiosqlite` with strict coroutine dispatch.
- **Encountered Limitation**: When testing in zero-dependency environments without `aiosqlite` pre-installed, runtime errors occurred during local SQLite testing.
- **Correction Applied**: Implemented a universal `db_execute` / `db_commit` abstraction in `backend/app/db/session.py` that transparently handles both standard Python standard-library `sqlite3` (with SQLAlchemy sync sessions) and PostgreSQL `asyncpg` connection pools. This guarantees that anyone can clone the repo and run `python3 -m unittest` with zero external dependencies, while retaining high-performance `asyncpg` for PostgreSQL in Docker Compose.

### Iteration 2: Grounding Provenance & Hallucination Guardrails
- **Initial Attempt**: Relying purely on standard vector similarity top-K often retrieved adjacent chunks that lacked exact speaker attribution or timestamp context.
- **Correction Applied**: Created `TranscriptChunker` with regex-based speaker diarization preservation and implemented `HybridRetriever` combining dense cosine embeddings with BM25 sparse keyword ranking via Reciprocal Rank Fusion (RRF). Added `GroundingGuard` to parse structured citations and enforce strict refusal when questions fall outside the Lenny transcript corpus.

### Iteration 3: Secure In-Browser HTML Artifact Rendering
- **Initial Attempt**: Rendering generated HTML directly via `dangerouslySetInnerHTML` presented severe Cross-Site Scripting (XSS) risks.
- **Correction Applied**: Created `SandboxedIframe.tsx` which renders generated HTML inside an `iframe` with `sandbox="allow-scripts"` and strictly **NO** `allow-same-origin`. Injected a locked-down Content-Security-Policy (CSP) meta tag into the `srcDoc`, completely isolating parent session cookies, `localStorage`, and DOM from generated code while allowing interactive buttons, calculators, and visualizations to function.

### Iteration 4: Ship 30 for 30 Skill Formalization
- **Initial Attempt**: A generic prompt produced standard unstructured bullet points.
- **Correction Applied**: Encoded the formal Ship 30 for 30 framework into `backend/app/skills/ship30.py` (1-3-1 sentence hook, visual architecture with bold anchors, ~1,250-word depth, and single 24-hour actionable takeaway).

---

## 2. Transcript Log Summary
The accompanying `transcript_build_log.jsonl` file provides a structured JSON log of the agent execution steps.
