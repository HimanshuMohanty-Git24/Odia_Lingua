# Home.py
import streamlit as st

# Page config
st.set_page_config(
    page_title="Odia Lingua 🐚🤖",
    page_icon="🐚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header image and title
col1, col2 = st.columns([3,1])
with col1:
    st.title("Odia Lingua 🐚🤖")
    st.subheader("Your AI-powered Odia Language Assistant")

with col2:
    st.image("https://upload.wikimedia.org/wikipedia/commons/0/09/Odisha_banner.jpg", 
             caption="Odisha Heritage", use_column_width=True)

# About section
st.markdown("""
### About Odia Lingua
Odia Lingua is an AI-powered chatbot that can help anyone who knows odia to chat with AI in odia this is a bridge to bring inclusivity in the AI world.
This chatbot is designed to help you practice Odia conversations, learn about Odia culture and traditions, get information in Odia language, and listen to proper Odia pronunciation.
This was made keeping in mind the people who are not comfortable with English and can use this chatbot to get information in their native language.


#### How it can help:
- Practice Odia conversations
- Learn about Odia culture and traditions  
- Get information in Odia language
- Listen to proper Odia pronunciation
""")

# Start chat button
st.sidebar.success("Select a page above.")

if st.button("🗣️ Start Chatting in Odia", type="primary", use_container_width=True):
    st.switch_page("pages/Chatbot.py")