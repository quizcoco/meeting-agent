
from typing import List

class Embedder:

    # 생성자
    def __init__(self, model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(model_name)


    # 임베딩
    def embed(self, documents: List[str]):
        
        result = self.model.encode(documents, normalize_embeddings=True)

        return result

    


