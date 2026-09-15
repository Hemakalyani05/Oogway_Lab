"""
Artifact parser and builder skill for native side-by-side rendering.
"""
import re
from typing import Optional, Dict, Any, Tuple
from app.core.security import sanitize_html, validate_artifact_content


class ArtifactBuilder:
    """
    Detects, extracts, and validates <artifact> tags from LLM stream responses.
    """
    ARTIFACT_REGEX = re.compile(
        r'<artifact\s+title=["\'](?P<title>[^"\']+)["\']\s+type=["\'](?P<type>[^"\']+)["\'](?:\s+language=["\'](?P<lang>[^"\']+)["\'])?\s*>(?P<content>.*?)(?:</artifact>|$)',
        re.DOTALL | re.IGNORECASE
    )

    @classmethod
    def extract_artifact(cls, text: str) -> Optional[Dict[str, Any]]:
        match = cls.ARTIFACT_REGEX.search(text)
        if not match:
            return None

        title = match.group("title").strip()
        art_type = match.group("type").strip().lower()
        lang = match.group("lang") or ("html" if art_type == "html" else "markdown")
        content = match.group("content").strip()

        # Security Sanitization for HTML
        if art_type == "html":
            content = sanitize_html(content)

        is_valid, reason = validate_artifact_content(content, art_type)

        return {
            "title": title,
            "artifact_type": art_type,
            "language": lang,
            "content": content,
            "is_valid": is_valid,
            "validation_message": reason
        }

    @classmethod
    def strip_artifact_tags(cls, text: str) -> str:
        """Strips the raw <artifact> markup from the main chat message content for clean reading."""
        return cls.ARTIFACT_REGEX.sub("", text).strip()
