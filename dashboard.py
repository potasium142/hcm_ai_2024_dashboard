import streamlit as st
import clip
import db
import numpy as np
import googletrans
from dash import gadget as gd

from prompt import Prompt

st.set_page_config(
    page_title="Video search dashboard",
    page_icon="🐍",
    layout="wide")


ss = st.session_state

if "query_result" not in ss:
    ss["query_result"] = dict()

keyframes_dir = "./keyframes"


@st.cache_resource
def init(show_spinner=True):
    model = clip.CLIPModel("./ckpt/longclip-L.pt", "cpu")
    database = db.DB(
        "./db/faiss_LongCLIP_merge.bin",
        "./db/index_compact_merge.npy"
    )
    translator = googletrans.Translator()
    video_metadata = db.VideoMetadata("./db/video_metadata.npy")
    return model, database, translator, video_metadata


model, database, translator, metadata = init()


def search():
    texts = ss["search_query"]
    clip_token = model.encode_text(texts)
    result = database.query(clip_token)
    ss["query_result"] = result.group_output()


ss["output_dict"] = dict()

with st.sidebar:
    prompt_input = st.text_area("prompt", value="")

    ss["prompt"] = Prompt(text=prompt_input, translator=translator)

    translate_text = st.toggle("Translate")
    if translate_text:
        try:
            ss["prompt"].translate()
        except:
            pass

    with st.container(border=True):
        st.write(ss["prompt"].text)

    ss["token_sentence"] = ss["prompt"].tokenize()

    ss["token_sentence"].append(ss["prompt"].text)

    ss["search_query"] = st.multiselect(
        label="Tokenize sentence",
        options=ss["token_sentence"]
    )

    st.button(
        label="search",
        on_click=search,
        use_container_width=True
    )


results_container = st.container()


with results_container:
    for vid in ss["query_result"]:

        bi, vi = divmod(vid[0], 1000)

        batch_id = f"Videos_L{bi:02d}_a"
        vid_id = f"L{bi:02d}_V{vi:03d}"

        f_set = sorted(vid[1])
        with st.expander(
            label=f"ID : {vid_id}, amount : {len(vid[1])}",
            expanded=True
        ):

            cols = st.columns(4)

            m = metadata.get_by_name(vid_id)

            url = f"https://youtu.be/{m[1]}"
            for i, f in enumerate(f_set):
                time = int(f/m[0])
                with cols[i % 4]:
                    gd.display_image(
                        f"./keyframes/{batch_id}/{vid_id}/{f:06d}.jpg",
                        f,
                        time,
                        f"{url}&t={time}"
                    )
