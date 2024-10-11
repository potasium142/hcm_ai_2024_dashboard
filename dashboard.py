import streamlit as st
import dash.sidebar.paging
import longclip_model
import dash.sidebar.output
import dash.sidebar.query
import dash.output
import db
import googletrans
import dash
import query_result as qr
import openclip_model
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="Video search dashboard",
    page_icon="🐍",
    layout="wide")


ss = st.session_state


if "query_result" not in ss:
    ss["query_result"] = None
    ss["result"] = [[]]
    ss["page_num"] = 0


if "max_result" not in ss:
    ss["max_result"] = 100

if "kf_dir" not in ss:
    ss["kf_dir"] = "./keyframes"


@st.cache_resource
def init_longclip(show_spinner=True):
    model = longclip_model.LongCLIPModel(
        "./ckpt/longclip-L.pt", "cpu")

    db_longclip = db.DB(
        "./db/faiss_LongCLIP.bin",
    )
    return model, db_longclip


@st.cache_resource
def init_metaclip(show_spinner=True):
    model = openclip_model.OpenCLIP(
        "ViT-L-14-quickgelu",
        "metaclip_fullcc"
    )
    db_metaclip = db.DB(
        "./db/faiss_MetaCLIP.bin",
    )
    return model, db_metaclip


@st.cache_resource
def init_openclip(show_spinner=True):
    model = openclip_model.OpenCLIP(
        "ViT-H-14-quickgelu",
        "dfn5b"
    )
    db_metaclip = db.DB(
        "./db/faiss_openCLIP.bin",
    )
    return model, db_metaclip


@st.cache_resource
def init_miscelleneous(show_spinner=True):

    translator = googletrans.Translator()
    video_metadata = db.VideoMetadata(
        "./db/video_metadata.npy",
        "./db/index_frame.pkl",
        "./db/index_compact_2.npy"
    )

    return translator, video_metadata


translator, metadata = init_miscelleneous()

longclip_model, db_longclip = init_longclip()

metaclip_model, db_metaclip = init_metaclip()

openclip_model, db_openclip = init_openclip()


def search():
    texts = ss["search_query"]
    results = []
    if ss["query_longclip"]:
        longclip_token = longclip_model.encode_text(texts)
        results.append(
            db_longclip.query(
                longclip_token,
                ss["max_result"]
            )
        )

    if ss["query_metaclip"]:
        metaclip_token = metaclip_model.encode_text(texts)
        results.append(
            db_metaclip.query(
                metaclip_token,
                ss["max_result"]
            )
        )

    if ss["query_openclip"]:
        openclip_token = openclip_model.encode_text(texts)
        results.append(
            db_openclip.query(
                openclip_token,
                ss["max_result"]
            )
        )

    ss["query_result"] = np.concatenate(results)
    dash.sidebar.output.update(ss, metadata)


with st.sidebar:
    if len(ss["result"]) > 1:
        dash.sidebar.paging.paging()
    else:
        ss["page_num"] = 0

    tabs = st.tabs(["Query", "Output", "Table"])
    with tabs[0]:
        dash.sidebar.query.gadget(ss, translator, search)
    with tabs[1]:
        dash.sidebar.output.gadget(ss, metadata)
    with tabs[2]:
        st.write("vo dc vong sau r lam")


results_container = st.container()

ss["page_num"] = max(0, ss["page_num"])

dash.output.show_result(
    ss["result"][ss["page_num"]],
    results_container,
    metadata,
    ss["display_columns"]
)
