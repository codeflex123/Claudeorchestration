# 🧪 Claude Orchestration: Manual QA Test Prompts

Use these prompts to verify the Orchestration Layer's intent classification, strategy generation, and environment routing.

---

### 🟢 1. Simple / Direct Response (Target: Claude AI)
*Test if the system identifies basic queries that don't require complex planning.*

- "What is the capital of France?"
- "Explain the concept of photosynthesis in two sentences."
- "What time is it in Tokyo right now?"
- "Give me a quick recipe for scrambled eggs."

---

### 🔵 2. Complex Research & Strategy (Target: Claude Cowork)
*Test if the system generates a multi-step plan for business and research tasks.*

- "Help me create a Go-To-Market strategy for a new gym based in Mumbai and send it to my email."
- "Research the top 5 emerging trends in sustainable fashion for 2026 and draft a brief report."
- "I want to launch a podcast about AI. Give me a 4-week launch plan including equipment and marketing."
- "Analyze the current state of the Indian stock market and suggest a portfolio diversification strategy."

---

### 🔴 3. Engineering & Coding (Target: Claude Code)
*Test if the system identifies technical tasks requiring terminal/file access.*

- "Fix the bug in my Python script that is causing a memory leak during data processing."
- "Initialize a new Next.js project with Tailwind CSS and set up a basic authentication flow."
- "Refactor the backend API to use asynchronous database calls and add unit tests."
- "Migrate my existing project from JavaScript to TypeScript and fix all type errors."

---

### 🟠 4. Mixed / Edge Cases (Target: Ambiguous)
*Test how the system handles variety and ambiguity.*

- "Compare the performance of Python and Go for high-concurrency backend services."
- "help me write a blog post about fitness then research some images for it"
- "I need to deploy my app to Vercel but first I need a README."
- "What should I do today? (Note: See if it asks clarifying questions or gives a generic plan)."

---

### 🛠️ How to Test:
1. Copy a prompt from above.
2. Paste it into the **Claude Orchestration Home** screen.
3. Review the **Strategy Artifact**:
    - Does the **Intent** match (Simple vs Complex)?
    - Is the **Execution Plan** logical?
    - Is the **Recommended Environment** correct?
4. Click **"Proceed"** and verify the simulation view matches the recommendation.
