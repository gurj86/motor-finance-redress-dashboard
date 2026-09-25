"""Generate the motor finance governance dashboard and summary."""

from __future__ import annotations

import html
import json
from collections import Counter
from pathlib import Path


def summarise(cases: list[dict]) -> dict:
    statuses = Counter(case["indicative_status"] for case in cases)
    arrangements = Counter(case["arrangement_type"] for case in cases)
    priorities = Counter(case["review_priority"] for case in cases)
    evidence_gaps = sum(case["evidence_gaps"] != "None identified" for case in cases)
    total_redress = round(sum(case["illustrative_total_redress"] for case in cases), 2)
    eligible = statuses["Indicatively eligible"]
    return {
        "total": len(cases), "statuses": statuses, "arrangements": arrangements,
        "priorities": priorities, "evidence_gaps": evidence_gaps,
        "total_redress": total_redress,
        "average_redress": round(total_redress / eligible, 2) if eligible else 0,
        "vulnerable": sum(case["customer_vulnerability"] for case in cases),
        "aged": sum(case["complaint_age_days"] > 180 for case in cases),
    }


def _money(value: float) -> str:
    return f"£{value:,.0f}"


def _bar(label: str, value: int, total: int, color: str) -> str:
    width = round(value / total * 100, 1) if total else 0
    return f'<div class="bar-row"><div class="bar-label"><span>{html.escape(label)}</span><strong>{value}</strong></div><div class="bar-track"><div class="bar-fill" style="width:{width}%;background:{color}"></div></div></div>'


def build_governance_summary(cases: list[dict], path: Path) -> None:
    s = summarise(cases)
    lines = [
        "# Motor Finance Commission Remediation — Governance Summary", "",
        "> Fictional portfolio demonstration. All eligibility and redress outputs require validation under the operative FCA rules.", "",
        "## Executive summary", "",
        f"The review population contains **{s['total']} fictional agreements**. "
        f"The rules identify **{s['statuses']['Indicatively eligible']} indicative eligible**, "
        f"**{s['statuses']['Further investigation']} further-investigation**, and "
        f"**{s['statuses']['Excluded / no redress indicator'] + s['statuses']['No redress indicator']} other/no-redress-indicator** cases.", "",
        f"Illustrative total redress is **{_money(s['total_redress'])}**, averaging **{_money(s['average_redress'])}** across indicatively eligible cases. These figures are not real compensation calculations.", "",
        "## Arrangement indicators", "", "| Arrangement | Agreements |", "|---|---:|",
    ]
    for label, count in s["arrangements"].items():
        lines.append(f"| {label} | {count} |")
    lines.extend(["", "## Management attention", "",
        f"- Resolve evidence gaps in {s['evidence_gaps']} cases.",
        f"- Prioritise {s['priorities']['Urgent']} urgent cases involving vulnerability or deceased customers.",
        f"- Review ownership and next actions for {s['aged']} complaints aged over 180 days.",
        "- Revalidate eligibility and redress after the legal challenge and any FCA rule changes.",
        "- Record source evidence, calculation assumptions, QA and final human approval.", "",
        "## Regulatory status", "",
        "The FCA scheme was introduced in March 2026, but parts are suspended during legal challenges. This dashboard is a readiness and portfolio demonstration, not an instruction to calculate or pay compensation.", ""])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def build_dashboard(cases: list[dict], path: Path) -> None:
    template = Path(__file__).with_name("dashboard_template.html").read_text(encoding="utf-8")
    ordered = sorted(
        cases,
        key=lambda x: (
            {"Urgent": 0, "Priority": 1, "Standard": 2}[x["review_priority"]],
            -x["illustrative_total_redress"],
        ),
    )
    rows = "".join(
        f'''<tr data-status="{html.escape(c['indicative_status'])}" data-priority="{c['review_priority']}" data-search="{html.escape(' '.join((c['case_id'], c['product'], c['broker_group'], c['arrangement_type'])).lower())}">
        <td><strong>{c['case_id']}</strong><small>{html.escape(c['product'])} · {c['agreement_start'][:4]}</small></td>
        <td><span class="status-pill">{html.escape(c['indicative_status'])}</span></td>
        <td><span class="priority-pill {c['review_priority'].lower()}">{c['review_priority']}</span></td>
        <td>{html.escape(c['arrangement_type'])}<small>{html.escape(c['broker_group'])}</small></td>
        <td>{_money(c['commission_paid'])}</td>
        <td>{_money(c['illustrative_total_redress'])}</td>
        <td>{html.escape(c['evidence_gaps'])}</td></tr>'''
        for c in ordered
    )
    case_json = json.dumps(cases, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    page = template.replace("__CASE_DATA__", case_json).replace("__CASE_ROWS__", rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(page, encoding="utf-8")
