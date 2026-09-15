"""
Artifact parser and builder skill for native side-by-side rendering.
"""

import re
from typing import Optional, Dict, Any

from app.core.security import sanitize_html, validate_artifact_content


class ArtifactBuilder:
    """
    Detects, extracts, and validates <artifact> tags from LLM responses.
    """

    ARTIFACT_REGEX = re.compile(
        r'<artifact\s+'
        r'title=["\'](?P<title>[^"\']+)["\']\s+'
        r'type=["\'](?P<type>[^"\']+)["\']'
        r'(?:\s+language=["\'](?P<lang>[^"\']+)["\'])?'
        r'\s*>'
        r'(?P<content>.*?)'
        r'</artifact>',
        re.DOTALL | re.IGNORECASE
    )

    @classmethod
    def extract_artifact(
        cls,
        text: str
    ) -> Optional[Dict[str, Any]]:
        """
        Extract the first <artifact>...</artifact> block.
        """

        match = cls.ARTIFACT_REGEX.search(text)

        if not match:
            return None

        title = match.group("title").strip()

        artifact_type = match.group("type").strip().lower()

        language = match.group("lang")

        if not language:
            language = (
                "html"
                if artifact_type == "html"
                else "markdown"
            )

        content = match.group("content").strip()

        # Sanitize generated HTML before rendering.
        if artifact_type == "html":
            content = sanitize_html(content)

        is_valid, reason = validate_artifact_content(
            content,
            artifact_type
        )

        return {
            "title": title,
            "artifact_type": artifact_type,
            "language": language,
            "content": content,
            "is_valid": is_valid,
            "validation_message": reason
        }

    @classmethod
    def strip_artifact_tags(cls, text: str) -> str:
        """
        Remove the raw <artifact>...</artifact> block
        from the normal chat response.
        """

        return cls.ARTIFACT_REGEX.sub("", text).strip()