"""Unit and API integration tests for Automated Multi-Platform Posting."""

import unittest
from starlette.testclient import TestClient
from app.main import app
from app.services.posting_service import PostingService
from app.platforms.base import BasePlatform
from app.schemas.posting import PlatformPostResult


class MockFailingPlatform(BasePlatform):
    """Platform simulator that deliberately fails."""

    def __init__(self):
        super().__init__(name="FailingPlatform", is_public=True)

    async def post(self, message: str, cta_url: str) -> PlatformPostResult:
        return self.create_failed_result("Simulated connection timeout")


class MockSuccessfulPlatform(BasePlatform):
    """Platform simulator that always succeeds."""

    def __init__(self):
        super().__init__(name="SuccessfulPlatform", is_public=True)

    async def post(self, message: str, cta_url: str) -> PlatformPostResult:
        return self.create_success_result("https://success.platform/post/42")


class TestPostingAPI(unittest.TestCase):
    """Test suite for /posting API endpoint and multi-platform service."""

    def setUp(self):
        self.client = TestClient(app)

    def test_post_success(self):
        """Test successful multi-platform post request with valid message."""
        payload = {
            "message": "Discover our innovative AI workflow platform today! https://example.com"
        }
        response = self.client.post("/posting", json=payload)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("results", data)
        self.assertGreaterEqual(len(data["results"]), 5)

        # Verify required fields in each result
        for result in data["results"]:
            self.assertIn("platform", result)
            self.assertIn("status", result)
            self.assertIn("posted_url", result)
            self.assertIn("public_access", result)
            self.assertIn("date", result)
            self.assertIn("time", result)
            self.assertIn("error", result)

    def test_post_exceeds_200_chars(self):
        """Test that messages exceeding 200 characters return 422 Unprocessable Entity."""
        payload = {
            "message": "A" * 190 + " https://example.com"
        }
        response = self.client.post("/posting", json=payload)
        self.assertEqual(response.status_code, 422)
        self.assertIn("exceeds maximum limit of 200 characters", response.json()["detail"])

    def test_post_missing_cta_link(self):
        """Test that messages with 0 CTA links return 422."""
        payload = {
            "message": "Check out our services for your next digital transformation project."
        }
        response = self.client.post("/posting", json=payload)
        self.assertEqual(response.status_code, 422)
        self.assertIn("exactly one CTA link", response.json()["detail"])

    def test_post_multiple_cta_links(self):
        """Test that messages with more than 1 CTA link return 422."""
        payload = {
            "message": "See https://site1.com and https://site2.com for details!"
        }
        response = self.client.post("/posting", json=payload)
        self.assertEqual(response.status_code, 422)
        self.assertIn("found 2", response.json()["detail"])

    def test_fault_isolation(self):
        """Verify that when one platform fails, other platforms continue independently."""
        import asyncio

        svc = PostingService(
            platforms=[MockSuccessfulPlatform(), MockFailingPlatform()]
        )
        response = asyncio.run(
            svc.publish_message("Great update https://example.com")
        )
        self.assertTrue(response.success)
        self.assertEqual(len(response.results), 2)

        p1, p2 = response.results[0], response.results[1]
        self.assertEqual(p1.status, "success")
        self.assertEqual(p1.posted_url, "https://success.platform/post/42")

        self.assertEqual(p2.status, "failed")
        self.assertIn("Simulated connection timeout", p2.error)


if __name__ == "__main__":
    unittest.main()
