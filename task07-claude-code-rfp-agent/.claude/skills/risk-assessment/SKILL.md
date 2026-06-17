---
name: risk-assessment
description: BTS-Synthetic internal risk assessment framework. Three-step process: (1) build a risk framework from the RFP, (2) assess the drafted proposal against that framework, (3) produce a self-contained interactive HTML risk dashboard. Use whenever producing an internal risk vs. revenue analysis before a proposal goes out. Trigger on any request to assess risk, score a deal, review a proposal for risk, or produce a risk dashboard.
---

# Risk Assessment — Three-Step Process

## Step 1 — Build the Risk Framework from the RFP

Read the RFP and extract every clause that creates financial, legal, or operational exposure. Map each clause to a risk category below. Assign a base risk contribution (%) and severity. This becomes the personalised risk register for this deal.

### Risk Categories

**A. Commercial Risk**

| Pattern to look for | Base risk | Severity |
|---|---|---|
| Discount demanded > 25% off list | 1.5% | HIGH |
| Price freeze for full contract term (no escalators) | 1.5% | HIGH |
| Payment terms Net 90 or longer | 0.5% | MEDIUM |
| MFN / most-favoured-nation pricing clause | 2.0% | BLOCKER |
| Short initial term (< 2 years) at Enterprise tier | 0.5% | LOW |

**B. Contractual / Legal Risk**

| Pattern to look for | Base risk | Severity |
|---|---|---|
| Uncapped vendor liability for data breach | 3.0% | BLOCKER |
| IP assignment — all work product vests in customer | 1.5% | BLOCKER |
| Termination for convenience with < 60 days notice | 0.5% | MEDIUM |
| Immediate termination right on any SLA miss | 2.0% | BLOCKER |
| Customer veto over all subprocessors | 1.5% | HIGH |
| Unannounced audits, > 2 per year, vendor pays | 1.0% | HIGH |
| SLA > 99.95% demanded (our Enterprise cap) | 0.5% | MEDIUM |
| Uncapped indemnification for regulatory fines | 2.5% | BLOCKER |

### Aggregate Risk Calculation

Sum the base risk % for every clause present in the RFP. This is the **gross risk score** — the worst-case exposure if every clause is accepted.

A deal-ready proposal must bring the **net risk score** (after negotiating key clauses) to ≤ 5%.

---

## Step 2 — Assess the Proposal

Read the proposal draft or the synthesised findings from the other specialists. For each risky clause identified in Step 1, determine:

- **Is it accepted as-is?** → clause risk counts in full
- **Is there a counter-position proposed?** → risk reduced by 50%
- **Is it rejected / redlined?** → risk drops to 0% for that clause

Also score the **revenue opportunity** (0–100):

| Signal present in the deal | Points |
|---|---|
| Enterprise tier, 3+ year term | +30 |
| Deal value > $500K / year | +20 |
| Named reference customer potential | +15 |
| Target vertical (manufacturing, IoT, industrial) | +15 |
| Deep Azure / Microsoft stack alignment | +10 |
| Competitive displacement (Databricks / Snowflake) | +10 |

**Decision thresholds:**

| Net risk | Revenue score | Action |
|---|---|---|
| ≤ 5% | Any | **Proceed** — standard redlines |
| 5–10% | ≥ 70 | **Escalate to VP** — must resolve blockers |
| 5–10% | < 70 | **No-bid or major redline** |
| > 10% | Any | **No-bid** |

---

## Step 3 — Produce the HTML Risk Dashboard

Output a **single self-contained HTML file** with no external CSS or JS dependencies. Save it as `outputs/risk-assessment-<customer>-<date>.html`.

### Page structure

**Header**
- Deal name and date
- Overall risk badge: green (≤ 5%) / amber (5–10%) / red (> 10%)
- Decision banner: "Proceed" / "Escalate to VP" / "No-bid" — styled prominently

**Risk Gauge (SVG arc)**
- Shows net risk % as a needle on a 0–15% arc
- Colour: green below 5%, amber 5–10%, red above 10%
- Updates in real time when clause toggles change

**Revenue Score Bar**
- Horizontal bar 0–100 with a gradient fill
- Labelled: "Revenue Attractiveness"

**Clause Toggle Cards (grid layout)**

One card per risky clause found in Step 1. Each card shows:
- Clause name (short, business-readable)
- Risk contribution: e.g. "+2.0%"
- Severity badge: `BLOCKER` (dark red) / `HIGH` (orange) / `MEDIUM` (yellow) / `LOW` (grey)
- Toggle checkbox: "Accepted in proposal?" — checked = risk counts, unchecked = 0%
- Expandable section (click to reveal): our counter-position text in plain English
- Pre-populate each toggle based on Step 2 findings (accepted/counter/rejected)

**Summary Table**
- Left column: "Clauses accepted (risk carried)" — sum of their %
- Right column: "Clauses negotiated/rejected (risk saved)"

**Footer**
- "This is an internal risk assessment. Do not share with the customer."
- Timestamp

### Interactivity (vanilla JS, inline)

- Toggling any checkbox instantly recalculates aggregate risk and re-renders the gauge, badge, and decision banner
- "Show worst-case" button: sets all toggles to accepted
- "Show proposed position" button: resets to the Step 2 defaults
- Gauge needle animates on value change (CSS transition 0.4s)

### Colour palette

```
Background:  #0f172a
Card:        #1e293b
Border:      #334155
Text:        #e2e8f0
Green:       #22c55e
Amber:       #f59e0b
Red:         #ef4444
Blocker:     #7f1d1d  (badge background)
Accent:      #3b82f6
```

---

## Tone

Write clause names and counter-positions in plain business English — no legalese. Every BLOCKER card must include one sentence explaining the financial consequence if accepted (e.g. "Uncapped breach liability voids our cyber insurance policy ceiling of 24 months of fees.").
