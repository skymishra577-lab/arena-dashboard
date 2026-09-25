import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# ---------------------------
# Page Setup
# ---------------------------

st.set_page_config(
    page_title="NEXA Executive Dashboard",
    page_icon="🚗",
    layout="wide"
)

# ---------------------------
# Load Data
# ---------------------------

@st.cache_data
def load_data():
    df = pd.read_excel("discount_data.xlsx")

    df["SPECIAL DISCOUNT"] = pd.to_numeric(
        df["SPECIAL DISCOUNT"],
        errors="coerce"
    ).fillna(0)

    return df

df = load_data()

# ---------------------------
# Header
# ---------------------------

st.title("🚗 NEXA Executive Dashboard")
st.markdown("### Discount Analysis Report")

# ---------------------------
# Sidebar Filters
# ---------------------------

st.sidebar.header("Filters")

vehicle_list = ["All"] + sorted(df["VEH"].dropna().unique().tolist())
tl_list = ["All"] + sorted(df["T.L. NAME"].dropna().unique().tolist())

selected_vehicle = st.sidebar.selectbox(
    "Vehicle Model",
    vehicle_list
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

if selected_tl != "All":
    filtered_df = filtered_df[
        filtered_df["T.L. NAME"] == selected_tl
    ]

# ---------------------------
# KPI Cards
# ---------------------------

total_discount = filtered_df["SPECIAL DISCOUNT"].sum()
avg_discount = filtered_df["SPECIAL DISCOUNT"].mean()
total_records = len(filtered_df)
max_discount = filtered_df["SPECIAL DISCOUNT"].max()

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
    "Total Records",
    f"{total_records}"
)

col4.metric(
    "Highest Discount",
    f"₹ {max_discount:,.0f}"
)

st.divider()

# ---------------------------
# Charts
# ---------------------------

left, right = st.columns(2)

with left:

    model_discount = (
        filtered_df.groupby("VEH")["SPECIAL DISCOUNT"]
        .sum()
        .reset_index()
    )

    fig_model = px.bar(
        model_discount,
        x="VEH",
        y="SPECIAL DISCOUNT",
        color="VEH",
        title="Vehicle Wise Discount"
    )

    st.plotly_chart(
        fig_model,
        use_container_width=True
    )

with right:

    fig_pie = px.pie(
        model_discount,
        names="VEH",
        values="SPECIAL DISCOUNT",
        hole=0.4,
        title="Discount Share by Vehicle"
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )

# ---------------------------
# TL Analysis
# ---------------------------

tl_discount = (
    filtered_df.groupby("T.L. NAME")["SPECIAL DISCOUNT"]
    .sum()
    .reset_index()
    .sort_values("SPECIAL DISCOUNT", ascending=False)
)

fig_tl = px.bar(
    tl_discount,
    x="T.L. NAME",
    y="SPECIAL DISCOUNT",
    color="SPECIAL DISCOUNT",
    title="TL Wise Discount Ranking"
)

st.plotly_chart(
    fig_tl,
    use_container_width=True
)

# ---------------------------
# Top 10 Records
# ---------------------------

st.subheader("Top 10 Highest Discounts")

top10 = filtered_df.sort_values(
    "SPECIAL DISCOUNT",
    ascending=False
).head(10)

st.dataframe(
    top10,
    use_container_width=True
)

# ---------------------------
# Full Data
# ---------------------------

st.subheader("All Records")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ---------------------------
# Excel Download
# ---------------------------

excel_buffer = BytesIO()

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:

    filtered_df.to_excel(
        writer,
        index=False,
        sheet_name="Report"
    )

st.download_button(
    label="📥 Download Excel Report",
    data=excel_buffer.getvalue(),
    file_name="NEXA_Discount_Report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)