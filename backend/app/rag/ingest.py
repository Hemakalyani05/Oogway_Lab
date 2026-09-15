"""
Transcript ingestion pipeline for Lenny's Podcast knowledge base.
"""
import os
import glob
from typing import List, Dict, Any

from app.core.config import settings
from app.core.logging import logger
from app.rag.chunker import TranscriptChunker
from app.rag.hybrid_retriever import hybrid_retriever


def parse_transcript_metadata(content: str, filename: str) -> Dict[str, Any]:
    """Extracts title, guest, host, date, and URL from markdown header metadata."""
    title = os.path.splitext(filename)[0].replace("_", " ").title()
    guest = "Unknown Guest"
    date = "2024"
    url = "https://www.lennysnewsletter.com"

    lines = content.split("\n")
    for line in lines[:15]:
        if line.startswith("# Episode:"):
            title = line.replace("# Episode:", "").strip()
        elif line.startswith("**Guest:**"):
            guest = line.replace("**Guest:**", "").strip()
        elif line.startswith("**Date:**"):
            date = line.replace("**Date:**", "").strip()
        elif line.startswith("**URL:**"):
            url = line.replace("**URL:**", "").strip()

    return {
        "title": title,
        "guest": guest,
        "date": date,
        "url": url,
        "episode_id": os.path.splitext(filename)[0]
    }


def load_and_index_transcripts(data_dir: str = None) -> int:
    """
    Scans the data directory, parses all podcast transcript markdown files,
    chunks them with semantic preservation, and loads them into the Hybrid Retriever.
    """
    target_dir = data_dir or settings.TRANSCRIPTS_DATA_DIR
    if not os.path.exists(target_dir):
        logger.warning(f"Transcripts directory not found at: {target_dir}")
        return 0

    files = glob.glob(os.path.join(target_dir, "*.md"))
    chunker = TranscriptChunker(chunk_size_words=200, chunk_overlap_words=40)
    all_chunks: List[Dict[str, Any]] = []

    logger.info(f"Ingesting transcripts from {len(files)} files in {target_dir}...")

    for fpath in files:
        fname = os.path.basename(fpath)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        meta = parse_transcript_metadata(content, fname)
        chunks = chunker.chunk_transcript(
            episode_id=meta["episode_id"],
            episode_title=meta["title"],
            guest=meta["guest"],
            text=content
        )
        for chunk in chunks:
            chunk["episode_url"] = meta["url"]
            chunk["publication_date"] = meta["date"]
            all_chunks.append(chunk)

    # Index into hybrid retriever
    hybrid_retriever.load_documents(all_chunks)
    logger.info(f"Successfully indexed {len(all_chunks)} semantic chunks across {len(files)} episodes.")
    return len(all_chunks)


if __name__ == "__main__":
    count = load_and_index_transcripts()
    print(f"Ingestion complete: {count} chunks indexed.")
