from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

try:
    from .classifier import Classifier, ClassificationResult
    from .planner import Planner, PlanningStrategy
    from .utils import InputAnalyzer
    from .context_manager import context_manager
except ImportError:
    from classifier import Classifier, ClassificationResult
    from planner import Planner, PlanningStrategy
    from utils import InputAnalyzer
    from context_manager import context_manager

app = FastAPI(title="Claude Orchestration Backend")

classifier = Classifier()
planner = Planner()

class TriageRequest(BaseModel):
    prompt: str

class TriageResponse(BaseModel):
    branch: str
    intent: str
    message: str
    classification: ClassificationResult
    strategy: PlanningStrategy

class HandoffRequest(BaseModel):
    prompt: str
    strategy: PlanningStrategy

@app.get("/")
def root_health():
    return {"status": "ok", "service": "Claude Orchestration Backend"}

@app.get("/api/health")
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/triage")
@app.post("/triage")
async def triage_prompt(request: TriageRequest):
    # Standardize input
    analyzer = InputAnalyzer(request.prompt)
    clean_prompt = analyzer.sanitize()
    
    # Classify intent
    classification = await classifier.classify(clean_prompt)
    
    # Generate execution plan
    strategy = await planner.generate_plan(clean_prompt)
    
    # Align strategy environment with classification if applicable
    if classification.intent == "SIMPLE":
        branch = "A"
        message = "Direct inquiry detected. Streamlined plan formulated for Claude AI."
    else:
        branch = "B"
        message = f"Complex task detected. Orchestrating specialized workflow for {strategy.recommended_environment}."
    
    return TriageResponse(
        branch=branch,
        intent=classification.intent,
        message=message,
        classification=classification,
        strategy=strategy
    )

@app.post("/api/handoff")
@app.post("/handoff")
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
        "detail": "If you are seeing this, verify route definition in FastAPI."
    }
