import streamlit as st


ss = st.session_state


def change_page(change):
    c = ss["page_num"] + change
    if c >= 0 and c < len(ss["result"]):
        ss["page_num"] = c


def paging():

    ss["page_num"] = st.slider(
        label="Page",
        value=ss["page_num"],
        min_value=0,
        max_value=len(ss["result"]) - 1
    )

    cols = st.columns(2)

    cols[0].button(
        label="<<",
        on_click=change_page,
        args=(-1,),
        use_container_width=True)
    cols[1].button(
        label="\>\>",
        on_click=change_page,
        args=(1,),
        use_container_width=True)
