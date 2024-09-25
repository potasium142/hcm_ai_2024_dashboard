import streamlit as st


def gadget(ss):
    ss["group_input"] = st.selectbox(
        "Group method",
        (None, "Video", "Confident")
    )
    ss["fetch_nearby"] = st.slider(
        "Fetch nearby frame",
        min_value=0,
        max_value=10
    )

    ss["display_columns"] = st.slider(
        "Display columns",
        value=3,
        min_value=1,
        max_value=8
    )
