import clip
import googletrans
import db
import numpy as np
import prompt

import prompt
# c = clip.LongCLIPModel("./ckpt/longclip-L.pt", device="cpu")
# db_ = db.DB("./db/faiss_LongCLIP.bin", "./db/index_compact.npy")

# t = c.encode_text(
#     "A person is being interviewed. The wall behind them is decorated with many shark jaws")

# result = db_.query(t)

# v = db.VideoMetadata(
#     "./db/video_metadata.npy",
#     "./db/index_frame.pkl"
# )

# try:
#     print(v.frame_index[21][21][1228])
# except:
#     pass

# print(result.results)
# [28, 231, 22, 22, 18418], [26, 228, 22, 22, 18260]

text = "Một chiếc mồi câu đang thả xuống dưới nước. Miếng mồi này nhìn giống một con cá, màu bạc. Tiếp theo cảnh chuyển qua một người làm động tác nâng lên hạ xuống chiếc cần câu. Người này đang đội nón trắng. Video quay cảnh xung quanh thì cũng có nhiều người đang bắt cá. Có người bắt được một con cá và con cá này vùng vẫy khi bị câu lên."
t = googletrans.Translator()

print(t.translate(text))

# p = prompt.Prompt(text=text, translator=t)

# p.translate()

# print(p.text)
