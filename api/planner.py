import os
import json
from pydantic import BaseModel
from typing import List, Literal, Optional
from anthropic import AsyncAnthropic
from groq import AsyncGroq
import google.generativeai as genai

try:
    from .classifier import Provider
    from .mcp import mcp_registry, MCPTool
    from .utils import SemanticAnalyzer
except ImportError:
    from classifier import Provider
    from mcp import mcp_registry, MCPTool
    from utils import SemanticAnalyzer

class TaskStep(BaseModel):
    title: str
    description: str
    estimated_minutes: int

class PlanningStrategy(BaseModel):
    steps: List[TaskStep]
    estimated_total_time_mins: int
    recommended_model: str
    recommended_environment: Literal["Claude AI", "Claude Cowork", "Claude Code"]
    reasoning: str
    mcp_required: List[MCPTool]

class Planner:
    def __init__(self):
        self._groq_key = os.getenv("GROQ_API_KEY", "").strip().strip("\"'")
        self._gemini_key = os.getenv("GEMINI_API_KEY", "").strip().strip("\"'")
        self._anthropic_key = os.getenv("ANTHROPIC_API_KEY", "").strip().strip("\"'")

    def _normalize_environment(self, env_str: str, baseline_env: str) -> Literal["Claude AI", "Claude Cowork", "Claude Code"]:
        env_lower = (env_str or "").lower()
        if "code" in env_lower or "terminal" in env_lower or "developer" in env_lower:
            return "Claude Code"
        if "cowork" in env_lower or "collaborat" in env_lower or "workspace" in env_lower:
            return "Claude Cowork"
        if "ai" in env_lower or "chat" in env_lower or "direct" in env_lower:
            return "Claude AI"
        return baseline_env if baseline_env in ["Claude AI", "Claude Cowork", "Claude Code"] else "Claude AI"

    async def generate_plan(self, prompt: str) -> PlanningStrategy:
        semantic = SemanticAnalyzer(prompt)
        base = semantic.generate_tailored_plan()

        system_prompt = """
        You are the "Strategist" for an AI Orchestration Layer.
        Analyze the user's prompt and generate a concrete step-by-step execution plan.
        
        MANDATORY ENVIRONMENT SELECTION RULES:
        1. "Claude Code": MUST be chosen for ANY technical engineering task, file inspection/arrangement, debugging, fixing bugs, programming, scripts, terminal commands, or git operations.
        2. "Claude Cowork": MUST be chosen for business strategy, Go-To-Market (GTM) plans, multi-step market research, collaborative product roadmaps, or structured proposals.
        3. "Claude AI": MUST be chosen for simple direct questions, quick Q&A, conceptual explanations, or short conversational writing.

        Available MCP connectors: github, gmail, google-drive, terminal, browser, slack.
        - For Claude Code tasks: authorize "terminal" and "github".
        - For email tasks: authorize "gmail".
        - For research tasks: authorize "browser".

        Respond ONLY in valid JSON format:
        {
            "steps": [
                {"title": "Step Title", "description": "Detailed action description", "estimated_minutes": 10}
            ],
            "estimated_total_time_mins": 30,
            "recommended_model": "Claude 3.7 Sonnet" or "Claude 3.5 Sonnet" or "Claude 3.5 Haiku",
            "recommended_environment": "Claude Code" or "Claude Cowork" or "Claude AI",
            "reasoning": "Concise reasoning for the chosen environment and strategy",
            "mcp_required": ["terminal", "github"]
        }
        """

        raw_plan = None

        # 1. Try Groq
        if self._groq_key:
            try:
                client = AsyncGroq(api_key=self._groq_key)
                try:
                    response = await client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": prompt}
                        ],
                        response_format={"type": "json_object"}
                    )
                except Exception:
                    response = await client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": prompt}
                        ],
                        response_format={"type": "json_object"}
                    )
                raw_plan = SemanticAnalyzer.extract_json(response.choices[0].message.content)
            except Exception as e:
                print(f"[Planner] Groq plan generation failed: {e}")

        # 2. Try Gemini if Groq didn't succeed
        if not raw_plan and self._gemini_key:
            try:
                genai.configure(api_key=self._gemini_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                full_prompt = f"{system_prompt}\n\nUser Prompt: {prompt}"
                response = await model.generate_content_async(full_prompt)
                raw_plan = SemanticAnalyzer.extract_json(response.text)
            except Exception as e:
                print(f"[Planner] Gemini plan generation failed: {e}")

        # 3. Try Anthropic if neither succeeded
        if not raw_plan and self._anthropic_key:
            try:
                client = AsyncAnthropic(api_key=self._anthropic_key)
                response = await client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=1000,
                    system=system_prompt,
                    messages=[{"role": "user", "content": prompt}]
                )
                raw_plan = SemanticAnalyzer.extract_json(response.content[0].text)
            except Exception as e:
                print(f"[Planner] Anthropic plan generation failed: {e}")

        # If LLM returned a valid structure, format and validate it
        if raw_plan and isinstance(raw_plan, dict):
            try:
                env_candidate = raw_plan.get("recommended_environment", "")
                target_env = self._normalize_environment(env_candidate, base["recommended_environment"])
                
                # Check semantic alignment: if baseline strongly indicates Claude Code, respect it
                if base["recommended_environment"] == "Claude Code" and target_env != "Claude Code":
                    target_env = "Claude Code"

                # Parse steps safely
                steps_data = raw_plan.get("steps", [])
                valid_steps = []
                if isinstance(steps_data, list) and len(steps_data) > 0:
                    for s in steps_data:
                        if isinstance(s, dict) and "title" in s:
                            valid_steps.append(TaskStep(
                                title=str(s.get("title", "Task Execution")),
                                description=str(s.get("description", "Execute task component.")),
                                estimated_minutes=int(s.get("estimated_minutes", 10))
                            ))
                if not valid_steps:
                    valid_steps = [TaskStep(**s) for s in base["steps"]]

                # Calculate or validate ETA
                eta = raw_plan.get("estimated_total_time_mins")
                if not isinstance(eta, int) or eta <= 0:
                    eta = sum(s.estimated_minutes for s in valid_steps)

                # Tools enrichment
                raw_tools = raw_plan.get("mcp_required", [])
                if not isinstance(raw_tools, list):
                    raw_tools = []
                
                # Ensure appropriate tools based on environment
                if target_env == "Claude Code":
                    if "terminal" not in raw_tools:
                        raw_tools.append("terminal")
                    if "github" not in raw_tools:
                        raw_tools.append("github")
                elif target_env == "Claude Cowork":
                    if any(term in prompt.lower() for term in ["email", "mail", "gmail"]):
                        if "gmail" not in raw_tools:
                            raw_tools.append("gmail")

                enriched_mcp = mcp_registry.get_tool_metadata(raw_tools)

                model_choice = raw_plan.get("recommended_model", base["recommended_model"])

                return PlanningStrategy(
                    steps=valid_steps,
                    estimated_total_time_mins=eta,
                    recommended_model=model_choice,
                    recommended_environment=target_env,
                    reasoning=raw_plan.get("reasoning", base["reasoning"]),
                    mcp_required=enriched_mcp
                )
            except Exception as e:
                print(f"[Planner] Error formatting LLM plan: {e}")

        # Fallback to high-fidelity Semantic Plan (Dynamic, tailored to user prompt)
        enriched_mcp = mcp_registry.get_tool_metadata(base["mcp_required"])
        return PlanningStrategy(
            steps=[TaskStep(**s) for s in base["steps"]],
            estimated_total_time_mins=base["estimated_total_time_mins"],
            recommended_model=base["recommended_model"],
            recommended_environment=base["recommended_environment"],
            reasoning=base["reasoning"],
            mcp_required=enriched_mcp
        )
