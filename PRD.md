# Product Requirements Document (PRD)
## The Lenny Growth Assistant — Forward Deployment Brief & Product Specification

---

## 1. Executive Summary & Forward Deployment Brief

### 1.1 Customer & Engagement Context
A product, growth, and venture team within an enterprise client requires a high-trust, internal AI assistant grounded strictly in verified operator knowledge from **Lenny’s Podcast** transcripts. 

While general LLMs produce generic product advice with high hallucination rates, this team requires:
1. **Authoritative, source-grounded answers** quoting real PM leaders (e.g., Brian Chesky, Elena Verna, Shreyas Doshi, Gokul Rajaram).
2. **Instant conversion of PM insights into reusable content** (specifically atomic essays matching the Ship 30 for 30 methodology).
3. **Native interactive artifacts** (growth models, SPADE decision matrices, retention visualizers) rendered side-by-side with chat without requiring third-party tools.
4. **Zero AI cognitive overhead**: The product and growth operators should not need prompt engineering skills or infrastructure management.

---

### 1.2 User Persona & Jobs to Be Done (JTBD)

| Persona | Role | Core Jobs to Be Done | Key Pains Removed |
| :--- | :--- | :--- | :--- |
| **Product Manager (PM)** | Senior / Lead PM | Formulate product strategy, launch plans, feature specs, and stakeholder trade-offs. | Eliminates hours searching through podcast episodes, transcripts, and newsletters for specific operator frameworks (e.g., LNO, SPADE, Founder Mode). |
| **Growth Lead** | Head of Growth | Design activation loops, PLG funnels, B2B pricing, and retention models. | Eliminates generic advice; replaces it with concrete playbooks from Elena Verna, Casey Winters, and Sean Ellis. |
| **Founder / Product Marketer** | Founder / PMM | Write thought leadership, company memos, and customer-facing essays. | Eliminates writer's block by transforming grounded knowledge directly into formatted ~1,250-word Ship 30 for 30 atomic essays. |

---

### 1.3 Success Metrics

| Category | Metric | Baseline | Target | Measurement Method |
| :--- | :--- | :--- | :--- | :--- |
| **Grounding Quality** | **Citation Precision Rate** | 60% (Raw LLM) | **≥ 98%** | Automated eval asserting every factual claim has an attributable episode title, guest name, and timestamped quote. |
| **Hallucination Rate** | **Out-of-Domain Refusal Rate** | 10% (Raw LLM) | **100%** | When prompted with unanswerable / out-of-scope questions, the system cleanly states it lacks transcript grounding. |
| **Content Velocity** | **Ship 30 Essay Generation Time** | 2-3 hours (Manual) | **< 15 seconds** | Time-to-artifact for a 1,250-word structured atomic essay. |
| **Artifact Usability** | **Interactive Render Success** | N/A | **≥ 99.5%** | Percentage of generated HTML/CSS artifacts that render safely in the sandboxed viewer without runtime errors. |
| **Operational Latency** | **Time to First Token (TTFT)** | N/A | **< 800ms (Cloud) / < 1.8s (Local)** | Measured via backend telemetry / Prometheus metrics. |

---

### 1.4 Assumptions & Forward Deployment Rationales

Because the client engagement brief contained ambiguities, the following explicit engineering and product assumptions were made:

1. **Deployment Flexibility (Local vs. Cloud)**: The client evaluator must be able to run and evaluate the system 100% locally using **Ollama** (e.g., `llama3.2`, `mistral`, `deepseek-r1`) without mandatory API keys, while retaining instant one-click switching to cloud models (**Anthropic Claude 3.7/3.5 Sonnet**, **OpenAI GPT-4o**). A deterministic mock mode is also provided for instant test runs.
2. **Zero-Friction Local Database**: While PostgreSQL with `pgvector` is the enterprise target deployed via Docker Compose, the backend automatically supports an embedded SQLite hybrid retrieval engine so that any local developer can run `uvicorn` or `pytest` with zero external setup.
3. **Artifact Security Model**: Since user-generated or LLM-generated HTML can execute arbitrary JavaScript, all HTML/CSS/JS artifacts are rendered in an isolated `iframe` with `sandbox="allow-scripts"` (strictly excluding `allow-same-origin`) to prevent cookie theft, local storage access, or XSS attacks on the parent application.
4. **Offline Transcript Ingestion**: Transcripts from the ChatPRD repository are bundled locally into structured semantic markdown files, while an ingestion CLI script allows one-command sync and re-indexing against upstream GitHub repositories.

---

### 1.5 Scope Choices: Inclusions & Intentional Exclusions

#### What We Included:
- **FastAPI Async Backend** with modular architecture, strict Pydantic schemas, and SSE streaming.
- **Hybrid RAG Retriever**: Combines dense vector semantic search (SentenceTransformers / pgvector) with sparse BM25 keyword matching using Reciprocal Rank Fusion (RRF).
- **Provenance & Grounding Engine**: Every response extracts and returns structured citations (Episode Title, Guest, Timestamp Chunk, Exact Quote).
- **Ship 30 for 30 Essay Skill**: A dedicated content generation engine enforcing the 1-3-1 sentence cadence, atomic hook, skimmable headings, selective bolding, ~1,250-word length, and takeaway framework.
- **Claude-Style Split-Pane Artifact Viewer**: Side-by-side rendering with live interactive preview, source code inspection, markdown viewing, copy-to-clipboard, and download.
- **Multi-Session State Management**: Persistent conversations, renameable session history, and session-specific memory.
- **Comprehensive Observability**: Structured JSON logging, request tracing, latency timers, and health/readiness probes (`/healthz`, `/readyz`, `/metrics`).
- **Docker Compose**: One-command reproducible local environment.

#### What We Intentionally Excluded (& Why):
- **Full User Authentication (OAuth/SAML)**: Excluded to eliminate friction for the evaluator; multi-tenant user IDs are supported via headers (`X-User-Id`) and session IDs.
- **Continuous Live YouTube Audio Transcription**: Excluded to avoid external API dependencies and long processing queues; instead, we ingest curated, verified transcripts from the official repository.
- **Direct Database Mutation from Agent Tools**: Excluded to prevent prompt injection from modifying database records; all agent actions are read-only against the knowledge base and produce transient/session artifacts.

---

### 1.6 Risks & Trade-Off Matrix

| Risk | Severity | Mitigation Implemented |
| :--- | :--- | :--- |
| **Hallucination of PM Frameworks** | High | Strict system prompt guardrails + Hybrid RAG retrieval + Grounding Verification layer that enforces source citations or outputs a standardized refusal. |
| **Local LLM Performance & Formatting Drift** | Medium | Local Ollama prompts use structured few-shot formatting and JSON-enforced artifact generation, with fallback to structured markdown parser. |
| **Unsafe HTML/JS Execution in Artifacts** | Critical | Strict iframe sandbox (`sandbox="allow-scripts"`, NO `allow-same-origin`), Content-Security-Policy (CSP) enforcement, and DOMPurify sanitization. |
| **Latency in Long-Context Retrieval** | Medium | Hybrid RRF retrieval pre-filters to top-K semantic chunks (K=5-8) rather than stuffing entire multi-hour transcripts, maintaining sub-second TTFT. |
| **Database Connection Failure** | Medium | Resilient async connection pools with automatic fallback to embedded SQLite vector store if PostgreSQL is unreachable. |

---

## 2. Product Functional Specifications

### 2.1 Feature 1: Grounded Conversational Assistant
- **User Action**: The user enters a product or growth query (e.g., *"How does Brian Chesky define Founder Mode?"* or *"What are the core loops in B2B PLG according to Elena Verna?"*).
- **System Behavior**:
  1. The agent queries the Hybrid RAG engine (Dense embeddings + BM25 keyword match).
  2. The system retrieves the top relevant transcript passages with metadata (Episode, Guest, Timestamp).
  3. The agent synthesizes an authoritative answer strictly using the context, embedding inline citation tags `[^1]`.
  4. The frontend renders interactive citation chips below the message. Clicking a chip slides open a source viewer displaying the exact transcript excerpt.
  5. If the topic is absent from the transcripts, the agent responds: *"The available Lenny's Podcast transcripts do not contain information on this topic."*

---

### 2.2 Feature 2: Ship 30 for 30 Content Engine
- **User Action**: The user clicks the **"Draft Ship 30 Essay"** button on any message or explicitly asks for an atomic essay on a PM topic.
- **System Behavior**:
  1. The agent invokes the `Ship30EssaySkill`.
  2. The skill extracts the core insight and builds an atomic essay structured with:
     - **Headline**: High-converting, benefit-driven hook.
     - **Lead-in**: 1-3-1 sentence structure capturing attention in the first 30 seconds.
     - **Body**: 3 to 5 clear sub-points with bold anchors, bulleted lists, and real operator examples from the transcripts.
     - **Takeaway**: 1 actionable playbook or mental model the reader can implement today.
     - **Word Count**: Target ~1,250 words.
  3. The resulting essay is created as an Artifact and automatically opened in the Artifact Viewer.

---

### 2.3 Feature 3: Interactive Artifact Generation & Viewer
- **User Action**: The user requests a template, framework, or interactive tool (e.g., *"Generate an interactive SPADE decision matrix calculator"* or *"Create a B2B Growth Funnel HTML widget"*).
- **System Behavior**:
  1. The agent detects artifact generation intent and outputs a structured `<artifact>` block with title, type (`html` or `markdown`), and code.
  2. The frontend parses the streaming response and immediately opens the right-hand split-pane viewer.
  3. The viewer renders the artifact live:
     - For **HTML/CSS/JS**: Renders inside a secure, sandboxed iframe with live interactivity (e.g. dynamic sliders, calculators).
     - For **Markdown**: Renders formatted typography with syntax highlighting and copy buttons.
  4. Actions available: **Live Preview**, **View Source Code**, **Copy Code**, **Download File**, **Fullscreen**.

---

### 2.4 Feature 4: Model Configuration & Live Toggle
- **User Action**: The user selects a model from the top navbar / sidebar dropdown (Ollama `llama3.2`, Anthropic `claude-3-7-sonnet`, OpenAI `gpt-4o`, or Mock Demo).
- **System Behavior**:
  1. The UI reflects the active provider with a live status indicator (Green = Connected, Yellow = Local Offline, Red = Error).
  2. The backend dynamically routes subsequent requests to the selected provider without requiring server restarts.
  3. If a selected provider fails (e.g., Ollama daemon stopped), the system gracefully reports the issue and offers automatic fallback.

---

## 3. Non-Functional & Operational Requirements

1. **Security**: Zero secrets in client-side code; input validation via Pydantic; isolated artifact rendering.
2. **Reliability**: Graceful degradation when external services (Ollama, PostgreSQL, Anthropic) are unreachable.
3. **Portability**: Runs on macOS, Linux, and Windows via Docker Compose or native Python/Node.
4. **Code Quality**: Strict TypeScript types, modular Python architecture, comprehensive Pytest suite (>85% coverage).
