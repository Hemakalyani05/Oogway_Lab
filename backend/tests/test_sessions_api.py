"""
Tests for Sessions and Health API Endpoints using FastAPI TestClient.
"""
import unittest
from starlette.testclient import TestClient

from app.main import app
from app.db.session import engine, Base
from app.rag.ingest import load_and_index_transcripts


class TestSessionsApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        load_and_index_transcripts()
        cls.client = TestClient(app)

    def test_health_endpoints(self):
        res_health = self.client.get("/healthz")
        self.assertEqual(res_health.status_code, 200)
        self.assertEqual(res_health.json()["status"], "healthy")

        res_ready = self.client.get("/readyz")
        self.assertEqual(res_ready.status_code, 200)
        data = res_ready.json()
        self.assertGreater(data["checks"]["knowledge_base_chunks"], 0)

    def test_session_lifecycle(self):
        # 1. Create session
        create_res = self.client.post(
            "/api/v1/sessions",
            json={"title": "Founder Mode Discussion", "active_model": "mock"}
        )
        self.assertEqual(create_res.status_code, 201)
        session_data = create_res.json()
        session_id = session_data["id"]
        self.assertEqual(session_data["title"], "Founder Mode Discussion")

        # 2. List sessions
        list_res = self.client.get("/api/v1/sessions")
        self.assertEqual(list_res.status_code, 200)
        sessions = list_res.json()
        self.assertTrue(any(s["id"] == session_id for s in sessions))

        # 3. Get session details
        detail_res = self.client.get(f"/api/v1/sessions/{session_id}")
        self.assertEqual(detail_res.status_code, 200)
        self.assertEqual(detail_res.json()["id"], session_id)

        # 4. Delete session
        del_res = self.client.delete(f"/api/v1/sessions/{session_id}")
        self.assertEqual(del_res.status_code, 200)

        # 5. Verify deleted
        get_after_del = self.client.get(f"/api/v1/sessions/{session_id}")
        self.assertEqual(get_after_del.status_code, 404)


if __name__ == "__main__":
    unittest.main()
