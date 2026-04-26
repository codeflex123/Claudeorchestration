import os
import json
from enum import Enum
from pydantic import BaseModel
from typing import Literal, Optional
from anthropic import AsyncAnthropic
from groq import AsyncGroq
import google.generativeai as genai

class ClassificationResult(BaseModel):
    intent: Literal["SIMPLE", "COMPLEX"]
    reasoning: str
    confidence: float

class Provider(str, Enum):
    ANTHROPIC = "anthropic"
    GROQ = "groq"
    GEMINI = "gemini"

class Classifier:
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

    async def classify(self, prompt: str) -> ClassificationResult:
        system_prompt = """
        You are an Intent Classifier for an AI Orchestration Layer.
        Determine if the prompt is "SIMPLE" (basic inquiry) or "COMPLEX" (agentic task).
        Respond ONLY in JSON: {"intent": "SIMPLE" | "COMPLEX", "reasoning": "...", "confidence": 0.0-1.0}
        """

        try:
            if self.provider == Provider.ANTHROPIC:
                response = await self.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=200,
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
                # Gemini doesn't support system prompt in standard way for some models, 
                # but we'll use the combined prompt for flash.
                full_prompt = f"{system_prompt}\n\nUser Prompt: {prompt}"
                response = await self.client.generate_content_async(full_prompt)
                # Clean up json markdown wrapper if present
                text = response.text.strip()
                if text.startswith("```json"):
                    text = text[7:-3]
                data = json.loads(text)

            return ClassificationResult(**data)
        except Exception as e:
            return ClassificationResult(
                intent="COMPLEX", 
                reasoning=f"Error using {self.provider}: {str(e)}", 
                confidence=0.0
            )
