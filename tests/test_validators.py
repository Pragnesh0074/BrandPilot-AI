"""Unit tests for URL validation, SSRF protection, and posting message constraints."""

import unittest
from app.utils.validators import validate_and_sanitize_url, validate_posting_message, is_private_ip


class TestValidators(unittest.TestCase):
    """Test suite for validators."""

    def test_valid_public_url(self):
        """Test that valid public HTTP/HTTPS URLs pass validation."""
        url = "https://example.com"
        result = validate_and_sanitize_url(url, allow_private=True)
        self.assertEqual(result, "https://example.com")

    def test_invalid_scheme(self):
        """Test that non-HTTP schemes are rejected."""
        with self.assertRaises(ValueError) as ctx:
            validate_and_sanitize_url("ftp://example.com/file.txt")
        self.assertIn("Invalid URL scheme", str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            validate_and_sanitize_url("file:///etc/passwd")
        self.assertIn("Invalid URL scheme", str(ctx.exception))

    def test_ssrf_blocked_localhost(self):
        """Test that localhost and 127.0.0.1 are blocked by SSRF defense."""
        with self.assertRaises(ValueError) as ctx:
            validate_and_sanitize_url("http://localhost:8000/secret")
        self.assertIn("blocked", str(ctx.exception).lower())

        with self.assertRaises(ValueError) as ctx:
            validate_and_sanitize_url("http://127.0.0.1:4000/admin")
        self.assertIn("blocked", str(ctx.exception).lower())

    def test_is_private_ip(self):
        """Test IP private detection logic."""
        self.assertTrue(is_private_ip("127.0.0.1"))
        self.assertTrue(is_private_ip("10.0.0.5"))
        self.assertTrue(is_private_ip("192.168.1.1"))
        self.assertTrue(is_private_ip("172.16.0.1"))
        self.assertTrue(is_private_ip("169.254.169.254"))
        self.assertTrue(is_private_ip("::1"))
        self.assertFalse(is_private_ip("8.8.8.8"))
        self.assertFalse(is_private_ip("1.1.1.1"))

    def test_posting_message_valid(self):
        """Test valid posting message with exactly 1 CTA link under 200 chars."""
        msg = "Check out our latest business platform and grow your online visibility. https://example.com"
        sanitized, url = validate_posting_message(msg)
        self.assertEqual(sanitized, msg)
        self.assertEqual(url, "https://example.com")

    def test_posting_message_too_long(self):
        """Test rejection when message exceeds 200 characters."""
        long_msg = "A" * 190 + " https://example.com"
        self.assertGreater(len(long_msg), 200)
        with self.assertRaises(ValueError) as ctx:
            validate_posting_message(long_msg)
        self.assertIn("exceeds maximum limit of 200 characters", str(ctx.exception))

    def test_posting_message_no_url(self):
        """Test rejection when message contains 0 CTA links."""
        no_url_msg = "Check out our latest platform and grow online."
        with self.assertRaises(ValueError) as ctx:
            validate_posting_message(no_url_msg)
        self.assertIn("none was found", str(ctx.exception))

    def test_posting_message_multiple_urls(self):
        """Test rejection when message contains more than 1 CTA link."""
        multi_url_msg = "Visit https://site1.com or https://site2.com for details!"
        with self.assertRaises(ValueError) as ctx:
            validate_posting_message(multi_url_msg)
        self.assertIn("found 2", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
