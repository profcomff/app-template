import streamlit as st
import random
import time


def typewrite(message: str):
    for s in message:
        yield s
        time.sleep(random.random() * 0.1)


st.title("Simple chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
