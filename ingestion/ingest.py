from pathlib import Path
from ingestion.converter import converter
from ingestion.indexer import indexer
from core.chunker import chunker
from core.embedder import embedder
from db.qdrant_client import db_manager
from config.settings import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ingest_file(file_path: Path):
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return

    # 1. Check if already indexed
    if indexer.is_already_indexed(file_path):
        logger.info(f"File already indexed: {file_path.name}")
        return

    # 2. Convert to MD
    logger.info(f"Converting {file_path.name} to Markdown...")
    processed_path = converter.to_markdown(file_path)

    # 3. Read content
    with open(processed_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 4. Chunk
    logger.info(f"Chunking {file_path.name}...")
    chunks = chunker.split_text(content)
    if not chunks:
        logger.warning(f"No content found in {file_path.name}")
        return

    # 5. Embed
    logger.info(f"Generating embeddings for {len(chunks)} chunks...")
    embeddings = embedder.get_embeddings(chunks)

    # 6. Store in Qdrant
    logger.info(f"Storing in Vector DB...")
    metadata = [
        {"source": str(file_path.name), "path": str(processed_path)}
        for _ in chunks
    ]
    db_manager.upsert_chunks(chunks, embeddings, metadata)

    # 7. Index metadata
    indexer.index_file(file_path, processed_path)
    logger.info(f"Successfully ingested {file_path.name}")

def ingest_directory(dir_path: Path):
    supported = [".pdf", ".txt", ".md"]
    for file_path in dir_path.iterdir():
        if file_path.suffix.lower() in supported:
            ingest_file(file_path)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Ingest files into Memora")
    parser.add_argument("path", type=str, help="Path to file or directory")
    args = parser.parse_args()
    
    path = Path(args.path)
    if path.is_dir():
        ingest_directory(path)
    else:
        ingest_file(path)
