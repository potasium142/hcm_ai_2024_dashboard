import streamlit as st
import clip
import dash.sidebar.output
import dash.sidebar.query
import dash.output
import db
import googletrans
import dash
import query_result as qr
import metaclip
import numpy as np

st.set_page_config(
    page_title="Video search dashboard",
    page_icon="🐍",
    layout="wide")


ss = st.session_state

if "query_result" not in ss:
    ss["query_result"] = None

if "answer_table" not in ss:
    ss["answer_table"] = set()

if "max_result" not in ss:
    ss["max_result"] = 100


keyframes_dir = "./keyframes"


@st.cache_resource
def init_longclip(show_spinner=True):
    longclip_model = clip.LongCLIPModel("./ckpt/longclip-L.pt", "cpu")

    db_longclip = db.DB(
        "./db/faiss_LongCLIP.bin",
        "./db/index_compact.npy"
    )
    return longclip_model, db_longclip


@st.cache_resource
def init_metaclip(show_spinner=True):
    metaclip_model = metaclip.MetaCLIP("cpu")
    db_metaclip = db.DB(
        "./db/faiss_MetaCLIP.bin",
        "./db/index_compact.npy"
    )
    return metaclip_model, db_metaclip


@st.cache_resource
def init_miscelleneous(show_spinner=True):

    translator = googletrans.Translator()
    video_metadata = db.VideoMetadata(
        "./db/video_metadata.npy",
        "./db/index_frame.pkl"
    )

    return translator, video_metadata


translator, metadata = init_miscelleneous()
longclip_model, db_longclip = init_longclip()
metaclip_model, db_metaclip = init_metaclip()


def search():
    texts = ss["search_query"]
    results = []
    if ss["query_longclip"]:
        longclip_token = longclip_model.encode_text(texts)
        results.append(
            db_longclip.query(
                longclip_token,
                ss["max_result"]
            ).results
        )

    if ss["query_metaclip"]:
        metaclip_token = metaclip_model.encode_text(texts)
        results.append(
            db_metaclip.query(
                metaclip_token,
                ss["max_result"]
            ).results
        )

    ss["query_result"] = np.concatenate(results)


with st.sidebar:
    tabs = st.tabs(["Query", "Output"])
    with tabs[0]:
        dash.sidebar.query.gadget(ss, translator, search)
    with tabs[1]:
        dash.sidebar.output.gadget(ss)

results_container = st.container()

if ss["query_result"] is not None:
    with results_container:
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

        dash.output.show_result(
            result,
            metadata,
            keyframes_dir,
            ss["display_columns"]
        )
