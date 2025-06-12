# app.py – Finactive Dashboard MVP with Excel Upload & Scoring

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Finactive – Wealth Dashboard", layout="wide")
st.title("🏦 Finactive – Personal Financial Dashboard")

# --- Sidebar File Upload ---
uploaded_file = st.sidebar.file_uploader("📂 Upload Client Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    client_names = df["Client"].unique()
    selected_client = st.sidebar.selectbox("🔍 Select Client", client_names)
    data = df[df["Client"] == selected_client].iloc[0]

    # --- Net Worth Calculation ---
    assets = data[["Cash", "FDs", "Equity", "MFs", "Real Estate", "EPF"]].sum()
    liabilities = data[["Home Loan", "Car Loan"]].sum()
    net_worth = assets - liabilities
    savings_rate = 1 - data["Expenses"] / data["Income"]
    debt_ratio = liabilities / data["Income"]
    emergency_months = data["Emergency Fund"] / (data["Expenses"] / 12)

    # --- Scores ---
    scores = {
        "Investment Score": int(min(100, (data["Equity"] + data["MFs"]) / data["Income"] * 100)),
        "Debt Score": int(max(0, 100 - debt_ratio * 100)),
        "Budgeting Score": int(savings_rate * 100),
        "Emergency Fund Score": int(min(100, emergency_months / 6 * 100))
    }

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Net Worth")
        st.metric("💰 Net Worth", f"₹ {net_worth:,.0f}")
        st.write("### Assets")
        st.bar_chart(data[["Cash", "FDs", "Equity", "MFs", "Real Estate", "EPF"]])
        st.write("### Liabilities")
        st.bar_chart(data[["Home Loan", "Car Loan"]])

    with col2:
        st.subheader("📈 Portfolio Allocation")
        pie_data = data[["Equity", "MFs"]]
        fig, ax = plt.subplots()
        ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%')
        ax.axis('equal')
        st.pyplot(fig)

        st.subheader("🧠 Financial Scores")
        for label, score in scores.items():
            st.metric(label, f"{score}/100")
            st.progress(score / 100)

    st.markdown("---")
    st.subheader("📌 Smart Recommendations")
    if savings_rate < 0.2:
        st.warning("Your savings rate is below 20%. Reduce discretionary expenses.")
    if emergency_months < 6:
        st.info("Emergency fund should cover at least 6 months of expenses.")
    if debt_ratio > 0.4:
        st.error("High debt ratio. Try to reduce liabilities.")
    if scores["Investment Score"] < 60:
        st.info("Consider increasing investments for long-term growth.")

else:
    st.info("Please upload an Excel file with client data to begin.")
# Main app logic placeholder
