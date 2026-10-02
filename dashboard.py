import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Nexa Executive Dashboard",
    page_icon="🚗",
    layout="wide"
)

# =========================================================
# COLORS
# =========================================================

COLORS = [
    "#00BFFF",
    "#7B2CBF",
    "#00C853",
    "#FFB300",
    "#FF4081",
    "#FF6D00",
    "#00ACC1",
    "#8BC34A",
    "#E91E63",
    "#5E35B1",
    "#3949AB",
    "#00897B",
    "#C0CA33",
    "#F4511E",
    "#6D4C41"
]

MONTH_COLORS = {
    "April": "#00BFFF",
    "May": "#7B2CBF",
    "June": "#00C853",
    "July": "#FFB300",
    "August": "#FF4081",
    "September": "#FF6D00",
    "October": "#00ACC1",
    "November": "#8BC34A",
    "December": "#E91E63",
    "January": "#5E35B1",
    "February": "#3949AB",
    "March": "#00897B"
}

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_excel("nexa_data.xlsx")

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.upper()
    )

    for col in [
        "MONTH",
        "VEH.MODEL",
        "RM NAME",
        "SRM NAME"
    ]:
        df[col] = (
            df[col]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )

    df["SPECIAL DISCOUNT"] = pd.to_numeric(
        df["SPECIAL DISCOUNT"],
        errors="coerce"
    ).fillna(0)

    return df


df = load_data()

# =========================================================
# MONTH ORDER
# =========================================================

month_order = [
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
    "January",
    "February",
    "March"
]

available_months = [
    x for x in month_order
    if x in df["MONTH"].unique()
]

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🚗 Nexa Filters")

selected_month = st.sidebar.selectbox(
    "Month",
    ["All"] + available_months
)

selected_model = st.sidebar.selectbox(
    "Vehicle Model",
    ["All"] +
    sorted(df["VEH.MODEL"].unique())
)

selected_rm = st.sidebar.selectbox(
    "RM Name",
    ["All"] +
    sorted(df["RM NAME"].unique())
)

selected_srm = st.sidebar.selectbox(
    "SRM Name",
    ["All"] +
    sorted(df["SRM NAME"].unique())
)

# =========================================================
# FILTER
# =========================================================

filtered_df = df.copy()

if selected_month != "All":
    filtered_df = filtered_df[
        filtered_df["MONTH"] == selected_month
    ]

if selected_model != "All":
    filtered_df = filtered_df[
        filtered_df["VEH.MODEL"] == selected_model
    ]

if selected_rm != "All":
    filtered_df = filtered_df[
        filtered_df["RM NAME"] == selected_rm
    ]

if selected_srm != "All":
    filtered_df = filtered_df[
        filtered_df["SRM NAME"] == selected_srm
    ]

# =========================================================
# HEADER
# =========================================================

st.title("🚗 Nexa Executive Dashboard")

st.caption(
    "Special Discount Analysis & Performance Dashboard"
)

# =========================================================
# KPI
# =========================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "💰 Total Discount",
        f"₹ {filtered_df['SPECIAL DISCOUNT'].sum():,.0f}"
    )

with c2:
    st.metric(
        "📋 Records",
        f"{len(filtered_df):,}"
    )

with c3:
    st.metric(
        "🚘 Models",
        filtered_df["VEH.MODEL"].nunique()
    )

with c4:
    st.metric(
        "👤 RM Count",
        filtered_df["RM NAME"].nunique()
    )

st.divider()

# =========================================================
# MONTH DATA
# =========================================================

month_data = (
    filtered_df
    .groupby("MONTH", as_index=False)
    ["SPECIAL DISCOUNT"]
    .sum()
)

month_data["MONTH"] = pd.Categorical(
    month_data["MONTH"],
    categories=month_order,
    ordered=True
)

month_data = month_data.sort_values("MONTH")

# =========================================================
# MODEL DATA
# =========================================================

model_data = (
    filtered_df
    .groupby("VEH.MODEL", as_index=False)
    ["SPECIAL DISCOUNT"]
    .sum()
    .sort_values(
        "SPECIAL DISCOUNT",
        ascending=False
    )
)

# =========================================================
# RM DATA
# =========================================================

rm_data = (
    filtered_df
    .groupby("RM NAME", as_index=False)
    ["SPECIAL DISCOUNT"]
    .sum()
    .sort_values(
        "SPECIAL DISCOUNT",
        ascending=False
    )
)

# =========================================================
# SRM DATA
# =========================================================

srm_data = (
    filtered_df
    .groupby("SRM NAME", as_index=False)
    ["SPECIAL DISCOUNT"]
    .sum()
    .sort_values(
        "SPECIAL DISCOUNT",
        ascending=False
    )
)

# =========================================================
# COMMON CHART SETTINGS
# =========================================================

common_layout = dict(
    template="plotly_dark",
    margin=dict(
        l=50,
        r=30,
        t=70,
        b=50
    ),
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font=dict(size=12)
)

# =========================================================
# ROW 1
# =========================================================

col1, col2 = st.columns(2)

# =========================================================
# MONTH CHART
# =========================================================

with col1:

    fig_month = px.bar(
        month_data,
        x="MONTH",
        y="SPECIAL DISCOUNT",
        color="MONTH",
        color_discrete_map=MONTH_COLORS,
        title="📅 Month Wise Discount"
    )

    fig_month.update_traces(
        texttemplate="₹%{y:,.0f}",
        textposition="inside"
    )

    fig_month.update_layout(
        **common_layout,
        height=400,
        showlegend=False,
        xaxis_title="Month",
        yaxis_title="Special Discount"
    )

    st.plotly_chart(
        fig_month,
        use_container_width=True
    )

# =========================================================
# MODEL CHART
# =========================================================

with col2:

    fig_model = px.bar(
        model_data,
        x="SPECIAL DISCOUNT",
        y="VEH.MODEL",
        orientation="h",
        color="VEH.MODEL",
        color_discrete_sequence=COLORS,
        title="🚘 Model Wise Discount"
    )

    fig_model.update_traces(
        texttemplate="₹%{x:,.0f}",
        textposition="inside"
    )

    fig_model.update_layout(
        **common_layout,
        height=400,
        showlegend=False,
        xaxis_title="Special Discount",
        yaxis_title="Vehicle Model"
    )

    st.plotly_chart(
        fig_model,
        use_container_width=True
    )

# =========================================================
# DONUT CHART
# =========================================================

st.subheader("🍩 Vehicle Model Contribution")

col1, col2 = st.columns(2)

with col1:

    fig_donut = px.pie(
        model_data,
        names="VEH.MODEL",
        values="SPECIAL DISCOUNT",
        hole=0.55,
        color="VEH.MODEL",
        color_discrete_sequence=COLORS,
        title="Special Discount Contribution"
    )

    fig_donut.update_traces(
        textposition="inside",
        textinfo="percent"
    )

    fig_donut.update_layout(
        **common_layout,
        height=450,
        legend=dict(
            orientation="h",
            y=-0.15
        )
    )

    st.plotly_chart(
        fig_donut,
        use_container_width=True
    )

# =========================================================
# TOP 10 MODEL
# =========================================================

with col2:

    top10 = model_data.head(10)

    fig_top10 = px.bar(
        top10,
        x="SPECIAL DISCOUNT",
        y="VEH.MODEL",
        orientation="h",
        color="VEH.MODEL",
        color_discrete_sequence=COLORS,
        title="🏆 Top 10 Vehicle Models"
    )

    fig_top10.update_traces(
        texttemplate="₹%{x:,.0f}",
        textposition="inside"
    )

    fig_top10.update_layout(
        **common_layout,
        height=450,
        showlegend=False,
        xaxis_title="Special Discount",
        yaxis_title="Vehicle Model"
    )

    st.plotly_chart(
        fig_top10,
        use_container_width=True
    )

# =========================================================
# RM / SRM
# =========================================================

st.subheader("🏆 Management Ranking")

col1, col2 = st.columns(2)

# =========================================================
# RM
# =========================================================

with col1:

    rm_top20 = rm_data.head(20)

    fig_rm = px.bar(
        rm_top20,
        x="SPECIAL DISCOUNT",
        y="RM NAME",
        orientation="h",
        color="RM NAME",
        color_discrete_sequence=COLORS,
        title="Top 20 RM Ranking"
    )

    fig_rm.update_traces(
        texttemplate="₹%{x:,.0f}",
        textposition="inside"
    )

    fig_rm.update_layout(
        **common_layout,
        height=600,
        showlegend=False,
        xaxis_title="Special Discount",
        yaxis_title="RM Name"
    )

    st.plotly_chart(
        fig_rm,
        use_container_width=True
    )

# =========================================================
# SRM
# =========================================================

with col2:

    srm_top20 = srm_data.head(20)

    fig_srm = px.bar(
        srm_top20,
        x="SPECIAL DISCOUNT",
        y="SRM NAME",
        orientation="h",
        color="SRM NAME",
        color_discrete_sequence=COLORS,
        title="Top 20 SRM Ranking"
    )

    fig_srm.update_traces(
        texttemplate="₹%{x:,.0f}",
        textposition="inside"
    )

    fig_srm.update_layout(
        **common_layout,
        height=600,
        showlegend=False,
        xaxis_title="Special Discount",
        yaxis_title="SRM Name"
    )

    st.plotly_chart(
        fig_srm,
        use_container_width=True
    )

# =========================================================
# TABLES
# =========================================================

st.subheader("📊 Data Tables")

tab1, tab2, tab3 = st.tabs(
    [
        "🏆 Top 20 RM",
        "🥇 Top 20 SRM",
        "📋 Detailed Data"
    ]
)

with tab1:

    st.dataframe(
        rm_data.head(20),
        use_container_width=True,
        hide_index=True
    )

with tab2:

    st.dataframe(
        srm_data.head(20),
        use_container_width=True,
        hide_index=True
    )

with tab3:

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

# =========================================================
# DOWNLOAD
# =========================================================

st.divider()

csv = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Report",
    data=csv,
    file_name="nexa_report.csv",
    mime="text/csv"
)