import PIL.Image
import streamlit as st
import PIL


def display_image(
        f,
        video_id,
        path,
        time,
        url,
        popup_callback,
):
    container = st.container(border=True)
    with container:
        m, s = divmod(time, 60)
        st.image(
            image=path,
            use_column_width=True
        )
        st.link_button(
            label=f"Conf {f[0]}% Time {m}:{s:02d}",
            use_container_width=True,
            url=url
        )
        st.code(
            f"{video_id}, {f[4]}",
            language="markdown"
        )
        # dialog window brokie rn
        # st.button(
        #     label="Watch",
        #     use_container_width=True,
        #     on_click=popup_callback,
        #     args=(url,), key=url
        # )
    return container
