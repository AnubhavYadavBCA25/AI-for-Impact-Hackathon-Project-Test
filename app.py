import streamlit as st
import os
import streamlit_lottie as st_lottie
from features.auth import authentication
from features.dashboard import user_dashboard
from features.contact_us import contact_us
from features.functions import load_lottie_file

# Streamlit page configuration
st.set_page_config(
    page_title="Dost AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state keys
if 'register' not in st.session_state:
    st.session_state['register'] = False
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = {}

#################################### Introduction Page ####################################
def introduction():
    st.header("🤖DostAI: Your Mental Health Companion", divider='rainbow')
    with st.container(border=False):
        left_column, right_column = st.columns(2)
        with left_column:
            st.subheader("Welcome to DostAI!", divider='rainbow')
            intro_text = '''
            **DostAI** is an AI-driven companion designed to support healthcare workers by providing mental health assistance, medical tools, and personalized care features. 
            This project addresses the challenges faced by healthcare workers in high-pressure environments, enhancing their well-being and professional efficiency. 
            The application includes a chatbot, symptom checker, daily plans maker, and daily report generator, among other features.

            **DostAI** is designed to provide a safe space for healthcare workers to express their feelings, seek advice, and access mental health resources. 
            The application leverages artificial intelligence to deliver personalized responses and recommendations based on the user's input. Users can interact with the chatbot,
            check their or their patients symptoms for early diagnosis, create daily plans, and generate daily reports to track their well-being and progress. With DostAI, healthare workers can
            receive the support they need to navigate the challenges of their profession and maintain their mental health.
            '''
            st.write(intro_text)
        with right_column:
            robot_file = load_lottie_file('animations/robot.json')
            st_lottie.st_lottie(robot_file, key='robot', height=450, width=450 ,loop=True)
        st.divider()
    
    with st.container(border=False):
        left_column, right_column = st.columns(2)
        with right_column:
            st.subheader("Key Features", divider='rainbow')
            features = [
                "**Share with Me (ChatBot)**: A conversational AI chatbot that provides mental health support, talks to you, and listens to your concerns. Chat in your preferred language.",
                "**Symptom Checker**: A tool to check symptoms and provide early diagnosis for health conditions.",
                "**Daily Plans Maker**: A feature to create daily plans and set goals for your day.",
                "**Daily Report**: A tool to generate a summary and advice based on your daily activities, feelings, and problems faced during the day.",
                "**Profile**: A user dashboard to view and update your personal and professional information.",
                "**Contact Us**: A feature to connect with us for feedback, queries, and support.",
            ]
            for feature in features:
                st.write(f"🔹 {feature}")
            st.write("*Explore the features in the sidebar to learn more about each one.*")
        
        with left_column:
            features_file = load_lottie_file('animations/features.json')
            st_lottie.st_lottie(features_file, key='features', height=450, width=450 ,loop=True)
        st.divider()

    with st.container(border=True):
        st.subheader("FAQs", divider='rainbow')
        
        with st.expander("What is DostAI?"):
            st.write("DostAI is an AI-driven companion designed to support healthcare workers by providing mental health assistance, medical tools, and personalized care features.")
        
        with st.expander("What are the key features of DostAI?"):
            st.write("DostAI includes a chatbot, symptom checker, daily plans maker, daily report generator, and user dashboard.")
        
        with st.expander("How can DostAI help healthcare workers?"):
            st.write("DostAI provides a safe space for healthcare workers to express their feelings, seek advice, and access mental health resources.")
        
        with st.expander("How does DostAI use artificial intelligence?"):
            st.write("DostAI leverages artificial intelligence to deliver personalized responses and recommendations based on the user's input. Where model is trained on healthcare data.")

        with st.expander("How can I get started with DostAI?"):
            st.write("To get started with DostAI, Register with your credentials and explore the features in the sidebar to learn more about each one.")

        with st.expander("Is my data secure with DostAI?"):
            st.write("DostAI takes data privacy and security seriously. Your data is encrypted and stored securely to protect your privacy.")

        with st.expander("How can I provide feedback or contact the DostAI team?"):
            st.write("You can provide feedback or contact the DostAI team by using the 'Contact Us' feature in the sidebar.")

            
# Initialize session state for authentication
authentication()

# Page Navigation
if st.session_state["authentication_status"]:
    pg = st.navigation([
        st.Page(introduction, title='Introduction', icon='🙋🏻‍♂️'),
        st.Page("features/1-ChatBot.py", title='Share with Me (ChatBot)', icon='🤖'),
        st.Page("features/2-SymptomChecker.py", title='Symptom Checker', icon='🩺'),
        st.Page("features/3-DailyPlans.py", title='Daily Plans Maker', icon='📅'),
        st.Page("features/4-DailyReport.py", title='Daily Report', icon='📋'),
        st.Page(user_dashboard, title='Profile', icon='🧑🏻‍⚕️'),
        st.Page(contact_us, title='Contact Us', icon='📞'),
    ])

    pg.run()