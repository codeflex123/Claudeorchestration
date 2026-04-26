import json
from typing import Dict, Any, List
try:
    from .planner import PlanningStrategy
except ImportError:
    from planner import PlanningStrategy

class ContextManager:
    def __init__(self):
        pass

    def generate_handoff_payload(self, prompt: str, strategy: PlanningStrategy) -> Dict[str, Any]:
        """
        Creates a structured payload that Claude can use to immediately start the task.
        """
        # 1. Format the strategy into a clear system directive
        roadmap_str = "\n".join([f"{idx+1}. {step.title}: {step.description}" for idx, step in enumerate(strategy.steps)])
        
        mcp_instructions = ""
        if strategy.mcp_required:
            mcp_ids = [t.id for t in strategy.mcp_required]
            mcp_instructions = f"\n\nCRITICAL: The following MCP tools are authorized and MUST be used: {', '.join(mcp_ids)}."

        system_instruction = (
            f"You are operating in '{strategy.recommended_model}' mode as part of an orchestrated handoff.\n\n"
            f"GOAL: {prompt}\n\n"
            f"EXECUTION STRATEGY:\n{roadmap_str}"
            f"{mcp_instructions}\n\n"
            f"REASONING FOR THIS PLAN:\n{strategy.reasoning}"
        )

        return {
            "target_environment": strategy.recommended_environment, # Use the selected environment
            "initial_prompt": prompt,
            "system_directive": system_instruction,
            "metadata": {
                "eta_mins": strategy.estimated_total_time_mins,
                "strategy_id": "STG-" + str(hash(prompt))[:8],
                "steps_count": len(strategy.steps),
                "mcp_context": [t.model_dump() for t in strategy.mcp_required]
            }
        }

context_manager = ContextManager()
