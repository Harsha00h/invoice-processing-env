"""FastAPI server for the Invoice Processing OpenEnv environment."""

import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from models import InvoiceAction, InvoiceObservation, InvoiceState
from server.environment import InvoiceEnvironment


app = FastAPI(
    title="Invoice Processing Environment",
    description="OpenEnv environment for AI agent invoice processing training",
    version="0.1.0",
)

env = InvoiceEnvironment()


# === Request/Response Models ===

class ResetRequest(BaseModel):
    task_id: str = "easy"
    seed: Optional[int] = None
    episode_id: Optional[str] = None


class StepRequest(BaseModel):
    answer: str
    explanation: str = ""


# === Standard OpenEnv Endpoints ===

@app.get("/")
def root():
    return {
        "name": "invoice-processing-env",
        "version": "0.1.0",
        "status": "running",
        "endpoints": ["/reset", "/step", "/state", "/health", "/tasks"],
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/reset")
def reset(request: ResetRequest) -> dict:
    obs = env.reset(
        task_id=request.task_id,
        seed=request.seed,
        episode_id=request.episode_id,
    )
    return obs.model_dump()


@app.post("/step")
def step(request: StepRequest) -> dict:
    action = InvoiceAction(answer=request.answer, explanation=request.explanation)
    obs = env.step(action)
    return obs.model_dump()


@app.get("/state")
def state() -> dict:
    s = env.state
    if s is None:
        raise HTTPException(status_code=400, detail="Environment not initialized. Call /reset first.")
    return s.model_dump()


@app.get("/tasks")
def tasks():
    return {
        "tasks": [
            {
                "id": "easy",
                "name": "Invoice Field Extraction",
                "description": "Extract vendor_name, invoice_number, date, and total_amount from an invoice.",
                "difficulty": "easy",
                "max_attempts": 5,
            },
            {
                "id": "medium",
                "name": "Invoice-PO Matching",
                "description": "Match an invoice to the correct purchase order and flag any mismatches.",
                "difficulty": "medium",
                "max_attempts": 5,
            },
            {
                "id": "hard",
                "name": "Complex Invoice Processing",
                "description": "Handle partial deliveries, currency conversions, and duplicate detection.",
                "difficulty": "hard",
                "max_attempts": 5,
            },
        ],
        "action_schema": {
            "answer": "JSON string with processed invoice data",
            "explanation": "Optional reasoning text",
        },
    }


def main():
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "7860"))
    uvicorn.run("server.app:app", host=host, port=port, workers=1)


if __name__ == "__main__":
    main()
