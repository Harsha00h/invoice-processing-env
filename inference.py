"""
Inference Script — Invoice Processing Environment
===================================================

Before submitting, ensure the following variables are defined in your environment configuration:
  API_BASE_URL   The API endpoint for the LLM.
  MODEL_NAME     The model identifier to use for inference.
  HF_TOKEN       Your Hugging Face / API key.
  LOCAL_IMAGE_NAME  The name of the local Docker image to use for the environment
                    (if you are using from_docker_image method).

The inference script must be named `inference.py` and placed in the root directory of the project.
Participants must use OpenAI Client for all LLM calls using above variables.

STDOUT FORMAT:
  The script must emit exactly three line types to stdout, in this order:
  [START] task=<task_name> env=<benchmark> model=<model_name>
  [STEP] step=<n> action=<action_str> reward=<R.RR> done=<true|false> error=<error_msg|null>
  [END] success=<true|false> steps=<n> score=<S.SS> rewards=<r1,r2,...,rn>

Rules:
  - One [START] line at episode begin.
  - One [STEP] line per step, immediately after each step() returns.
  - One [END] line after episode ends (always emitted, even on exception).
  - reward and rewards are formatted to 2 decimal places.
  - Each task should return score in [0, 1].
"""

import asyncio
import os
import sys
import json
import requests
from typing import List, Optional

from openai import OpenAI


# === Configuration ===
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "deepseek-ai/DeepSeek-V3-0324"
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
LOCAL_IMAGE_NAME = os.getenv("MY_ENV_SA_BENCHMARK", "invoice-processing-env")

BENCHMARK = os.getenv("MY_ENV_SA_BENCHMARK", "invoice-processing-env")
TASK_NAME = os.getenv("MY_ENV_SA_TASK", "hard")

MAX_STEPS = 5
MAX_TOKENS = 1024
TEMPERATURE = 0.7
SUCCESS_SCORE_THRESHOLD = 0.7

MAX_REWARD_PER_STEP = MAX_TOKENS * 0.1
MAX_TOTAL_REWARD = MAX_STEPS * MAX_REWARD_PER_STEP


# === Logging ===

def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str] = None) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}",
        flush=True,
    )


# === System Prompt ===

SYSTEM_PROMPT = """You are an invoice processing expert agent.
You will receive invoice text and must process it according to the task description.
Always respond with ONLY a valid JSON object matching the required schema.
No explanation, no markdown, no code blocks — just the raw JSON object.

For easy tasks: Return {"vendor_name": "...", "invoice_number": "...", "date": "YYYY-MM-DD", "total_amount": <number>}
For medium tasks: Return {"matching_po": "...", "mismatches": [{"field": "...", "line_item": "...", "invoice_value": "...", "po_value": "..."}]}
For hard tasks: Return {"matching_po": "...", "converted_total": <number>, "is_duplicate": <bool>, "duplicate_of": "..." or null, "partial_delivery": <bool>, "delivered_lines": ["..."], "mismatches": [{"field": "...", "line_item": "...", "invoice_value": "...", "po_value": "..."}]}
""".strip()


# === Helper Functions ===

def build_user_prompt(
    step: int,
    obs: dict,
    last_reward: float,
    history: list,
) -> str:
    parts = []
    parts.append(f"Step: {step}")
    parts.append(f"Task: {obs.get('task_id', 'unknown')} ({obs.get('difficulty', 'unknown')})")
    parts.append(f"Task Description: {obs.get('task_description', '')}")
    parts.append(f"\n--- INVOICE ---\n{obs.get('invoice_text', '')}")

    context = obs.get("context", "")
    if context:
        parts.append(f"\n--- CONTEXT ---\n{context}")

    if obs.get("feedback"):
        parts.append(f"\n--- FEEDBACK FROM PREVIOUS ATTEMPT ---\n{obs['feedback']}")
        parts.append(f"Previous reward: {last_reward:.2f}")

    if obs.get("hint"):
        parts.append(f"\n--- HINT ---\n{obs['hint']}")

    if obs.get("error_message"):
        parts.append(f"\n--- ERROR ---\n{obs['error_message']}")
        parts.append("Please fix your JSON and try again.")

    if history:
        parts.append(f"\nPrevious attempts: {len(history)}")

    parts.append("\nRespond with ONLY the JSON object. No markdown, no explanation.")
    return "\n".join(parts)


def get_model_message(
    client: OpenAI,
    step: int,
    obs: dict,
    last_reward: float,
    history: list,
) -> str:
    user_prompt = build_user_prompt(step, obs, last_reward, history)
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            stream=False,
        )
        text = (completion.choices[0].message.content or "").strip()
        return text if text else "{}"
    except Exception as exc:
        print(f"[WARN] Model request failed: {exc!r}", flush=True)
        return "{}"


# === Environment Client (HTTP) ===

class EnvClient:
    """Simple HTTP client for the OpenEnv environment."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def reset(self, task_id: str = "easy", seed: Optional[int] = None) -> dict:
        payload = {"task_id": task_id}
        if seed is not None:
            payload["seed"] = seed
        resp = requests.post(f"{self.base_url}/reset", json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def step(self, answer: str, explanation: str = "") -> dict:
        payload = {"answer": answer, "explanation": explanation}
        resp = requests.post(f"{self.base_url}/step", json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def health(self) -> bool:
        try:
            resp = requests.get(f"{self.base_url}/health", timeout=10)
            return resp.status_code == 200
        except Exception:
            return False


# === Main ===

def run_task(client: OpenAI, env: EnvClient, task_id: str) -> tuple[float, bool]:
    """Run a single task and return (score, success)."""
    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(task=task_id, env=BENCHMARK, model=MODEL_NAME)

    try:
        obs = env.reset(task_id=task_id)
        last_reward = 0.0
        history: List[str] = []

        for step in range(1, MAX_STEPS + 1):
            if obs.get("done", False):
                break

            message = get_model_message(client, step, obs, last_reward, history)
            obs = env.step(answer=message)

            reward = obs.get("reward", 0.0)
            done = obs.get("done", False)
            error = obs.get("error_message") or None

            rewards.append(reward)
            steps_taken = step
            last_reward = reward

            log_step(step=step, action=message, reward=reward, done=done, error=error)

            history.append(f"Step {step}: reward={reward:.2f}")

            if done:
                break

        if rewards:
            score = max(rewards)
        score = min(max(score, 0.0), 1.0)
        success = score >= SUCCESS_SCORE_THRESHOLD

    except Exception as exc:
        print(f"[ERROR] Task {task_id} failed: {exc!r}", flush=True)

    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)

    return score, success


def main():
    if not API_KEY:
        print("[ERROR] No API key found. Set HF_TOKEN or API_KEY environment variable.", flush=True)
        sys.exit(1)

    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    # Determine environment URL
    env_url = os.getenv("ENV_URL", "http://localhost:7860")
    env = EnvClient(base_url=env_url)

    # Check health
    if not env.health():
        print(f"[WARN] Environment at {env_url} is not responding. Proceeding anyway...", flush=True)

    # Run all 3 tasks
    task_ids = ["easy", "medium", "hard"]
    total_score = 0.0
    results = {}

    for task_id in task_ids:
        score, success = run_task(client, env, task_id)
        results[task_id] = {"score": score, "success": success}
        total_score += score

    avg_score = total_score / len(task_ids)
    print(f"\n=== FINAL RESULTS ===", flush=True)
    for tid, res in results.items():
        print(f"  {tid}: score={res['score']:.2f} success={res['success']}", flush=True)
    print(f"  Average Score: {avg_score:.2f}", flush=True)


if __name__ == "__main__":
    main()
