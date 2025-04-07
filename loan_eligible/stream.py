import streamlit as st
import requests

# Backend URL (Ensure it matches Flask port)
API_URL = "http://127.0.0.1:5000/predict"

st.title("🏦 Loan Eligibility Prediction")

# User input fields
experience = st.number_input("Experience (years)", min_value=0, max_value=50, step=1)
income = st.number_input("Annual Income ($)", min_value=10000, max_value=500000, step=1000)
cc_avg = st.number_input("Credit Card Avg. ($)", min_value=0.0, max_value=20.0, step=0.1)
education = st.selectbox("Education Level", [1, 2, 3])
mortgage = st.number_input("Mortgage ($)", min_value=0, max_value=500000, step=1000)
cd_account = st.selectbox("CD Account (1=Yes, 0=No)", [0, 1])
credit_card = st.selectbox("Has Credit Card? (1=Yes, 0=No)", [0, 1])

# Predict button
if st.button("🔍 Check Eligibility"):
    # Prepare data for API
    data = {
        "experience": experience, "income": income, "cc_avg": cc_avg,
        "education": education, "mortgage": mortgage,
        "cd_account": cd_account, "credit_card": credit_card
    }

    try:
        response = requests.post(API_URL, json=data)
        
        if response.status_code == 200:
            result = response.json()
            st.success(f"✅ Loan Eligibility: {result['result']}")
        else:
            error_msg = response.json().get("error", "Unknown error occurred")
            st.error(f"❌ Error: {error_msg}")

    except requests.exceptions.RequestException as e:
        st.error(f"🚨 Connection Error: {e}")
