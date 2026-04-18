from sentence_transformers import SentenceTransformer
from config.settings import settings

class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)

    def get_embeddings(self, texts):
        """
        texts: List of strings
        returns: List of vectors
        """
        if isinstance(texts, str):
            texts = [texts]
        embeddings = self.model.encode(texts)
        return embeddings.tolist()

    def get_embedding(self, text):
        return self.get_embeddings(text)[0]

embedder = Embedder()
