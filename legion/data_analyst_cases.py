"""Fixed, deterministic *synthetic* professional data-analysis benchmark.

30 purpose-authored arithmetic tasks (10 conversion, 10 total, 10 mean).
No external datasets, accounts or customer information; all answers remain
separate from model prompts. This is a small public reference benchmark, NOT
an unseen independently curated dataset or professional certificate.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json

VERSION = "legion-data-analyst-30-v1"
NUMBER = 30


@dataclass(frozen=True)
class AnalyticCase:
    id: str
    category: str
    prompt: str
    expected: Decimal
    unit: str


def build_cases() -> tuple[AnalyticCase, ...]:
    output = []
    for i in range(1, 11):
        visits = 101 + 17 * i
        orders = 3 + 2 * i
        value = (Decimal(orders) * 100 / Decimal(visits)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP)
        output.append(AnalyticCase(
            f"conversion-{i:02d}", "conversion",
            f"A fictional online store had {visits} visits and {orders} orders. "
            "Calculate the conversion rate in percent, rounded to two decimal places.",
            value, "%"
        ))
    for i in range(1, 11):
        counts = (6 + i, 12 + 3 * i, 14 + 2 * i)
        output.append(AnalyticCase(
            f"total-{i:02d}", "total",
            f"A fictional store recorded {counts[0]}, {counts[1]}, and {counts[2]} "
            "orders on three consecutive days. How many orders in total?",
            Decimal(sum(counts)), "orders"
        ))
    for i in range(1, 11):
        # All means are exact; no ambiguity over numeric rounding.
        counts = (4 * i, 4 * (i + 1), 4 * (i + 2), 4 * (i + 3))
        output.append(AnalyticCase(
            f"mean-{i:02d}", "mean",
            f"A fictional help desk resolved {counts[0]}, {counts[1]}, "
            f"{counts[2]} and {counts[3]} synthetic tickets in four days. "
            "What was the average daily number of resolved tickets?",
            Decimal(sum(counts)) / Decimal(4), "tickets/day"
        ))
    assert len(output) == NUMBER
    assert len({case.id for case in output}) == NUMBER
    return tuple(output)


def prompt_for(case: AnalyticCase) -> str:
    # The expected result must NEVER be forwarded to the candidate.
    return (
        "LEGION OFFLINE APPRENTICE EXAM - synthetic data, no accounts, "
        "no external effects. Do the arithmetic carefully.\n"
        + case.prompt + "\n"
        + 'Reply ONLY with one JSON object: {"answer": number, "unit": "'
        + case.unit + '"}. No markdown or extra claims.'
    )


def dataset_sha256(cases: tuple[AnalyticCase, ...] | None = None) -> str:
    cases = build_cases() if cases is None else cases
    serialized = [
        {"id": c.id, "category": c.category, "prompt": c.prompt,
         "answer": str(c.expected), "unit": c.unit}
        for c in cases
    ]
    return hashlib.sha256(
        json.dumps({"version": VERSION, "cases": serialized},
                   sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
