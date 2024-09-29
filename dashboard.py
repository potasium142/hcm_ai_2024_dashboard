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


def create_answer_table():
    ss["answer_table"] = pd.DataFrame(
        columns=["Video", "Index"]
    )

    ss["answer_table_final"] = pd.DataFrame(
        columns=["Video", "Frames"]
    )


if "query_result" not in ss:
    ss["query_result"] = None
    ss["result"] = [[]]
    ss["page_num"] = 0


if "answer_table" not in ss:
    create_answer_table()

if "max_result" not in ss:
    ss["max_result"] = 100


keyframes_dir = "./keyframes"


@st.cache_resource
def init_longclip(show_spinner=True):
    model = longclip_model.LongCLIPModel(
        "./ckpt/longclip-L.pt", "cpu")

    db_longclip = db.DB(
        "./db/faiss_LongCLIP.bin",
        "./db/index_compact_2.npy"
    )
    return model, db_longclip


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
    #     st.button(
    #         "Reset table",
    #         on_click=create_answer_table
    #     )
    #     st.download_button(
    #         label="Download data as CSV",
    #         data=ss["answer_table_final"].to_csv(
    #             header=False,
    #             index=False
    #         ),
    #         mime="text/csv",
    #     )
    #     ss["answer_table_final"] = st.data_editor(
    #         ss["answer_table"],
    #         use_container_width=True,
    #         num_rows="dynamic"
    #     )


results_container = st.container()
# with results_container:
#     ss["result"][ss["page_num"]]

ss["page_num"] = max(0, ss["page_num"])

dash.output.show_result(
    ss["result"][ss["page_num"]],
    results_container,
    metadata,
    keyframes_dir,
    ss["display_columns"]
)
