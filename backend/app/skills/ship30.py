"""
Ship 30 for 30 Content Generation Skill.
Transforms product management and growth insights into high-impact ~1,250-word Atomic Essays
adhering strictly to Ship 30 for 30 writing principles by Nicolas Cole & Dickie Bush.
"""
from typing import Dict, Any, List
from app.rag.hybrid_retriever import hybrid_retriever


SHIP30_SYSTEM_PROMPT = """
You are an expert product growth writer and Ship 30 for 30 essay specialist.
Your goal is to take product management concepts grounded in Lenny's Podcast transcripts and transform them into an authoritative, highly skimmable ~1,250-word Atomic Essay.

### Ship 30 for 30 Core Rules:
1. **The Headline & Hook:** Start with a provocative, benefit-driven title that solves a high-stakes problem for product leaders. Follow with a 1-3-1 sentence cadence to hook the reader immediately in the first 30 seconds.
2. **Skimmable Visual Architecture:**
   - Use clear `###` section headers.
   - Use `####` sub-points (3 to 5 core pillars).
   - Use bulleted lists and selective bolding (`**term**`) as visual anchors for rapid skimming.
   - Never write dense walls of text longer than 3 sentences.
3. **Rigorous Grounding:** Attribute key principles directly to the operators in Lenny's transcripts (e.g. Brian Chesky, Elena Verna, Shreyas Doshi, Gokul Rajaram, Casey Winters, Claire Vo).
4. **The Ultimate Takeaway:** Conclude with 1 concrete, non-obvious action the reader can implement within 24 hours.
5. **Length:** Comprehensive, high-signal depth targeting approximately 1,250 words.

Output format:
Return the complete essay enclosed in an `<artifact title="Ship 30 Essay: [Title]" type="markdown" language="markdown">` block so that the native artifact viewer renders it automatically.
"""


def build_ship30_prompt(topic: str, context_chunks: List[Dict[str, Any]]) -> str:
    """Constructs the prompt for Ship 30 essay generation with injected transcript context."""
    context_str = "\n\n".join([
        f"--- Transcript Excerpt from '{c.get('episode_title', 'Lenny Podcast')}' (Guest: {c.get('guest', 'Operator')}) ---\n"
        f"{c.get('content', '')}"
        for c in context_chunks
    ])

    return f"""
Please write a comprehensive ~1,250-word Ship 30 for 30 Atomic Essay on the topic: "{topic}".

Use the following grounded transcript knowledge from Lenny's Podcast as your factual backbone:
{context_str}

Ensure the essay follows all Ship 30 formatting rules (1-3-1 cadence, bold anchors, skimmability, strong takeaways, transcript citations) and output it in an `<artifact title="Ship 30 Essay: {topic}" type="markdown" language="markdown">` block.
"""
