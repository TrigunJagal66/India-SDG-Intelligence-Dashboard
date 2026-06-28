import streamlit as st
import pandas as pd
import plotly.express as px

from sdg_engine import (
    master,
    generate_state_report
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="India SDG Dashboard",
    layout="wide"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🇮🇳 India SDG State Intelligence Dashboard")
st.markdown("""
This dashboard analyzes Sustainable Development Goal (SDG) performance across Indian states using machine learning, clustering, and a policy recommendation engine.
""")

# --------------------------------------------------
# STATE SELECTION
# --------------------------------------------------

st.sidebar.title("Navigation")

state = st.sidebar.selectbox(
    "Select State",
    sorted(master["state"].unique())
)

report = generate_state_report(state)

cluster_df = master[
    master["cluster"] == report["cluster_id"]
]

cluster_avg = cluster_df.mean(
    numeric_only=True
)

# --------------------------------------------------
# METRICS
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Composite Score",
        report["composite_score"]
    )

with col2:
    st.metric(
        "Strengths",
        report["strength_count"]
    )

with col3:
    st.metric(
        "Weaknesses",
        report["weakness_count"]
    )

with col4:
    st.metric(
        "Neutral",
        report["neutral_count"]
    )

# --------------------------------------------------
# STATE PROFILE
# --------------------------------------------------

st.divider()

st.subheader("📍 State Profile")

st.info(
    f"""
State: {report['state']}

Cluster: {report['cluster']}

Composite SDG Score: {report['composite_score']}
"""
)

# --------------------------------------------------
# CLUSTER MEMBERS
# --------------------------------------------------

cluster_states = master[
    master["cluster"] == report["cluster_id"]
]["state"].tolist()

st.subheader("🏘️ States in the Same Cluster")

cluster_df = pd.DataFrame({
    "States": sorted(cluster_states)
})

st.dataframe(
    cluster_df,
    use_container_width=True
)







# --------------------------------------------------
# STRENGTHS & WEAKNESSES
# --------------------------------------------------

left_col, right_col = st.columns(2)

# ---------- STRENGTHS ----------

with left_col:

    st.subheader("✅ Key Strengths")

    if report["strengths"]:

        strengths_df = pd.DataFrame(
            report["strengths"]
        )[["name", "state_value", "india_avg"]]

        strengths_df.columns = [
            "Indicator",
            "State Value",
            "India Average"
        ]

        st.dataframe(
            strengths_df,
            use_container_width=True
        )

        chart_df = pd.DataFrame(
            report["strengths"]
        )

        chart_df = chart_df.head(10)

        fig = px.bar(
            chart_df,
            x="name",
            y=["state_value", "india_avg"],
            barmode="group",
            title="State vs India Comparison (Top Strengths)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "No major strengths identified."
        )

# ---------- WEAKNESSES ----------

with right_col:

    st.subheader("⚠️ Areas for Improvement")

    if report["weaknesses"]:

        weaknesses_df = pd.DataFrame(
            report["weaknesses"]
        )[["name", "state_value", "india_avg"]]

        weaknesses_df.columns = [
            "Indicator",
            "State Value",
            "India Average"
        ]

        st.dataframe(
            weaknesses_df,
            use_container_width=True
        )

    else:

        st.success(
            "No major weaknesses identified."
        )

# --------------------------------------------------
# RECOMMENDATIONS
# --------------------------------------------------

st.divider()

st.subheader("🎯 Policy Recommendations")

if report["recommendations"]:

    for rec in report["recommendations"]:

        st.info(rec)

else:

    st.success(
        "No specific recommendations required."
    )
    
    
    
report_text = f"""
STATE DEVELOPMENT REPORT

State: {report['state']}
Cluster: {report['cluster']}
Composite Score: {report['composite_score']}

Strength Count: {report['strength_count']}
Weakness Count: {report['weakness_count']}
Neutral Count: {report['neutral_count']}
"""


st.download_button(
    label="📄 Download Report",
    data=report_text,
    file_name=f"{report['state']}_SDG_Report.txt",
    mime="text/plain"
)
    
    
    

st.divider()

st.subheader("🏆 Top Performing States")

leaderboard = master[
    ["state", "composite_score_of_sdg_india_index"]
].sort_values(
    by="composite_score_of_sdg_india_index",
    ascending=False
).head(10)

leaderboard.columns = [
    "State",
    "SDG Score"
]

leaderboard.insert(
    0,
    "Rank",
    range(1, len(leaderboard) + 1)
)

st.dataframe(
    leaderboard,
    use_container_width=True
)


st.divider()

st.subheader("📊 Cluster Distribution")
cluster_counts = master["cluster"].value_counts().sort_index()

cluster_chart_df = pd.DataFrame({
    "Cluster": [
        "Development Challenge Cluster",
        "High Development Cluster",
        "North-East Development Cluster",
        "Unique Outlier Cluster"
    ],
    "States": cluster_counts.values
})

fig = px.bar(
    cluster_chart_df,
    x="Cluster",
    y="States",
    title="Distribution of States Across Clusters"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.divider()

st.subheader("⚔️ State Comparison")

col1, col2 = st.columns(2)

with col1:
    state_1 = st.selectbox(
        "Select First State",
        sorted(master["state"].unique()),
        key="state1"
    )

with col2:
    state_2 = st.selectbox(
        "Select Second State",
        sorted(master["state"].unique()),
        index=1,
        key="state2"
    )
    
    
    
report_1 = generate_state_report(state_1)

report_2 = generate_state_report(state_2)


comparison_df = pd.DataFrame({

    "Metric": [
        "Composite Score",
        "Cluster",
        "Strength Count",
        "Weakness Count"
    ],

    state_1: [
        report_1["composite_score"],
        report_1["cluster"],
        report_1["strength_count"],
        report_1["weakness_count"]
    ],

    state_2: [
        report_2["composite_score"],
        report_2["cluster"],
        report_2["strength_count"],
        report_2["weakness_count"]
    ]

})

st.dataframe(
    comparison_df,
    use_container_width=True
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Recommendation engine based on Random Forest feature importance and national benchmark comparison."
)