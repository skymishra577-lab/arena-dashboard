# Step 1: Install libraries
# pip install pandas streamlit plotly openpyxl

import pandas as pd
import plotly.express as px
import streamlit as st

# Step 2: Load Excel Data
df = pd.read_excel("discount_data.xlsx")  # apna file name yahan daalo

# Step 3: Clean Data
# Agar 'SPECIAL DISCOUNT' column me blanks hain to unhe 0 kar do
df["SPECIAL DISCOUNT"] = pd.to_numeric(df["SPECIAL DISCOUNT"], errors="coerce").fillna(0)

# Step 4: Dashboard Title
st.title("NEXA Discount Dashboard - September 2026")
st.subheader("Model-wise & TL-wise Analysis")

# Show raw data
st.dataframe(df)

# Step 5: Model-wise Total Discount
model_discount = df.groupby("VEH")["SPECIAL DISCOUNT"].sum().reset_index()
fig_model = px.bar(model_discount, x="VEH", y="SPECIAL DISCOUNT",
                   title="Model-wise Total Discount", color="VEH")
st.plotly_chart(fig_model)

# Step 6: TL-wise Performance
tl_discount = df.groupby("T.L. NAME")["SPECIAL DISCOUNT"].sum().reset_index()
fig_tl = px.bar(tl_discount, x="T.L. NAME", y="SPECIAL DISCOUNT",
                title="TL-wise Discount Performance", color="SPECIAL DISCOUNT")
st.plotly_chart(fig_tl)

# Step 7: Pie Chart - Discount Share by Model
fig_pie = px.pie(model_discount, names="VEH", values="SPECIAL DISCOUNT",
                 title="Discount Share by Vehicle Model")
st.plotly_chart(fig_pie)

# Step 8: Average Discount per Vehicle Model
avg_discount = df.groupby("VEH")["SPECIAL DISCOUNT"].mean().reset_index()
fig_avg = px.bar(avg_discount, x="VEH", y="SPECIAL DISCOUNT",
                 title="Average Discount per Vehicle", color="VEH")
st.plotly_chart(fig_avg)
