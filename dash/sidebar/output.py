import streamlit as st
import query_result as qr


def update(ss, metadata):
    result = ss["query_result"]

    if ss["fetch_nearby"] != 0:
        result = qr.get_nearby(
            result,
            ss["fetch_nearby"],
            metadata.frame_index
        )

    match ss["group_input"]:
        case None:
            result = [["", result]]
        case "Confident":
            result = qr.group_by_conf(result)
        case "Video":
            result = qr.group_by_video(result)

    ss["result"] = result


@st.fragment
def gadget(ss, metadata):
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
    if st.button(
        label="Update",
        use_container_width=True,
        on_click=update,
        args=(ss, metadata)
    ):
        st.rerun()
