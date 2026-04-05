"""Grading logic for all 3 difficulty tiers with partial-credit scoring (0.0-1.0)."""

import re
from datetime import datetime
from typing import Optional


def grade(task_data: dict, agent_answer: dict, task_id: str) -> tuple[float, str]:
    """Dispatch grading to the appropriate difficulty handler."""
    if task_id == "easy":
        return _grade_easy(task_data, agent_answer)
    elif task_id == "medium":
        return _grade_medium(task_data, agent_answer)
    elif task_id == "hard":
        return _grade_hard(task_data, agent_answer)
    return 0.0, "Unknown task_id"


# =============================================================================
# Easy: Field Extraction (4 fields, 0.25 each)
# =============================================================================

def _grade_easy(task_data: dict, agent_answer: dict) -> tuple[float, str]:
    gt = task_data["ground_truth"]
    score = 0.0
    feedback_parts = []

    # Vendor name (0.25) — fuzzy match
    agent_vendor = _normalize_string(str(agent_answer.get("vendor_name", "")))
    gt_vendor = _normalize_string(gt["vendor_name"])
    if agent_vendor == gt_vendor:
        score += 0.25
        feedback_parts.append("vendor_name: CORRECT")
    elif gt_vendor in agent_vendor or agent_vendor in gt_vendor:
        score += 0.15
        feedback_parts.append(f"vendor_name: PARTIAL (expected '{gt['vendor_name']}', got '{agent_answer.get('vendor_name', '')}')")
    else:
        feedback_parts.append(f"vendor_name: INCORRECT (expected '{gt['vendor_name']}', got '{agent_answer.get('vendor_name', '')}')")

    # Invoice number (0.25) — exact match
    agent_inv = str(agent_answer.get("invoice_number", "")).strip()
    gt_inv = gt["invoice_number"].strip()
    if agent_inv == gt_inv:
        score += 0.25
        feedback_parts.append("invoice_number: CORRECT")
    else:
        feedback_parts.append(f"invoice_number: INCORRECT (expected '{gt_inv}', got '{agent_inv}')")

    # Date (0.25) — parse and compare
    agent_date = _parse_date(str(agent_answer.get("date", "")))
    gt_date = _parse_date(gt["date"])
    if agent_date and gt_date and agent_date == gt_date:
        score += 0.25
        feedback_parts.append("date: CORRECT")
    else:
        feedback_parts.append(f"date: INCORRECT (expected '{gt['date']}', got '{agent_answer.get('date', '')}')")

    # Total amount (0.25) — numeric comparison with 1% tolerance
    agent_amount = _parse_amount(str(agent_answer.get("total_amount", "")))
    gt_amount = gt["total_amount"]
    if agent_amount is not None and _compare_amounts(agent_amount, gt_amount, 0.01):
        score += 0.25
        feedback_parts.append("total_amount: CORRECT")
    else:
        feedback_parts.append(f"total_amount: INCORRECT (expected {gt_amount}, got '{agent_answer.get('total_amount', '')}')")

    return round(score, 2), " | ".join(feedback_parts)


# =============================================================================
# Medium: PO Matching + Mismatch Detection
# =============================================================================

def _grade_medium(task_data: dict, agent_answer: dict) -> tuple[float, str]:
    gt = task_data["ground_truth"]
    score = 0.0
    feedback_parts = []

    # Correct PO match (0.40)
    agent_po = str(agent_answer.get("matching_po", "")).strip()
    gt_po = gt["matching_po"]
    if agent_po == gt_po:
        score += 0.40
        feedback_parts.append("matching_po: CORRECT")
    else:
        feedback_parts.append(f"matching_po: INCORRECT (expected '{gt_po}', got '{agent_po}')")

    # Mismatch detection (0.60)
    gt_mismatches = gt.get("mismatches", [])
    agent_mismatches = agent_answer.get("mismatches", [])
    if not isinstance(agent_mismatches, list):
        agent_mismatches = []

    if len(gt_mismatches) == 0:
        # No mismatches expected
        if len(agent_mismatches) == 0:
            score += 0.60
            feedback_parts.append("mismatches: CORRECT (none expected, none reported)")
        else:
            penalty = min(len(agent_mismatches) * 0.15, 0.60)
            score += max(0.60 - penalty, 0.0)
            feedback_parts.append(f"mismatches: PARTIAL (none expected, but {len(agent_mismatches)} reported as false positives)")
    else:
        per_mismatch = 0.60 / len(gt_mismatches)
        found = 0
        false_positives = 0

        for gt_m in gt_mismatches:
            gt_line = _normalize_string(gt_m.get("line_item", ""))
            matched = False
            for agent_m in agent_mismatches:
                agent_line = _normalize_string(str(agent_m.get("line_item", agent_m.get("field", ""))))
                if gt_line and agent_line and (gt_line in agent_line or agent_line in gt_line):
                    matched = True
                    break
            if matched:
                found += 1

        # Count false positives (agent reported mismatches not in ground truth)
        for agent_m in agent_mismatches:
            agent_line = _normalize_string(str(agent_m.get("line_item", agent_m.get("field", ""))))
            is_fp = True
            for gt_m in gt_mismatches:
                gt_line = _normalize_string(gt_m.get("line_item", ""))
                if gt_line and agent_line and (gt_line in agent_line or agent_line in gt_line):
                    is_fp = False
                    break
            if is_fp:
                false_positives += 1

        mismatch_score = found * per_mismatch - false_positives * 0.10
        mismatch_score = max(mismatch_score, 0.0)
        score += mismatch_score
        feedback_parts.append(
            f"mismatches: {found}/{len(gt_mismatches)} found, {false_positives} false positives"
        )

    return round(min(score, 1.0), 2), " | ".join(feedback_parts)


# =============================================================================
# Hard: Partial Delivery + Currency + Duplicates + Mismatches
# =============================================================================

def _grade_hard(task_data: dict, agent_answer: dict) -> tuple[float, str]:
    gt = task_data["ground_truth"]
    score = 0.0
    feedback_parts = []

    # 1. Correct PO match (0.15)
    agent_po = str(agent_answer.get("matching_po", "")).strip()
    if agent_po == gt["matching_po"]:
        score += 0.15
        feedback_parts.append("matching_po: CORRECT")
    else:
        feedback_parts.append(f"matching_po: INCORRECT (expected '{gt['matching_po']}')")

    # 2. Currency conversion (0.20)
    agent_total = _parse_amount(str(agent_answer.get("converted_total", "")))
    gt_total = gt["converted_total"]
    if agent_total is not None:
        if _compare_amounts(agent_total, gt_total, 0.01):
            score += 0.20
            feedback_parts.append("converted_total: CORRECT")
        elif _compare_amounts(agent_total, gt_total, 0.05):
            score += 0.10
            feedback_parts.append(f"converted_total: CLOSE (expected {gt_total}, got {agent_total})")
        else:
            feedback_parts.append(f"converted_total: INCORRECT (expected {gt_total}, got {agent_total})")
    else:
        feedback_parts.append(f"converted_total: MISSING or unparseable")

    # 3. Duplicate detection (0.25)
    agent_is_dup = agent_answer.get("is_duplicate", None)
    gt_is_dup = gt["is_duplicate"]
    if isinstance(agent_is_dup, bool) and agent_is_dup == gt_is_dup:
        score += 0.15
        feedback_parts.append("is_duplicate: CORRECT")
        if gt_is_dup:
            agent_dup_of = str(agent_answer.get("duplicate_of", "")).strip()
            gt_dup_of = gt.get("duplicate_of", "")
            if agent_dup_of == gt_dup_of:
                score += 0.10
                feedback_parts.append("duplicate_of: CORRECT")
            else:
                feedback_parts.append(f"duplicate_of: INCORRECT (expected '{gt_dup_of}')")
        else:
            score += 0.10  # No duplicate_of needed
    else:
        feedback_parts.append(f"is_duplicate: INCORRECT (expected {gt_is_dup})")

    # 4. Partial delivery (0.25)
    agent_partial = agent_answer.get("partial_delivery", None)
    gt_partial = gt["partial_delivery"]
    if isinstance(agent_partial, bool) and agent_partial == gt_partial:
        score += 0.10
        feedback_parts.append("partial_delivery: CORRECT")
    else:
        feedback_parts.append(f"partial_delivery: INCORRECT (expected {gt_partial})")

    # Delivered lines comparison (0.15)
    agent_lines = agent_answer.get("delivered_lines", [])
    gt_lines = gt.get("delivered_lines", [])
    if not isinstance(agent_lines, list):
        agent_lines = []
    if gt_lines:
        matched_lines = 0
        for gt_line in gt_lines:
            gt_norm = _normalize_string(gt_line)
            for agent_line in agent_lines:
                if _normalize_string(str(agent_line)) == gt_norm or gt_norm in _normalize_string(str(agent_line)):
                    matched_lines += 1
                    break
        line_score = (matched_lines / len(gt_lines)) * 0.15
        score += line_score
        feedback_parts.append(f"delivered_lines: {matched_lines}/{len(gt_lines)} matched")
    else:
        if len(agent_lines) == 0:
            score += 0.15
        feedback_parts.append("delivered_lines: OK")

    # 5. Mismatches (0.15) — same logic as medium
    gt_mismatches = gt.get("mismatches", [])
    agent_mismatches = agent_answer.get("mismatches", [])
    if not isinstance(agent_mismatches, list):
        agent_mismatches = []

    if len(gt_mismatches) == 0:
        if len(agent_mismatches) == 0:
            score += 0.15
            feedback_parts.append("mismatches: CORRECT (none expected)")
        else:
            penalty = min(len(agent_mismatches) * 0.05, 0.15)
            score += max(0.15 - penalty, 0.0)
            feedback_parts.append(f"mismatches: {len(agent_mismatches)} false positives")
    else:
        per_mismatch = 0.15 / len(gt_mismatches)
        found = 0
        for gt_m in gt_mismatches:
            gt_line = _normalize_string(gt_m.get("line_item", ""))
            for agent_m in agent_mismatches:
                agent_line = _normalize_string(str(agent_m.get("line_item", agent_m.get("field", ""))))
                if gt_line and agent_line and (gt_line in agent_line or agent_line in gt_line):
                    found += 1
                    break
        score += found * per_mismatch
        feedback_parts.append(f"mismatches: {found}/{len(gt_mismatches)} found")

    return round(min(score, 1.0), 2), " | ".join(feedback_parts)


# =============================================================================
# Helper Functions
# =============================================================================

def _normalize_string(s: str) -> str:
    """Lowercase, strip, collapse whitespace."""
    return re.sub(r"\s+", " ", s.strip().lower())


def _parse_amount(s: str) -> Optional[float]:
    """Parse a monetary string to float, stripping currency symbols and commas."""
    if not s:
        return None
    try:
        cleaned = re.sub(r"[^\d.\-]", "", s.replace(",", ""))
        return float(cleaned) if cleaned else None
    except (ValueError, TypeError):
        return None


def _parse_date(s: str) -> Optional[datetime]:
    """Try multiple date formats and return a datetime or None."""
    if not s:
        return None
    s = s.strip()
    formats = [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%B %d, %Y",
        "%b %d, %Y",
        "%d %B %Y",
        "%d %b %Y",
        "%Y/%m/%d",
        "%m-%d-%Y",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None


def _compare_amounts(a: float, b: float, tolerance: float = 0.01) -> bool:
    """Check if two amounts are within relative tolerance."""
    if b == 0:
        return a == 0
    return abs(a - b) / abs(b) <= tolerance
