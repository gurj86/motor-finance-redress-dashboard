"""Transparent, illustrative motor finance remediation rules.

This is a portfolio prototype based on high-level FCA public information checked
on 17 September 2026. It is not a production interpretation of PS26/3.
"""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path


HIGH_VALUE_THRESHOLDS = {
    2008: 38_000, 2009: 39_000, 2010: 43_000, 2011: 45_000,
    2012: 47_000, 2013: 51_000, 2014: 56_000, 2015: 60_000,
    2016: 61_000, 2017: 65_000, 2018: 68_000, 2019: 70_000,
    2020: 73_000, 2021: 75_000, 2022: 80_000, 2023: 82_000,
    2024: 82_000,
}

ARRANGEMENTS = ("DCA", "High commission", "Contractual tie", "No flagged arrangement")
PRODUCTS = ("PCP", "Hire Purchase", "Conditional Sale", "PCH")
BROKER_GROUPS = ("Dealer Group A", "Dealer Group B", "Independent Dealer", "Online Broker")


def create_fictional_agreements(count: int = 100, seed: int = 260917) -> list[dict]:
    """Create deterministic synthetic agreements with varied evidence and outcomes."""
    rng = random.Random(seed)
    agreements: list[dict] = []
    base_date = date(2007, 4, 6)

    for number in range(1, count + 1):
        start_date = base_date + timedelta(days=(number * 67) % 6_390)
        product = PRODUCTS[(number - 1) % len(PRODUCTS)]
        arrangement = ARRANGEMENTS[(number * 3) % len(ARRANGEMENTS)]
        amount_financed = float(
            90_000 if number % 20 == 0 else 4_000 + ((number * 675) % 14_000)
        )
        cost_of_credit = round(amount_financed * (0.12 + ((number * 7) % 25) / 100), 2)
        if arrangement == "High commission":
            commission = round(amount_financed * (0.10 + (number % 2) / 100), 2)
        else:
            commission = round(100 + ((number * 43) % 1_200), 2)
        apr = round(3.9 + ((number * 13) % 170) / 10, 1)
        commission_disclosed = number % 5 == 0
        key_evidence_complete = number % 11 != 0
        vulnerable = number % 9 == 0 or number % 17 == 0
        customer_deceased = number % 23 == 0
        duplicate_representatives = number % 19 == 0
        existing_resolution = number % 29 == 0
        business_purpose = number % 31 == 0
        adapted_vehicle = number % 37 == 0
        zero_interest = number % 41 == 0
        lowest_five_percent = number % 22 == 0
        visible_captive_link = arrangement == "Contractual tie" and number % 4 == 0
        complaint_age_days = 12 + ((number * 17) % 290)

        agreements.append({
            "case_id": f"MF-{number:03d}",
            "agreement_start": start_date.isoformat(),
            "product": product,
            "broker_group": BROKER_GROUPS[number % len(BROKER_GROUPS)],
            "arrangement_type": arrangement,
            "amount_financed": amount_financed,
            "total_cost_of_credit": cost_of_credit,
            "commission_paid": commission,
            "apr_percent": apr,
            "commission_disclosed": commission_disclosed,
            "key_evidence_complete": key_evidence_complete,
            "customer_vulnerability": vulnerable,
            "customer_deceased": customer_deceased,
            "duplicate_representatives": duplicate_representatives,
            "existing_resolution": existing_resolution,
            "business_purpose": business_purpose,
            "adapted_vehicle": adapted_vehicle,
            "zero_interest": zero_interest,
            "lowest_five_percent_apr": lowest_five_percent,
            "visible_captive_link": visible_captive_link,
            "complaint_age_days": complaint_age_days,
            "remediation_status": ("Evidence gathering", "Assessment", "QA", "Awaiting rules")[number % 4],
            "years_deprived": round(1 + ((number * 5) % 12) + rng.random(), 2),
            "illustrative_interest_rate": round(max(0.03, 0.03 + ((number * 2) % 4) / 100), 3),
            "adjusted_credit_cap": round(cost_of_credit * (0.55 + (number % 20) / 100), 2),
            "reviewer_note": "Fictional agreement created for portfolio demonstration.",
        })
    return agreements


def _is_high_value(case: dict) -> bool:
    year = date.fromisoformat(case["agreement_start"]).year
    threshold = HIGH_VALUE_THRESHOLDS.get(year)
    return bool(threshold and case["amount_financed"] > threshold and not case["adapted_vehicle"])


def _arrangement_supported(case: dict) -> tuple[bool, str]:
    arrangement = case["arrangement_type"]
    if arrangement == "DCA":
        return True, "DCA indicator"
    if arrangement == "High commission":
        high = (
            case["commission_paid"] >= 0.39 * case["total_cost_of_credit"]
            and case["commission_paid"] >= 0.10 * case["amount_financed"]
        )
        return high, "High commission thresholds met" if high else "High commission thresholds not met"
    if arrangement == "Contractual tie":
        return not case["visible_captive_link"], (
            "Contractual tie indicator" if not case["visible_captive_link"]
            else "Visible captive link exception"
        )
    return False, "No flagged commission arrangement"


def review_agreement(case: dict) -> dict:
    """Return transparent scope flags and an illustrative redress scenario."""
    start = date.fromisoformat(case["agreement_start"])
    evidence_gaps: list[str] = []
    exclusions: list[str] = []
    arrangement_supported, arrangement_reason = _arrangement_supported(case)

    if not case["key_evidence_complete"]:
        evidence_gaps.append("Key agreement or commission evidence missing")
    if case["duplicate_representatives"]:
        evidence_gaps.append("Multiple representatives require resolution")
    if case["product"] == "PCH":
        exclusions.append("Personal Contract Hire")
    if start < date(2008, 4, 6) and case["amount_financed"] > 25_000:
        exclusions.append("Pre-6 April 2008 agreement over £25,000")
    if case["business_purpose"]:
        exclusions.append("Business-purpose agreement")
    if case["existing_resolution"]:
        exclusions.append("Prior court/FOS decision or accepted compensation")
    if _is_high_value(case):
        exclusions.append("High-value loan threshold")
    if case["zero_interest"]:
        exclusions.append("No interest charged")
    if case["lowest_five_percent_apr"]:
        exclusions.append("APR in illustrative lowest 5% group")

    de_minimis = 120 if start < date(2014, 4, 1) else 150
    if case["commission_paid"] <= de_minimis:
        exclusions.append("Commission at or below de minimis level")

    if exclusions:
        status = "Excluded / no redress indicator"
    elif evidence_gaps:
        status = "Further investigation"
    elif not arrangement_supported or case["commission_disclosed"]:
        status = "No redress indicator"
    else:
        status = "Indicatively eligible"

    discount = 0.21 if start < date(2014, 4, 1) else 0.17
    estimated_loss = round(case["total_cost_of_credit"] * discount, 2)
    hybrid_principal = round((estimated_loss + case["commission_paid"]) / 2, 2)
    commission_cap = round(case["commission_paid"] * 0.90, 2)
    actual_credit_cap = case["total_cost_of_credit"]
    principal = 0.0
    cap_applied = "Not applicable"

    if status == "Indicatively eligible":
        caps = {
            "90% commission cap": commission_cap,
            "Adjusted credit-cost cap": case["adjusted_credit_cap"],
            "Actual credit-cost cap": actual_credit_cap,
        }
        cap_applied, lowest_cap = min(caps.items(), key=lambda item: item[1])
        principal = round(min(hybrid_principal, lowest_cap), 2)

    interest = round(principal * case["illustrative_interest_rate"] * case["years_deprived"], 2)
    total_redress = round(principal + interest, 2)

    priority = "Standard"
    if case["customer_vulnerability"] or case["customer_deceased"]:
        priority = "Urgent"
    elif status == "Further investigation" or complaint_age_days_over(case, 180):
        priority = "Priority"

    return {
        **case,
        "arrangement_reason": arrangement_reason,
        "indicative_status": status,
        "evidence_gaps": "; ".join(evidence_gaps) or "None identified",
        "exclusion_reasons": "; ".join(exclusions) or "None identified",
        "estimated_loss": estimated_loss,
        "hybrid_principal_before_caps": hybrid_principal,
        "cap_applied": cap_applied,
        "illustrative_principal_redress": principal,
        "illustrative_interest": interest,
        "illustrative_total_redress": total_redress,
        "review_priority": priority,
        "human_decision_required": True,
        "calculation_status": "Illustrative only — scheme partly suspended",
    }


def complaint_age_days_over(case: dict, days: int) -> bool:
    return case["complaint_age_days"] > days


def review_agreements(agreements: list[dict]) -> list[dict]:
    return [review_agreement(case) for case in agreements]


def write_csv(cases: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=list(cases[0]))
        writer.writeheader()
        writer.writerows(cases)
