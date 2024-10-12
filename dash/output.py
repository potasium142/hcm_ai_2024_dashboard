import streamlit as st
import dash.gadget as gd
import db
import query_result as qr
from db import VideoMetadata

ss = st.session_state


@st.dialog("YouTube popup", width="large")
def youtube_popup(url, start_time):
    st.video(url, start_time=start_time)


@st.dialog("Nearby frame", width="large")
def nearby_popup(
        f,
        metadata: VideoMetadata,
        set_name,
        vid_name,
        fps
):
    flist = qr.get_nearby(f, ss["fetch_nearby"], metadata.nearby_index)

    with st.container(border=True):
        f = flist[0]
        gd.display_img_nearby(f, fps, set_name, vid_name)

    cols = st.columns(2)
    for i, f in enumerate(flist[1:]):
        with cols[i % 2]:
            gd.display_img_nearby(f, fps, set_name, vid_name)


def show_result(results,
                container,
                metadata: db.VideoMetadata,
                columns=4):
    with container:
        # stinky hack for button key
        kidx = 0
        for group in results:
            div = st.expander(label=str(group[0]), expanded=True)

            cols = div.columns(columns)
            for ci, f in enumerate(group[1]):
                with cols[ci % columns]:

                    gd.display_image_full(
                        f,
                        metadata,
                        youtube_popup,
                        nearby_popup,
                        kidx
                    )

                kidx += 1
