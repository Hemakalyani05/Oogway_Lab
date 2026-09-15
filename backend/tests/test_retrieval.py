"""
Tests for Hybrid RAG Retrieval and Grounding Guardrails.
"""
import unittest
from app.rag.ingest import load_and_index_transcripts
from app.rag.hybrid_retriever import hybrid_retriever
from app.skills.grounding_guard import GroundingGuard


class TestRetrieval(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load_and_index_transcripts()

    def test_hybrid_retrieval_brian_chesky(self):
        query = "What is Founder Mode and how did Brian Chesky change product management at Airbnb?"
        results = hybrid_retriever.search(query, top_k=3)
        self.assertGreater(len(results), 0)
        top_result = results[0]
        self.assertTrue("Brian Chesky" in top_result["guest"] or "Founder Mode" in top_result["episode_title"])
        self.assertGreater(top_result["score"], 0)

    def test_hybrid_retrieval_elena_verna_plg(self):
        query = "What is Product-Led Sales and how does Elena Verna define PQLs?"
        results = hybrid_retriever.search(query, top_k=3)
        self.assertGreater(len(results), 0)
        top_result = results[0]
        self.assertTrue("Elena Verna" in top_result["guest"] or "Product-Led" in top_result["episode_title"])

    def test_grounding_citations_format(self):
        results = hybrid_retriever.search("SPADE framework Gokul Rajaram", top_k=2)
        citations = GroundingGuard.extract_citations(results)
        self.assertEqual(len(citations), 2)
        self.assertTrue("Gokul Rajaram" in citations[0].guest or "SPADE" in citations[0].episode_title)
        self.assertIsNotNone(citations[0].quote)


if __name__ == "__main__":
    unittest.main()
