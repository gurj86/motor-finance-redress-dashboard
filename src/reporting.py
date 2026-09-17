"""Generate the motor finance governance dashboard and summary."""

from __future__ import annotations

import html
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
    s = summarise(cases)
    status_bars = "".join([
        _bar("Indicatively eligible", s["statuses"]["Indicatively eligible"], s["total"], "#16794b"),
        _bar("Further investigation", s["statuses"]["Further investigation"], s["total"], "#d18a00"),
        _bar("Excluded / no redress", s["statuses"]["Excluded / no redress indicator"] + s["statuses"]["No redress indicator"], s["total"], "#b42318"),
    ])
    arrangement_bars = "".join(_bar(k, v, s["total"], "#4f46e5") for k, v in s["arrangements"].items())
    rows = "".join(
        f'''<tr data-status="{html.escape(c['indicative_status'])}" data-priority="{c['review_priority']}">
        <td><strong>{c['case_id']}</strong><small>{c['product']} • {c['agreement_start'][:4]}</small></td>
        <td><span class="pill">{html.escape(c['indicative_status'])}</span></td>
        <td><span class="priority {c['review_priority'].lower()}">{c['review_priority']}</span></td>
        <td>{html.escape(c['arrangement_type'])}</td><td>{_money(c['commission_paid'])}</td>
        <td>{_money(c['illustrative_total_redress'])}</td><td>{html.escape(c['evidence_gaps'])}</td></tr>'''
        for c in sorted(cases, key=lambda x: ({"Urgent": 0, "Priority": 1, "Standard": 2}[x["review_priority"]], -x["illustrative_total_redress"]))
    )
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Motor Finance Redress Dashboard</title>
    <style>
    :root{{--ink:#172033;--muted:#667085;--line:#e4e7ec;--bg:#f3f6fb;--navy:#14213d}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 Inter,system-ui,sans-serif}}header{{background:linear-gradient(125deg,#101c35,#28447e);color:#fff;padding:34px max(24px,calc((100vw - 1180px)/2)) 54px}}header p{{color:#d8e2ff;max-width:820px}}h1{{margin:0;font-size:clamp(28px,4vw,42px);letter-spacing:-.03em}}.eyebrow{{color:#b9c7fb;font-size:12px;font-weight:800;letter-spacing:.13em;text-transform:uppercase}}main{{max-width:1180px;margin:-26px auto 48px;padding:0 22px}}.notice{{background:#fff5dc;border:1px solid #f2ce75;border-radius:12px;padding:13px 16px;margin-bottom:16px;color:#6b4f00}}.metrics{{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}}.card,.panel{{background:#fff;border:1px solid var(--line);border-radius:16px;box-shadow:0 8px 25px rgba(16,24,40,.05)}}.card{{padding:18px}}.card span{{display:block;color:var(--muted);font-size:11px;font-weight:800;text-transform:uppercase}}.card strong{{font-size:29px;display:block;margin-top:7px}}.card em{{font-size:12px;color:var(--muted);font-style:normal}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px}}.panel{{padding:22px}}.panel h2{{font-size:18px;margin:0 0 16px}}.bar-row{{margin:13px 0}}.bar-label{{display:flex;justify-content:space-between;font-size:13px;margin-bottom:5px}}.bar-track{{height:8px;background:#edf0f5;border-radius:9px;overflow:hidden}}.bar-fill{{height:100%;border-radius:9px}}.table-panel{{margin-top:16px;overflow:hidden}}.actions{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:13px}}button{{border:1px solid #cfd5e1;background:#fff;padding:8px 12px;border-radius:999px;font-weight:700;cursor:pointer}}button.active{{background:var(--navy);color:#fff}}.table-wrap{{overflow:auto}}table{{width:100%;border-collapse:collapse;min-width:950px}}th{{text-align:left;color:var(--muted);font-size:11px;text-transform:uppercase;padding:10px;border-bottom:1px solid var(--line)}}td{{padding:12px 10px;border-bottom:1px solid #edf0f4;vertical-align:top}}td small{{display:block;color:var(--muted)}}.pill,.priority{{display:inline-block;padding:4px 8px;border-radius:999px;font-size:11px;font-weight:800}}.pill{{background:#edf4ff;color:#1849a9}}.urgent{{background:#feeceb;color:#b42318}}.priority{{background:#fff5dc;color:#8a5b00}}.standard{{background:#e8f7ef;color:#16794b}}footer{{text-align:center;color:var(--muted);font-size:13px;padding:5px 20px 40px}}@media(max-width:850px){{.metrics{{grid-template-columns:repeat(2,1fr)}}.grid{{grid-template-columns:1fr}}}}@media(max-width:480px){{.metrics{{grid-template-columns:1fr}}}}
    </style></head><body><header><div class="eyebrow">Motor finance • Remediation readiness</div><h1>Commission Redress Dashboard</h1><p>Portfolio view of 100 fictional agreements, combining evidence gathering, scope indicators, illustrative redress scenarios and accountable human review.</p></header><main>
    <div class="notice"><strong>Regulatory status:</strong> parts of the FCA scheme are suspended during legal challenges. All figures are fictional and illustrative; no payment decision should be based on this dashboard.</div>
    <section class="metrics"><div class="card"><span>Agreements</span><strong>{s['total']}</strong><em>fictional records</em></div><div class="card"><span>Indicative eligible</span><strong>{s['statuses']['Indicatively eligible']}</strong><em>human validation required</em></div><div class="card"><span>Illustrative redress</span><strong>{_money(s['total_redress'])}</strong><em>not for payment</em></div><div class="card"><span>Average scenario</span><strong>{_money(s['average_redress'])}</strong><em>eligible indicators only</em></div><div class="card"><span>Evidence gaps</span><strong>{s['evidence_gaps']}</strong><em>investigation required</em></div></section>
    <section class="grid"><div class="panel"><h2>Indicative review status</h2>{status_bars}</div><div class="panel"><h2>Commission arrangement recorded</h2>{arrangement_bars}</div><div class="panel"><h2>Operational readiness</h2><ul><li>{s['priorities']['Urgent']} urgent human reviews</li><li>{s['aged']} complaints aged over 180 days</li><li>{s['vulnerable']} vulnerability indicators</li><li>Revalidate calculations after legal challenge</li></ul></div><div class="panel"><h2>Calculation control</h2><p>The scenario uses a simplified hybrid calculation and visible caps based on high-level FCA consumer guidance. It deliberately prevents payment instructions and requires source evidence, QA and approval.</p></div></section>
    <section class="panel table-panel"><h2>Human-review queue</h2><div class="actions"><button class="active" data-filter="All">All</button><button data-filter="Urgent">Urgent</button><button data-filter="Indicatively eligible">Indicatively eligible</button><button data-filter="Further investigation">Further investigation</button></div><div class="table-wrap"><table><thead><tr><th>Case</th><th>Indicative status</th><th>Priority</th><th>Arrangement</th><th>Commission</th><th>Illustrative redress</th><th>Evidence gaps</th></tr></thead><tbody>{rows}</tbody></table></div></section></main>
    <footer>Fictional portfolio demonstration • FCA position checked 17 September 2026 • Final decisions remain with accountable human reviewers</footer><script>const b=[...document.querySelectorAll('button[data-filter]')],r=[...document.querySelectorAll('tbody tr')];b.forEach(x=>x.addEventListener('click',()=>{{b.forEach(y=>y.classList.remove('active'));x.classList.add('active');const f=x.dataset.filter;r.forEach(z=>z.style.display=f==='All'||z.dataset.status===f||z.dataset.priority===f?'':'none')}}));</script></body></html>'''
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(page, encoding="utf-8")

