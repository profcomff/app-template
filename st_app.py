import streamlit as st
import bot
import time
import random


def typewrite(message: str):
    for s in message:
        yield s
        time.sleep(random.random() * 0.05)


st.title("MAKAKI V ATAKE")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.uid = random.randint(0, 1 << 64)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Any quetions?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        answer = bot.answer(prompt, st.session_state.uid)
        response = st.write_stream(typewrite(answer))
    st.session_state.messages.append({"role": "assistant", "content": response})