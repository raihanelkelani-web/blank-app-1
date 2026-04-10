import streamlit as st
import numpy as np
import tensorflow as tf
import joblib

# ----------------------------------
# LOAD MODEL + SCALER
# ----------------------------------
model = tf.keras.models.load_model("sleep_apnea_model.h5")
scaler = joblib.load("scaler.pkl")

# ----------------------------------
# PAGE DESIGN
# ----------------------------------
st.set_page_config(page_title="Sleep Apnea AI", layout="centered")

st.title("💤 Sleep Apnea Detection System")
st.write("AI-powered sleep apnea risk assessment")

# ----------------------------------
# USER INPUTS
# ----------------------------------
st.header("Enter Patient Data")

spo2 = st.number_input("SpO₂ (%)", 80, 100, 95)
heart_rate = st.number_input("Heart Rate (bpm)", 40, 120, 75)
breathing_rate = st.number_input("Breathing Rate", 10, 30, 16)
snoring = st.slider("Snoring Level", 0.0, 1.0, 0.3)
bmi = st.number_input("BMI", 10, 50, 25)

# ----------------------------------
# GENERATE REPORT
# ----------------------------------
if st.button("Generate Sleep Report"):

    # Prepare data
    input_data = np.array([[spo2, heart_rate, breathing_rate, snoring, bmi]])
    input_scaled = scaler.transform(input_data)

    # AI Prediction
    prediction = model.predict(input_scaled)[0][0]

    # ----------------------------------
    # REPORT OUTPUT
    # ----------------------------------
    st.title("🧾 Sleep Apnea Report")

    # Patient Info
    st.subheader("Patient Data")
    st.write(f"SpO₂: {spo2}%")
    st.write(f"Heart Rate: {heart_rate} bpm")
    st.write(f"Breathing Rate: {breathing_rate}")
    st.write(f"Snoring Level: {snoring}")
    st.write(f"BMI: {bmi}")

    # AI Result
    st.subheader("AI Risk Assessment")
    st.write(f"Risk Score: {prediction:.2f}")

    # ----------------------------------
    # MEDICAL INTERPRETATION
    # ----------------------------------
    st.subheader("Analysis")

    if spo2 < 92:
        st.write("⚠ Low oxygen levels detected")
    if heart_rate > 90:
        st.write("⚠ Elevated heart rate")
    if breathing_rate > 20:
        st.write("⚠ Abnormal breathing rate")
    if snoring > 0.7:
        st.write("⚠ High snoring intensity")
    if bmi > 30:
        st.write("⚠ High BMI (risk factor)")

    # ----------------------------------
    # FINAL CONCLUSION
    # ----------------------------------
    st.subheader("Conclusion")

    if prediction > 0.7:
        st.error("⚠ HIGH RISK OF SLEEP APNEA")
        st.write("Recommendation: Consult a sleep specialist immediately.")
    elif prediction > 0.4:
        st.warning("⚠ MODERATE RISK")
        st.write("Recommendation: Monitor condition and consider sleep study.")
    else:
        st.success("✔ LOW RISK")
        st.write("Recommendation: Maintain healthy lifestyle.")

    st.write("---")
    st.caption("This is an AI-based estimation and not a medical diagnosis.")