---
title: Invoice Processing Env
emoji: 🌖
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# Invoice Processing Environment

An OpenEnv environment where an AI agent learns to process invoices — from basic field extraction to complex multi-step reconciliation involving purchase order matching, currency conversions, partial deliveries, and duplicate detection.

## Environment Description

Invoice processing is a critical real-world accounts payable workflow. AP departments handle varied invoice formats, match them against purchase orders, convert currencies, detect duplicates, and flag discrepancies — all manually. This environment simulates that workflow across three difficulty tiers.

## Tasks

### Easy — Invoice Field Extraction
Extract `vendor_name`, `invoice_number`, `date`, and `total_amount` from structured invoice text.

**Scoring (0.25 each):**
- `vendor_name`: Fuzzy string match (exact = 0.25, partial = 0.15)
- `invoice_number`: Exact match
- `date`: Parsed date comparison (any format → YYYY-MM-DD)
- `total_amount`: Numeric comparison (1% tolerance)

### Medium — Invoice-PO Matching
Match an invoice to the correct purchase order and flag quantity/price mismatches.

**Scoring:**
- Correct PO identification: 0.40
- Mismatch detection: 0.60 (proportional to found vs. ground truth, minus false positives)

### Hard — Complex Invoice Processing
Handle partial deliveries, currency conversions, and duplicate detection simultaneously.

**Scoring:**
- PO match: 0.15
- Currency conversion: 0.20 (within 1% = full, within 5% = half)
- Duplicate detection: 0.25 (flag + ID)
- Partial delivery: 0.25 (flag + delivered lines)
- Mismatches: 0.15

## Action Space

```json
{
  "answer": "JSON string with extracted/processed invoice data",
  "explanation": "Optional reasoning text"
}
```

## Observation Space

| Field | Type | Description |
|-------|------|-------------|
| `invoice_text` | string | Raw invoice content |
| `context` | string | PO data, exchange rates, historical invoices |
| `task_description` | string | What the agent must accomplish |
| `task_id` | string | "easy", "medium", or "hard" |
| `difficulty` | string | Difficulty level |
| `attempt_number` | int | Current attempt (1-indexed) |
| `max_attempts` | int | Maximum allowed (5) |
| `feedback` | string | Detailed grader feedback from prior attempt |
| `hint` | string | Revealed after 2 failed attempts with score < 0.5 |
| `error_message` | string | JSON parse error if agent output was malformed |
| `done` | bool | Whether the episode is over |
| `reward` | float | Score 0.0–1.0 |

## Reward Function

- **Continuous 0.0–1.0** with partial credit per component
- **Feedback loop**: Detailed feedback after each attempt helps agents improve
- **Hint system**: Hints provided after 2 low-scoring attempts
- **Exhaustion penalty**: 0.85x multiplier if max attempts reached without perfect score

## Setup & Usage

### Prerequisites
- Python 3.10+
- Docker (for containerized deployment)

### Local Development

```bash
pip install -r requirements.txt
python -m server.app
```

The server starts at `http://localhost:7860`.

### Docker

```bash
docker build -t invoice-processing-env .
docker run -p 7860:7860 invoice-processing-env
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/reset` | POST | Start new episode: `{"task_id": "easy\|medium\|hard"}` |
| `/step` | POST | Submit action: `{"answer": "<json>"}` |
| `/state` | GET | Current environment state |
| `/tasks` | GET | List available tasks |

### Running Inference

```bash
export API_BASE_URL="https://router.huggingface.co/v1"
export MODEL_NAME="deepseek-ai/DeepSeek-V3-0324"
export HF_TOKEN="your-token"
export ENV_URL="http://localhost:7860"

python inference.py
```

## Baseline Scores

| Task | Expected Baseline |
|------|------------------|
| Easy | ~0.85 |
| Medium | ~0.65 |
| Hard | ~0.45 |
