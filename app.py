import os
import sys
import subprocess
import streamlit as st
import matplotlib.pyplot as plt
import streamlit.components.v1 as components  # Import the components module
from utils import calculate_bmi, calculate_bmr, calculate_daily_calories, estimate_body_composition

# Include custom CSS
with open("static/style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Include custom JavaScript
custom_js = """
<script>
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Custom JavaScript loaded');
        // Add your custom JavaScript here
    });
</script>
"""
components.html(custom_js)

st.title("Fat Loss Planner")

with st.form("user_input_form"):
    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("Height", min_value=0, format="%d")
        height_unit = st.selectbox("Height Unit", ["cm", "m", "inches", "feet"], key="height_unit", label_visibility="collapsed", format_func=lambda x: x, help="Select height unit")
        weight = st.number_input("Weight", min_value=0, format="%d")
        weight_unit = st.selectbox("Weight Unit", ["kg", "lbs"], key="weight_unit", label_visibility="collapsed", format_func=lambda x: x, help="Select weight unit")
        age = st.number_input("Age", min_value=0, format="%d")
        gender = st.selectbox("Gender", ["Male", "Female"])
    with col2:
        activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly active", "Moderately active", "Very active", "Super active"])
        target_weight = st.number_input("Target Weight (kg)", min_value=0, format="%d")
        time_period = st.number_input("Time Period (weeks)", min_value=0, format="%d")
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    height_unit = st.session_state["height_unit"]
    weight_unit = st.session_state["weight_unit"]

    if height_unit == "inches":
        height_m = height * 0.0254
    elif height_unit == "feet":
        height_m = height * 0.3048
    elif height_unit == "m":
        height_m = height
    else:
        height_m = height / 100

    if weight_unit == "lbs":
        weight_kg = weight * 0.453592
    else:
        weight_kg = weight

    bmi = calculate_bmi(weight_kg, height_m)
    bmr = calculate_bmr(weight_kg, height_m * 100, age, gender)  # height in cm

    activity_factors = {
        "Sedentary": 1.2,
        "Lightly active": 1.375,
        "Moderately active": 1.55,
        "Very active": 1.725,
        "Super active": 1.9
    }
    activity_factor = activity_factors[activity_level]

    result = calculate_daily_calories(weight_kg, target_weight, time_period, bmr, activity_factor)
    daily_calorie_deficit = result["Daily Calorie Deficit"]
    tdee = result["TDEE"]

    body_composition = estimate_body_composition(weight_kg, height_m, bmi, gender)

    # Determine BMI category
    if bmi < 18.5:
        bmi_category = "Underweight"
    elif 18.5 <= bmi < 25:
        bmi_category = "Normal weight"
    elif 25 <= bmi < 30:
        bmi_category = "Overweight"
    elif 30 <= bmi < 35:
        bmi_category = "Obesity Class I (Moderate)"
    elif 35 <= bmi < 40:
        bmi_category = "Obesity Class II (Severe)"
    else:
        bmi_category = "Obesity Class III (Very Severe/Morbid Obesity)"

    # Record inputs and results in chat history
    chat_history = ""
    chat_history += f"\nHeight: {height} {height_unit}, Weight: {weight} {weight_unit}, Age: {age}, Gender: {gender}, Activity Level: {activity_level}, Target Weight: {target_weight} kg, Time Period: {time_period} weeks"
    chat_history += f"\nTDEE: {tdee:.2f} kcal/day, Daily Calorie Deficit: {daily_calorie_deficit if isinstance(daily_calorie_deficit, str) else f'{daily_calorie_deficit:.2f} kcal/day'}"
    st.sidebar.text_area("Chat History", chat_history, height=300, disabled=True)

    # Display results on a new page
    st.title("Results")
    st.write(f"**Your BMI**: {bmi:.2f} ({bmi_category})")
    st.write(f"**Daily Calories Burned (TDEE)**: {tdee:.2f} kcal/day")

    if isinstance(daily_calorie_deficit, str):
        st.write(f"**Daily Calorie Deficit**: {daily_calorie_deficit}")
    else:
        st.write(f"**Daily Calorie Deficit**: {daily_calorie_deficit:.2f} kcal/day")

    # Plotting body composition
    fig, ax = plt.subplots()
    labels = ['Lean Body Mass', 'Fat Mass']
    sizes = [body_composition['lean_mass'], body_composition['fat_mass']]
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    st.pyplot(fig)

if __name__ == "__main__":
    # Check if the script is being run by Streamlit
    if not os.getenv("STREAMLIT_RUN"):
        os.environ["STREAMLIT_RUN"] = "true"
        subprocess.run(["streamlit", "run", sys.argv[0]])