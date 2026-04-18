import ollama
from db.qdrant_client import db_manager
from core.embedder import embedder
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self):
        self.client = ollama.Client(host=settings.OLLAMA_BASE_URL)

    def query(self, question: str):
        # 1. Embed question
        question_vector = embedder.get_embedding(question)

        # 2. Retrieve top-k
        results = db_manager.search(question_vector)
        
        if not results:
            return "Not found in memory"

        # 3. Build context
        context_parts = []
        for res in results:
            context_parts.append(f"Source: {res.payload.get('source')}\nContent: {res.payload.get('content')}")
        
        context = "\n---\n".join(context_parts)

        # 4. Prompt LLM
        prompt = self._build_prompt(context, question)
        
        response = self.client.generate(
            model=settings.OLLAMA_MODEL,
            prompt=prompt,
            options={"temperature": 0}
        )

        return response['response']

    def _build_prompt(self, context, question):
        return f"""You are Memora, a personal knowledge assistant.

Rules:
* Answer ONLY using the provided context
* If not found, say: "Not found in memory"
* Be concise and clear
* Do NOT hallucinate

Context:
{context}

Question:
{question}
"""

rag_pipeline = RAGPipeline()
