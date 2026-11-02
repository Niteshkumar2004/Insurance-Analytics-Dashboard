import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Insurance Analytics", page_icon="🛡️", layout="wide")

@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_csv(Path(__file__).parent / "data" / "insurance_data.csv")
    data["policy_date"] = pd.to_datetime(data["policy_date"], errors="coerce")
    data["claim_amount"] = pd.to_numeric(data["claim_amount"], errors="coerce").fillna(0)
    data["annual_premium"] = pd.to_numeric(data["annual_premium"], errors="coerce").fillna(0)
    data["has_claim"] = pd.to_numeric(data["has_claim"], errors="coerce").fillna(0).astype(int)
    return data

st.title("🛡️ Insurance Analytics Dashboard")
st.caption("Explore policy performance, claims trends, risk indicators and unusual claim patterns.")

with st.sidebar:
    st.header("Dashboard controls")
    uploaded = st.file_uploader("Upload your insurance CSV (optional)", type=["csv"])
    data = load_data(uploaded)
    types = st.multiselect("Insurance type", sorted(data["insurance_type"].dropna().unique()),
                           default=sorted(data["insurance_type"].dropna().unique()))
    regions = st.multiselect("Region", sorted(data["region"].dropna().unique()),
                             default=sorted(data["region"].dropna().unique()))
    st.info("Demo data is synthetic and created for learning purposes.")

filtered = data[data["insurance_type"].isin(types) & data["region"].isin(regions)].copy()
if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()

policies = len(filtered)
claims = int(filtered["has_claim"].sum())
claim_rate = claims / policies * 100 if policies else 0
premiums = filtered["annual_premium"].sum()
losses = filtered["claim_amount"].sum()
loss_ratio = losses / premiums * 100 if premiums else 0

c1,c2,c3,c4 = st.columns(4)
c1.metric("Total policies", f"{policies:,}")
c2.metric("Claims reported", f"{claims:,}")
c3.metric("Claim frequency", f"{claim_rate:.1f}%")
c4.metric("Incurred loss ratio", f"{loss_ratio:.1f}%")

st.divider()
left, right = st.columns(2)
with left:
    st.subheader("Policies by insurance type")
    counts = filtered.groupby("insurance_type", as_index=False).size().rename(columns={"size":"policies"})
    st.plotly_chart(px.bar(counts, x="insurance_type", y="policies", color="insurance_type",
                           title="Policy distribution"), use_container_width=True)
with right:
    st.subheader("Claims by region")
    region_claims = filtered.groupby("region", as_index=False)["claim_amount"].sum()
    st.plotly_chart(px.pie(region_claims, names="region", values="claim_amount",
                           title="Claim amount share by region", hole=.45), use_container_width=True)

st.subheader("Monthly claims trend")
monthly = filtered.set_index("policy_date").resample("MS").agg(
    claim_amount=("claim_amount","sum"), claims=("has_claim","sum")).reset_index()
st.plotly_chart(px.line(monthly, x="policy_date", y="claim_amount", markers=True,
                        title="Monthly incurred claim amount"), use_container_width=True)

st.divider()
st.subheader("Risk and unusual-claim review")
# Transparent demonstration rules, not a validated fraud model.
claimants = filtered[filtered["has_claim"] == 1].copy()
if not claimants.empty:
    threshold = claimants["claim_amount"].quantile(.95)
    claimants["review_reason"] = np.where(
        claimants["claim_amount"] >= threshold, "Claim amount in top 5% of this view",
        np.where(claimants["days_to_claim"] <= 3, "Claim reported within 3 days", "No rule triggered")
    )
    flagged = claimants[(claimants["claim_amount"] >= threshold) | (claimants["days_to_claim"] <= 3)]
    a,b,c = st.columns(3)
    a.metric("Claims needing review", f"{len(flagged):,}")
    b.metric("High-value threshold", f"₹{threshold:,.0f}")
    c.metric("Average claim amount", f"₹{claimants['claim_amount'].mean():,.0f}")
    st.caption("Review flags are simple educational rules, not proof of fraud. Human investigation is required.")
    st.dataframe(flagged[["policy_id","insurance_type","region","claim_amount","days_to_claim","review_reason"]]
                 .sort_values("claim_amount", ascending=False), use_container_width=True, hide_index=True)
else:
    st.info("No claims in the current filter selection.")

st.subheader("Policy-level data")
st.dataframe(filtered, use_container_width=True, hide_index=True)
st.download_button("Download filtered data as CSV", filtered.to_csv(index=False).encode("utf-8"),
                   file_name="insurance_filtered_data.csv", mime="text/csv")

st.divider()
st.caption("Built with Python, Streamlit, Pandas and Plotly • Demo dataset • For educational use only")
