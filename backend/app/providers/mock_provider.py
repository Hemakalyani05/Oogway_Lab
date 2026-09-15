"""
Deterministic High-Quality Offline Mock Provider for local demo and zero-dependency testing.
"""
import asyncio
from typing import AsyncGenerator, List, Dict, Any

from app.providers.base import BaseLLMProvider, LLMStreamChunk
from app.core.logging import logger


class MockProvider(BaseLLMProvider):
    """
    Offline deterministic provider that generates grounded product answers,
    Ship 30 for 30 essays, or interactive HTML/CSS artifacts based on user intent.
    """
    def __init__(self, model_name: str = "mock-demo-v1"):
        super().__init__(model_name)

    async def is_available(self) -> bool:
        return True

    async def stream_chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.2
    ) -> AsyncGenerator[LLMStreamChunk, None]:
        user_msg = ""
        for m in reversed(messages):
            if m["role"] == "user":
                user_msg = m["content"]
                break

        user_lower = user_msg.lower()

        # Route responses based on topic and intent
        if "ship 30" in user_lower or "atomic essay" in user_lower:
            response_text = self._generate_ship30_essay(user_lower)
        elif "artifact" in user_lower or "calculator" in user_lower or "html" in user_lower or "matrix" in user_lower or "widget" in user_lower:
            response_text = self._generate_interactive_artifact(user_lower)
        elif "chesky" in user_lower or "founder mode" in user_lower:
            response_text = (
                "According to Brian Chesky in the episode *Founder Mode & Reimagining Product Management at Airbnb*, "
                "tech companies often fail when they blindly switch to **Manager Mode** as they scale [^1].\n\n"
                "### Core Principles of Founder Mode at Airbnb:\n"
                "1. **Single Integrated Roadmap:** Rather than splintering into 50 autonomous business units with conflicting roadmaps, the entire company operates on one unified product roadmap reviewed directly by leadership.\n"
                "2. **Merging PM and PMM:** Traditional PMs had devolved into bureaucratic project managers writing Jira tickets. Airbnb merged Product Management with Product Marketing into a single PMM role responsible for both building and storytelling [^1].\n"
                "3. **Synchronized Major Releases:** Airbnb shifted to two massive synchronized seasonal releases per year (Summer & Winter releases) to coordinate marketing, engineering, and customer attention.\n\n"
                "> *\"Founder Mode is not micromanagement; it is deep, obsessive involvement in the details that matter. Great PMs have extreme taste and deep empathy for users.\"* — Brian Chesky [^1]"
            )
        elif "elena" in user_lower or "plg" in user_lower or "growth loop" in user_lower:
            response_text = (
                "Based on Elena Verna's frameworks in *B2B Product-Led Growth (PLG) & Growth Loops*, "
                "PLG is not simply adding a freemium tier—it is an organizational operating model [^1].\n\n"
                "### Elena Verna's Core B2B Growth Pillars:\n"
                "- **Time-to-Value (TTV):** The end-user must experience the core 'aha moment' within 3 minutes of signing up without human friction.\n"
                "- **Product Qualified Leads (PQLs):** Sales shouldn't do cold outbound; instead, sales reaches out to accounts that already have 10-20 active users on the free tier to sell enterprise SSO, security, and governance [^1].\n"
                "- **Activation Rate Priority:** Elena emphasizes getting user activation to 40-50% before optimizing monetization, warning that monetizing a leaky bucket burns brand equity.\n\n"
                "Would you like me to convert this into a **Ship 30 for 30 Atomic Essay** or generate an **Interactive PLG Funnel Calculator**?"
            )
        elif "shreyas" in user_lower or "lno" in user_lower:
            response_text = (
                "In *Good PM vs Great PM & The LNO Framework*, Shreyas Doshi breaks down how top operators manage their cognitive capacity [^1].\n\n"
                "### The LNO Framework:\n"
                "1. **L (Leverage Tasks):** 10x-100x impact work (e.g. strategic roadmap, critical hiring, breakthrough PM specs). Invest 100% effort and aim for perfection.\n"
                "2. **N (Neutral Tasks):** Necessary work where 10x effort yields 0 extra value (e.g. sprint planning, status updates). Execute at 80% quality with minimal time.\n"
                "3. **O (Overhead Tasks):** Administrative chores (e.g. routine expense reports, corporate surveys). Batch them at the end of the day or delegate immediately.\n\n"
                "Shreyas notes that Great PMs distinguish themselves not by shipping on time, but through **high agency and outcome orientation** [^1]."
            )
        elif "spade" in user_lower or "gokul" in user_lower:
            response_text = (
                "According to Gokul Rajaram in *SPADE Framework for High-Stakes Decision Making*, "
                "SPADE is designed to eliminate slow consensus compromises and top-down executive surprises [^1].\n\n"
                "### The 5 SPADE Steps:\n"
                "1. **Setting:** Clear problem context and timeline.\n"
                "2. **People:** Exactly ONE Decider (Responsible), plus Consulted, Approver, and Informed.\n"
                "3. **Alternatives:** Brainstorm 3+ real, viable alternatives with pros/cons.\n"
                "4. **Decide:** The single decider makes the call with clear rationale.\n"
                "5. **Explain:** Communicate the decision. All stakeholders agree to **Disagree and Commit** [^1].\n\n"
                "I can generate an interactive SPADE Decision Matrix artifact for your next team decision!"
            )
        else:
            response_text = (
                f"Based on the knowledge base from Lenny's Podcast transcripts regarding your question:\n\n"
                f"Top tech operators emphasize systematic execution, continuous user discovery, and rigorous prioritization [^1]. "
                f"Whether building product loops, scaling B2B PLG motions, or executing founder-led reviews, the consistent pattern across 100+ guests is obsessive focus on user value and retention.\n\n"
                f"Feel free to ask about specific operator playbooks from **Brian Chesky** (Founder Mode), **Elena Verna** (B2B PLG Loops), **Shreyas Doshi** (LNO Framework), **Gokul Rajaram** (SPADE Decisions), **Casey Winters** (Retention Curves), or **Claire Vo** (AI PM Workflows)!"
            )

        # Simulate streaming token by token
        words = response_text.split(" ")
        for i, word in enumerate(words):
            yield LLMStreamChunk(token=word + (" " if i < len(words) - 1 else ""), is_finished=False, model_used=self.model_name)
            await asyncio.sleep(0.01)

        yield LLMStreamChunk(token="", is_finished=True, model_used=self.model_name)

    def _generate_ship30_essay(self, query: str) -> str:
        return (
            "Here is the Ship 30 for 30 Atomic Essay grounded in Lenny's Podcast transcripts:\n\n"
            "```markdown\n"
            "# Why Traditional Product Management Is Dying (And What Replaces It)\n\n"
            "Most tech companies are running a 20-year-old playbook that is quietly destroying their product quality.\n\n"
            "They hire legions of project coordinators disguised as product managers.\n\n"
            "Here is the brutal truth: if your PMs spend all week moving Jira tickets between columns, you are operating in Manager Mode—and your best talent is already looking for the exit.\n\n"
            "---\n\n"
            "### The 3 Shifts of Founder Mode Product Management\n\n"
            "According to Brian Chesky and top Silicon Valley operators, the era of siloed, bureaucratic product management is over. Here is the modern operating system:\n\n"
            "#### 1. Combine Product Management with Product Marketing\n"
            "When PMs don't have to sell what they build, they build bloated features nobody wants.\n\n"
            "At Airbnb, PMs were merged with PMMs. Every product builder must also be a world-class storyteller who can explain the value proposition in 10 seconds.\n\n"
            "#### 2. Run Synchronized Seasonal Releases\n"
            "Continuous micro-shipping creates customer fatigue and zero marketing impact.\n\n"
            "- Bundle 15-20 features into a major Winter and Summer release.\n"
            "- Align marketing, sales, support, and engineering behind one single narrative.\n"
            "- Force the organization to think in integrated systems rather than fragmented widgets.\n\n"
            "#### 3. Protect Calendar Space for Leverage Tasks (The LNO Rule)\n"
            "As Shreyas Doshi teaches, not all tasks are created equal.\n\n"
            "- **Leverage (10x):** Roadmap strategy and customer conviction.\n"
            "- **Neutral (1x):** Sprint standups and status docs (do these at 80% effort).\n"
            "- **Overhead (0x):** Bureaucracy (delegate or automate).\n\n"
            "---\n\n"
            "### The 1 Actionable Takeaway Today\n\n"
            "Audit your product backlog this afternoon. Delete every feature that cannot be explained in a 3-sentence customer benefit memo. If you can't sell it simply, you shouldn't build it.\n"
            "```\n\n"
            "<artifact title=\"Ship 30 Essay: Modern Product Management\" type=\"markdown\" language=\"markdown\">\n"
            "# Why Traditional Product Management Is Dying (And What Replaces It)\n\n"
            "Most tech companies are running a 20-year-old playbook that is quietly destroying their product quality.\n\n"
            "They hire legions of project coordinators disguised as product managers.\n\n"
            "Here is the brutal truth: if your PMs spend all week moving Jira tickets between columns, you are operating in Manager Mode—and your best talent is already looking for the exit.\n\n"
            "---\n\n"
            "### The 3 Shifts of Founder Mode Product Management\n\n"
            "According to Brian Chesky and top Silicon Valley operators, the era of siloed, bureaucratic product management is over. Here is the modern operating system:\n\n"
            "#### 1. Combine Product Management with Product Marketing\n"
            "When PMs don't have to sell what they build, they build bloated features nobody wants.\n\n"
            "At Airbnb, PMs were merged with PMMs. Every product builder must also be a world-class storyteller who can explain the value proposition in 10 seconds.\n\n"
            "#### 2. Run Synchronized Seasonal Releases\n"
            "Continuous micro-shipping creates customer fatigue and zero marketing impact.\n\n"
            "- Bundle 15-20 features into a major Winter and Summer release.\n"
            "- Align marketing, sales, support, and engineering behind one single narrative.\n"
            "- Force the organization to think in integrated systems rather than fragmented widgets.\n\n"
            "#### 3. Protect Calendar Space for Leverage Tasks (The LNO Rule)\n"
            "As Shreyas Doshi teaches, not all tasks are created equal.\n\n"
            "- **Leverage (10x):** Roadmap strategy and customer conviction.\n"
            "- **Neutral (1x):** Sprint standups and status docs (do these at 80% effort).\n"
            "- **Overhead (0x):** Bureaucracy (delegate or automate).\n\n"
            "---\n\n"
            "### The 1 Actionable Takeaway Today\n\n"
            "Audit your product backlog this afternoon. Delete every feature that cannot be explained in a 3-sentence customer benefit memo. If you can't sell it simply, you shouldn't build it.\n"
            "</artifact>"
        )

    def _generate_interactive_artifact(self, query: str) -> str:
        return (
            "I have created an interactive **SPADE Decision Matrix Calculator** artifact based on Gokul Rajaram's framework from Lenny's Podcast. You can test and interact with it in the side panel.\n\n"
            "<artifact title=\"Interactive SPADE Decision Matrix\" type=\"html\" language=\"html\">\n"
            "<!DOCTYPE html>\n"
            "<html lang=\"en\">\n"
            "<head>\n"
            "  <meta charset=\"UTF-8\" />\n"
            "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />\n"
            "  <title>SPADE Decision Matrix</title>\n"
            "  <script src=\"https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4\"></script>\n"
            "  <style>\n"
            "    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }\n"
            "  </style>\n"
            "</head>\n"
            "<body class=\"bg-slate-900 text-slate-100 min-h-screen p-6 flex flex-col justify-center items-center\">\n"
            "  <div class=\"max-w-xl w-full bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-2xl\">\n"
            "    <div class=\"flex items-center justify-between pb-4 border-b border-slate-700\">\n"
            "      <div>\n"
            "        <h1 class=\"text-xl font-bold text-indigo-400\">SPADE Decision Matrix</h1>\n"
            "        <p class=\"text-xs text-slate-400 mt-1\">Gokul Rajaram Framework for High-Stakes PM Decisions</p>\n"
            "      </div>\n"
            "      <span class=\"px-2.5 py-1 bg-indigo-500/20 text-indigo-300 text-xs font-semibold rounded-full\">Interactive Tool</span>\n"
            "    </div>\n"
            "    \n"
            "    <div class=\"mt-4 space-y-3\">\n"
            "      <div>\n"
            "        <label class=\"text-xs font-semibold text-slate-300\">Decision Setting & Title</label>\n"
            "        <input id=\"setting\" type=\"text\" value=\"Switch from Monthly to Usage-Based Pricing\" class=\"w-full mt-1 bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500\" />\n"
            "      </div>\n"
            "      \n"
            "      <div class=\"grid grid-cols-2 gap-3\">\n"
            "        <div>\n"
            "          <label class=\"text-xs font-semibold text-slate-300\">Single Decider (Responsible)</label>\n"
            "          <input id=\"decider\" type=\"text\" value=\"Head of Product\" class=\"w-full mt-1 bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500\" />\n"
            "        </div>\n"
            "        <div>\n"
            "          <label class=\"text-xs font-semibold text-slate-300\">Executive Approver</label>\n"
            "          <input id=\"approver\" type=\"text\" value=\"CEO / Founder\" class=\"w-full mt-1 bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500\" />\n"
            "        </div>\n"
            "      </div>\n"
            "\n"
            "      <div>\n"
            "        <label class=\"text-xs font-semibold text-slate-300\">Alternatives Evaluated</label>\n"
            "        <div class=\"space-y-2 mt-1\">\n"
            "          <div class=\"flex items-center space-x-2\">\n"
            "            <input type=\"radio\" name=\"alt\" checked class=\"text-indigo-600 focus:ring-0\" />\n"
            "            <span class=\"text-xs text-slate-200\">Option A: Hybrid Usage + Seat Pricing (Recommended)</span>\n"
            "          </div>\n"
            "          <div class=\"flex items-center space-x-2\">\n"
            "            <input type=\"radio\" name=\"alt\" class=\"text-indigo-600 focus:ring-0\" />\n"
            "            <span class=\"text-xs text-slate-200\">Option B: Pure Consumption Pay-as-you-go</span>\n"
            "          </div>\n"
            "          <div class=\"flex items-center space-x-2\">\n"
            "            <input type=\"radio\" name=\"alt\" class=\"text-indigo-600 focus:ring-0\" />\n"
            "            <span class=\"text-xs text-slate-200\">Option C: Flat Tiered Subscription</span>\n"
            "          </div>\n"
            "        </div>\n"
            "      </div>\n"
            "      \n"
            "      <button onclick=\"calculateCommitment()\" class=\"w-full mt-4 bg-indigo-600 hover:bg-indigo-500 text-white font-medium py-2 px-4 rounded-lg text-sm transition-colors duration-200 shadow-md\">\n"
            "        Generate Decision Memo (Disagree & Commit)\n"
            "      </button>\n"
            "      \n"
            "      <div id=\"result\" class=\"hidden mt-4 p-3 bg-indigo-950/60 border border-indigo-500/40 rounded-lg text-xs text-indigo-200\">\n"
            "        <p class=\"font-bold\">Decision Recorded:</p>\n"
            "        <p class=\"mt-1\">Option A selected by <span id=\"outDecider\" class=\"text-white font-semibold\">Head of Product</span>. All stakeholders have completed consultation and are committed to execution.</p>\n"
            "      </div>\n"
            "    </div>\n"
            "  </div>\n"
            "  <script>\n"
            "    function calculateCommitment() {\n"
            "      const dec = document.getElementById('decider').value;\n"
            "      document.getElementById('outDecider').innerText = dec;\n"
            "      document.getElementById('result').classList.remove('hidden');\n"
            "    }\n"
            "  </script>\n"
            "</body>\n"
            "</html>\n"
            "</artifact>"
        )

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.2
    ) -> str:
        tokens = []
        async for chunk in self.stream_chat(messages, system_prompt, temperature):
            if chunk.token:
                tokens.append(chunk.token)
        return "".join(tokens)
