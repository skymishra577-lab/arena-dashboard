import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# ------------------------------------------
# PAGE CONFIG
# ------------------------------------------

st.set_page_config(
    page_title="NEXA Executive Dashboard",
    page_icon="🚗",
    layout="wide"
)

# ------------------------------------------
# LOAD DATA
# ------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_excel("discount_data.xlsx")

    df.columns = df.columns.str.strip()

    if "VEH.MODEL" in df.columns:
        df.rename(
            columns={"VEH.MODEL": "VEH"},
            inplace=True
        )

    df["SPECIAL DISCOUNT"] = pd.to_numeric(
        df["SPECIAL DISCOUNT"],
        errors="coerce"
    ).fillna(0)

    df["R.M. NAME"] = df["R.M. NAME"].fillna("Unknown")
    df["T.L. NAME"] = df["T.L. NAME"].fillna("Unknown")
    df["CUST. NAME"] = df["CUST. NAME"].fillna("Unknown")
    df["VEH"] = df["VEH"].fillna("Unknown")

    return df

df = load_data()

# ------------------------------------------
# HEADER
# ------------------------------------------

st.title("🚗 NEXA Executive Dashboard")
st.markdown("### Discount Analysis Report")

# ------------------------------------------
# SIDEBAR FILTERS
# ------------------------------------------

st.sidebar.header("Filters")

vehicle_list = ["All"] + sorted(df["VEH"].unique())
rm_list = ["All"] + sorted(df["R.M. NAME"].unique())
tl_list = ["All"] + sorted(df["T.L. NAME"].unique())

selected_vehicle = st.sidebar.selectbox(
    "Vehicle Model",
    vehicle_list
)

selected_rm = st.sidebar.selectbox(
    "Relationship Manager",
    rm_list
)

selected_tl = st.sidebar.selectbox(
    "Team Leader",
    tl_list
)

filtered_df = df.copy()

if selected_vehicle != "All":
    filtered_df = filtered_df[
        filtered_df["VEH"] == selected_vehicle
    ]

if selected_rm != "All":
    filtered_df = filtered_df[
        filtered_df["R.M. NAME"] == selected_rm
    ]

if selected_tl != "All":
    filtered_df = filtered_df[
        filtered_df["T.L. NAME"] == selected_tl
    ]

# ------------------------------------------
# KPI CARDS
# ------------------------------------------

total_discount = filtered_df["SPECIAL DISCOUNT"].sum()
avg_discount = filtered_df["SPECIAL DISCOUNT"].mean()
highest_discount = filtered_df["SPECIAL DISCOUNT"].max()
total_deals = len(filtered_df)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Discount",
    f"₹ {total_discount:,.0f}"
)

col2.metric(
    "Average Discount",
    f"₹ {avg_discount:,.0f}"
)

col3.metric(
    "Highest Discount",
    f"₹ {highest_discount:,.0f}"
)

col4.metric(
    "Total Deals",
    total_deals
)

st.divider()

# ------------------------------------------
# VEHICLE ANALYSIS
# ------------------------------------------

vehicle_summary = (
    filtered_df.groupby("VEH")["SPECIAL DISCOUNT"]
    .sum()
    .reset_index()
)

left, right = st.columns(2)

with left:

    fig_vehicle = px.bar(
        vehicle_summary,
        x="VEH",
        y="SPECIAL DISCOUNT",
        color="VEH",
        title="Vehicle Wise Discount"
    )

    st.plotly_chart(
        fig_vehicle,
        use_container_width=True
    )

with right:

    fig_pie = px.pie(
        vehicle_summary,
        names="VEH",
        values="SPECIAL DISCOUNT",
        hole=0.4,
        title="Discount Share by Vehicle"
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )

# ------------------------------------------
# TL RANKING
# ------------------------------------------

st.subheader("🏆 Team Leader Ranking")

tl_summary = (
    filtered_df.groupby("T.L. NAME")["SPECIAL DISCOUNT"]
    .sum()
    .reset_index()
    .sort_values(
        "SPECIAL DISCOUNT",
        ascending=False
    )
)

fig_tl = px.bar(
    tl_summary,
    x="T.L. NAME",
    y="SPECIAL DISCOUNT",
    color="SPECIAL DISCOUNT",
    title="TL Wise Discount Ranking"
)

st.plotly_chart(
    fig_tl,
    use_container_width=True
)

st.dataframe(
    tl_summary,
    use_container_width=True
)

# ------------------------------------------
# RM RANKING
# ------------------------------------------

st.subheader("🏆 RM Ranking")

rm_summary = (
    filtered_df.groupby("R.M. NAME")["SPECIAL DISCOUNT"]
    .sum()
    .reset_index()
    .sort_values(
        "SPECIAL DISCOUNT",
        ascending=False
    )
)

fig_rm = px.bar(
    rm_summary,
    x="R.M. NAME",
    y="SPECIAL DISCOUNT",
    color="SPECIAL DISCOUNT",
    title="RM Wise Discount Ranking"
)

st.plotly_chart(
    fig_rm,
    use_container_width=True
)

st.dataframe(
    rm_summary,
    use_container_width=True
)

# ------------------------------------------
# RM + CUSTOMER RANKING
# ------------------------------------------

st.subheader("👤 RM Ranking With Customer")

rm_customer = filtered_df[
    [
        "R.M. NAME",
        "CUST. NAME",
        "VEH",
        "SPECIAL DISCOUNT"
    ]
].sort_values(
    "SPECIAL DISCOUNT",
    ascending=False
)

st.dataframe(
    rm_customer,
    use_container_width=True
)

# ------------------------------------------
# TL + CUSTOMER RANKING
# ------------------------------------------

st.subheader("👤 TL Ranking With Customer")

tl_customer = filtered_df[
    [
        "T.L. NAME",
        "CUST. NAME",
        "VEH",
        "SPECIAL DISCOUNT"
    ]
].sort_values(
    "SPECIAL DISCOUNT",
    ascending=False
)

st.dataframe(
    tl_customer,
    use_container_width=True
)

# ------------------------------------------
# TOP 20 CUSTOMER DISCOUNT
# ------------------------------------------

st.subheader("🔥 Top 20 Customers")

top_customer = filtered_df[
    [
        "CUST. NAME",
        "R.M. NAME",
        "T.L. NAME",
        "VEH",
        "SPECIAL DISCOUNT"
    ]
].sort_values(
    "SPECIAL DISCOUNT",
    ascending=False
).head(20)

st.dataframe(
    top_customer,
    use_container_width=True
)

# ------------------------------------------
# ALL DATA
# ------------------------------------------

st.subheader("📋 All Records")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ------------------------------------------
# DOWNLOAD REPORT
# ------------------------------------------

excel_buffer = BytesIO()

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:

    filtered_df.to_excel(
        writer,
        index=False,
        sheet_name="NEXA Report"
    )

st.download_button(
    label="📥 Download Excel Report",
    data=excel_buffer.getvalue(),
    file_name="NEXA_Discount_Report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)