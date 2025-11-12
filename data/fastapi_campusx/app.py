import streamlit as st
import requests
import pandas as pd
from typing import Dict, Any

# -----------------------------
# Page config & small theming
# -----------------------------
st.set_page_config(
    page_title="Insurance Premium Predictor · FastAPI Client",
    page_icon="🧮",
    layout="centered",
)

st.markdown(
    """
    <style>
      .app-card{background:rgba(255,255,255,0.65); border:1px solid #eee; padding:1.25rem; border-radius:1rem; box-shadow:0 8px 24px rgba(0,0,0,0.06)}
      .muted{opacity:.7}
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Sidebar: API endpoint & sample
# -----------------------------
with st.sidebar:
    st.header("🔌 Server Settings")
    api_url = st.text_input(
        "FastAPI Predict URL",
        value="http://127.0.0.1:8000/predict",
        help="Your FastAPI /predict endpoint",
    )

    st.divider()
    st.caption("Quick sample payload (click to fill form)")
    sample_btn = st.button("Use Sample Values")

st.title("Insurance Premium Category — Client UI")
st.caption("A sleek Streamlit frontend that talks to your FastAPI model API.")

# -----------------------------
# Form
# -----------------------------
with st.form("prediction_form"):
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=1, max_value=119, value=30, step=1)
        weight = st.number_input("Weight (kg)", min_value=1.0, value=70.0, step=0.1, format="%0.1f")
        height = st.number_input("Height (m)", min_value=0.5, value=1.70, step=0.01, format="%0.2f")
        income_lpa = st.number_input("Income (LPA)", min_value=0.1, value=10.0, step=0.1, format="%0.1f")
    with col2:
        smoker_flag = st.selectbox("Smoker?", ("No", "Yes"))
        city = st.text_input("City", value="Mumbai", placeholder="e.g., Mumbai")
        occupation = st.selectbox(
            "Occupation",
            ("retired", "unemployed", "business_owner", "government_job"),
        )
        # Live BMI preview
        if height > 0:
            bmi = weight / (height ** 2)
            st.metric("BMI (preview)", f"{bmi:.1f}")
        else:
            bmi = None
    submitted = st.form_submit_button("Predict", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Autofill with sample if requested
if sample_btn:
    st.session_state["prediction_form-Age"] = 32
    st.session_state["prediction_form-Weight (kg)"] = 78.5
    st.session_state["prediction_form-Height (m)"] = 1.75
    st.session_state["prediction_form-Income (LPA)"] = 14.5
    st.session_state["prediction_form-Smoker?"] = "Yes"
    st.session_state["prediction_form-City"] = "Bangalore"
    st.session_state["prediction_form-Occupation"] = "government_job"
    st.rerun()

# -----------------------------
# Helpers
# -----------------------------

def build_payload() -> Dict[str, Any]:
    return {
        "age": int(age),
        "weight": float(weight),
        "height": float(height),
        "income_lpa": float(income_lpa),
        "smoker": smoker_flag == "Yes",
        "city": city.strip(),
        "occupation": occupation,
    }

# -----------------------------
# Submit -> call FastAPI
# -----------------------------
if submitted:
    payload = build_payload()
    try:
        with st.spinner("Contacting FastAPI model…"):
            resp = requests.post(api_url, json=payload, timeout=20)
        if resp.status_code == 200:
            data = resp.json()
            pred = data['prediction']
            st.success(f"Predicted Insurance Premium Category: **{pred}**")
            with st.expander("View request & raw response"):
                st.code(pd.Series(payload).to_json(indent=2), language="json")
                st.code(pd.Series(data).to_json(indent=2), language="json")
        else:
            st.error(f"Server returned {resp.status_code}")
            st.text_area("Details", resp.text, height=150)
    except requests.exceptions.RequestException as e:
        st.error("Request failed. Is the FastAPI server running?")
        st.exception(e)

st.markdown("""
<div class="muted">
Tip: This UI sends **raw inputs** (age, weight, height, income, smoker, city, occupation). 
Your FastAPI app computes derived features (BMI, age_group, lifestyle_risk, city_tier) server-side.
</div>
""", unsafe_allow_html=True)
