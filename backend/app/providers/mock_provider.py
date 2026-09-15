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

        elif (
            "artifact" in user_lower
            or "calculator" in user_lower
            or "html" in user_lower
            or "matrix" in user_lower
            or "widget" in user_lower
        ):
            response_text = self._generate_interactive_artifact(user_lower)

        elif "chesky" in user_lower or "founder mode" in user_lower:
            response_text = (
                "According to Brian Chesky in the episode "
                "*Founder Mode & Reimagining Product Management at Airbnb*, "
                "tech companies often fail when they blindly switch to "
                "**Manager Mode** as they scale [^1].\n\n"

                "### Core Principles of Founder Mode at Airbnb:\n"

                "1. **Single Integrated Roadmap:** Rather than splintering "
                "into 50 autonomous business units with conflicting roadmaps, "
                "the entire company operates on one unified product roadmap "
                "reviewed directly by leadership.\n"

                "2. **Merging PM and PMM:** Traditional PMs had devolved into "
                "bureaucratic project managers writing Jira tickets. Airbnb "
                "merged Product Management with Product Marketing into a "
                "single PMM role responsible for both building and storytelling [^1].\n"

                "3. **Synchronized Major Releases:** Airbnb shifted to two "
                "massive synchronized seasonal releases per year "
                "(Summer & Winter releases) to coordinate marketing, "
                "engineering, and customer attention.\n\n"

                "> *\"Founder Mode is not micromanagement; it is deep, "
                "obsessive involvement in the details that matter. Great PMs "
                "have extreme taste and deep empathy for users.\"* — Brian Chesky [^1]"
            )

        elif "elena" in user_lower or "plg" in user_lower or "growth loop" in user_lower:
            response_text = (
                "Based on Elena Verna's frameworks in "
                "*B2B Product-Led Growth (PLG) & Growth Loops*, "
                "PLG is not simply adding a freemium tier—it is an "
                "organizational operating model [^1].\n\n"

                "### Elena Verna's Core B2B Growth Pillars:\n"

                "- **Time-to-Value (TTV):** The end-user must experience "
                "the core 'aha moment' within 3 minutes of signing up "
                "without human friction.\n"

                "- **Product Qualified Leads (PQLs):** Sales shouldn't do "
                "cold outbound; instead, sales reaches out to accounts that "
                "already have 10-20 active users on the free tier to sell "
                "enterprise SSO, security, and governance [^1].\n"

                "- **Activation Rate Priority:** Elena emphasizes getting "
                "user activation to 40-50% before optimizing monetization, "
                "warning that monetizing a leaky bucket burns brand equity.\n\n"

                "Would you like me to convert this into a "
                "**Ship 30 for 30 Atomic Essay** or generate an "
                "**Interactive PLG Funnel Calculator**?"
            )

        elif "shreyas" in user_lower or "lno" in user_lower:
            response_text = (
                "In *Good PM vs Great PM & The LNO Framework*, "
                "Shreyas Doshi breaks down how top operators manage "
                "their cognitive capacity [^1].\n\n"

                "### The LNO Framework:\n"

                "1. **L (Leverage Tasks):** 10x-100x impact work "
                "(e.g. strategic roadmap, critical hiring, breakthrough "
                "PM specs). Invest 100% effort and aim for perfection.\n"

                "2. **N (Neutral Tasks):** Necessary work where 10x effort "
                "yields 0 extra value (e.g. sprint planning, status updates). "
                "Execute at 80% quality with minimal time.\n"

                "3. **O (Overhead Tasks):** Administrative chores "
                "(e.g. routine expense reports, corporate surveys). "
                "Batch them at the end of the day or delegate immediately.\n\n"

                "Shreyas notes that Great PMs distinguish themselves not "
                "by shipping on time, but through **high agency and outcome orientation** [^1]."
            )

        elif "spade" in user_lower or "gokul" in user_lower:
            response_text = (
                "According to Gokul Rajaram in "
                "*SPADE Framework for High-Stakes Decision Making*, "
                "SPADE is designed to eliminate slow consensus compromises "
                "and top-down executive surprises [^1].\n\n"

                "### The 5 SPADE Steps:\n"

                "1. **Setting:** Clear problem context and timeline.\n"
                "2. **People:** Exactly ONE Decider (Responsible), plus "
                "Consulted, Approver, and Informed.\n"
                "3. **Alternatives:** Brainstorm 3+ real, viable alternatives "
                "with pros/cons.\n"
                "4. **Decide:** The single decider makes the call with clear rationale.\n"
                "5. **Explain:** Communicate the decision. All stakeholders "
                "agree to **Disagree and Commit** [^1].\n\n"

                "I can generate an interactive SPADE Decision Matrix artifact "
                "for your next team decision!"
            )

        else:
            response_text = (
                "Based on the knowledge base from Lenny's Podcast transcripts "
                "regarding your question:\n\n"

                "Top tech operators emphasize systematic execution, continuous "
                "user discovery, and rigorous prioritization [^1]. Whether "
                "building product loops, scaling B2B PLG motions, or executing "
                "founder-led reviews, the consistent pattern across 100+ guests "
                "is obsessive focus on user value and retention.\n\n"

                "Feel free to ask about specific operator playbooks from "
                "**Brian Chesky** (Founder Mode), **Elena Verna** "
                "(B2B PLG Loops), **Shreyas Doshi** (LNO Framework), "
                "**Gokul Rajaram** (SPADE Decisions), **Casey Winters** "
                "(Retention Curves), or **Claire Vo** (AI PM Workflows)!"
            )

        # Simulate streaming token by token
        words = response_text.split(" ")

        for i, word in enumerate(words):
            yield LLMStreamChunk(
                token=word + (" " if i < len(words) - 1 else ""),
                is_finished=False,
                model_used=self.model_name
            )
            await asyncio.sleep(0.01)

        yield LLMStreamChunk(
            token="",
            is_finished=True,
            model_used=self.model_name
        )

    def _generate_ship30_essay(self, query: str) -> str:
        essay = """# Founder Mode: Stop Managing the Work and Start Leading the Product

Most product teams do not have a shortage of smart people.

They have a shortage of **clear ownership, strong product taste, and meaningful involvement from leaders**.

As companies grow, it is tempting to solve complexity by adding processes. More meetings. More layers. More roadmaps. More approvals. More people responsible for coordinating the people doing the actual work.

That can make a company look organized while quietly making the product worse.

Brian Chesky's discussion of Founder Mode offers a different way to think about scaling. The lesson is not that founders should personally control every decision. It is that leaders should remain deeply connected to the product, the customer, and the important decisions instead of disappearing behind layers of management.

That distinction matters for product managers too.

## The Problem With Manager Mode

When a company becomes larger, leaders naturally want to create systems that allow them to step away from details.

The intention is reasonable.

A founder cannot attend every meeting. A CEO cannot review every product decision. A product leader cannot personally manage every feature.

The danger appears when delegation turns into **distance**.

The people closest to the customer may know something important, but the information becomes filtered as it moves upward. A product manager reports to a product leader. The product leader reports to an executive. The executive sees a dashboard.

By the time the problem reaches the person who can make the biggest decision, the original customer problem may have disappeared behind metrics, presentations, and status updates.

Founder Mode challenges that pattern.

The answer is not micromanagement.

The answer is **high-quality involvement in the details that actually matter**.

## 1. Stay Close to the Product

A founder or senior product leader should understand what customers experience.

That does not mean reviewing every button, ticket, or line of code.

It means asking questions such as:

- What problem are we solving?
- Who experiences this problem?
- What does the customer see?
- Why are we making this decision?
- What evidence supports it?
- What happens if we are wrong?

These questions keep leadership connected to reality.

A product organization can have excellent dashboards and still misunderstand its customers. Metrics tell you what happened. Customer conversations, product usage, and direct observation help explain **why** it happened.

That is why product leaders need enough proximity to customers and the product to develop judgment.

## 2. Give Product People Real Ownership

One of the strongest implications of Founder Mode is that product people should not become simple project coordinators.

A product manager should not spend all of their energy asking whether a task moved from one column to another.

The more important responsibility is deciding **what should be built and why**.

That requires product judgment.

It requires understanding customer needs, identifying important problems, evaluating alternatives, communicating a clear direction, and making trade-offs.

The best product organizations therefore create ownership around outcomes rather than only around delivery.

Instead of saying:

> "The team shipped the feature."

Ask:

> "Did the feature solve the customer's problem?"

That small change in language can completely change how a team operates.

## 3. Combine Building With Explaining

A product idea is not valuable simply because it exists.

Customers need to understand why it matters.

This is one reason the relationship between product management and product marketing becomes important in the Founder Mode discussion.

The people building a product should have a strong understanding of the story behind it.

They should be able to explain:

- Who is this for?
- What problem does it solve?
- Why is this better?
- Why should someone care now?
- What is the simplest way to communicate the value?

When product teams understand both the product and its positioning, decisions can become more customer-oriented.

The goal is not to turn every PM into a professional marketer.

The goal is to make sure that **building and communicating value are connected**.

## 4. Focus on the Highest-Leverage Work

Shreyas Doshi's LNO framework provides another useful way to think about this.

Not every task deserves the same amount of attention.

Some work has extremely high leverage.

Other work is necessary but does not create additional value when you spend ten times more effort on it.

And some work is simply overhead.

The practical lesson is simple:

**Do not give every task equal importance.**

A product manager might spend an hour answering routine status questions and then discover that there was no time left for customer research or strategic product thinking.

That is backwards.

High-leverage work can include understanding an important customer problem, making a difficult product decision, defining strategy, improving the product experience, or helping the team understand the most important goal.

Low-leverage work should be simplified, delegated, automated, or completed efficiently.

The objective is not to work more hours.

It is to spend more attention on work that can change the outcome.

## 5. Reduce Organizational Distance

As organizations grow, communication becomes harder.

A leader may hear about a problem through several different people.

Every layer introduces the possibility of distortion.

This does not mean organizations should eliminate managers.

Managers are valuable.

The lesson is that hierarchy should not prevent important information from reaching the people who need to understand it.

Leaders should create opportunities to hear directly from teams and customers.

They should be willing to examine the details when a decision is important.

They should ask questions rather than simply accepting summaries.

This creates a culture where people care about the actual product rather than only about reporting that everything is on track.

## 6. Make Fewer, Better Decisions

Founder Mode is also connected to decision quality.

When too many people are expected to approve every decision, teams can become slow.

Everyone has a voice, but nobody has clear responsibility.

A better approach is to make ownership explicit.

Gokul Rajaram's SPADE framework is useful here.

First, define the **Setting**.

Then identify the **People** involved.

Next, establish the **Alternatives**.

Then the responsible **Decider** makes the decision.

Finally, **Explain** the decision to the people affected by it.

The important idea is that consultation does not have to mean consensus.

People can contribute information without becoming the person who makes the final call.

That creates both speed and accountability.

## What This Means for a Product Manager

You do not need to be a founder to operate in Founder Mode.

You can apply the principle to your own work.

Start by getting closer to the customer.

Do not rely only on reports. Read customer feedback. Watch users interact with the product. Understand the moments where customers become confused, frustrated, or delighted.

Then examine your calendar.

How much time goes toward high-leverage product thinking?

How much goes toward coordination?

How much goes toward administrative overhead?

Finally, look at your decisions.

Is ownership clear?

Are you collecting useful input before deciding?

Are you spending too much time trying to make everyone agree?

These questions can reveal where your operating system is slowing you down.

## The Bigger Lesson

The most important lesson from Founder Mode is not "founders should micromanage."

It is almost the opposite.

**Leadership should not become disconnected from the product simply because the company becomes larger.**

Scaling requires systems.

But systems should increase clarity rather than create distance.

Processes should help people make better decisions, not replace judgment.

Managers should create leverage, not create layers between customers and decision-makers.

Product managers should own outcomes, not simply coordinate tasks.

And executives should remain close enough to the product and customers to recognize when the organization is solving the wrong problem.

That is the real challenge of scaling.

You want the organization to become larger without allowing the product itself to become distant, bureaucratic, and disconnected from the people using it.

## One Action You Can Take Today

Open your calendar and your current product backlog.

Choose **one important product problem**.

Then ask three questions:

1. **What does the customer actually experience?**
2. **Why are we making our current decision?**
3. **Who has clear ownership of the final decision?**

If you cannot answer those questions quickly, do not immediately schedule another status meeting.

Go closer to the problem.

Talk to the customer.

Talk to the people building the product.

Look at the evidence.

Then make the decision with clear ownership.

That is a practical way to bring Founder Mode into everyday product work.

The goal is not to control everything.

The goal is to make sure that the important things never become somebody else's responsibility simply because the organization became bigger.

**Scale the company. Do not scale away the judgment.**
"""

        return (
            "Here is the Ship 30 for 30 Atomic Essay based on the grounded "
            "Lenny Podcast material:\n\n"
            + essay
            + "\n\n"
            "<artifact title=\"Ship 30 Essay: Founder Mode\" "
            "type=\"markdown\" language=\"markdown\">\n"
            + essay
            + "\n</artifact>"
        )

    def _generate_interactive_artifact(self, query: str) -> str:
        return (
            "I have created an interactive **SPADE Decision Matrix Calculator** "
            "artifact based on Gokul Rajaram's framework from Lenny's Podcast. "
            "You can test and interact with it in the side panel.\n\n"

            "<artifact title=\"Interactive SPADE Decision Matrix\" "
            "type=\"html\" language=\"html\">\n"

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

            "    <div class=\"mt-4 space-y-3\">\n"

            "      <div>\n"
            "        <label class=\"text-xs font-semibold text-slate-300\">Decision Setting & Title</label>\n"
            "        <input id=\"setting\" type=\"text\" value=\"Switch from Monthly to Usage-Based Pricing\" class=\"w-full mt-1 bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500\" />\n"
            "      </div>\n"

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

            "      <button onclick=\"calculateCommitment()\" class=\"w-full mt-4 bg-indigo-600 hover:bg-indigo-500 text-white font-medium py-2 px-4 rounded-lg text-sm transition-colors duration-200 shadow-md\">\n"
            "        Generate Decision Memo (Disagree & Commit)\n"
            "      </button>\n"

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

        async for chunk in self.stream_chat(
            messages,
            system_prompt,
            temperature
        ):
            if chunk.token:
                tokens.append(chunk.token)

        return "".join(tokens)