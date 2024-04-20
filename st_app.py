import streamlit as st
from bot import init_model
import time
import random


def typewrite(message: str):
    for s in message:
        yield s
        time.sleep(random.random() * 0.1)


st.title("MAKAKI V ATAKE")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Any quetions?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        answer = 
        response = st.write_stream(typewrite("echo echo echo ....  " + prompt))
    st.session_state.messages.append({"role": "assistant", "content": response})