"""
Semantic transcript chunker with speaker diarization and timestamp preservation.
"""
from typing import List, Dict, Any
import re
import uuid


class TranscriptChunker:
    """Chunks transcript text into overlapping semantic passages."""
    
    def __init__(self, chunk_size_words: int = 250, chunk_overlap_words: int = 50):
        self.chunk_size_words = chunk_size_words
        self.chunk_overlap_words = chunk_overlap_words

    def chunk_transcript(self, episode_id: str, episode_title: str, guest: str, text: str) -> List[Dict[str, Any]]:
        """
        Splits raw markdown/text transcript into structured semantic chunks,
        preserving speaker attribution and timestamp annotations where available.
        """
        # Split by timestamp patterns or double newlines
        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk_words = []
        current_speaker = guest
        current_timestamp = "00:00"
        chunk_idx = 0

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # Check for speaker / timestamp pattern like "[00:14:20] Brian Chesky:" or "**Elena Verna (12:30):**"
            speaker_match = re.search(r'\[?(\d{1,2}:\d{2}(?::\d{2})?)\]?\s*(?:\*\*)?([A-Za-z\s]+)(?:\*\*)?:?', para)
            if speaker_match:
                current_timestamp = speaker_match.group(1)
                current_speaker = speaker_match.group(2).strip()

            words = para.split()
            current_chunk_words.extend(words)

            if len(current_chunk_words) >= self.chunk_size_words:
                chunk_text = " ".join(current_chunk_words)
                chunks.append({
                    "id": str(uuid.uuid4()),
                    "episode_id": episode_id,
                    "episode_title": episode_title,
                    "guest": current_speaker,
                    "chunk_index": chunk_idx,
                    "timestamp": current_timestamp,
                    "content": chunk_text,
                    "word_count": len(current_chunk_words)
                })
                chunk_idx += 1
                # Slide with overlap
                current_chunk_words = current_chunk_words[len(current_chunk_words) - self.chunk_overlap_words:]

        # Remaining words
        if current_chunk_words:
            chunk_text = " ".join(current_chunk_words)
            chunks.append({
                "id": str(uuid.uuid4()),
                "episode_id": episode_id,
                "episode_title": episode_title,
                "guest": current_speaker,
                "chunk_index": chunk_idx,
                "timestamp": current_timestamp,
                "content": chunk_text,
                "word_count": len(current_chunk_words)
            })

        return chunks
