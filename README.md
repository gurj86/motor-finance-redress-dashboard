# Motor Finance Redress Executive Decision & Assurance Toolkit

![Tests](https://img.shields.io/badge/tests-20%20passing-16794b)
![Data](https://img.shields.io/badge/data-100%20fictional%20agreements-2563eb)
![Status](https://img.shields.io/badge/status-portfolio%20demonstration-7c3aed)

A business-analysis portfolio demonstration showing how structured data, transparent assumptions and AI-assisted review could support a UK motor finance commission remediation programme.

## View the live toolkit

**[Open the Motor Finance Redress Executive Decision Toolkit](https://gurj86.github.io/motor-finance-redress-dashboard/)**

The live page opens directly into the working toolkit. Use the four tabs to explore:

1. **Executive view** — leadership KPIs, key trends, Consumer Duty outcomes and decisions required.
2. **Scenario modeller** — adjustable assumptions for exposure, completion rates, capacity and QA.
3. **Operations & assurance** — pipeline, ageing, data quality and AI/human control points.
4. **Case review** — searchable and filterable fictional case-level indicators.

> All agreements, customers, firms and monetary figures are fictional. The calculator is illustrative and must not be used for real compensation decisions.

## Regulatory context

The FCA introduced the Motor Finance Consumer Redress Scheme in March 2026. Parts of the scheme are currently suspended following legal challenges, with the hearing expected in December 2026 or February 2027. Firms must continue with the scheme activities that have not been suspended, including identifying relevant agreements and gathering information.

This project therefore distinguishes between:

- agreement identification and evidence gathering;
- indicative eligibility and exception flags;
- illustrative redress scenarios; and
- final decisions that require the operative FCA rules, complete evidence and accountable human approval.

Primary FCA sources:

- [Car finance claims — consumer guidance](https://www.fca.org.uk/consumers/car-finance-complaints)
- [Information for firms on motor finance complaints](https://www.fca.org.uk/firms/information-firms-motor-finance-complaints)
- [PS26/3 — Motor finance consumer redress scheme](https://www.fca.org.uk/publications/policy-statements/ps26-3-motor-finance-consumer-redress-scheme)

Regulatory assumptions in this demonstration are versioned to **17 September 2026**. Users must check the current FCA position before applying any methodology.

## What this demonstrates

- Structuring agreement, commission, disclosure and complaint information
- Identifying DCA, high-commission and contractual-tie indicators
- Applying transparent scope and exception checks
- Separating missing evidence from a negative decision
- Producing illustrative redress estimates with visible assumptions
- Prioritising vulnerable customers and high-impact cases
- Turning case-level remediation work into governance information
- Translating operational data into concise senior-leadership insight
- Stress-testing exposure and delivery capacity through transparent scenarios
- Presenting decisions, owners, actions and control implications
- Challenging unsupported AI conclusions and retaining human accountability

## Toolkit contents

The demonstration analyses 100 fictional motor finance agreements and displays:

- indicative in-scope, excluded and further-investigation populations;
- commission-arrangement indicators;
- illustrative principal redress and compensatory interest;
- redress caps and calculation exceptions;
- missing evidence and remediation ageing;
- vulnerable-customer and priority-review queues;
- root-cause and operational-readiness information; and
- an automatically generated governance summary;
- an executive leadership brief with clear “so what?” interpretation;
- a configurable scenario and capacity modeller;
- a Consumer Duty outcome lens and decision register; and
- a print-ready board-pack view.

## Business analyst approach

The toolkit is designed around four management questions:

1. **What is happening?** — portfolio size, indicative cohorts, exposure and ageing.
2. **Why does it matter?** — customer harm, evidence uncertainty, delivery risk and governance impact.
3. **What should happen next?** — prioritised actions, owners, timescales and escalation.
4. **What decision is required?** — approve assumptions, capacity, controls or evidence-retrieval activity.

The scenario modeller deliberately separates planning assumptions from regulatory rules. Changes update exposure, completion volumes, review duration and QA requirements without presenting the result as a final compensation calculation.

## My contribution

I designed the remediation use case, evidence fields, review questions, exception logic, management information and governance outputs using my Consumer Duty and financial-services remediation experience. I used AI to help translate the design into a working technical demonstration, then tested and challenged the outputs and controls.

The operating principle is **AI-assisted, evidence-led and human-accountable**.

## Quick start

No external Python packages are required:

```bash
python demo.py
python -m unittest discover -s tests -v
```

This generates the fictional dataset, dashboard and governance summary.

## Important limitations

The project does not:

- use real customer, lender, broker or employer data;
- connect to a live AI model;
- reproduce the FCA rulebook in full;
- establish legal liability or unfairness;
- make final eligibility decisions;
- calculate real compensation or payment instructions; or
- replace firm-approved methodology, legal advice or human review.

See [methodology and controls](docs/methodology.md) and the [plain-English interview guide](docs/interview_guide.md).
