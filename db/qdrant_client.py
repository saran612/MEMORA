from qdrant_client import QdrantClient
from qdrant_client.http import models
from config.settings import settings

class QdrantManager:
    def __init__(self):
        self.client = QdrantClient(path=str(settings.DB_PATH))
        self._init_collection()

    def _init_collection(self):
        # We need to know the embedding dimension. 
        # For all-MiniLM-L6-v2, it's 384.
        # We'll check if collection exists, if not create it.
        collections = self.client.get_collections().collections
        exists = any(c.name == settings.QDRANT_COLLECTION for c in collections)
        
        if not exists:
            self.client.create_collection(
                collection_name=settings.QDRANT_COLLECTION,
                vectors_config=models.VectorParams(
                    size=384,  # Change this if using a different model
                    distance=models.Distance.COSINE
                )
            )

    def upsert_chunks(self, chunks, embeddings, metadata):
        """
        chunks: List of text
        embeddings: List of embedding vectors
        metadata: List of dicts
        """
        points = [
            models.PointStruct(
                id=i + hash(chunks[i]) % 10**10, # Simple deterministic ID
                vector=embeddings[i],
                payload={**metadata[i], "content": chunks[i]}
            )
            for i in range(len(chunks))
        ]
        
        self.client.upsert(
            collection_name=settings.QDRANT_COLLECTION,
            points=points
        )

    def search(self, vector, top_k=settings.TOP_K):
        results = self.client.query_points(
            collection_name=settings.QDRANT_COLLECTION,
            query=vector,
            limit=top_k
        ).points
        return results

db_manager = QdrantManager()
