import faiss
import numpy as np
import pickle


class DB():
    def __init__(self,
                 faiss_db_path: str,
                 frame_index_path: str) -> None:
        self.faiss_db = faiss.read_index(faiss_db_path)
        self.frame_index = np.load(frame_index_path)

    def __map_result(self,
                     x):
        return x[0], self.frame_index[x[1]]

    def query(self,
              query: np.ndarray,
              k: int = 100):
        conf, indices = self.faiss_db.search(query, k)

        conf = (conf*100).astype(int)

        results = np.stack((conf, indices), axis=2)
        return Result(
            [list(
                map(
                    self.__map_result,
                    result
                )
            ) for result in results]
        )


class VideoMetadata():
    def __init__(self,
                 metadata_path: str,
                 frame_index_path: str) -> None:
        self.metadata = self.__open_metadata(metadata_path)
        self.frame_index = self.__load_frame_index(frame_index_path)

    def __load_frame_index(self,
                           frame_index_path: str) -> list:
        with open(frame_index_path, "rb") as f:
            return pickle.load(f)

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
        self.results = self.__decode_list(results)

    def __decode(self,
                 entry):
        conf = entry[0]
        index_compact = entry[1]
        index, frame = divmod(index_compact, 1000000)
        index, video = divmod(index, 1000)
        index, folder = divmod(index, 100)

        return [conf, index, folder, video, frame]

    def __decode_list(self,
                      results):
        return np.concatenate([list(
            map(
                self.__decode,
                indice
            )
        ) for indice in results])
