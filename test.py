import clip
import googletrans
import db
import numpy as np

import prompt
# c = clip.CLIPModel("./ckpt/longclip-L.pt", device="cpu")
# db_ = db.DB("./db/faiss_LongCLIP.bin", "./db/index_compact.npy")

# t = c.encode_text(
#     "A person is being interviewed. The wall behind them is decorated with many shark jaws")

# result = db_.query(t)

# print(result.group_output())

v = db.VideoMetadata("./db/video_metadata.npy")

print(v.metadata)
