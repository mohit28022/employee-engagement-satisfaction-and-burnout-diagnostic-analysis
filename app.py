"""
Employee Engagement, Satisfaction & Burnout Diagnostic Dashboard
Palo Alto Networks — HR Analytics
Built with Streamlit + Plotly
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------------------------------------------------------
# PAGE CONFIG & THEME
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="PANW Engagement & Burnout Diagnostic",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

PANW_RED = "#FA582D"
PANW_DARK = "#141414"
PANW_GRAY = "#4A4A4A"
ACCENT_GREEN = "#2ECC71"
ACCENT_AMBER = "#F5B041"
ACCENT_RED = "#E74C3C"

CUSTOM_CSS = f"""
<style>
    .stApp {{ background-color: #FAFAFA; }}
    [data-testid="stMetricValue"] {{ color: {PANW_DARK}; font-weight: 700; }}
    [data-testid="stMetricLabel"] {{ color: {PANW_GRAY}; }}
    .main-header {{
        font-size: 2.1rem; font-weight: 800; color: {PANW_DARK};
        border-left: 6px solid {PANW_RED}; padding-left: 14px; margin-bottom: 0px;
    }}
    .sub-header {{ color: {PANW_GRAY}; font-size: 0.95rem; margin-top:0; margin-bottom: 1.2rem;}}
    .kpi-card {{
        background: white; border-radius: 10px; padding: 16px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08); border-top: 4px solid {PANW_RED};
    }}
    section[data-testid="stSidebar"] {{ background-color: #141414; }}
    section[data-testid="stSidebar"] * {{ color: #EAEAEA !important; }}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

RISK_COLORS = {"Low": ACCENT_GREEN, "Medium": ACCENT_AMBER, "High": ACCENT_RED}
BAND_COLORS = {"High": ACCENT_GREEN, "Moderate": ACCENT_AMBER, "Low": ACCENT_RED}


# ----------------------------------------------------------------------------
# DATA LOADING
# ----------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("employee_data_enriched.csv")
    return df


df = load_data()

# ----------------------------------------------------------------------------
# SIDEBAR — FILTERS
# ----------------------------------------------------------------------------
st.sidebar.markdown("## 🛡️ PANW HR Diagnostics")
st.sidebar.markdown("Filter the workforce below. All modules update live.")
st.sidebar.markdown("---")

departments = st.sidebar.multiselect(
    "Department", options=sorted(df["Department"].unique()),
    default=sorted(df["Department"].unique())
)

roles = st.sidebar.multiselect(
    "Job Role", options=sorted(df["JobRole"].unique()),
    default=sorted(df["JobRole"].unique())
)

overtime_filter = st.sidebar.radio("OverTime", options=["All", "Yes", "No"], index=0, horizontal=True)

engagement_threshold = st.sidebar.slider(
    "Minimum Engagement Index", 0, 100, 0,
    help="Show only employees at or above this engagement score"
)

tenure_range = st.sidebar.slider(
    "Years at Company", int(df["YearsAtCompany"].min()), int(df["YearsAtCompany"].max()),
    (int(df["YearsAtCompany"].min()), int(df["YearsAtCompany"].max()))
)

st.sidebar.markdown("---")
st.sidebar.caption("Data: PANW HR records (n={:,})".format(len(df)))

# Apply filters
fdf = df[
    df["Department"].isin(departments) &
    df["JobRole"].isin(roles) &
    (df["EngagementIndex"] >= engagement_threshold) &
    (df["YearsAtCompany"].between(*tenure_range))
]
if overtime_filter != "All":
    fdf = fdf[fdf["OverTime"] == overtime_filter]

if fdf.empty:
    st.warning("No employees match the current filters. Adjust filters in the sidebar.")
    st.stop()

# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
st.markdown('<p class="main-header">Employee Engagement & Burnout Diagnostic</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Early-warning HR analytics — moving from reactive attrition analysis to preventive employee experience diagnostics</p>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Engagement Health Overview",
    "🔥 Burnout Risk Dashboard",
    "📈 Role & Career Stage Analysis",
    "🚨 Manager Action Panel",
])

# ============================================================================
# TAB 1 — ENGAGEMENT HEALTH OVERVIEW
# ============================================================================
with tab1:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Org Engagement Index", f"{fdf['EngagementIndex'].mean():.1f} / 100")
    c2.metric("Work-Life Balance Index", f"{fdf['WorkLifeBalanceIndex'].mean():.1f} / 100")
    c3.metric("Satisfaction Stability", f"{fdf['SatisfactionStabilityScore'].mean():.1f} / 100")
    c4.metric("Headcount (filtered)", f"{len(fdf):,}")

    st.markdown("#### Engagement Distribution")
    col1, col2 = st.columns([1.3, 1])
    with col1:
        fig = px.histogram(
            fdf, x="EngagementIndex", nbins=30, color_discrete_sequence=[PANW_RED],
            labels={"EngagementIndex": "Engagement Index"}
        )
        fig.update_layout(bargap=0.05, height=360, margin=dict(t=10))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        band_counts = fdf["EngagementBand"].value_counts().reindex(["High", "Moderate", "Low"]).fillna(0)
        fig2 = px.pie(
            names=band_counts.index, values=band_counts.values, hole=0.55,
            color=band_counts.index, color_discrete_map=BAND_COLORS
        )
        fig2.update_layout(height=360, margin=dict(t=10), showlegend=True)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("#### Satisfaction Pillars (org average)")
    pillars = ["JobInvolvement", "JobSatisfaction", "EnvironmentSatisfaction", "RelationshipSatisfaction"]
    pillar_avg = fdf[pillars].mean()
    fig3 = go.Figure()
    fig3.add_trace(go.Scatterpolar(
        r=pillar_avg.values, theta=pillars, fill='toself',
        line_color=PANW_RED, fillcolor="rgba(250,88,45,0.25)"
    ))
    fig3.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 4])), height=380, margin=dict(t=10))
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("#### Engagement by Department")
    dep = fdf.groupby("Department")["EngagementIndex"].mean().sort_values()
    fig4 = px.bar(dep, orientation="h", color=dep.values, color_continuous_scale="RdYlGn",
                  labels={"value": "Avg Engagement Index", "Department": ""})
    fig4.update_layout(height=280, margin=dict(t=10), coloraxis_showscale=False)
    st.plotly_chart(fig4, use_container_width=True)

# ============================================================================
# TAB 2 — BURNOUT RISK DASHBOARD
# ============================================================================
with tab2:
    risk_counts = fdf["BurnoutRiskLevel"].value_counts().reindex(["Low", "Medium", "High"]).fillna(0)
    c1, c2, c3 = st.columns(3)
    c1.metric("🟢 Low Risk", f"{int(risk_counts['Low']):,}", f"{risk_counts['Low']/len(fdf)*100:.0f}%")
    c2.metric("🟠 Medium Risk", f"{int(risk_counts['Medium']):,}", f"{risk_counts['Medium']/len(fdf)*100:.0f}%")
    c3.metric("🔴 High Risk", f"{int(risk_counts['High']):,}", f"{risk_counts['High']/len(fdf)*100:.0f}%")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Burnout Risk Composition")
        fig = px.pie(names=risk_counts.index, values=risk_counts.values, hole=0.5,
                     color=risk_counts.index, color_discrete_map=RISK_COLORS)
        fig.update_layout(height=340, margin=dict(t=10))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("#### Attrition Rate by Burnout Risk")
        attr_by_risk = fdf.groupby("BurnoutRiskLevel")["Attrition"].mean().reindex(["Low", "Medium", "High"]) * 100
        fig2 = px.bar(attr_by_risk, color=attr_by_risk.index, color_discrete_map=RISK_COLORS,
                      labels={"value": "Attrition Rate (%)", "BurnoutRiskLevel": ""})
        fig2.update_layout(height=340, margin=dict(t=10), showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("#### OverTime & Work-Life Balance Interaction")
    heat = fdf.pivot_table(index="WorkLifeBalance", columns="OverTime", values="EngagementIndex", aggfunc="mean")
    fig3 = px.imshow(heat, text_auto=".1f", color_continuous_scale="RdYlGn",
                      labels=dict(color="Avg Engagement"))
    fig3.update_layout(height=320, margin=dict(t=10))
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("#### Workload Stress by Travel Frequency")
    fig4 = px.box(fdf, x="BusinessTravel", y="WorkloadStressIndicator", color="BusinessTravel",
                  color_discrete_sequence=px.colors.sequential.Reds)
    fig4.update_layout(height=340, margin=dict(t=10), showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)

# ============================================================================
# TAB 3 — ROLE & CAREER STAGE ANALYSIS
# ============================================================================
with tab3:
    st.markdown("#### Engagement by Job Role")
    role_eng = fdf.groupby("JobRole")["EngagementIndex"].mean().sort_values()
    fig = px.bar(role_eng, orientation="h", color=role_eng.values, color_continuous_scale="RdYlGn",
                 labels={"value": "Avg Engagement Index", "JobRole": ""})
    fig.update_layout(height=420, margin=dict(t=10), coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Engagement by Job Level")
        lvl = fdf.groupby("JobLevel")["EngagementIndex"].mean()
        fig2 = px.line(lvl, markers=True, color_discrete_sequence=[PANW_RED],
                       labels={"value": "Avg Engagement Index", "JobLevel": "Job Level"})
        fig2.update_layout(height=340, margin=dict(t=10), showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
    with col2:
        st.markdown("#### Engagement by Tenure Stage")
        order = ["0-2 yrs", "3-5 yrs", "6-10 yrs", "10+ yrs"]
        ten = fdf.groupby("TenureBucket")["EngagementIndex"].mean().reindex(order)
        fig3 = px.line(ten, markers=True, color_discrete_sequence=[PANW_DARK],
                       labels={"value": "Avg Engagement Index", "TenureBucket": "Tenure"})
        fig3.update_layout(height=340, margin=dict(t=10), showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("#### Stagnation Signal: Years Since Last Promotion vs Engagement")
    fig4 = px.scatter(fdf, x="YearsSinceLastPromotion", y="EngagementIndex", color="BurnoutRiskLevel",
                       color_discrete_map=RISK_COLORS, opacity=0.7, trendline="lowess")
    fig4.update_layout(height=380, margin=dict(t=10))
    st.plotly_chart(fig4, use_container_width=True)

# ============================================================================
# TAB 4 — MANAGER ACTION PANEL
# ============================================================================
with tab4:
    st.markdown("#### 🚨 Priority Intervention List")
    st.caption("Employees with **High burnout risk** and/or **Low engagement** — surfaced for proactive 1:1 check-ins.")

    priority = fdf[(fdf["BurnoutRiskLevel"] == "High") | (fdf["EngagementBand"] == "Low")].copy()
    priority = priority.sort_values(["BurnoutRiskScore", "EngagementIndex"], ascending=[False, True])

    show_cols = ["Department", "JobRole", "JobLevel", "EngagementIndex", "EngagementBand",
                 "BurnoutRiskLevel", "OverTime", "WorkLifeBalance", "YearsAtCompany",
                 "YearsSinceLastPromotion"]

    st.dataframe(
        priority[show_cols].reset_index(drop=True),
        use_container_width=True, height=420
    )
    st.caption(f"⚠️ {len(priority):,} employees flagged out of {len(fdf):,} in current filter ({len(priority)/len(fdf)*100:.0f}%).")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Where the risk concentrates (by Department)")
        dep_risk = priority["Department"].value_counts()
        fig = px.bar(dep_risk, color_discrete_sequence=[PANW_RED],
                     labels={"value": "Flagged employees", "index": ""})
        fig.update_layout(height=320, margin=dict(t=10), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("#### Where the risk concentrates (by Role)")
        role_risk = priority["JobRole"].value_counts().head(8)
        fig2 = px.bar(role_risk, color_discrete_sequence=[PANW_DARK],
                      labels={"value": "Flagged employees", "index": ""})
        fig2.update_layout(height=320, margin=dict(t=10), showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.download_button(
        "⬇️ Download priority list (CSV)",
        priority[show_cols].to_csv(index=False),
        file_name="priority_intervention_list.csv",
        mime="text/csv"
    )

st.markdown("---")
st.caption("Built for the Unified Mentor × Palo Alto Networks Employee Engagement Diagnostic project. "
            "Engagement Index, Burnout Risk Score, and related KPIs are derived composite metrics — see README for methodology.")
