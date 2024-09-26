import streamlit as st
import dash.gadget as gd
import db

ss = st.session_state


@st.dialog("YouTube popup", width="large")
def youtube_popup(url, start_time):
    st.video(url, start_time=start_time)


def show_result(results,
                container,
                metadata: db.VideoMetadata,
                keyframes_dir: str,
                columns=4):
    with container:
        # stinky hack for button key
        kidx = 0

        youtube_url = f"https://youtu.be"
        for group in results:
            div = st.expander(label=str(group[0]), expanded=True)

            cols = div.columns(columns)
            for ci, f in enumerate(group[1]):
                with cols[ci % columns]:
                    vid_name = f"L{f[2]:02d}_V{f[3]:03d}"
                    set_name = f"Videos_L{f[2]:02d}_a"

                    fps, youtube_id = metadata.get_by_name(vid_name)

                    time = int(f[4]/fps)
                    url = f"{youtube_url}/{youtube_id}"

                    path = f"{keyframes_dir}/{set_name}/{vid_name}/{f[4]:06d}.jpg"
                    gd.display_image(
                        f,
                        vid_name,
                        path,
                        time,
                        url,
                        youtube_popup,
                        kidx
                    )

                kidx += 1
