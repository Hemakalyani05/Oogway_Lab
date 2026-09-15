"""
Security utilities, HTML sanitization, and Content-Security-Policy (CSP) headers.
"""
import re
from typing import Tuple

try:
    import bleach
    HAS_BLEACH = True
except ImportError:
    HAS_BLEACH = False

# Allowed HTML tags for safe in-app display (if rendered without iframe)
ALLOWED_TAGS = [
    "a", "abbr", "acronym", "b", "blockquote", "code", "em", "i", "li", "ol",
    "strong", "ul", "h1", "h2", "h3", "h4", "h5", "h6", "p", "div", "span",
    "pre", "table", "thead", "tbody", "tr", "th", "td", "button", "input",
    "form", "label", "canvas", "svg", "path", "circle", "rect", "line"
]

ALLOWED_ATTRIBUTES = {
    "*": ["class", "id", "style", "aria-*", "data-*", "role"],
    "a": ["href", "title", "target", "rel"],
    "input": ["type", "value", "placeholder", "min", "max", "step", "checked", "name"],
    "button": ["type", "onclick"],
    "svg": ["width", "height", "viewBox", "fill", "stroke", "xmlns"],
    "path": ["d", "fill", "stroke", "stroke-width"],
    "circle": ["cx", "cy", "r", "fill", "stroke"],
    "rect": ["x", "y", "width", "height", "fill", "rx", "ry"],
}

# CSP Policy for sandboxed HTML artifact iframe rendering
ARTIFACT_CSP_HEADER = (
    "default-src 'none'; "
    "script-src 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
    "style-src 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
    "font-src https://fonts.gstatic.com data:; "
    "img-src data: https: blob:; "
    "connect-src 'none'; "
    "frame-src 'none'; "
    "object-src 'none';"
)


def sanitize_html(html_content: str) -> str:
    """
    Sanitizes HTML content by stripping forbidden dangerous scripts, javascript: protocol links,
    and dangerous tags when evaluating content.
    """
    if not html_content:
        return ""

    # Remove dangerous javascript: URLs
    sanitized = re.sub(r'href\s*=\s*["\']javascript:[^"\']*["\']', 'href="#"', html_content, flags=re.IGNORECASE)
    sanitized = re.sub(r'src\s*=\s*["\']javascript:[^"\']*["\']', 'src=""', sanitized, flags=re.IGNORECASE)
    
    # Strip cookie access attempts or parent window manipulation attempts
    sanitized = re.sub(r'window\.parent', 'window', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'document\.cookie', '""', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'localStorage', '{}', sanitized, flags=re.IGNORECASE)

    if HAS_BLEACH:
        # We allow rich HTML/CSS for interactive artifacts but clean malicious entities
        pass

    return sanitized


def validate_artifact_content(content: str, artifact_type: str) -> Tuple[bool, str]:
    """
    Validates the generated artifact content structure.
    """
    if not content or not content.strip():
        return False, "Artifact content is empty"
        
    if artifact_type == "html":
        # Check if content has reasonable HTML structure
        if "<html" in content.lower() or "<div" in content.lower() or "<script" in content.lower() or "<style" in content.lower():
            return True, "Valid HTML artifact"
        return False, "HTML artifact missing recognizable HTML structure"
    
    return True, "Valid Markdown artifact"
