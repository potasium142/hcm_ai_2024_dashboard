import streamlit as st
import requests
import json

ss = st.session_state
if "messages" not in ss:
    ss["messages"] = []

MSG_TEMPLATE = {
    "model": "llama2",
    "messages": [{
        "role": "user",
        "content": ""
    }],
    "stream": False
}


def update_endpoint(endpoint: str):
    ss["llm_endpoint"] = endpoint


def sent_chat(msg):
    msg_dict = MSG_TEMPLATE.copy()
    msg_dict["messages"][0]["content"] = msg

    r = requests.post(
        "http://0.0.0.0:11434/api/chat",
        json=msg_dict,
        stream=False
    )
    return r.json()["message"]


def llm_chat(container):
    with container:
        with st.expander(
                label="LLM Endpoint",
        ):
            llm_endpoint_u = st.text_input(
                label="URL",
                value=ss["llm_endpoint"]
            )
            st.button(
                label="Update endpoint",
                on_click=lambda x: update_endpoint(x),
                args=(llm_endpoint_u,)
            )

        messages_container = st.container(height=300)

        prompt = st.chat_input()

        if prompt:
            ss["messages"].append({"role": "user", "content": prompt})

            chat_output = sent_chat(prompt)
            ss["messages"].append(chat_output)

        for msg in ss["messages"]:
            messages_container.chat_message(msg["role"]).write(msg["content"])
