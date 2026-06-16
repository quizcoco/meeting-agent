import faiss
import numpy as np
import os
import json

from src.services.s3_service import upload_vector_store


class VectorStore:

    def __init__(
        self,
        dimension=384,
        path="vector_store"
    ):

        self.path = path

        if os.path.exists(
            f"{path}/index.faiss"
        ):
            self._load()
        else:
            self.index = faiss.IndexFlatL2(
                dimension
            )

            self.documents = []
            self.metadatas = []
            self.ids = []

    def save_local(self):

        os.makedirs(
            self.path,
            exist_ok=True
        )

        faiss.write_index(
            self.index,
            f"{self.path}/index.faiss"
        )

        with open(
            f"{self.path}/metadatas.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.metadatas,
                f,
                ensure_ascii=False
            )

        with open(
            f"{self.path}/ids.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.ids,
                f,
                ensure_ascii=False
            )

        with open(
            f"{self.path}/documents.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.documents,
                f,
                ensure_ascii=False
            )

    def add_documents(
        self,
        vectors,
        docs,
        doc_ids,
        metadatas
    ):

        vectors = np.array(
            vectors
        ).astype("float32")

        self.index.add(vectors)

        self.documents.extend(docs)
        self.ids.extend(doc_ids)
        self.metadatas.extend(
            metadatas
        )

        self.save_local() # 로컬에 저장
        upload_vector_store() #s3에 저장


    def search_vector(self, query_vector, k):

        query_vector = np.array(query_vector).astype('float32')
        distances, indices = self.index.search(query_vector, k) # 거리값과 인덱스 번호

        results = []

        for idx, dist in zip(indices[0], distances[0]): # 두 개 리스트를 짝지어서 묶어주는 함수
            if idx == -1: # 결과 없으면
                continue

            results.append({
                "document": self.documents[idx],
                "id": self.ids[idx],
                "metadata": self.metadatas[idx],
                "distance": dist # L2는 작을수록 유사함
            })

        return results

    def _load(self):

        self.index = faiss.read_index(
            f"{self.path}/index.faiss"
        )

        with open(
            f"{self.path}/documents.json",
            "r",
            encoding="utf-8"
        ) as f:

            self.documents = json.load(f)

        with open(
            f"{self.path}/ids.json",
            "r",
            encoding="utf-8"
        ) as f:

            self.ids = json.load(f)

        with open(
            f"{self.path}/metadatas.json",
            "r",
            encoding="utf-8"
        ) as f:

            self.metadatas = json.load(f)

        return self