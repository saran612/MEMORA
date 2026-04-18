from config.settings import settings
import re

class Chunker:
    def __init__(self, chunk_size=settings.CHUNK_SIZE, overlap=settings.CHUNK_OVERLAP):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split_text(self, text):
        """
        Splits text into chunks of approx chunk_size words with overlap.
        """
        words = text.split()
        chunks = []
        
        if not words:
            return chunks

        for i in range(0, len(words), self.chunk_size - self.overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = " ".join(chunk_words)
            chunks.append(chunk_text)
            
            if i + self.chunk_size >= len(words):
                break
                
        return chunks

chunker = Chunker()
