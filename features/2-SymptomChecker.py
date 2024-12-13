import google.generativeai as genai
import streamlit as st
import time
import os
from dotenv import load_dotenv
from features.system_settings import safety_settings, system_instruction_symptom_checker, generation_config_symptom_checker

load_dotenv()
GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-pro',
                safety_settings=safety_settings,
                system_instruction=system_instruction_symptom_checker,
                generation_config=generation_config_symptom_checker)

st.warning('⚠️Note: Dost AI Symptom Checker is a AI based features which is just a Prototype right now. Please use it with caution and consult a doctor for professional advice.')

st.header('🩺Symptom Checker', anchor='symptom-checker', divider='rainbow')
with st.expander('What is Symptom Checker?'):
    st.write('Symptom Checker is a tool that uses Google Artificial Intelligence Model to help you identify possible health conditions based on your symptoms. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a doctor for professional advice.')
st.divider()

st.subheader('Enter your details to check your symptoms:')
with st.form(key='symptom-checker-form'):
    gender = st.selectbox('Select your gender*', ['Male', 'Female', 'Other'])
    age = st.number_input('Enter your age*', min_value=1, max_value=100)
    body_temperature = st.number_input('Enter your body temperature in Fahrenheit*', min_value=95.0, max_value=110.0, step=0.1)
    symptoms = st.text_area('Enter your symptoms*', height=100, placeholder='Example: headache, fever, cough etc. from last 2 days or other relevant information')
    st.markdown('*Required**')
    submit_button = st.form_submit_button(label='Check Symptoms')

    if submit_button:
        if not gender or not age or not symptoms or not body_temperature:
            st.error('Please fill all the required fields.')
            st.stop()
        else:
            st.success('Please wait while DostAI is processing your request...')
st.divider()

with st.spinner('Processing your request...'):
    if gender and age and symptoms and body_temperature is not None:
        st.subheader('Symptom Checker Results:')
        prompt = f""" I am a {age} year's old {gender} with body temperature {body_temperature} and symptoms like {symptoms}. Can you help me to identify the possible health conditions and what to do next?"""
        response = model.generate_content(prompt)
        st.write(response.text)
    else:
        st.warning('Please fill all the required fields to check your symptoms.')