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
        return self.frame_index[x]

    def query(self,
              query: np.ndarray,
              k: int = 100):
        conf, indices = self.faiss_db.search(query, k)

        frames_data = np.array(list(
            map(
                self.__map_result,
                indices.flatten()
            )
        ))

        frames_data[:, 0] = (conf.flatten() * 100).astype(int)

        return frames_data


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
