"""
Tests for Ship 30 for 30 Content Generation Skill.
"""
import unittest
from app.skills.ship30 import build_ship30_prompt, SHIP30_SYSTEM_PROMPT
from app.skills.artifact_builder import ArtifactBuilder


class TestShip30Skill(unittest.TestCase):
    def test_ship30_prompt_generation(self):
        mock_chunks = [{
            "episode_title": "Founder Mode & Airbnb",
            "guest": "Brian Chesky",
            "content": "We merged PM and PMM into a single product marketing manager role."
        }]
        prompt = build_ship30_prompt("Modern PM Role", mock_chunks)
        self.assertIn("Ship 30 for 30", prompt)
        self.assertIn("Brian Chesky", prompt)
        self.assertIn("1,250-word", prompt)
        self.assertIn("<artifact", prompt)

    def test_ship30_artifact_extraction(self):
        sample_llm_output = (
            "Here is the essay:\n\n"
            "<artifact title=\"Ship 30 Essay: Founder Mode\" type=\"markdown\" language=\"markdown\">\n"
            "# Why Founder Mode Is Replacing Manager Mode\n\n"
            "Most tech companies are broken.\n\n"
            "### 1. Single Roadmap\n"
            "Airbnb operates on one roadmap.\n"
            "</artifact>"
        )
        artifact = ArtifactBuilder.extract_artifact(sample_llm_output)
        self.assertIsNotNone(artifact)
        self.assertEqual(artifact["title"], "Ship 30 Essay: Founder Mode")
        self.assertEqual(artifact["artifact_type"], "markdown")
        self.assertIn("Why Founder Mode Is Replacing Manager Mode", artifact["content"])
        self.assertTrue(artifact["is_valid"])


if __name__ == "__main__":
    unittest.main()
