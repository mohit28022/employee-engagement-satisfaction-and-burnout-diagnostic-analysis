# 🛡️ Employee Engagement, Satisfaction & Burnout Diagnostic — Palo Alto Networks

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-app-FF4B4B?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

An HR analytics project that shifts attrition analysis from **reactive** to **preventive** by building an
early-warning engagement and burnout diagnostic on employee data, delivered as an interactive Streamlit dashboard.

> Built for the **Unified Mentor × Palo Alto Networks** HR analytics project brief.

🔗 **Live dashboard:** _add your Streamlit Cloud link here after deploying_
📄 **Research paper:** [`research_paper.md`](research_paper.md)
📊 **Executive summary:** [`executive_summary.md`](executive_summary.md)

---

## 🎯 Problem Statement

Palo Alto Networks currently lacks:
- A unified engagement health index
- Clear visibility into burnout-prone employee groups
- Understanding of how overtime, work-life balance, and satisfaction interact
- Preventive insights into employee experience deterioration

As a result, HR interventions are often late-stage and reactive. This project builds the diagnostics to fix that.

## 🧮 Methodology

| Step | What it does |
|---|---|
| **Data validation** | Checked ordinal scales (1–4), confirmed no missing values (n=1,470) |
| **Engagement Index** | Z-score standardized composite of `JobInvolvement`, `JobSatisfaction`, `EnvironmentSatisfaction`, `RelationshipSatisfaction`, rescaled 0–100 |
| **Burnout Risk Score** | Weighted rule-based score: OverTime (+3), Low Work-Life Balance ≤2 (+3), Travel intensity (+0–2), 4+ years since promotion (+1), Job Satisfaction ≤2 (+1) → banded Low / Medium / High |
| **Work-Life Balance Index** | `WorkLifeBalance` rescaled to 0–100 |
| **Satisfaction Stability Score** | Inverse of the standard deviation across the three satisfaction dimensions — a high score means an employee's experience is consistent, not just high on average |
| **Workload Stress Indicator** | Composite of travel frequency, overtime, and commute distance |

Full feature-engineering code: [`feature_engineering.py`](feature_engineering.py)

## 📊 Key Findings

- Employees flagged **High burnout risk** leave at **~29%**, vs. **~8%** for Low-risk employees — burnout risk is a strong leading indicator, well before an exit interview.
- Employees who eventually left had a **~9-point lower** average Engagement Index than those who stayed (46.6 vs. 55.6).
- **Research Scientists, Sales Executives, and Laboratory Technicians** carry the largest raw counts of High-burnout-risk employees.
- Work-life balance is comparatively **weakest in R&D**, PANW's largest department (961 employees).
- Engagement dips slightly at **Job Level 3**, suggesting a mid-career "squeeze" worth investigating with managers.

_(See `research_paper.md` for the full write-up, charts, and recommendations.)_

## 🖥️ Dashboard Modules

1. **Engagement Health Overview** — org-wide engagement score, satisfaction distribution, satisfaction-pillar radar
2. **Burnout Risk Dashboard** — risk segmentation, overtime × work-life-balance heatmap, attrition-by-risk chart
3. **Role & Career Stage Analysis** — engagement by job role/level/tenure, stagnation vs. engagement scatter
4. **Manager Action Panel** — a filterable, downloadable priority intervention list for at-risk employees

**Interactive controls:** department filter, job-role filter, overtime toggle, engagement threshold slider, tenure range selector.

## 🚀 Run Locally

```bash
git clone https://github.com/<your-username>/employee-engagement-satisfaction-and-burnout-diagnostic-analysis.git
cd employee-engagement-satisfaction-and-burnout-diagnostic-analysis
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Project Structure

```
├── app.py                        # Streamlit dashboard
├── feature_engineering.py        # KPI / engagement / burnout scoring logic
├── data_raw.csv                  # Source dataset
├── employee_data_enriched.csv    # Dataset with computed KPIs (used by app.py)
├── research_paper.md             # Full EDA, insights & recommendations
├── executive_summary.md          # 1-page summary for stakeholders
├── requirements.txt
└── README.md
```

## 🛠️ Tech Stack

`Python` · `Pandas` · `NumPy` · `Plotly` · `Streamlit`

## 📌 Dataset

1,470 employee records covering demographics, compensation, satisfaction ratings, tenure, and attrition status.
See `research_paper.md` for the full field dictionary.

## ⚠️ Disclaimer

This dataset is a publicly available synthetic/anonymized HR analytics dataset used for educational purposes and
is **not** actual internal data from Palo Alto Networks.

---

<sub>Built with ❤️ using Streamlit · Feel free to fork and adapt for other organizations.</sub>
