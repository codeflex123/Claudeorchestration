from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import os

# Load environment variables (Phase 1-5 connectivity fix)
load_dotenv()

from .classifier import Classifier, ClassificationResult
from .planner import Planner, PlanningStrategy
from .utils import InputAnalyzer
from .context_manager import context_manager

app = FastAPI()
classifier = Classifier()
planner = Planner()

class TriageRequest(BaseModel):
    prompt: str

class TriageResponse(BaseModel):
    branch: str
    intent: str
    message: str
    classification: ClassificationResult
    strategy: Optional[PlanningStrategy] = None

class HandoffRequest(BaseModel):
    prompt: str
    strategy: PlanningStrategy

@app.get("/")
def root_health():
    return {"status": "ok", "service": "Claude Orchestration Backend"}

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/triage")
async def triage_prompt(request: TriageRequest):
    # Standardize input
    analyzer = InputAnalyzer(request.prompt)
    clean_prompt = analyzer.sanitize()
    
    # Classify intent
    classification = await classifier.classify(clean_prompt)
    
    # Branching logic
    if classification.confidence > 0.8 and classification.intent == "SIMPLE":
        return TriageResponse(
            branch="A",
            intent="SIMPLE",
            message="This is a direct query. Responding immediately via Claude AI...",
            classification=classification
        )
    
    # Complex branch - Generate Strategy
    strategy = await planner.generate_plan(clean_prompt)
    
    return TriageResponse(
        branch="B",
        intent="COMPLEX",
        message="Complex task detected. Triage Dashboard initiated for strategic planning.",
        classification=classification,
        strategy=strategy
    )

@app.post("/api/handoff")
async def perform_handoff(request: HandoffRequest):
    """
    Finalizes the triage session and returns the handoff bundle.
    """
    payload = context_manager.generate_handoff_payload(request.prompt, request.strategy)
    return {
        "status": "success",
        "handoff_bundle": payload
    }

@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(path_name: str):
    return {
        "error": "Endpoint not found",
        "requested_path": path_name,
        "detail": "If you are seeing this, the proxy is hitting the backend but the route is not defined in FastAPI with the correct prefix."
    }
