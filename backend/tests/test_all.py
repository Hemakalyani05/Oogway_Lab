"""
Comprehensive Backend Test Suite using standard library unittest and FastAPI TestClient.
"""
import unittest
import json
import sys
import os

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from starlette.testclient import TestClient

from app.main import app
from app.db.session import engine, Base
from app.rag.ingest import load_and_index_transcripts
from app.rag.hybrid_retriever import hybrid_retriever
from app.skills.grounding_guard import GroundingGuard
from app.skills.ship30 import build_ship30_prompt
from app.skills.artifact_builder import ArtifactBuilder
from app.core.security import sanitize_html, validate_artifact_content


class TestLennyGrowthAssistant(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create tables
        Base.metadata.create_all(bind=engine)
        # Index knowledge base
        load_and_index_transcripts()
        cls.client = TestClient(app)

    def test_01_health_and_readiness(self):
        res_health = self.client.get("/healthz")
        self.assertEqual(res_health.status_code, 200)
        self.assertEqual(res_health.json()["status"], "healthy")

        res_ready = self.client.get("/readyz")
        self.assertEqual(res_ready.status_code, 200)
        data = res_ready.json()
        self.assertGreater(data["checks"]["knowledge_base_chunks"], 0)

    def test_02_model_status_endpoint(self):
        res = self.client.get("/api/v1/models")
        self.assertEqual(res.status_code, 200)
        models = res.json()
        provider_ids = [m["provider_id"] for m in models]
        self.assertIn("ollama", provider_ids)
        self.assertIn("anthropic", provider_ids)
        self.assertIn("openai", provider_ids)
        self.assertIn("mock", provider_ids)

    def test_03_hybrid_rag_retrieval(self):
        # Test Brian Chesky Founder Mode
        results = hybrid_retriever.search("Brian Chesky founder mode vs manager mode", top_k=3)
        self.assertGreater(len(results), 0)
        self.assertTrue(any("Brian Chesky" in r["guest"] or "Founder Mode" in r["episode_title"] for r in results))

        # Test Elena Verna PLG
        results_elena = hybrid_retriever.search("Elena Verna B2B PLG growth loops and PQLs", top_k=3)
        self.assertGreater(len(results_elena), 0)
        self.assertTrue(any("Elena Verna" in r["guest"] or "Product-Led" in r["episode_title"] for r in results_elena))

        # Test Gokul Rajaram SPADE
        results_gokul = hybrid_retriever.search("Gokul Rajaram SPADE framework decision", top_k=3)
        self.assertGreater(len(results_gokul), 0)
        self.assertTrue(any("Gokul" in r["guest"] or "SPADE" in r["episode_title"] for r in results_gokul))

    def test_04_grounding_citations(self):
        results = hybrid_retriever.search("Shreyas Doshi LNO framework", top_k=2)
        citations = GroundingGuard.extract_citations(results)
        self.assertEqual(len(citations), 2)
        self.assertTrue("Shreyas" in citations[0].guest or "LNO" in citations[0].episode_title)
        self.assertIsNotNone(citations[0].quote)

    def test_05_ship30_skill_prompt_and_extraction(self):
        mock_chunks = [{
            "episode_title": "Founder Mode & Airbnb",
            "guest": "Brian Chesky",
            "content": "We merged PM and PMM into a single role."
        }]
        prompt = build_ship30_prompt("Modern PM Role", mock_chunks)
        self.assertIn("Ship 30 for 30", prompt)
        self.assertIn("Brian Chesky", prompt)

        sample_llm_output = (
            "Here is the atomic essay:\n\n"
            "<artifact title=\"Ship 30 Essay: Founder Mode\" type=\"markdown\" language=\"markdown\">\n"
            "# Why Founder Mode Is Replacing Manager Mode\n\n"
            "Most companies are run poorly.\n"
            "</artifact>"
        )
        artifact = ArtifactBuilder.extract_artifact(sample_llm_output)
        self.assertIsNotNone(artifact)
        self.assertEqual(artifact["title"], "Ship 30 Essay: Founder Mode")
        self.assertEqual(artifact["artifact_type"], "markdown")
        self.assertTrue(artifact["is_valid"])

    def test_06_artifact_security_sanitization(self):
        malicious_html = '<a href="javascript:alert(\'xss\')">Click</a>'
        clean = sanitize_html(malicious_html)
        self.assertNotIn("javascript:", clean)
        self.assertIn('href="#"', clean)

        valid_html = '<div class="card"><p>Hello World</p></div>'
        is_valid, _ = validate_artifact_content(valid_html, "html")
        self.assertTrue(is_valid)

    def test_07_session_crud_lifecycle(self):
        # 1. Create Session
        create_res = self.client.post("/api/v1/sessions", json={"title": "Test Session", "active_model": "mock"})
        self.assertEqual(create_res.status_code, 201)
        session_id = create_res.json()["id"]

        # 2. List Sessions
        list_res = self.client.get("/api/v1/sessions")
        self.assertEqual(list_res.status_code, 200)
        self.assertTrue(any(s["id"] == session_id for s in list_res.json()))

        # 3. Get Session Detail
        detail_res = self.client.get(f"/api/v1/sessions/{session_id}")
        self.assertEqual(detail_res.status_code, 200)
        self.assertEqual(detail_res.json()["id"], session_id)

        # 4. Delete Session
        del_res = self.client.delete(f"/api/v1/sessions/{session_id}")
        self.assertEqual(del_res.status_code, 200)

        # 5. Verify 404
        get_after = self.client.get(f"/api/v1/sessions/{session_id}")
        self.assertEqual(get_after.status_code, 404)

    def test_08_chat_streaming_endpoint(self):
        payload = {
            "message": "Explain Brian Chesky's Founder Mode and how Airbnb changed PMs",
            "provider": "mock"
        }
        res = self.client.post("/api/v1/chat", json=payload)
        self.assertEqual(res.status_code, 200)
        self.assertIn("text/event-stream", res.headers["content-type"])
        body = res.text
        self.assertIn("session_init", body)
        self.assertIn("Founder Mode", body)
        self.assertIn("citations", body)


if __name__ == "__main__":
    unittest.main()
