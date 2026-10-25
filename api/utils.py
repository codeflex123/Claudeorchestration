import re
import json
from typing import Dict, Any, List

class SemanticAnalyzer:
    def __init__(self, prompt: str):
        self.raw_prompt = prompt.strip()
        self.clean_prompt = prompt.strip()
        self.lower = self.clean_prompt.lower()

    @staticmethod
    def extract_json(text: str) -> Dict[str, Any]:
        """Robustly extracts JSON from an LLM response string."""
        if not text:
            raise ValueError("Empty response received")
            
        text = text.strip()
        
        # 1. Match ```json ... ``` or ``` ... ```
        block_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text, re.IGNORECASE)
        if block_match:
            candidate = block_match.group(1).strip()
            try:
                return json.loads(candidate)
            except Exception:
                pass
        
        # 2. Match outermost { ... }
        brace_match = re.search(r'(\{[\s\S]*\})', text)
        if brace_match:
            candidate = brace_match.group(1).strip()
            try:
                return json.loads(candidate)
            except Exception:
                pass
        
        # 3. Direct parse
        return json.loads(text)

    def analyze_intent(self) -> Dict[str, Any]:
        p = self.lower
        words = p.split()
        word_count = len(words)

        # 1. Coding & Technical Indicators (Target: Claude Code)
        code_keywords = [
            "file", "files", "bug", "bugs", "debug", "debugging", "fix", "code", "coding", 
            "script", "scripts", "function", "functions", "refactor", "arrange", "terminal", 
            "git", "github", "repo", "repository", "compile", "compiler", "syntax", "error", 
            "traceback", "exception", "unit test", "test", "tests", "python", "javascript", 
            "typescript", "react", "next.js", "nextjs", "fastapi", "html", "css", "sql", 
            "database", "api", "endpoint", "npm", "pip", "docker", "deploy", "build", 
            "leak", "memory", "variable", "class", "loop", "regex", "json", "yaml", "xml",
            "sh", "bash", "cli", "pull request", "commit", "merge", "branch", "patch", "lint"
        ]
        
        # 2. Cowork & Strategy & Multi-step Indicators (Target: Claude Cowork)
        cowork_keywords = [
            "strategy", "gtm", "go-to-market", "market", "marketing", "business", 
            "business plan", "plan", "roadmap", "launch", "campaign", "pitch", 
            "proposal", "research", "competitor", "competitive", "budget", "finance", 
            "financial", "investment", "portfolio", "podcast", "cowork", "collaborate", 
            "collaborative", "workflow", "multi-step", "trend", "trends", "report",
            "presentation", "slides", "survey", "schedule", "quarterly", "audience"
        ]

        # 3. Simple & Direct AI Starters (Target: Claude AI)
        simple_starters = [
            "what is", "what are", "who is", "who was", "where is", "when did", 
            "why is", "why do", "how do i", "how to", "explain", "define", "summarize",
            "translate", "tell me about", "give me a recipe", "recipe", "greeting", 
            "hello", "hi", "hey"
        ]

        # Calculate keyword signal strength
        code_score = 0
        for kw in code_keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', p):
                code_score += 2

        cowork_score = 0
        for kw in cowork_keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', p):
                cowork_score += 2

        is_simple_starter = any(p.startswith(s) for s in simple_starters)

        # Classification decision hierarchy
        if code_score > cowork_score and code_score >= 2:
            env = "Claude Code"
            intent = "COMPLEX"
            confidence = min(0.88 + (code_score * 0.02), 0.98)
            reason = f"Detected engineering and technical task ({code_score} code signals) requiring code/terminal workspace."
        elif cowork_score > code_score and cowork_score >= 2:
            env = "Claude Cowork"
            intent = "COMPLEX"
            confidence = min(0.88 + (cowork_score * 0.02), 0.98)
            reason = f"Detected strategic, research, or multi-step business workflow ({cowork_score} strategy signals) requiring collaborative workspace."
        elif is_simple_starter and word_count < 25:
            env = "Claude AI"
            intent = "SIMPLE"
            confidence = 0.94
            reason = "Direct conceptual inquiry or conversational question suitable for direct response in Claude AI."
        elif word_count > 18:
            env = "Claude Cowork"
            intent = "COMPLEX"
            confidence = 0.88
            reason = "Extended multi-part prompt requiring structured coordination in Claude Cowork."
        else:
            env = "Claude AI"
            intent = "SIMPLE"
            confidence = 0.90
            reason = "Standard inquiry well-suited for direct Claude AI response."

        return {
            "intent": intent,
            "confidence": round(confidence, 2),
            "recommended_environment": env,
            "reasoning": reason,
            "code_score": code_score,
            "cowork_score": cowork_score
        }

    def generate_tailored_plan(self) -> Dict[str, Any]:
        """Generates dynamic, rich steps and tools based on the prompt semantics."""
        analysis = self.analyze_intent()
        env = analysis["recommended_environment"]
        p = self.raw_prompt

        # Determine tools and steps based on environment & prompt content
        if env == "Claude Code":
            mcp_tools = ["terminal", "github"]
            model = "Claude 3.7 Sonnet"
            eta = 25
            steps = [
                {
                    "title": "Codebase & File Inspection",
                    "description": f"Scan directory structure and parse syntax related to: '{p[:70]}'.",
                    "estimated_minutes": 5
                },
                {
                    "title": "Static Analysis & Bug Detection",
                    "description": "Trace logical flaws, unhandled exceptions, and anti-patterns across relevant modules.",
                    "estimated_minutes": 8
                },
                {
                    "title": "Refactoring & Arrangement",
                    "description": "Reorganize code modules, patch identified bugs, and maintain backward compatibility.",
                    "estimated_minutes": 7
                },
                {
                    "title": "Verification & Test Execution",
                    "description": "Execute local test runner via terminal to confirm fix integrity and performance.",
                    "estimated_minutes": 5
                }
            ]
        elif env == "Claude Cowork":
            mcp_tools = ["browser", "google-drive"]
            if any(term in self.lower for term in ["mail", "email", "gmail", "inbox"]):
                mcp_tools.append("gmail")
            model = "Claude 3.5 Sonnet"
            eta = 60
            steps = [
                {
                    "title": "Discovery & Context Gathering",
                    "description": f"Compile domain research, market benchmarks, and relevant background for: '{p[:70]}'.",
                    "estimated_minutes": 15
                },
                {
                    "title": "Strategic Architecture & Modeling",
                    "description": "Structure multi-phased roadmap, target persona breakdown, and operational milestones.",
                    "estimated_minutes": 25
                },
                {
                    "title": "Deliverable Synthesis & Review",
                    "description": "Draft executive deliverable, validate actionable steps, and prepare handoff assets.",
                    "estimated_minutes": 20
                }
            ]
        else:
            mcp_tools = []
            if any(term in self.lower for term in ["search", "latest", "news", "current", "price", "rate"]):
                mcp_tools.append("browser")
            model = "Claude 3.5 Haiku"
            eta = 2
            steps = [
                {
                    "title": "Direct Query Analysis",
                    "description": f"Synthesize core answer and relevant examples for: '{p[:70]}'.",
                    "estimated_minutes": 1
                },
                {
                    "title": "Response Formulation",
                    "description": "Deliver structured, high-clarity output in Claude AI chat interface.",
                    "estimated_minutes": 1
                }
            ]

        return {
            "steps": steps,
            "estimated_total_time_mins": eta,
            "recommended_model": model,
            "recommended_environment": env,
            "reasoning": analysis["reasoning"],
            "mcp_required": mcp_tools,
            "confidence": analysis["confidence"],
            "intent": analysis["intent"]
        }


class InputAnalyzer:
    def __init__(self, prompt: str):
        self.prompt = prompt.strip()
        self.semantic = SemanticAnalyzer(self.prompt)

    def sanitize(self) -> str:
        """Standardizes the input prompt by stripping whitespace."""
        return self.prompt

    def analyze(self) -> dict:
        """Analyzes the input prompt and returns metadata."""
        intent_info = self.semantic.analyze_intent()
        return {
            "original_length": len(self.prompt),
            "word_count": len(self.prompt.split()),
            "is_url": bool(re.match(r'https?://[^\s]+', self.prompt)),
            "sanitized_prompt": self.prompt,
            "intent_info": intent_info
        }
