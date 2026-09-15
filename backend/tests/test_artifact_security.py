"""
Tests for Artifact HTML Sanitization and Security Validation.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.security import sanitize_html, validate_artifact_content
from app.skills.artifact_builder import ArtifactBuilder


class TestArtifactSecurity(unittest.TestCase):
    def test_sanitize_html_removes_dangerous_links(self):
        malicious_html = '<a href="javascript:alert(\'hack\')">Click Me</a>'
        sanitized = sanitize_html(malicious_html)
        self.assertNotIn('javascript:', sanitized)
        self.assertIn('href="#"', sanitized)

    def test_sanitize_html_removes_cookie_stealing_attempts(self):
        malicious_js = '<script>var c = document.cookie; window.parent.postMessage(c);</script>'
        sanitized = sanitize_html(malicious_js)
        self.assertNotIn('document.cookie', sanitized)
        self.assertNotIn('window.parent', sanitized)

    def test_validate_artifact_content(self):
        valid_html = '<div class="p-4 bg-slate-900"><button>Test</button></div>'
        is_valid, _ = validate_artifact_content(valid_html, "html")
        self.assertTrue(is_valid)

        empty_content = ""
        is_valid_empty, _ = validate_artifact_content(empty_content, "markdown")
        self.assertFalse(is_valid_empty)


if __name__ == "__main__":
    unittest.main()
