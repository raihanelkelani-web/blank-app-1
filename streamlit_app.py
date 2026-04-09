import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sleep Apnea App", layout="wide")

# ------------------ SIDEBAR NAVIGATION ------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Welcome", "Sleep Analysis"])

# ------------------ PAGE 1: WELCOME ------------------
if page == "Welcome":

    st.title("🫁 Sleep Apnea Monitoring System")

    st.image("sleep_apnea.jpg", use_column_width=True)

    st.markdown("""
    ## Welcome!

    This system helps monitor and assess the risk of sleep apnea using:
    - Oxygen saturation (SpO2)
    - Heart rate
    - Respiratory rate
    - Apnea events

    ### Features:
    ✔ AHI Calculation  
    ✔ Risk Assessment  
    ✔ Severity Classification  
    ✔ Clinical Recommendations  

    👉 Use the sidebar to start analysis.
    """)

# ------------------ PAGE 2: MAIN APP ------------------
elif page == "Sleep Analysis":

    st.title("📊 Sleep Apnea Analysis")

    # -------- INPUT --------
    st.markdown("### Patient Data")

    col1, col2, col3 = st.columns(3)

    with col1:
        spo2 = st.number_input("SpO2 (%)", min_value=50, max_value=100, value=98)

    with col2:
        hr = st.number_input("Heart Rate (bpm)", min_value=40, max_value=180, value=70)

    with col3:
        resp = st.number_input("Respiratory Rate", min_value=5, max_value=40, value=16)

    st.markdown("### Sleep Data")

    col4, col5 = st.columns(2)

    with col4:
        events = st.number_input("Number of Apnea Events", min_value=0, value=5)

    with col5:
        hours = st.number_input("Hours of Sleep", min_value=1.0, value=8.0)

    # -------- BUTTON --------
    if st.button("Analyze"):

        # AHI
        ahi = events / hours

        # Severity
        if ahi < 5:
            severity = "Normal"
        elif ahi < 15:
            severity = "Mild"
        elif ahi < 30:
            severity = "Moderate"
        else:
            severity = "Severe"

        # Risk Score
        risk_score = (100 - spo2) + (hr / 10) + resp

        # -------- RESULTS --------
        st.markdown("## Results")

        col6, col7, col8 = st.columns(3)
        col6.metric("AHI Score", round(ahi, 2))
        col7.metric("SpO2", spo2)
        col8.metric("Risk Score", round(risk_score, 2))

        # Alerts
        if severity == "Severe":
            st.error("⚠️ Severe Sleep Apnea")
        elif severity == "Moderate":
            st.warning("⚠️ Moderate Sleep Apnea")
        elif severity == "Mild":
            st.info("ℹ️ Mild Sleep Apnea")
        else:
            st.success("✅ Normal")

        st.write(f"### Severity: {severity}")

        # Recommendations
        st.markdown("## Recommendations")

        if severity == "Severe":
            st.write("⚠️ Immediate medical consultation recommended.")
        elif severity == "Moderate":
            st.write("⚠️ Sleep study advised.")
        elif severity == "Mild":
            st.write("✔ Monitor and improve sleep habits.")
        else:
            st.write("✔ Maintain healthy lifestyle.")

        # Graph
        st.markdown("## Sample Trend")

        data = pd.DataFrame({
            "SpO2": [98, 96, 95, 92, 90],
            "Heart Rate": [70, 75, 80, 85, 90]
        })

        st.line_chart(data)

        # Report
        st.markdown("## Sleep Report")

        st.write(f"AHI: {round(ahi, 2)}")
        st.write(f"Severity: {severity}")
        st.write(f"Risk Score: {round(risk_score, 2)}")

        # Save
        record = pd.DataFrame([[spo2, hr, resp, events, hours, ahi, severity]],
                              columns=["SpO2", "HR", "Resp", "Events", "Hours", "AHI", "Severity"])

        record.to_csv("records.csv", mode='a', header=False, index=False)

        st.success("Data saved successfully!")