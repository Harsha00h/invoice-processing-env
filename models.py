"""Pydantic models for the Invoice Processing OpenEnv environment."""

from typing import Optional
from pydantic import BaseModel, Field


class InvoiceAction(BaseModel):
    """Action submitted by the agent — a JSON answer string and optional explanation."""
    answer: str = Field(..., description="JSON string with extracted/processed invoice data")
    explanation: str = Field(default="", description="Optional reasoning text")


class InvoiceObservation(BaseModel):
    """Observation returned to the agent after each step or reset."""
    invoice_text: str = Field(default="", description="The raw invoice content to process")
    context: str = Field(default="", description="Additional context (PO data, exchange rates, historical invoices)")
    task_description: str = Field(default="", description="What the agent must accomplish")
    task_id: str = Field(default="", description="easy | medium | hard")
    difficulty: str = Field(default="", description="Difficulty level")
    attempt_number: int = Field(default=0, description="Current attempt count")
    max_attempts: int = Field(default=5, description="Maximum allowed attempts")
    feedback: str = Field(default="", description="Grader feedback from prior attempt")
    hint: str = Field(default="", description="Hint revealed after 2 failed attempts")
    error_message: str = Field(default="", description="Error message if agent JSON was malformed")
    done: bool = Field(default=False, description="Whether the episode is over")
    reward: float = Field(default=0.0, description="Score 0.0-1.0")


class InvoiceState(BaseModel):
    """Internal environment state tracked across steps."""
    episode_id: str = Field(default="")
    step_count: int = Field(default=0)
    task_id: str = Field(default="")
    difficulty: str = Field(default="")
    max_attempts: int = Field(default=5)
    last_score: float = Field(default=0.0)
    completed: bool = Field(default=False)
