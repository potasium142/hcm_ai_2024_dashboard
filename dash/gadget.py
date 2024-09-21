import PIL.Image
import streamlit as st
import PIL


def display_image(
        path,
        id,
        time,
        url
):
    container = st.container(border=True)
    image = PIL.Image.open(path)
    with container:
        m, s = divmod(time, 60)
        st.image(
            image=image,
            use_column_width=True
        )
        st.write(f"ID:{id} - Time : {m:d}:{s:d}")
        st.link_button(
            label="Watch",
            url=f"{url}",
            use_container_width=True
        )
    return container
