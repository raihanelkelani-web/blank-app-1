import streamlit as st

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="Sleep Apnea Monitor",
    page_icon="🫁",
    layout="centered"
)

# ---------------- CUSTOM CSS (RED THEME) ----------------
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }

    h1 {
        color: red;
        text-align: center;
    }

    .stButton>button {
        background-color: red;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-size: 16px;
    }

    .stButton>button:hover {
        background-color: darkred;
        color: white;
    }

    .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h1>Sleep Apnea Monitoring System</h1>", unsafe_allow_html=True)

st.markdown("### Enter patient readings for analysis")

# ---------------- INPUT SECTION ----------------
st.subheader("Patient Data Input")

oxygen = st.number_input("Oxygen Saturation (%)", 70, 100, 95)
heart_rate = st.number_input("Heart Rate (bpm)", 30, 180, 75)
snore_level = st.slider("Snoring Level (0–10)", 0, 10, 3)
breathing_pauses = st.number_input("Breathing Pauses (per hour)", 0, 60, 5)

# ---------------- CALCULATIONS ----------------
# Simple Apnea Index (API) estimation (you can improve later)
api = breathing_pauses + (10 - (oxygen - 90)) + (snore_level * 0.5)

# Risk logic
risk = "Low"
if oxygen < 90 or breathing_pauses > 10 or api > 15:
    risk = "High"
elif oxygen < 94 or api > 8:
    risk = "Medium"

# ---------------- BUTTON ----------------
if st.button("Analyze Patient"):

    st.markdown("## 🔴 Results")

    # Metrics display
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Oxygen", f"{oxygen}%")

    with col2:
        st.metric("Heart Rate", f"{heart_rate} bpm")

    with col3:
        st.metric("API Score", f"{api:.1f}")

    # Risk output
    st.markdown("### Risk Assessment")

    if risk == "High":
        st.error("⚠ High risk of Sleep Apnea detected")
    elif risk == "Medium":
        st.warning("⚠ Moderate risk detected")
    else:
        st.success("✔ Low risk detected")

    # Extra explanation
    st.markdown("---")
    st.markdown("### Clinical Note")
    st.write(
        "This is a simplified model for educational purposes. "
        "API (Apnea Index) is estimated based on oxygen level, snoring, "
        "and breathing pauses."
    )
