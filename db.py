import faiss
import numpy as np
import pickle


class DB():
    def __init__(self,
                 faiss_db_path: str,
                 frame_index_path: str) -> None:
        self.faiss_db = faiss.read_index(faiss_db_path)
        self.frame_index = np.load(frame_index_path)

    def query(self,
              query: np.ndarray,
              k: int = 100):
        _, indices = self.faiss_db.search(query, k)

        return Result(
            list(
                map(
                    lambda x: self.frame_index[x],
                    indices
                )
            )
        )


class VideoMetadata():
    def __init__(self,
                 metadata_path: str) -> None:
        self.metadata = self.__open_metadata(metadata_path)

    def __open_metadata(self,
                        path) -> dict:
        return np.load(
            path,
            allow_pickle=True
        ).item()

    def get_by_index(self,
                     batch: int,
                     vid: int) -> list:
        i = f"L{batch:02d}_V{vid:03d}"
        return self.metadata.get(i)

    def get_by_name(self,
                    i: str) -> list:
        return self.metadata.get(i)


class Result():
    def __init__(self,
                 results: list):
        self.results = results

    def __decode(self,
                 index_compact):
        index, frame = divmod(index_compact, 1000000)
        index, video = divmod(index, 1000)
        index, folder = divmod(index, 100)

        return [index, folder, video, frame]

    def __decode_path(self,
                      index_compact):
        d = self.__decode(index_compact)

        return [
            d[0],
            f"Videos_L{d[1]:02d}_a/L{d[1]:02d}_V{d[2]:03d}/{d[3]:06d}.jpg"
        ]

    def decode(self) -> list:
        return [list(
            map(
                self.__decode,
                indice
            )
        ) for indice in self.results]

    def get_path_list(self) -> list:
        return [list(
            map(
                self.__decode_path,
                indice
            )
        ) for indice in self.results]

    # SHIT FUCKING STINK -- TODO: burn this
    def group_output(self):
        gr = dict()

        for r in self.results:
            for f in r:
                d = self.__decode(f)

                index = d[1].item() * 1000 + d[2].item()

                vid_bin = gr.get(index, set())

                vid_bin.add(d[3].item())

                gr[index] = vid_bin

        return sorted(
            gr.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
