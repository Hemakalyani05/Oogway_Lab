# UI/UX Design Specification
## The Lenny Growth Assistant

---

## 1. Design Philosophy & Aesthetic Principles

The Lenny Growth Assistant interface follows the **Impeccable Minimalist** and **Claude Workspace** design languages:

1. **Information Density with Breathing Room**: High-signal product typography, clean 1px borders, subtle slate/zinc neutral palettes, and minimal decorative noise.
2. **Side-by-Side Artifact Immersion**: Chat is the reasoning canvas; the right pane is the tangible artifact workspace. Users never need to switch browser tabs or copy code to an external tool.
3. **Instant Transparency & Provenance**: Grounding citations are not hidden footnotes; they are interactive chips showing the exact guest, episode, and timestamp snippet on hover/click.
4. **Predictable Interaction States**: Every action (streaming, tool execution, model switching, artifact rendering) provides clear visual feedback with zero layout shifts.

---

## 2. Color Palette & Typography Tokens

| Token | Dark Mode (Default) | Light Mode | Usage |
| :--- | :--- | :--- | :--- |
| `--bg-base` | `#0D1117` (Zinc 950) | `#FAFAFA` (Zinc 50) | Main background canvas |
| `--bg-surface` | `#161B22` (Zinc 900) | `#FFFFFF` (White) | Chat containers, Sidebar, Cards |
| `--bg-subtle` | `#21262D` (Zinc 800) | `#F4F4F5` (Zinc 100) | Hover states, Code block backgrounds |
| `--border-default`| `#30363D` (Zinc 700) | `#E4E4E7` (Zinc 200) | 1px clean structure borders |
| `--text-primary` | `#F0F6FC` (Zinc 100) | `#09090B` (Zinc 950) | Primary titles, body text |
| `--text-secondary`| `#8B949E` (Zinc 400) | `#71717A` (Zinc 500) | Metadata, timestamps, captions |
| `--accent-brand` | `#6366F1` (Indigo 500) | `#4F46E5` (Indigo 600) | Primary CTA buttons, active state |
| `--accent-success`| `#10B981` (Emerald 500)| `#059669` (Emerald 600)| Live model connected, healthy status |
| `--accent-amber` | `#F59E0B` (Amber 500) | `#D97706` (Amber 600) | Citation badges, Ship 30 triggers |

### Typography Scale
- **Display / Headers**: `Inter`, `-apple-system`, `sans-serif` (Semibold 600 / Medium 500)
- **Monospace / Code**: `JetBrains Mono`, `Fira Code`, `ui-monospace` (Regular 400 / Medium 500)
- **Body / Chat**: `Inter` (Regular 400, line-height 1.6 for enhanced reading cadence)

---

## 3. Information Architecture & Workspace Layout

```
+-----------------------------------------------------------------------------------------------+
| Top Bar: Lenny Assistant Logo | Model Toggle [Ollama v] | KB Status [9 Episodes Indexed] | Theme |
+------------------+-----------------------------------------------+----------------------------+
| Left Sidebar     | Center Chat Area                              | Right Artifact Viewer      |
|                  |                                               | (Collapsible Split Pane)   |
| [ + New Chat ]   | User: "How does Brian Chesky view PM?"        | Tab: [ Preview | Code | MD]|
|                  |                                               |                            |
| Recent Sessions: | Lenny Assistant:                              | +------------------------+ |
| • Founder Mode   | "According to Brian Chesky in the episode     | | Interactive Artifact:  | |
| • B2B PLG Loops  | 'Founder Mode & Reimagining Product'...       | | SPADE Decision Matrix  | |
| • SPADE Matrix   |                                               | |                        | |
| • Retention Curve| Citations: [Brian Chesky #124 14:20]          | | Decision: [Pricing]    | |
|                  |                                               | | Impact:   [High]       | |
| Quick Prompts:   | Actions: [Draft Ship 30 Essay] [Make Artifact]| | +--------------------+ | |
| • PLG Playbook   |                                               | | | [Calculate Score]  | | |
| • LNO Framework  |                                               | | +--------------------+ | |
| • YC PMF Matrix  |                                               | +------------------------+ |
|                  | [ Message Lenny's Assistant...            ^ ] | [ Copy ] [ Download ] [ X ]|
+------------------+-----------------------------------------------+----------------------------+
```

---

## 4. Key Interaction States & Micro-interactions

### 4.1 Chat Streaming & Citation Pinning
- **Thinking / Retrieval State**: Displays an animated pulse indicator: `Searching 120+ transcript chunks...`.
- **Token Streaming**: Uses a typewriter effect with smooth autoscroll.
- **Citation Chips**: Rendered dynamically as footnotes (`[1]`, `[2]`). Hovering over a chip triggers a popover showing the speaker quote; clicking opens the full transcript drawer.

### 4.2 Artifact Split-Screen Transition
- When the assistant outputs an `<artifact>` block, the right pane smoothly animates into view (width transitions from `0` to `48%`).
- Users can toggle between **Preview** (interactive execution), **Source Code** (syntax highlighted), and **Markdown View**.
- A device responsive toggle (`Desktop`, `Tablet`, `Mobile`) allows previewing generated HTML at multiple viewports.

### 4.3 Skill Trigger Buttons
- Each assistant message includes contextual action chips:
  - **"Draft Ship 30 Essay"**: One-click transformation of the message into an atomic essay.
  - **"Generate Visual Artifact"**: Generates a dedicated interactive HTML/CSS tool for the discussed PM concept.

---

## 5. Accessibility (WCAG 2.1 AA Compliance)

1. **Color Contrast**: All text pairings maintain a minimum contrast ratio of 4.5:1 for normal text and 3:1 for large text against `--bg-surface`.
2. **Keyboard Navigation**:
   - `Cmd+K` / `Ctrl+K`: Focus prompt input or search sessions.
   - `Escape`: Close open drawers, modals, or collapse the artifact viewer.
   - `Tab` / `Shift+Tab`: Logical traversal across session list, model dropdown, chat actions, and artifact tabs.
3. **Screen Reader Support**: ARIA attributes on all interactive elements (`aria-expanded`, `aria-label`, `role="region"`, `role="status"`).
4. **Sandboxed Focus Isolation**: The iframe artifact viewer traps focus only when focused, allowing users to Tab back out to the parent chat.
