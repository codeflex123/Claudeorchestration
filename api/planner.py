import os
import json
from pydantic import BaseModel
from typing import List, Literal, Optional
from anthropic import AsyncAnthropic
from groq import AsyncGroq
import google.generativeai as genai
from .classifier import Provider
from .mcp import mcp_registry, MCPTool

class TaskStep(BaseModel):
    title: str
    description: str
    estimated_minutes: int

class PlanningStrategy(BaseModel):
    steps: List[TaskStep]
    estimated_total_time_mins: int
    recommended_model: str
    recommended_environment: Literal["Claude AI", "Claude Cowork", "Claude Code"] # Added for Phase 5 UI
    reasoning: str
    mcp_required: List[MCPTool]

class Planner:
    def __init__(self):
        self.provider = self._determine_provider()
        self._init_client()

    def _determine_provider(self) -> Provider:
        if os.getenv("GROQ_API_KEY"):
            return Provider.GROQ
        if os.getenv("GEMINI_API_KEY"):
            return Provider.GEMINI
        if os.getenv("ANTHROPIC_API_KEY"):
            return Provider.ANTHROPIC
        raise ValueError("No API key found for Anthropic, Groq, or Gemini.")

    def _init_client(self):
        if self.provider == Provider.ANTHROPIC:
            self.client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        elif self.provider == Provider.GROQ:
            self.client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
        elif self.provider == Provider.GEMINI:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.client = genai.GenerativeModel('gemini-1.5-flash')

    async def generate_plan(self, prompt: str) -> PlanningStrategy:
        system_prompt = """
        You are the "Strategist" for an AI Orchestration Layer.
        Analyze the user's complex prompt and generate a step-by-step execution plan.
        
        Provide:
        1. A list of logical steps (title, description, estimated time).
        2. Total estimated time to completion.
        3. Recommended Claude model (Claude 3.5 Sonnet for general engineering/coding, Claude 3 Opus for deep research/reasoning).
        4. Reasoning for the model choice.
        5. Any potential MCP (Model Context Protocol) connectors required. Available examples: github, gmail, google-drive, terminal, browser, slack. Use 'gmail' specifically for email-related tasks.
        
        Respond ONLY in JSON format:
        {
            "steps": [{"title": "...", "description": "...", "estimated_minutes": 5}],
            "estimated_total_time_mins": 30,
            "recommended_model": "Claude 3.5 Sonnet",
            "reasoning": "...",
            "mcp_required": ["github", "gmail", "terminal"]
        }
        """

        try:
            if self.provider == Provider.ANTHROPIC:
                response = await self.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=1000,
                    system=system_prompt,
                    messages=[{"role": "user", "content": prompt}]
                )
                data = json.loads(response.content[0].text)
            
            elif self.provider == Provider.GROQ:
                response = await self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"}
                )
                data = json.loads(response.choices[0].message.content)
            
            elif self.provider == Provider.GEMINI:
                full_prompt = f"{system_prompt}\n\nUser Prompt: {prompt}"
                response = await self.client.generate_content_async(full_prompt)
                text = response.text.strip()
                if text.startswith("```json"):
                    text = text[7:-3]
                data = json.loads(text)

            # Step 3: Enrich MCP data (Phase 3)
            raw_mcp = data.get("mcp_required", [])
            data["mcp_required"] = mcp_registry.get_tool_metadata(raw_mcp)

            # Step 4: Determine environment (Wireframe Alignment)
            if "terminal" in raw_mcp or "github" in raw_mcp:
                data["recommended_environment"] = "Claude Code"
            elif len(data.get("steps", [])) > 3:
                data["recommended_environment"] = "Claude Cowork"
            else:
                data["recommended_environment"] = "Claude AI"

            return PlanningStrategy(**data)
        except Exception as e:
            # Fallback strategy
            return PlanningStrategy(
                steps=[{"title": "Initial Analysis", "description": "Analyzing the task for execution.", "estimated_minutes": 5}],
                estimated_total_time_mins=5,
                recommended_model="Claude 3.5 Sonnet",
                recommended_environment="Claude AI",
                reasoning=f"Engine fallback due to error: {str(e)}",
                mcp_required=[]
            )
