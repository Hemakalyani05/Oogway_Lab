# 🎥 Demo Video Script & Evaluator Walkthrough Guide
## "The Lenny Growth Assistant" — 2 to 3 Minute Presentation Script

---

## Video Summary & Presentation Details
- **Title**: Forward Deployed Engineer Assignment — The Lenny Growth Assistant
- **Length**: 2 minutes 45 seconds
- **Format**: Screen share with presenter camera enabled in top-right corner.
- **Presenter**: Forward Deployed Engineer Candidate

---

## 🎬 Step-by-Step Presentation Script with Cue Points

### 0:00 - 0:35 | 1. Problem Context & Forward Deployment Brief
- **Visual**: Presenter on camera $\to$ Transition to The Lenny Growth Assistant home screen.
- **Spoken Script**:
  > *"Hi everyone, my name is [Your Name]. Today, I'm presenting 'The Lenny Growth Assistant,' a production-grade AI system built for product and growth teams.*  
  > *Product managers and growth leads spend hours digging through podcast episodes and newsletters trying to extract actionable frameworks. Generic LLMs often hallucinate or provide bland, ungrounded advice.*  
  > *Our objective was to build an enterprise-ready assistant grounded strictly in Lenny’s Podcast transcripts, capable of producing verifiable answers, Ship 30 for 30 atomic essays, and live interactive artifacts—all runnable locally with Ollama and zero AI friction for the end user."*

---

### 0:35 - 1:20 | 2. Core Demo: Grounded Conversations & Citation Provenance
- **Visual**: Click on quick prompt: *"Explain Brian Chesky's Founder Mode vs Manager Mode."*
- **Spoken Script**:
  > *"Let's look at the conversational assistant in action. Here, I'm running our system. When I ask about Brian Chesky’s Founder Mode, the backend uses a Hybrid RAG retriever—combining dense vector cosine similarity and sparse BM25 keyword matching with Reciprocal Rank Fusion.*  
  > *Notice that every claim has a verified citation chip. If I click on the source chip, a transcript drawer slides open showing the exact episode title, guest name, timestamp, and the raw quote excerpt.*  
  > *If I were to ask an out-of-domain question, the guardrail system refuses cleanly rather than speculating."*

---

### 1:20 - 1:55 | 3. Ship 30 for 30 Content Skill & Native Artifact Viewer
- **Visual**: Click the **"Draft Ship 30 Essay"** button below the message $\to$ Watch the right-hand split-pane smoothly animate open.
- **Spoken Script**:
  > *"Next, let's explore our dedicated skills. With one click on 'Draft Ship 30 Essay', the agent triggers our Ship 30 content skill.*  
  > *Rather than a generic prompt, the skill encodes the exact writing principles of Nicolas Cole and Dickie Bush: a provocative hook, 1-3-1 sentence rhythm, skimmable bold anchors, and a concrete 24-hour takeaway.*  
  > *Notice that the essay doesn't dump into raw chat; it renders natively in our Claude-style Artifact Viewer beside the chat. Users can toggle between Document view, raw Markdown, or copy/download the file with a single click."*

---

### 1:55 - 2:30 | 4. Interactive HTML Artifacts & Security Isolation
- **Visual**: Click prompt: *"Generate an interactive SPADE decision matrix calculator."* Switch Artifact Viewer to **Preview** tab and click buttons inside the widget. Switch between Desktop/Tablet/Mobile viewports.
- **Spoken Script**:
  > *"Now for interactive artifacts. When we request a tool like Gokul Rajaram's SPADE Decision Matrix, the assistant writes an interactive HTML, CSS, and JavaScript widget.*  
  > *Crucially from a security standpoint: generated code is treated as untrusted. We render this in an isolated iframe with `sandbox="allow-scripts"` and strictly NO `allow-same-origin`. This blocks access to parent window cookies, local storage, and the DOM, while injecting a strict Content-Security-Policy.*  
  > *Users can test the calculator live and toggle viewports between Desktop, Tablet, and Mobile."*

---

### 2:30 - 2:45 | 5. Model Toggle, Operability & Wrap-up
- **Visual**: Open Model Selector dropdown $\to$ Show Ollama (Local), Claude 3.7 Sonnet, OpenAI GPT-4o, and Demo Mock status.
- **Spoken Script**:
  > *"Finally, operability: The system supports instant runtime switching between Local Ollama for 100% offline inference and Cloud providers like Claude 3.7 and GPT-4o.*  
  > *The entire application is packaged with Docker Compose for a one-command startup, backed by automated tests covering retrieval, sessions, and security.*  
  > *Thank you for watching, and I look forward to your questions!"*
