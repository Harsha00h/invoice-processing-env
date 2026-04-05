"""Reward computation wrapper — wraps grader with episode-level adjustments."""

from server.grader import grade


def compute_reward(
    task_data: dict,
    agent_answer: dict,
    task_id: str,
    step_count: int,
    max_attempts: int,
) -> tuple[float, str, bool]:
    """
    Compute reward with episode-level adjustments.

    Returns:
        (reward, feedback, is_perfect)
    """
    raw_score, feedback = grade(task_data, agent_answer, task_id)

    # Apply exhaustion penalty if max attempts reached without perfect score
    if step_count >= max_attempts and raw_score < 1.0:
        raw_score *= 0.85
        feedback += " | NOTE: Exhaustion penalty applied (0.85x) — max attempts reached."

    # Clamp and round
    reward = round(max(0.0, min(1.0, raw_score)), 2)
    is_perfect = reward >= 1.0

    return reward, feedback, is_perfect
