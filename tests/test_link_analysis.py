"""Unit and API integration tests for AI-Powered Website Link Analysis."""

import unittest
from unittest.mock import patch, AsyncMock
from starlette.testclient import TestClient
from app.main import app
from app.services.website_extractor import ExtractedWebsiteData, WebsiteExtractor
from app.services.llm_service import FreeLocalAIEngine


class TestLinkAnalysis(unittest.TestCase):
    """Test suite for /link-analysis API endpoint and Free AI engine."""

    def setUp(self):
        self.client = TestClient(app)
        self.sample_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Nova Tech Solutions | Enterprise Cloud & Custom Software</title>
            <meta name="description" content="Nova Tech Solutions delivers high-performance cloud software, API integrations, and digital transformation for modern enterprises.">
            <meta name="keywords" content="cloud software, enterprise development, API architecture, devops consulting">
            <meta property="og:site_name" content="Nova Tech Solutions">
        </head>
        <body>
            <h1>Empowering Enterprises with Scalable Cloud Software</h1>
            <h2>Custom Software Engineering</h2>
            <p>We build robust web and mobile applications tailored to your business workflows.</p>
            <h2>Cloud Infrastructure Migration</h2>
            <p>Seamlessly transition legacy workloads to modern AWS and GCP cloud architectures.</p>
            <h2>DevOps and CI/CD Automation</h2>
            <p>Accelerate your release cycles with automated continuous integration pipelines.</p>
            <h2>API Design and Microservices</h2>
            <p>High-throughput, resilient API architectures for scalable data exchange.</p>
            <h2>Dedicated Engineering Teams</h2>
            <p>Scale your engineering capacity with vetted senior full-stack developers.</p>
        </body>
        </html>
        """

    def test_local_ai_engine_analysis(self):
        """Test that FreeLocalAIEngine generates all 5 required sections accurately."""
        extractor = WebsiteExtractor()
        extracted = extractor.extract_from_html("https://novatech.io", self.sample_html)

        engine = FreeLocalAIEngine()
        brand_name = engine._extract_brand_name(extracted)
        self.assertEqual(brand_name, "Nova Tech Solutions")

        analysis = engine.analyze(extracted)

        # Section 1: Competitor Analysis
        self.assertIsNotNone(analysis.competitor_analysis)
        self.assertGreaterEqual(len(analysis.competitor_analysis.competitors), 3)
        self.assertTrue(len(analysis.competitor_analysis.strengths) > 0)
        self.assertTrue(len(analysis.competitor_analysis.opportunities) > 0)
        self.assertTrue(len(analysis.competitor_analysis.competitive_advantages) > 0)

        # Section 2: Top 5 Target Search Queries
        self.assertEqual(len(analysis.target_search_queries), 5)
        for q in analysis.target_search_queries:
            self.assertTrue(len(q.platforms) > 0)
            self.assertTrue(len(q.query) > 0)
            self.assertTrue(len(q.intent) > 0)

        # Section 3: SEO Improvements
        self.assertIsNotNone(analysis.seo_improvements)
        self.assertTrue(len(analysis.seo_improvements.primary_keyword) > 0)
        self.assertTrue(len(analysis.seo_improvements.recommended_title) > 0)
        self.assertTrue(len(analysis.seo_improvements.meta_description) > 0)
        self.assertTrue(len(analysis.seo_improvements.supporting_content) > 0)

        # Section 4: Top 5 Services
        self.assertEqual(len(analysis.top_services), 5)
        for s in analysis.top_services:
            self.assertTrue(len(s.service_name) > 0)
            self.assertTrue(len(s.target_industry) > 0)
            self.assertTrue(len(s.main_benefit) > 0)

        # Section 5: Target Audience Identification
        self.assertIsNotNone(analysis.target_audience)
        self.assertTrue(len(analysis.target_audience.primary_audience) > 0)
        self.assertTrue(len(analysis.target_audience.customer_profiles) > 0)
        self.assertTrue(len(analysis.target_audience.customer_needs) > 0)

    @patch("socket.getaddrinfo")
    @patch("app.services.website_extractor.WebsiteExtractor.fetch_html", new_callable=AsyncMock)
    def test_link_analysis_endpoint_success(self, mock_fetch, mock_dns):
        """Test POST /link-analysis end-to-end with mocked network fetch and DNS."""
        mock_dns.return_value = [(2, 1, 6, "", ("93.184.216.34", 0))]
        mock_fetch.return_value = self.sample_html

        payload = {"url": "https://novatech.io"}
        response = self.client.post("/link-analysis", json=payload)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["website"], "https://novatech.io")
        self.assertEqual(data["brand"]["name"], "Nova Tech Solutions")

        # Verify all 5 sections are present in API response
        analysis = data["analysis"]
        self.assertIn("competitor_analysis", analysis)
        self.assertIn("target_search_queries", analysis)
        self.assertIn("seo_improvements", analysis)
        self.assertIn("top_services", analysis)
        self.assertIn("target_audience", analysis)

        # Verify Free AI model used is reported
        self.assertIn("model_used", data)
        self.assertIn("free", data["model_used"].lower())

    def test_link_analysis_invalid_url(self):
        """Test POST /link-analysis rejects non-HTTP URLs."""
        payload = {"url": "ftp://files.example.com"}
        response = self.client.post("/link-analysis", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid URL scheme", response.json()["detail"])

    def test_link_analysis_ssrf_blocked(self):
        """Test POST /link-analysis rejects internal localhost URLs (SSRF protection)."""
        payload = {"url": "http://localhost:8000/internal-api"}
        response = self.client.post("/link-analysis", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("blocked", response.json()["detail"].lower())


if __name__ == "__main__":
    unittest.main()
