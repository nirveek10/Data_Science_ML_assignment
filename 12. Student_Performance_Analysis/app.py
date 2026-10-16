import streamlit as st
import pandas as pd
import joblib

# -------------------------
# Page configuration
# -------------------------
st.set_page_config(
    page_title="Student Performance Analysis",
    page_icon="📚",
    layout="wide"
)

# -------------------------
# Load saved models
# -------------------------
@st.cache_resource
def load_models():
    regression = joblib.load("models/regression_model.joblib")
    classification = joblib.load("models/classification_model.joblib")
    metadata = joblib.load("models/model_metadata.joblib")
    return regression, classification, metadata

regression_model, classification_model, metadata = load_models()

st.title("📚 Student Performance Analysis")
st.write(
    "Enter student details to estimate their final grade "
    "and identify whether additional academic support may be needed."
)

st.info(
    "This application provides estimates from machine learning models. "
    "Teachers should consider other information and their own judgment "
    "before making decisions about a student."
)

# -------------------------
# Input form
# -------------------------
with st.form("student_details"):
    st.subheader("Student Details")

    st.caption("Basic information")

    col1, col2, col3 = st.columns(3)

    with col1:
        school = st.selectbox("School", ["GP", "MS"])
        sex = st.selectbox("Sex", ["F", "M"])
        age = st.slider("Age", 15, 22, 17)
        address = st.selectbox("Home address type", ["U", "R"])
        famsize = st.selectbox("Family size", ["GT3", "LE3"])
        Pstatus = st.selectbox(
            "Parents' cohabitation status", ["T", "A"]
        )

    with col2:
        Medu = st.selectbox("Mother's education (0–4)", [0, 1, 2, 3, 4])
        Fedu = st.selectbox("Father's education (0–4)", [0, 1, 2, 3, 4])
        Mjob = st.selectbox(
            "Mother's job",
            ["teacher", "health", "services", "at_home", "other"]
        )
        Fjob = st.selectbox(
            "Father's job",
            ["teacher", "health", "services", "at_home", "other"]
        )
        reason = st.selectbox(
            "Reason for choosing school",
            ["home", "reputation", "course", "other"]
        )
        guardian = st.selectbox(
            "Guardian", ["mother", "father", "other"]
        )

    with col3:
        traveltime = st.selectbox(
            "Travel time (1–4)", [1, 2, 3, 4]
        )
        studytime = st.selectbox(
            "Weekly study time (1–4)", [1, 2, 3, 4]
        )
        failures = st.selectbox(
            "Past class failures", [0, 1, 2, 3]
        )
        absences = st.number_input(
            "School absences", min_value=0, max_value=100, value=4
        )

    st.divider()
    st.subheader("Family and School Support")

    col4, col5, col6 = st.columns(3)

    with col4:
        schoolsup = st.selectbox(
            "Extra educational support", ["yes", "no"]
        )
        famsup = st.selectbox(
            "Family educational support", ["yes", "no"]
        )
        paid = st.selectbox(
            "Extra paid classes", ["yes", "no"]
        )

    with col5:
        activities = st.selectbox(
            "Extracurricular activities", ["yes", "no"]
        )
        nursery = st.selectbox(
            "Attended nursery school", ["yes", "no"]
        )
        higher = st.selectbox(
            "Wants higher education", ["yes", "no"]
        )

    with col6:
        internet = st.selectbox("Internet access at home", ["yes", "no"])
        romantic = st.selectbox(
            "In a romantic relationship", ["yes", "no"]
        )

    st.divider()
    st.subheader("Lifestyle and Well-being")

    col7, col8, col9 = st.columns(3)

    with col7:
        famrel = st.slider("Family relationship quality (1–5)", 1, 5, 4)
        freetime = st.slider("Free time after school (1–5)", 1, 5, 3)

    with col8:
        goout = st.slider("Going out with friends (1–5)", 1, 5, 3)
        Dalc = st.slider("Workday alcohol consumption (1–5)", 1, 5, 1)

    with col9:
        Walc = st.slider("Weekend alcohol consumption (1–5)", 1, 5, 1)
        health = st.slider("Self-reported health (1–5)", 1, 5, 4)

    submitted = st.form_submit_button(
        "Predict Student Performance",
        type="primary",
        use_container_width=True
    )

# -------------------------
# Make predictions
# -------------------------
if submitted:
    student = pd.DataFrame([{
        "school": school,
        "sex": sex,
        "age": age,
        "address": address,
        "famsize": famsize,
        "Pstatus": Pstatus,
        "Medu": Medu,
        "Fedu": Fedu,
        "Mjob": Mjob,
        "Fjob": Fjob,
        "reason": reason,
        "guardian": guardian,
        "traveltime": traveltime,
        "studytime": studytime,
        "failures": failures,
        "schoolsup": schoolsup,
        "famsup": famsup,
        "paid": paid,
        "activities": activities,
        "nursery": nursery,
        "higher": higher,
        "internet": internet,
        "romantic": romantic,
        "famrel": famrel,
        "freetime": freetime,
        "goout": goout,
        "Dalc": Dalc,
        "Walc": Walc,
        "health": health,
        "absences": absences
    }])

    # Ensure columns match the training feature order
    student = student[metadata["features"]]

    predicted_grade = float(
        regression_model.predict(student)[0]
    )

    risk_prediction = int(
        classification_model.predict(student)[0]
    )

    risk_probabilities = classification_model.predict_proba(student)[0]
    class_labels = list(classification_model.named_steps["model"].classes_)
    at_risk_index = class_labels.index(1)
    risk_score = float(risk_probabilities[at_risk_index])

    st.divider()
    st.subheader("Prediction Results")

    result1, result2, result3 = st.columns(3)

    with result1:
        st.metric(
            "Estimated Final Grade",
            f"{predicted_grade:.1f} / 20"
        )

    with result2:
        if risk_prediction == 1:
            st.metric("Risk Classification", "At risk")
        else:
            st.metric("Risk Classification", "Likely to pass")

    with result3:
        st.metric(
            "Estimated At-risk Score",
            f"{risk_score:.1%}"
        )

    st.progress(min(max(risk_score, 0.0), 1.0))

    if risk_prediction == 1:
        st.warning(
            "The classification model has flagged this student as "
            "potentially at risk. Consider reviewing their learning needs "
            "and whether additional support would help."
        )
    else:
        st.success(
            "The classification model predicts that this student is "
            "likely to pass. Continue monitoring their progress as usual."
        )

    st.caption(
        "The grade is a regression estimate. The risk score is the "
        "classifier's estimated probability, not a guaranteed outcome "
        "or necessarily a calibrated probability."
    )

    with st.expander("View entered student information"):
        st.dataframe(student, use_container_width=True)
