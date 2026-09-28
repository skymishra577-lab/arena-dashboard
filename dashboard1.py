import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Arena Executive Dashboard",
    page_icon="🚗",
    layout="wide"
)

# ---------------- LOAD DATA ----------------

@st.cache_data
def load_data():
    df = pd.read_excel("arena_data.xlsx")

    # Remove extra spaces from column names
    df.columns = df.columns.str.strip()

    # Convert discount column to numeric
    df["SPECIAL DISCOUNT"] = pd.to_numeric(
        df["SPECIAL DISCOUNT"],
        errors="coerce"
    ).fillna(0)

    return df

df = load_data()

# ---------------- HEADER ----------------

st.title("🚗 Arena Executive Dashboard")
st.markdown("### Special Discount Analysis Report")

# ---------------- SIDEBAR FILTERS ----------------

st.sidebar.header("Filters")

vehicle_list = ["All"] + sorted(df["VEH"].dropna().astype(str).unique())
rm_list = ["All"] + sorted(df["RM"].dropna().astype(str).unique())
srm_list = ["All"] + sorted(df["SRM"].dropna().astype(str).unique())
customer_list = ["All"] + sorted(df["CUSTOMER_NAME"].dropna().astype(str).unique())

selected_vehicle = st.sidebar.selectbox(
    "Vehicle Model",
    vehicle_list
)

selected_rm = st.sidebar.selectbox(
    "RM",
    rm_list
)

selected_srm = st.sidebar.selectbox(
    "SRM",
    srm_list
)

selected_customer = st.sidebar.selectbox(
    "Customer Name",
    customer_list
)

# ---------------- FILTER DATA ----------------

filtered_df = df.copy()

if selected_vehicle != "All":
    filtered_df = filtered_df[
        filtered_df["VEH"] == selected_vehicle
    ]

if selected_rm != "All":
    filtered_df = filtered_df[
        filtered_df["RM"] == selected_rm
    ]

if selected_srm != "All":
    filtered_df = filtered_df[
        filtered_df["SRM"] == selected_srm
    ]

if selected_customer != "All":
    filtered_df = filtered_df[
        filtered_df["CUSTOMER_NAME"] == selected_customer
    ]

# ---------------- KPI CARDS ----------------

total_discount = filtered_df["SPECIAL DISCOUNT"].sum()
avg_discount = filtered_df["SPECIAL DISCOUNT"].mean()
total_records = len(filtered_df)
max_discount = filtered_df["SPECIAL DISCOUNT"].max()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Discount",
        f"₹ {total_discount:,.0f}"
    )

with col2:
    st.metric(
        "Average Discount",
        f"₹ {avg_discount:,.0f}"
    )

with col3:
    st.metric(
        "Total Records",
        total_records
    )

with col4:
    st.metric(
        "Highest Discount",
        f"₹ {max_discount:,.0f}"
    )

st.divider()

# ---------------- VEHICLE ANALYSIS ----------------

st.subheader("Vehicle Wise Discount Analysis")

vehicle_discount = (
    filtered_df.groupby("VEH")["SPECIAL DISCOUNT"]
    .sum()
    .reset_index()
)

left, right = st.columns(2)

with left:
    fig_vehicle = px.bar(
        vehicle_discount,
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
        vehicle_discount,
        names="VEH",
        values="SPECIAL DISCOUNT",
        hole=0.4,
        title="Vehicle Share In Discount"
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )

# ---------------- RM ANALYSIS ----------------

st.subheader("RM Wise Discount Ranking")

rm_discount = (
    filtered_df.groupby("RM")["SPECIAL DISCOUNT"]
    .sum()
    .reset_index()
    .sort_values(
        "SPECIAL DISCOUNT",
        ascending=False
    )
)

fig_rm = px.bar(
    rm_discount,
    x="RM",
    y="SPECIAL DISCOUNT",
    color="SPECIAL DISCOUNT",
    title="RM Wise Discount"
)

st.plotly_chart(
    fig_rm,
    use_container_width=True
)

# ---------------- SRM ANALYSIS ----------------

st.subheader("SRM Wise Discount Ranking")

srm_discount = (
    filtered_df.groupby("SRM")["SPECIAL DISCOUNT"]
    .sum()
    .reset_index()
    .sort_values(
        "SPECIAL DISCOUNT",
        ascending=False
    )
)

fig_srm = px.bar(
    srm_discount,
    x="SRM",
    y="SPECIAL DISCOUNT",
    color="SPECIAL DISCOUNT",
    title="SRM Wise Discount"
)

st.plotly_chart(
    fig_srm,
    use_container_width=True
)

# ---------------- TOP 10 CUSTOMERS ----------------

st.subheader("Top 10 Customers")

top_customers = (
    filtered_df.groupby("CUSTOMER_NAME")["SPECIAL DISCOUNT"]
    .sum()
    .reset_index()
    .sort_values(
        by="SPECIAL DISCOUNT",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_customers,
    use_container_width=True
)

# ---------------- TOP 10 RM ----------------

st.subheader("Top 10 RM Ranking")

top_rm = (
    filtered_df.groupby("RM")["SPECIAL DISCOUNT"]
    .sum()
    .reset_index()
    .sort_values(
        by="SPECIAL DISCOUNT",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_rm,
    use_container_width=True
)

# ---------------- TOP 10 SRM ----------------

st.subheader("Top 10 SRM Ranking")

top_srm = (
    filtered_df.groupby("SRM")["SPECIAL DISCOUNT"]
    .sum()
    .reset_index()
    .sort_values(
        by="SPECIAL DISCOUNT",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_srm,
    use_container_width=True
)

# ---------------- TOP RM RECORDS ----------------

st.subheader("Top 10 RM Records With Customer Name")

top_rm_records = (
    filtered_df[
        ["RM", "CUSTOMER_NAME", "VEH", "SPECIAL DISCOUNT"]
    ]
    .sort_values(
        by="SPECIAL DISCOUNT",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_rm_records,
    use_container_width=True
)

# ---------------- TOP SRM RECORDS ----------------

st.subheader("Top 10 SRM Records With Customer Name")

top_srm_records = (
    filtered_df[
        ["SRM", "CUSTOMER_NAME", "VEH", "SPECIAL DISCOUNT"]
    ]
    .sort_values(
        by="SPECIAL DISCOUNT",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_srm_records,
    use_container_width=True
)

# ---------------- ALL RECORDS ----------------

st.subheader("All Records")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ---------------- DOWNLOAD EXCEL ----------------

excel_buffer = BytesIO()

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:
    filtered_df.to_excel(
        writer,
        index=False,
        sheet_name="Arena Report"
    )

st.download_button(
    label="📥 Download Arena Report",
    data=excel_buffer.getvalue(),
    file_name="Arena_Report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)