import pandas as pd
import numpy as np

df = pd.read_csv("data_raw.csv")

# ---------- 1. Engagement Index ----------
# Standardize (z-score) the 4 satisfaction/involvement pillars, then average -> rescale to 0-100
pillars = ["JobInvolvement", "JobSatisfaction", "EnvironmentSatisfaction", "RelationshipSatisfaction"]
z = (df[pillars] - df[pillars].mean()) / df[pillars].std()
df["EngagementIndex_Z"] = z.mean(axis=1)
# rescale 0-100 for readability
mn, mx = df["EngagementIndex_Z"].min(), df["EngagementIndex_Z"].max()
df["EngagementIndex"] = ((df["EngagementIndex_Z"] - mn) / (mx - mn) * 100).round(1)

def engagement_band(x):
    if x >= 70: return "High"
    elif x >= 40: return "Moderate"
    else: return "Low"
df["EngagementBand"] = df["EngagementIndex"].apply(engagement_band)

# ---------- 2. Burnout Risk Score ----------
# Rule-based + weighted score: OverTime + low WLB + high travel + long tenure w/o promotion
travel_weight = {"Non-Travel": 0, "Travel_Rarely": 1, "Travel_Frequently": 2}
df["TravelStress"] = df["BusinessTravel"].map(travel_weight)

df["BurnoutRiskScore"] = (
    (df["OverTime"].eq("Yes")).astype(int) * 3 +
    (df["WorkLifeBalance"] <= 2).astype(int) * 3 +
    df["TravelStress"] +
    (df["YearsSinceLastPromotion"] >= 4).astype(int) * 1 +
    (df["JobSatisfaction"] <= 2).astype(int) * 1
)
# Max possible score = 3+3+2+1+1 = 10
def burnout_level(s):
    if s >= 6: return "High"
    elif s >= 3: return "Medium"
    else: return "Low"
df["BurnoutRiskLevel"] = df["BurnoutRiskScore"].apply(burnout_level)

# ---------- 3. Work-Life Balance Index ----------
df["WorkLifeBalanceIndex"] = df["WorkLifeBalance"] / 4 * 100  # normalize 1-4 -> 25-100

# ---------- 4. Satisfaction Stability Score ----------
# Lower std across satisfaction dims = more stable/consistent experience. Invert so higher = more stable.
sat_cols = ["JobSatisfaction", "EnvironmentSatisfaction", "RelationshipSatisfaction"]
sat_std = df[sat_cols].std(axis=1)
df["SatisfactionStabilityScore"] = (100 - (sat_std / sat_std.max() * 100)).round(1)

# ---------- 5. Workload Stress Indicator ----------
df["WorkloadStressIndicator"] = (
    df["TravelStress"] * 10 + df["OverTime"].eq("Yes").astype(int) * 30 +
    (df["DistanceFromHome"] / df["DistanceFromHome"].max() * 20)
).round(1)

# ---------- Tenure / career stage buckets ----------
def tenure_bucket(y):
    if y <= 2: return "0-2 yrs"
    elif y <= 5: return "3-5 yrs"
    elif y <= 10: return "6-10 yrs"
    else: return "10+ yrs"
df["TenureBucket"] = df["YearsAtCompany"].apply(tenure_bucket)

df.to_csv("employee_data_enriched.csv", index=False)
print("Saved enriched dataset:", df.shape)
print(df[["EngagementIndex","EngagementBand","BurnoutRiskScore","BurnoutRiskLevel",
          "WorkLifeBalanceIndex","SatisfactionStabilityScore","WorkloadStressIndicator"]].describe())
print(df["EngagementBand"].value_counts())
print(df["BurnoutRiskLevel"].value_counts())
