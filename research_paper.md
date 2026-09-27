# Employee Engagement, Satisfaction, and Burnout Diagnostic Analysis at Palo Alto Networks

**A preventive HR analytics research paper — Unified Mentor × Palo Alto Networks**

---

## 1. Background & Problem Statement

In a high-performance cybersecurity organization like Palo Alto Networks, burnout often precedes attrition, declining
engagement quietly erodes productivity and innovation, and poor work-life balance compounds into long-term turnover
risk. Historically, HR has diagnosed these problems only *after* an employee resigns — through exit interviews and
attrition reports. By then, the intervention window has closed.

This paper builds a **unified engagement health index**, a **burnout risk model**, and a set of supporting KPIs that
let HR identify at-risk employees and teams *before* they leave, using routinely collected HR data.

## 2. Dataset

- **1,470 employee records**, 31 original fields, 0 missing values
- Covers demographics, compensation, job role/level, satisfaction ratings (1–4 ordinal scales), overtime status,
  business travel frequency, tenure, and attrition outcome
- Departments: Research & Development (961), Sales (446), Human Resources (63)
- Overall attrition rate: **16.1%** (237 of 1,470)

## 3. Methodology

### 3.1 Data Validation & Normalization
All ordinal satisfaction/involvement fields (`JobInvolvement`, `JobSatisfaction`, `EnvironmentSatisfaction`,
`RelationshipSatisfaction`, `WorkLifeBalance`) were confirmed to fall within their documented 1–4 range with no
missing values, so no imputation was required. Continuous fields were left in their native units; composite scores
were built on z-standardized inputs to keep pillars comparable.

### 3.2 Engagement Index
A composite **Engagement Index (0–100)** was built by z-score standardizing four pillars —
`JobInvolvement`, `JobSatisfaction`, `EnvironmentSatisfaction`, and `RelationshipSatisfaction` — averaging them, and
rescaling to a 0–100 range for interpretability. Employees are banded as **High (≥70)**, **Moderate (40–69)**, or
**Low (<40)**.

### 3.3 Burnout Risk Score
A weighted, rule-based score (0–10) flags burnout exposure from observable HR signals:

| Signal | Condition | Weight |
|---|---|---|
| Overtime | `OverTime = Yes` | +3 |
| Work-life balance | `WorkLifeBalance ≤ 2` | +3 |
| Travel intensity | Non-Travel / Rarely / Frequently | +0 / +1 / +2 |
| Promotion stagnation | `YearsSinceLastPromotion ≥ 4` | +1 |
| Job dissatisfaction | `JobSatisfaction ≤ 2` | +1 |

Scores are banded **Low (0–2)**, **Medium (3–5)**, **High (6–10)**.

### 3.4 Supporting KPIs
- **Work-Life Balance Index** — `WorkLifeBalance` rescaled to 0–100
- **Satisfaction Stability Score** — inverse of the standard deviation across the three satisfaction dimensions;
  a high score means an employee's experience is *consistently* positive (or negative) rather than volatile
- **Workload Stress Indicator** — composite of travel intensity, overtime, and commute distance

## 4. Key Findings

### 4.1 Engagement is materially lower among employees who eventually left

![Engagement vs Attrition](assets/engagement_vs_attrition.png)

Employees who left the organization had an average Engagement Index of **46.6**, compared to **55.6** for those who
stayed — a **9-point gap**. Engagement was measurably deteriorating in the population that later attrited, well
before they resigned.

### 4.2 Burnout risk is a strong leading indicator of attrition

![Attrition by Burnout Risk](assets/attrition_by_burnout.png)

- **Low burnout risk** → 8.2% attrition rate
- **Medium burnout risk** → 20.0% attrition rate
- **High burnout risk** → **28.7% attrition rate** — more than 3.5x the low-risk group

This is the single clearest signal in the dataset: burnout risk band alone stratifies attrition risk by a factor
of ~3.5x, and it can be computed the day an employee's HR record is entered — no waiting for a resignation.

### 4.3 Burnout risk composition across the workforce

![Burnout Composition](assets/burnout_composition.png)

15% of the workforce currently sits in the **High** burnout risk band, and 41% in **Medium** — meaning **56% of
employees carry at least moderate burnout exposure**, a much larger addressable population than the 16% who actually
attrite in a given period.

### 4.4 Department-level engagement gaps

![Engagement by Department](assets/engagement_by_department.png)

Engagement varies meaningfully by department, and **Research & Development — PANW's largest department at 961
employees — also shows comparatively weaker work-life balance**, making it the highest-leverage target for
intervention by sheer headcount.

### 4.5 Overtime and work-life balance interact, not just add

![Overtime x WLB Heatmap](assets/overtime_wlb_heatmap.png)

Engagement does not decline uniformly with overtime — it is the **combination** of overtime *and* poor work-life
balance that suppresses engagement most, which is why the burnout score treats them as compounding signals rather
than a single flag.

### 4.6 Career-stage findings
- Engagement dips slightly at **Job Level 3**, a common "mid-career squeeze" point worth exploring qualitatively
  with managers (compensation plateau, unclear promotion path, or scope ambiguity).
- Employees **4+ years since their last promotion** show elevated burnout risk scores, reinforcing promotion
  stagnation as a genuine engagement lever, not just a compensation one.
- Concentration of **High-burnout-risk** employees by role: Research Scientists, Sales Executives, and Laboratory
  Technicians carry the largest raw counts — useful for prioritizing manager outreach.

## 5. Recommendations

1. **Operationalize the Burnout Risk Score as a standing HR metric**, refreshed quarterly, with High-risk employees
   automatically routed to the Manager Action Panel for a check-in — not a performance review.
2. **Target Research & Development for a work-life balance intervention** given its combination of largest headcount
   and comparatively weaker WLB index.
3. **Review promotion cadence for employees 4+ years without advancement**, especially where burnout risk is already
   elevated — this is a controllable HR lever, unlike compensation benchmarking cycles.
4. **Treat overtime + poor work-life balance as a compounding risk, not two independent flags** — policies that cap
   overtime *only* for employees already reporting WorkLifeBalance ≤ 2 will have outsized impact per intervention.
5. **Re-run this diagnostic on a rolling basis** (e.g., quarterly) so engagement trends — not just snapshots — become
   visible, and so the model's leading-indicator value against attrition can be validated longitudinally.

## 6. Limitations

- The Engagement Index and Burnout Risk Score are **derived, rule-based composites** validated against attrition as
  a contextual outcome, not clinically validated psychometric instruments — they should be tested against future
  attrition cohorts and refined over time.
- The dataset is a single, static snapshot; true early-warning value requires tracking these KPIs **over time** per
  employee, which this analysis was not able to do with cross-sectional data.
- This is a publicly available HR analytics dataset used for educational purposes, adapted with a Palo Alto Networks
  framing — it does not reflect PANW's actual internal HR data.

## 7. Conclusion

This project reframes HR analytics from a reactive, post-resignation exercise into a preventive diagnostic. By
combining a standardized Engagement Index with a compounding Burnout Risk Score, HR can identify the ~56% of the
workforce carrying at least moderate burnout exposure, prioritize outreach by department and role, and intervene
before attrition — not after.
