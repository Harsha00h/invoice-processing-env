"""Core Invoice Processing OpenEnv environment implementation."""

import json
import random
from typing import Optional
from uuid import uuid4

from models import InvoiceAction, InvoiceObservation, InvoiceState
from data.invoices import EASY_TASKS, MEDIUM_TASKS, HARD_TASKS
from server.rewards import compute_reward


TASK_DESCRIPTIONS = {
    "easy": (
        "Extract the following fields from the invoice: vendor_name, invoice_number, date, total_amount. "
        "Return a JSON object with these exact keys. For date, use YYYY-MM-DD format. "
        "For total_amount, return the numeric value (e.g., 1247.50)."
    ),
    "medium": (
        "Match this invoice to the correct purchase order from the provided list. "
        "Return a JSON object with 'matching_po' (the PO number string) and "
        "'mismatches' (a list of objects, each with 'field', 'line_item', 'invoice_value', 'po_value' "
        "for any discrepancies in quantity or unit price). If no mismatches, return an empty list."
    ),
    "hard": (
        "Process this invoice considering partial deliveries, currency conversions, and duplicate detection. "
        "Return a JSON object with: "
        "'matching_po' (PO number), "
        "'converted_total' (total converted to USD using provided exchange rates), "
        "'is_duplicate' (boolean — true if this invoice duplicates a historical one), "
        "'duplicate_of' (historical invoice ID string, or null), "
        "'partial_delivery' (boolean — true if invoice covers fewer lines than the PO), "
        "'delivered_lines' (list of line item description strings that appear on the invoice), "
        "'mismatches' (list of discrepancy objects with 'field', 'line_item', 'invoice_value', 'po_value')."
    ),
}

HINTS = {
    "easy": (
        "Hint: The vendor name is typically at the top of the invoice. "
        "The total amount is usually labeled 'Total', 'Total Due', or 'Grand Total'. "
        "Dates may appear in various formats — convert to YYYY-MM-DD."
    ),
    "medium": (
        "Hint: Match by vendor name first, then compare line items. "
        "Check quantities and unit prices for each line item against the PO. "
        "Report mismatches with the specific line item name."
    ),
    "hard": (
        "Hint: For currency conversion, multiply the invoice total by the exchange rate "
        "(e.g., EUR amount * EUR_USD rate = USD amount). "
        "For duplicate detection, compare vendor names (may differ slightly), dates (within 30 days), "
        "and line items. Partial delivery means the invoice has fewer line items than the PO."
    ),
}


class InvoiceEnvironment:
    """OpenEnv-compatible invoice processing environment."""

    def __init__(self):
        self.tasks = {
            "easy": EASY_TASKS,
            "medium": MEDIUM_TASKS,
            "hard": HARD_TASKS,
        }
        self.max_attempts = 5
        self._state: Optional[InvoiceState] = None
        self._current_task: Optional[dict] = None

    def reset(
        self,
        task_id: str = "easy",
        seed: Optional[int] = None,
        episode_id: Optional[str] = None,
    ) -> InvoiceObservation:
        """Reset the environment for a new episode."""
        if task_id not in self.tasks:
            task_id = "easy"

        task_pool = self.tasks[task_id]
        if seed is not None:
            rng = random.Random(seed)
            selected = rng.choice(task_pool)
        else:
            selected = random.choice(task_pool)

        self._current_task = selected
        self._state = InvoiceState(
            episode_id=episode_id or str(uuid4()),
            step_count=0,
            task_id=task_id,
            difficulty=task_id,
            max_attempts=self.max_attempts,
            last_score=0.0,
            completed=False,
        )

        context = self._build_context(selected, task_id)

        return InvoiceObservation(
            invoice_text=selected["invoice_text"],
            context=context,
            task_description=TASK_DESCRIPTIONS[task_id],
            task_id=task_id,
            difficulty=task_id,
            attempt_number=0,
            max_attempts=self.max_attempts,
            done=False,
            reward=0.0,
        )

    def step(self, action: InvoiceAction) -> InvoiceObservation:
        """Process an agent action and return the next observation."""
        if self._state is None or self._current_task is None:
            return InvoiceObservation(
                error_message="Environment not initialized. Call reset() first.",
                done=True,
                reward=0.0,
            )

        if self._state.completed:
            return InvoiceObservation(
                feedback="Episode already completed.",
                done=True,
                reward=self._state.last_score,
                task_id=self._state.task_id,
                difficulty=self._state.difficulty,
            )

        self._state.step_count += 1

        # Parse agent JSON
        parsed, parse_error = self._parse_agent_answer(action.answer)
        if parse_error:
            hint = ""
            if self._state.step_count >= 2:
                hint = HINTS.get(self._state.task_id, "")
            return InvoiceObservation(
                invoice_text=self._current_task["invoice_text"],
                context=self._build_context(self._current_task, self._state.task_id),
                task_description=TASK_DESCRIPTIONS[self._state.task_id],
                task_id=self._state.task_id,
                difficulty=self._state.difficulty,
                attempt_number=self._state.step_count,
                max_attempts=self.max_attempts,
                error_message=parse_error,
                hint=hint,
                done=self._state.step_count >= self.max_attempts,
                reward=0.0,
            )

        # Grade the answer
        reward, feedback, is_perfect = compute_reward(
            self._current_task,
            parsed,
            self._state.task_id,
            self._state.step_count,
            self.max_attempts,
        )

        self._state.last_score = reward

        # Determine done
        done = False
        if is_perfect:
            done = True
            self._state.completed = True
        elif self._state.step_count >= self.max_attempts:
            done = True

        # Provide hint after 2 failed attempts with low score
        hint = ""
        if self._state.step_count >= 2 and reward < 0.5:
            hint = HINTS.get(self._state.task_id, "")

        return InvoiceObservation(
            invoice_text=self._current_task["invoice_text"] if not done else "",
            context=self._build_context(self._current_task, self._state.task_id) if not done else "",
            task_description=TASK_DESCRIPTIONS[self._state.task_id],
            task_id=self._state.task_id,
            difficulty=self._state.difficulty,
            attempt_number=self._state.step_count,
            max_attempts=self.max_attempts,
            feedback=feedback,
            hint=hint,
            done=done,
            reward=reward,
        )

    @property
    def state(self) -> Optional[InvoiceState]:
        return self._state

    def _build_context(self, task: dict, task_id: str) -> str:
        """Build context string based on difficulty."""
        if task_id == "easy":
            return ""

        parts = []

        # Purchase orders
        pos = task.get("purchase_orders", [])
        if pos:
            parts.append("=== PURCHASE ORDERS ===")
            for po in pos:
                parts.append(f"\nPO Number: {po['po_number']}")
                parts.append(f"Vendor: {po['vendor']}")
                currency = po.get("currency", "USD")
                parts.append(f"Currency: {currency}")
                parts.append("Line Items:")
                for item in po["line_items"]:
                    parts.append(
                        f"  - {item['description']}  Qty: {item['quantity']}  "
                        f"Unit Price: ${item['unit_price']:.2f}"
                    )
                parts.append(f"PO Total: ${po['total']:.2f}")

        # Exchange rates (hard only)
        rates = task.get("exchange_rates", {})
        if rates:
            parts.append("\n=== EXCHANGE RATES ===")
            for pair, rate in rates.items():
                parts.append(f"  {pair}: {rate}")

        # Historical invoices (hard only)
        historical = task.get("historical_invoices", [])
        if historical:
            parts.append("\n=== HISTORICAL INVOICES ===")
            for inv in historical:
                parts.append(f"\nInvoice ID: {inv['invoice_id']}")
                parts.append(f"Vendor: {inv['vendor']}")
                parts.append(f"Date: {inv['date']}")
                parts.append(f"Total: {inv['total']} {inv['currency']}")
                parts.append("Line Items:")
                for item in inv["line_items"]:
                    parts.append(f"  - {item}")

        return "\n".join(parts)

    def _parse_agent_answer(self, answer: str) -> tuple[Optional[dict], Optional[str]]:
        """Parse agent's answer string as JSON, handling common LLM output quirks."""
        if not answer or not answer.strip():
            return None, "Empty answer provided."

        cleaned = answer.strip()

        # Strip markdown code blocks
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            # Remove first line (```json or ```) and last line (```)
            lines = [l for l in lines if not l.strip().startswith("```")]
            cleaned = "\n".join(lines).strip()

        try:
            parsed = json.loads(cleaned)
            if isinstance(parsed, dict):
                return parsed, None
            return None, f"Expected a JSON object, got {type(parsed).__name__}."
        except json.JSONDecodeError as e:
            return None, f"Invalid JSON: {str(e)}"
