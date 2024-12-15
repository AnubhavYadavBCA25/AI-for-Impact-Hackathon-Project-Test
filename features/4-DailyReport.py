import streamlit as st
import google.generativeai as genai
from features.auth import get_user_details
from features.system_settings import  safety_settings, generation_config_daily_report, system_instruction_daily_report
from dotenv import load_dotenv
import os
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Connecting to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
daily_report_sheet = conn.read(worksheet="Daily Report Data", ttl=60)

load_dotenv()
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel(model_name="gemini-1.5-flash-8b",
                safety_settings=safety_settings,
                generation_config=generation_config_daily_report,
                system_instruction=system_instruction_daily_report)

# Get user data from session state
user_data = get_user_details()
user_name = user_data.get('name', 'User')

if not user_data:
    st.warning("You need to log in to create your daily report.")
    st.stop()

st.header("📋Daily Report", divider="rainbow")
with st.expander("What is Daily Report?"):
    st.write("Daily Report is a tool that uses Google Artificial Intelligence Model to help you generate a summary and advice based on your daily activities, feelings, and problems faced during the day. DostAI will help you to understand your day, feelings, tone, and activities. Healthcare workers can use this tool to reflect on their day, track their progress, and receive personalized advice.")

# Create a form for user input
with st.form("daily_report_form"):
    how_long_sleep = st.number_input("How long did you sleep last night?*", min_value=1, max_value=24)
    day_description = st.text_area("How was your day?*", placeholder="Ex: I had a busy day at work. I felt tired and stressed.")
    day_quality = st.radio("How would you rate your day?*", ["Great", "Good", "Average", "Bad", "Poor"])
    day_rating = st.slider("Rate your day*", 1, 10)
    problems = st.text_area("Did you face any problems or frustrations (Write Below)?*", placeholder="Ex: I had a conflict with a colleague and felt overwhelmed.")
    gratitude_exer = st.text_area("Gratitude Exercise*", placeholder="Ex: I am grateful for my family, friends, and health. Something good that happened today. I am proud of myself for completing a task and etc.")
    feelings = st.text_area("How are you feeling?*", placeholder="Ex: I feel tired, stressed, and anxious.")
    st.markdown("*Required**")
    submit_button = st.form_submit_button(label="Submit")

# Generate summary and advice based on user input
if submit_button:
    if not how_long_sleep or not day_description or not day_rating or not gratitude_exer or not problems or not feelings or not day_quality:
        st.error("Please fill out all the required fields.")
        st.stop()
    else:
        # Save the daily report data to Google Sheets
        daily_report_data = pd.DataFrame({
            "Name": user_name,
            "How long sleep": how_long_sleep,
            "Day description": day_description,
            "Day Quality": day_quality,
            "Day rating": day_rating,
            "Problems": problems,
            "Gratitude Exercise": gratitude_exer,
            "Feelings": feelings,
        }, index=[0])

        updated_daily_report_sheet = pd.concat([daily_report_sheet, daily_report_data], ignore_index=True)
        conn.update(worksheet="Daily Report Data", data=updated_daily_report_sheet)
        st.success("Your daily report has been submitted successfully.")
st.divider()

with st.spinner("Generating summary and advice..."):
    if how_long_sleep and day_description and day_rating and gratitude_exer and problems and feelings and day_quality is not None:
        st.subheader(f"Hello {user_name}, here is your daily report:")   
        user_name = user_data.get('name', 'User')
        prompt = f"""
        User: {user_name}
        How long user slept: {how_long_sleep}
        Day description: {day_description}
        Day Quality: {day_quality}
        Day rating: {day_rating}
        Gratitude Exercise: {gratitude_exer}
        Problems: {problems}
        Feelings: {feelings}
        Day quality: {day_quality}
        
        Greet the user for sharing their day and provide some advice based on their input.
        """
        response = model.generate_content(prompt)
        st.write(response.text)
    else:
        st.warning("Please fill out all the required fields to generate your daily report.")
