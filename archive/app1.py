import streamlit as st
import pandas as pd
import plotly.express as px

from sdg_engine import (
    master,
    generate_state_report
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="India SDG Intelligence Dashboard",
    page_icon="🇮🇳",
    layout="wide"
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🇮🇳 SDG Dashboard")

st.sidebar.markdown("---")

state = st.sidebar.selectbox(
    "Select State",
    sorted(master["state"].unique())
)

st.sidebar.markdown("---")

st.sidebar.subheader("Project Overview")

st.sidebar.write("📍 States : 36")
st.sidebar.write("📊 Indicators : 25")
st.sidebar.write("🤖 ML Model : Random Forest")
st.sidebar.write("🧠 Clustering : K-Means")
st.sidebar.write("🎯 Recommendation Engine")

st.sidebar.markdown("---")

st.sidebar.caption("Developed by")
st.sidebar.write("**Trigun Jagal**")

# =====================================================
# LOAD REPORT
# =====================================================

report = generate_state_report(state)

# =====================================================
# TITLE
# =====================================================

st.title("🇮🇳 India SDG State Intelligence Dashboard")

st.markdown("""
An interactive data science dashboard for analyzing Sustainable Development Goal (SDG) performance across Indian states using **Machine Learning**, **K-Means Clustering**, and a **Policy Recommendation Engine**.
""")

st.divider()

# =====================================================
# OVERVIEW
# =====================================================

st.header("📊 Overview")

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

st.divider()

# =====================================================
# STATE OVERVIEW
# =====================================================

st.header("📍 State Overview")

left_col, right_col = st.columns([1,1])

with left_col:

    st.subheader("State Profile")

    st.info(
        f"""
State : {report['state']}

Cluster : {report['cluster']}

Composite SDG Score : {report['composite_score']}
"""
    )

with right_col:

    st.subheader("States in Same Cluster")

    cluster_states = master[
        master["cluster"] == report["cluster_id"]
    ]["state"].tolist()

    cluster_df = pd.DataFrame({
        "State": sorted(cluster_states)
    })

    st.dataframe(
        cluster_df,
        use_container_width=True,
        height=250
    )

st.divider()

# =====================================================
# PERFORMANCE ANALYSIS
# =====================================================

st.header("📈 Performance Analysis")

st.markdown(
    """
These indicators are identified by comparing the selected state's performance against the national average using the top 25 Random Forest features.
"""
)

left_col, right_col = st.columns(2)



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
            use_container_width=True,
            height=420
        )

    else:

        st.success("No major strengths identified.")
    
    
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
            use_container_width=True,
            height=420
        )

    else:

        st.success("No major weaknesses identified.")
        
st.divider()

# =====================================================
# VISUAL ANALYTICS
# =====================================================

st.header("📊 Visual Analytics")

st.subheader("State vs India Comparison")

chart_df = pd.DataFrame(
    report["strengths"] + report["weaknesses"]
)

chart_df = chart_df.head(10)

fig = px.bar(
    chart_df,
    x=["state_value", "india_avg"],
    y="name",
    orientation="h",
    barmode="group",
    title="Top Indicators: State vs India"
)

fig.update_layout(
    height=650,
    yaxis_title="",
    xaxis_title="Value",
    legend_title=""
)

st.plotly_chart(
    fig,
    use_container_width=True
)

left, right = st.columns(2)

with left:

    summary_df = pd.DataFrame({

        "Category": [
            "Strengths",
            "Weaknesses",
            "Neutral"
        ],

        "Count": [
            report["strength_count"],
            report["weakness_count"],
            report["neutral_count"]
        ]

    })

    fig = px.bar(
        summary_df,
        x="Category",
        y="Count",
        title="Indicator Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig = px.pie(
        summary_df,
        names="Category",
        values="Count",
        title="Performance Composition"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()
# =====================================================
# POLICY RECOMMENDATIONS
# =====================================================
policy_domains = {

    "Improve income generation opportunities and strengthen social welfare programs for economically weaker households.":
        ("💰 Poverty & Livelihood", "Improve income generation opportunities and strengthen social welfare programs for economically weaker households."),

    "Improve access to healthcare, education, housing, sanitation, and other basic services.":
        ("💰 Poverty & Livelihood", "Improve access to healthcare, education, housing, sanitation, and other basic services."),

    "Strengthen poverty alleviation, livelihood generation, and employment programs.":
        ("💰 Poverty & Livelihood", "Strengthen poverty alleviation, livelihood generation, and employment programs."),

    "Increase ATM penetration and improve access to formal banking services.":
        ("🏦 Financial Inclusion", "Increase ATM penetration and improve access to formal banking services."),

    "Expand banking infrastructure and financial inclusion initiatives.":
        ("🏦 Financial Inclusion", "Expand banking infrastructure and financial inclusion initiatives."),

    "Improve telecom infrastructure and digital connectivity.":
        ("📡 Connectivity", "Improve telecom infrastructure and digital connectivity."),

    "Promote clean cooking fuel adoption and expand LPG/PNG coverage.":
        ("📡 Connectivity", "Promote clean cooking fuel adoption and expand LPG/PNG coverage."),

    "Improve school infrastructure, electricity access, drinking water, and sanitation facilities.":
        ("🎓 Education", "Improve school infrastructure, electricity access, drinking water, and sanitation facilities."),

    "Increase higher secondary school enrollment and retention.":
        ("🎓 Education", "Increase higher secondary school enrollment and retention."),

    "Improve learning outcomes through teacher training and quality education initiatives.":
        ("🎓 Education", "Improve learning outcomes through teacher training and quality education initiatives."),

    "Increase access to higher education and skill development opportunities.":
        ("🎓 Education", "Increase access to higher education and skill development opportunities."),

    "Strengthen inclusive education and accessibility for persons with disabilities.":
        ("🎓 Education", "Strengthen inclusive education and accessibility for persons with disabilities."),

    "Implement targeted interventions to reduce school dropout rates.":
        ("🎓 Education", "Implement targeted interventions to reduce school dropout rates."),

    "Improve maternal healthcare services and institutional deliveries.":
        ("🏥 Health", "Improve maternal healthcare services and institutional deliveries."),

    "Expand HIV awareness, testing, prevention, and treatment programs.":
        ("🏥 Health", "Expand HIV awareness, testing, prevention, and treatment programs."),

    "Strengthen nutrition programs and iron supplementation initiatives.":
        ("🏥 Health", "Strengthen nutrition programs and iron supplementation initiatives."),

    "Improve child healthcare, immunization, and nutrition services.":
        ("🏥 Health", "Improve child healthcare, immunization, and nutrition services."),

    "Promote women's workforce participation and economic empowerment.":
        ("👩 Employment & Gender", "Promote women's workforce participation and economic empowerment."),

    "Create employment opportunities and strengthen workforce participation.":
        ("👩 Employment & Gender", "Create employment opportunities and strengthen workforce participation."),

    "Promote women's ownership and management of agricultural land and assets.":
        ("👩 Employment & Gender", "Promote women's ownership and management of agricultural land and assets."),

    "Improve industrial environmental compliance and wastewater treatment practices.":
        ("🌱 Environment", "Improve industrial environmental compliance and wastewater treatment practices."),

    "Promote renewable energy adoption and improve energy efficiency.":
        ("🌱 Environment", "Promote renewable energy adoption and improve energy efficiency."),

    "Improve urban road safety infrastructure and traffic management systems.":
        ("🚦 Road Safety", "Improve urban road safety infrastructure and traffic management systems."),

    "Strengthen road safety awareness, enforcement, and emergency response systems.":
        ("🚦 Road Safety", "Strengthen road safety awareness, enforcement, and emergency response systems."),

    "Improve agricultural productivity through technology adoption and farmer support programs.":
        ("🌾 Agriculture", "Improve agricultural productivity through technology adoption and farmer support programs.")
}

st.header("🎯 Policy Recommendations")

st.markdown("""
The following policy recommendations are generated based on the identified weaknesses of the selected state.
""")

shown_domains = set()

for rec in report["recommendations"]:

    domain, text = policy_domains[rec]

    if domain not in shown_domains:

        st.subheader(domain)

        shown_domains.add(domain)

    st.success(text)
    
st.divider()

# =====================================================
# NATIONAL INSIGHTS
# =====================================================

st.header("🇮🇳 National Insights")

st.markdown("""
Explore India's overall SDG performance through state rankings and the distribution of states across development clusters.
""")

left_col, right_col = st.columns(2)
with left_col:

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
        use_container_width=True,
        height=390
    )
    
with right_col:

    st.subheader("📊 Cluster Distribution")

    cluster_counts = master["cluster"].value_counts().sort_index()

    cluster_df = pd.DataFrame({

        "Cluster":[

            "Development Challenge",

            "High Development",

            "North-East",

            "Unique Outlier"

        ],

        "States":cluster_counts.values

    })

    fig = px.pie(

        cluster_df,

        names="Cluster",

        values="States",

        hole=0.55,

        title="Distribution of States Across Clusters"

    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    
    

st.divider()

# =====================================================
# State Comparison
# =====================================================

st.header("⚔️ State Comparison")

st.markdown("""
Compare the SDG performance of any two Indian states across key development metrics.
""")

col1, col2 = st.columns(2)

with col1:
    state_1 = st.selectbox(
        "Select First State",
        sorted(master["state"].unique()),
        key="compare_1"
    )

with col2:
    state_2 = st.selectbox(
        "Select Second State",
        sorted(master["state"].unique()),
        index=1,
        key="compare_2"
    )

report_1 = generate_state_report(state_1)
report_2 = generate_state_report(state_2)

st.subheader("Comparison Summary")

left, right = st.columns(2)

with left:

    st.markdown(f"### {state_1}")

    st.metric(
        "Composite Score",
        report_1["composite_score"]
    )

    st.metric(
        "Strengths",
        report_1["strength_count"]
    )

    st.metric(
        "Weaknesses",
        report_1["weakness_count"]
    )

    st.metric(
        "Neutral",
        report_1["neutral_count"]
    )

    st.write(f"**Cluster:** {report_1['cluster']}")

with right:

    st.markdown(f"### {state_2}")

    st.metric(
        "Composite Score",
        report_2["composite_score"]
    )

    st.metric(
        "Strengths",
        report_2["strength_count"]
    )

    st.metric(
        "Weaknesses",
        report_2["weakness_count"]
    )

    st.metric(
        "Neutral",
        report_2["neutral_count"]
    )

    st.write(f"**Cluster:** {report_2['cluster']}")
    
    
comparison_df = pd.DataFrame({

    "State": [
        state_1,
        state_2
    ],

    "Composite Score": [
        report_1["composite_score"],
        report_2["composite_score"]
    ]

})

fig = px.bar(

    comparison_df,

    x="State",

    y="Composite Score",

    text="Composite Score",

    title="Composite SDG Score Comparison"

)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =====================================================
# DOWNLOAD REPORT
# =====================================================

st.header("📄 Export Report")

st.markdown("""
Download a summary report for the selected state. The report includes the SDG score, cluster information, strengths, weaknesses, and policy recommendations.
""")

report_text = f"""
=========================================================
        INDIA SDG STATE DEVELOPMENT REPORT
=========================================================

State : {report['state']}

Cluster : {report['cluster']}

Composite SDG Score : {report['composite_score']}

---------------------------------------------------------
SUMMARY
---------------------------------------------------------

Strengths : {report['strength_count']}

Weaknesses : {report['weakness_count']}

Neutral Indicators : {report['neutral_count']}

---------------------------------------------------------
KEY STRENGTHS
---------------------------------------------------------
"""

for item in report["strengths"]:

    report_text += (
        f"\n✓ {item['name']}"
        f"\n   State : {item['state_value']}"
        f"\n   India Average : {item['india_avg']}\n"
    )
    
    
report_text += """

---------------------------------------------------------
AREAS FOR IMPROVEMENT
---------------------------------------------------------
"""

for item in report["weaknesses"]:

    report_text += (
        f"\n• {item['name']}"
        f"\n   State : {item['state_value']}"
        f"\n   India Average : {item['india_avg']}\n"
    )
    
report_text += """

---------------------------------------------------------
POLICY RECOMMENDATIONS
---------------------------------------------------------
"""

for rec in report["recommendations"]:

    report_text += f"\n• {rec}"
    
st.download_button(

    label="📥 Download State Report",

    data=report_text,

    file_name=f"{report['state']}_SDG_Report.txt",

    mime="text/plain"

)