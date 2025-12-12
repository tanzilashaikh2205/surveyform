
import mysql.connector
import streamlit as st

def get_connection():
    return mysql.connector.connect(
        host="mysql.railway.internal",
        user="root",
        password="zpJRNnJmlngUkNzUxmVDRAiPymXJEeFM",
        database="railway",
        port=3306
    )

# ----------------------------------------
# PAGE CONFIG
# ----------------------------------------
st.set_page_config(page_title="Road Accident Survey", layout="centered")

st.markdown("""
<h1 style='text-align:center; color:#FF4B4B;'>🚦 Road Accident Causes Survey</h1>
<p style='text-align:center; color:gray;'>Help us analyze road safety issues in your area</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ----------------------------------------
# FORM
# ----------------------------------------
with st.form("accident_form"):
    st.markdown("<h3 style='color:white;'>🧍 Respondent Information</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
    with col2:
        age = st.selectbox("Age", ["15–20", "21–25", "26–30", "31–40", "40+"])


    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Gender", ["Male", "Female", "Prefer not to say"])
    with col2:
        city = st.text_input("City / Area")

    st.markdown("---")
    st.markdown("<h3 style='color:white;'>🚗 Driving Information</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        drive_vehicle = st.radio("Do you drive a vehicle?", ["Yes", "No"])
    with col2:
        vehicle_type = st.selectbox(
            "Vehicle Type",
            ["Two-wheeler", "Car", "Auto-rickshaw", "Heavy vehicle", "Bicycle", "Not applicable"]
        )

    col1, col2 = st.columns(2)
    with col1:
        driving_frequency = st.selectbox(
            "Driving Frequency",
            ["Daily", "Occasionally", "Rarely", "Never"]
        )
    with col2:
        avg_speed = st.selectbox(
            "Average Speed",
            ["Below 40 km/h", "40–60 km/h", "60–80 km/h", "Above 80 km/h"]
        )

    st.markdown("---")
    st.markdown("<h3 style='color:white;'>⚠️ Safety Behaviour</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        helmet_seatbelt = st.selectbox(
            "Helmet/Seatbelt Usage",
            ["Always", "Sometimes", "Rarely", "Never"]
        )
    with col2:
        mobile_use = st.selectbox(
            "Mobile Usage While Driving",
            ["Frequently", "Sometimes", "Rarely", "Never"]
        )

    col1, col2 = st.columns(2)
    with col1:
        stress_driving = st.selectbox(
            "Drive Under Stress/Anger?",
            ["Often", "Sometimes", "Rarely", "Never"]
        )
    with col2:
        traffic_rules = st.selectbox(
            "Traffic Rule Following",
            ["Always", "Mostly", "Sometimes", "Rarely", "Never"]
        )

    st.markdown("---")
    st.markdown("<h3 style='color:white;'>📍 Accident Details</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        accident_experience = st.selectbox(
            "Accident Experience",
            ["Witnessed", "Involved", "Both", "No"]
        )
    with col2:
        accident_time = st.selectbox(
            "Time of Accident",
            ["Morning", "Afternoon", "Evening", "Night", "Not applicable"]
        )

    col1, col2 = st.columns(2)
    with col1:
        accident_location = st.selectbox(
            "Accident Location",
            ["Highway", "City", "Rural Road", "Near School/College", "Junction", "Not applicable"]
        )
    with col2:
        accident_cause = st.selectbox(
            "Main Accident Cause",
            [
                "Overspeeding", "Drunk driving", "Mobile usage", "Poor roads",
                "Weather", "Breaking rules", "Vehicle issue",
                "Pedestrian negligence", "Not applicable"
            ]
        )

    major_causes = st.multiselect(
        "Major Causes in Your Area",
        [
            "Overspeeding", "Mobile usage", "Rash driving", "Drunk driving",
            "Lack of traffic police", "Poor roads", "Street animals",
            "No street lights", "No pedestrian crossing"
        ]
    )

    st.markdown("---")
    st.markdown("<h3 style='color:white;'>🌍 Area Condition</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        road_condition = st.selectbox(
            "Road Condition",
            ["Very good", "Good", "Average", "Poor", "Very poor"]
        )
    with col2:
        street_lights = st.selectbox(
            "Street Light Availability",
            ["Sufficient", "Average", "Poor", "No street lights"]
        )

    col1, col2 = st.columns(2)
    with col1:
        police_presence = st.selectbox(
            "Traffic Police Presence",
            ["Always", "Sometimes", "Rarely", "Never"]
        )
    with col2:
        road_sign_visibility = st.selectbox(
            "Road Sign Visibility",
            ["Yes", "Partially", "No"]
        )

    animal_presence = st.selectbox(
        "Stray Animals Causing Risk?",
        ["Frequently", "Sometimes", "Rarely", "No"]
    )

    penalties = st.selectbox(
        "Should strict penalties be applied?",
        ["Yes", "Maybe", "No"]
    )

    st.markdown("---")
    st.markdown("<h3 style='color:white;'>💬 Suggestions</h3>", unsafe_allow_html=True)
    suggestions = st.text_area("Any suggestions to improve road safety?")

    submit = st.form_submit_button("Submit", use_container_width=True)


# ----------------------------------------
# INSERT INTO DATABASE
# ----------------------------------------
if submit:
    try:
        db = connect_db()
        cursor = db.cursor()

        sql = """
            INSERT INTO accident_survey (
                name, age, gender, city, drive_vehicle, vehicle_type,
                driving_frequency, avg_speed, helmet_seatbelt, mobile_use,
                stress_driving, traffic_rules, accident_experience,
                accident_time, accident_location, accident_cause, major_causes,
                road_condition, street_lights, police_presence,
                road_sign_visibility, animal_presence, penalties, suggestions
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            name, age, gender, city, drive_vehicle, vehicle_type,
            driving_frequency, avg_speed, helmet_seatbelt, mobile_use,
            stress_driving, traffic_rules, accident_experience, accident_time,
            accident_location, accident_cause, ",".join(major_causes),
            road_condition, street_lights, police_presence,
            road_sign_visibility, animal_presence, penalties, suggestions
        )

        cursor.execute(sql, values)
        db.commit()

        st.success("✅ Your response has been saved to the database!")

    except Exception as e:
        st.error(f"❌ Error saving data: {e}")
