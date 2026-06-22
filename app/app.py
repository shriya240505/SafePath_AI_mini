import streamlit as st
import pandas as pd

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(
    page_title="Women Safety Analytics Dashboard",
    layout="wide"
)

# ======================
# LOAD DATA
# ======================
df = pd.read_csv("data/CrimesOnWomenData.csv")

# CLEAN STATE NAMES (IMPORTANT FIX)
df["State"] = df["State"].str.strip().str.title()

# ======================
# WSI CALCULATION (NORMALIZED)
# ======================
crime_cols = ["Rape", "K&A", "DD", "AoW", "AoM", "DV", "WT"]

# Min-Max Scaling
# Safe Min-Max Scaling (FIX)
for col in crime_cols:
    min_val = df[col].min()
    max_val = df[col].max()

    if max_val == min_val:
        df[col + "_scaled"] = 0
    else:
        df[col + "_scaled"] = (df[col] - min_val) / (max_val - min_val)

df["Crime_Risk_Score"] = (
    df["Rape_scaled"] * 0.30 +
    df["K&A_scaled"] * 0.25 +
    df["AoW_scaled"] * 0.20 +
    df["DV_scaled"] * 0.15 +
    df["DD_scaled"] * 0.05 +
    df["WT_scaled"] * 0.05
)

df["WSI"] = 100 - (df["Crime_Risk_Score"] * 100)

# ======================
# TITLE
# ======================
st.title("🚨 Women Safety Analytics Dashboard")
st.caption("SafePath AI - Phase 1 | Data Analytics Project")

# ======================
# SIDEBAR
# ======================
st.sidebar.title("Filters")

selected_state = st.sidebar.selectbox(
    "Select State",
    sorted(df["State"].unique())
)

year = st.sidebar.selectbox(
    "Select Year",
    sorted(df["Year"].unique())
)

st.sidebar.markdown("---")
st.sidebar.info("Women Safety Analytics Dashboard\nSafePath AI Phase 1")

# ======================
# KPI CARDS
# ======================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Records", len(df))

with col2:
    st.metric("Years Covered", "2001-2021")

with col3:
    st.metric("Avg Safety Score", round(df["WSI"].mean(), 2))

st.divider()

# ======================
# FILTER DATA
# ======================
filtered_df = df[
    (df["State"] == selected_state) &
    (df["Year"] == year)
]

# EMPTY CHECK FIX (IMPORTANT)
if filtered_df.empty:
    st.warning("No data available for selected State and Year")
    st.stop()

st.subheader(f"📍 {selected_state} - {year}")

# ======================
# WSI SCORE
# ======================
wsi_score = round(filtered_df["WSI"].mean(), 2)

st.subheader("🧠 Women Safety Index")
st.metric("WSI Score", wsi_score)
st.progress(wsi_score / 100)

# Safety Category
if wsi_score >= 95:
    st.success("🟢 Very Safe")
elif wsi_score >= 85:
    st.warning("🟡 Moderate Risk")
else:
    st.error("🔴 High Risk")

st.divider()

# ======================
# TOP CRIME CATEGORY (IMPORTANT INSIGHT)
# ======================
top_crime = filtered_df[crime_cols].iloc[0].idxmax()
st.info(f"🚨 Most Reported Crime Category: {top_crime}")

st.divider()

# ======================
# SAFE STATES
# ======================
st.subheader("🏆 Top 10 Safest States")

safe_states = (
    df.groupby("State")[crime_cols]
    .mean()
    .sum(axis=1)
    .sort_values()
    .head(10)
)
st.bar_chart(safe_states)
st.dataframe(safe_states.round(2))

# ======================
# RISKY STATES
# ======================
st.subheader("⚠️ Top 10 Riskiest States")

risky_states = (
    df.groupby("State")[crime_cols]
    .mean()
    .sum(axis=1)
    .sort_values(ascending=False)
    .head(10)
)


st.bar_chart(risky_states)
st.dataframe(risky_states.round(2))

# ======================
# TREND
# ======================
st.subheader("📈 Crime Trend (Selected State)")

trend = df[df["State"] == selected_state]
trend_data = trend.groupby("Year")["Rape"].sum()

st.line_chart(trend_data)

st.divider()

# ======================
# INSIGHTS
# ======================
st.subheader("💡 Key Insights")

st.markdown("""
- WSI is computed using normalized crime indicators.
- Higher WSI means safer state.
- Uttar Pradesh and Bihar show higher crime intensity historically.
- Domestic Violence and Assault dominate overall crime pattern.
""")

st.divider()

# ======================
# FUTURE SCOPE
# ======================
st.subheader("🗺️ SafePath AI Future Features")

st.info("""
- Route Safety Score
- Street Light Analysis
- Crowd Density Detection
- Nearby Hospitals & Police Stations
- Real-time Safe Navigation System
""")