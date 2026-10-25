import os
import json
from enum import Enum
from pydantic import BaseModel
from typing import Literal, Optional
from anthropic import AsyncAnthropic
from groq import AsyncGroq
import google.generativeai as genai

try:
    from .utils import SemanticAnalyzer
except ImportError:
    from utils import SemanticAnalyzer

class ClassificationResult(BaseModel):
    intent: Literal["SIMPLE", "COMPLEX"]
    reasoning: str
    confidence: float
    recommended_environment: Optional[Literal["Claude AI", "Claude Cowork", "Claude Code"]] = None

class Provider(str, Enum):
    ANTHROPIC = "anthropic"
    GROQ = "groq"
    GEMINI = "gemini"
    LOCAL_SEMANTIC = "local_semantic"

class Classifier:
    def __init__(self):
        self._groq_key = os.getenv("GROQ_API_KEY", "").strip().strip("\"'")
        self._gemini_key = os.getenv("GEMINI_API_KEY", "").strip().strip("\"'")
        self._anthropic_key = os.getenv("ANTHROPIC_API_KEY", "").strip().strip("\"'")

    def _get_active_provider(self) -> Provider:
        if self._groq_key:
            return Provider.GROQ
        if self._gemini_key:
            return Provider.GEMINI
        if self._anthropic_key:
            return Provider.ANTHROPIC
        return Provider.LOCAL_SEMANTIC

    async def classify(self, prompt: str) -> ClassificationResult:
        # Pre-compute semantic baseline
        semantic = SemanticAnalyzer(prompt)
        base = semantic.analyze_intent()

        system_prompt = """
        You are the Intent Classifier for an AI Orchestration Layer.
        Analyze the user's prompt and evaluate:
        1. "intent": "SIMPLE" (for direct questions, casual queries, quick Q&A) or "COMPLEX" (for multi-step plans, coding, debugging, file handling, strategy, research).
        2. "confidence": float between 0.80 and 1.0.
        3. "recommended_environment": 
           - "Claude Code": For coding, bug fixing, script writing, terminal, file organization, git.
           - "Claude Cowork": For business plans, GTM strategies, market research, collaborative multi-step workflows.
           - "Claude AI": For direct explanations, conceptual Q&A, simple conversational queries.
        4. "reasoning": 1-2 concise sentences explaining the categorization.

        Respond ONLY with a valid JSON object matching this structure:
        {
            "intent": "SIMPLE" or "COMPLEX",
            "confidence": 0.95,
            "recommended_environment": "Claude Code" or "Claude Cowork" or "Claude AI",
            "reasoning": "..."
        }
        """

        # 1. Try Groq if key exists
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

                data = SemanticAnalyzer.extract_json(response.choices[0].message.content)
                intent = "SIMPLE" if data.get("intent", "").upper() == "SIMPLE" else "COMPLEX"
                confidence = float(data.get("confidence", base["confidence"]))
                if confidence <= 0.0 or confidence > 1.0:
                    confidence = base["confidence"]
                
                env = data.get("recommended_environment", base["recommended_environment"])
                if "code" in env.lower():
                    env = "Claude Code"
                elif "cowork" in env.lower():
                    env = "Claude Cowork"
                else:
                    env = "Claude AI"

                return ClassificationResult(
                    intent=intent,
                    reasoning=data.get("reasoning", base["reasoning"]),
                    confidence=confidence,
                    recommended_environment=env
                )
            except Exception as e:
                print(f"[Classifier] Groq classification failed: {e}")

        # 2. Try Gemini if key exists
        if self._gemini_key:
            try:
                genai.configure(api_key=self._gemini_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                full_prompt = f"{system_prompt}\n\nUser Prompt: {prompt}"
                response = await model.generate_content_async(full_prompt)
                data = SemanticAnalyzer.extract_json(response.text)
                
                intent = "SIMPLE" if data.get("intent", "").upper() == "SIMPLE" else "COMPLEX"
                confidence = float(data.get("confidence", base["confidence"]))
                if confidence <= 0.0 or confidence > 1.0:
                    confidence = base["confidence"]

                env = data.get("recommended_environment", base["recommended_environment"])
                if "code" in env.lower():
                    env = "Claude Code"
                elif "cowork" in env.lower():
                    env = "Claude Cowork"
                else:
                    env = "Claude AI"

                return ClassificationResult(
                    intent=intent,
                    reasoning=data.get("reasoning", base["reasoning"]),
                    confidence=confidence,
                    recommended_environment=env
                )
            except Exception as e:
                print(f"[Classifier] Gemini classification failed: {e}")

        # 3. Try Anthropic if key exists
        if self._anthropic_key:
            try:
                client = AsyncAnthropic(api_key=self._anthropic_key)
                response = await client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=300,
                    system=system_prompt,
                    messages=[{"role": "user", "content": prompt}]
                )
                data = SemanticAnalyzer.extract_json(response.content[0].text)
                intent = "SIMPLE" if data.get("intent", "").upper() == "SIMPLE" else "COMPLEX"
                confidence = float(data.get("confidence", base["confidence"]))
                
                env = data.get("recommended_environment", base["recommended_environment"])
                if "code" in env.lower():
                    env = "Claude Code"
                elif "cowork" in env.lower():
                    env = "Claude Cowork"
                else:
                    env = "Claude AI"

                return ClassificationResult(
                    intent=intent,
                    reasoning=data.get("reasoning", base["reasoning"]),
                    confidence=confidence,
                    recommended_environment=env
                )
            except Exception as e:
                print(f"[Classifier] Anthropic classification failed: {e}")

        # 4. Local High-Fidelity Semantic Fallback (Ensures 100% reliability)
        return ClassificationResult(
            intent=base["intent"],
            reasoning=base["reasoning"],
            confidence=base["confidence"],
            recommended_environment=base["recommended_environment"]
        )
