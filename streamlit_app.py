import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

st.set_page_config(page_title = "Generative AI Assistant")

with st.sidebar:
    st.title("Let's get chatting!")
    if ('EMAIL' in st.secrets) and ('PASS' in st.secrets):
        st.success("Credentials already entered! Let's go!")
        user_email = st.secrets['EMAIL']
        user_pass = st.secrets['PASS']
    else:
        user_email = st.text_input("Enter your email address")
        user_pass = st.text_input("Enter your password")
        if not(user_email and user_pass):
            st.warning("Don't forget to put your credentials in!")
        else:
            st.success("Alright! Let's get started!")

if "messages" not in st.session_state.keys():
    st.session_state["messages"] = [{"role":"assistant", "content" : "What's up today?"}]

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def generate_response(prompt_input, email, pwd):
    sign = Login(email,pwd)
    cookies = sign.login()
    chatbot = hugchat.ChatBot(cookies = cookies.get_dict())
    return chatbot.chat(prompt_input)

if prompt:=st.chat_input(disabled = not(user_email and user_pass)):
    st.session_state["messages"].append({"role":"user", "content" : prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state["messages"][-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("I'm thinking..."):
            bot_response = generate_response(prompt, user_email, user_pass)
            st.write(bot_response)
    message = {"role":"assistant", "content":bot_response}
    st.session_state["messages"].append(message)

