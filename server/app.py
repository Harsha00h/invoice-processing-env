"""FastAPI server for the Invoice Processing OpenEnv environment."""

import os
import uvicorn
from fastapi import FastAPI, HTTPException, Request
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
async def reset(request: Request) -> dict:
    # Accept empty body, missing fields, or full ResetRequest
    try:
        body = await request.json()
    except Exception:
        body = {}
    if body is None:
        body = {}
    task_id = body.get("task_id", "easy") if isinstance(body, dict) else "easy"
    seed = body.get("seed") if isinstance(body, dict) else None
    episode_id = body.get("episode_id") if isinstance(body, dict) else None

    obs = env.reset(task_id=task_id, seed=seed, episode_id=episode_id)
    return obs.model_dump()


@app.post("/step")
async def step(request: Request) -> dict:
    try:
        body = await request.json()
    except Exception:
        body = {}
    if body is None:
        body = {}
    answer = body.get("answer", "") if isinstance(body, dict) else ""
    explanation = body.get("explanation", "") if isinstance(body, dict) else ""

    action = InvoiceAction(answer=answer, explanation=explanation)
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
