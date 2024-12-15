import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from features.auth import get_user_details

# Connecting to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
feedback_sheet = conn.read(worksheet="Feedback Data", ttl=60)

def contact_us():

    user_data = get_user_details()
    name = user_data.get('name', 'N/A')
    email = user_data.get('email', 'N/A')

    if not user_data:
        st.warning("You need to log in to view your dashboard.")
        return

    st.header("📞Contact Us", divider="rainbow")
    st.write("We value your feedback and queries. Please fill out the form below to get in touch with us.")

    with st.form("contact_form"):
        name = st.text_input("Your Name*", value=name)
        email = st.text_input("Your Email*", value=email)
        rate_us = st.selectbox("Rate Us*", ["Excellent", "Good", "Average", "Poor"])
        subject = st.text_input("Subject*", placeholder="Enter the subject of your message")
        message = st.text_area("Message*", placeholder="Enter your message here", height=200)
        st.markdown("*Required**")
        submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        if not name or not email or not subject or not message or not rate_us:
            st.error("Please fill out all fields.")
        else:

            feedback_data = pd.DataFrame({
                "Name": name,
                "Email": email,
                "Rate Us": rate_us,
                "Subject": subject,
                "Message": message,
            }, index=[0])

            updated_feedback_sheet = pd.concat([feedback_sheet, feedback_data], ignore_index=True)
            conn.update(worksheet="Feedback Data",data=updated_feedback_sheet)
            # Here you can add the logic to handle the form submission
            # For example, send an email, save to a database, etc.
            st.success("Thank you for your feedback! We will get back to you soon.")

if __name__ == "__main__":
    contact_us()