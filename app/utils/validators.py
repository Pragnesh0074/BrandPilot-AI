"""Validation utilities for URLs, SSRF protection, and message constraints."""

import ipaddress
import re
import socket
from urllib.parse import urlparse
from typing import Tuple


# Regex pattern to match HTTP/HTTPS URLs
URL_PATTERN = re.compile(
    r"https?://(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?::\d+)?(?:/[^\s<>\"'{}|\\^`]*)*",
    re.IGNORECASE,
)


def is_private_ip(ip_str: str) -> bool:
    """Check if an IP string belongs to private, loopback, or reserved network spaces."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_multicast
            or ip.is_unspecified
        )
    except ValueError:
        return True


def validate_and_sanitize_url(url: str, allow_private: bool = False) -> str:
    """
    Validate target URL format and enforce SSRF protection against private networks.
    
    Raises:
        ValueError: If URL format is invalid or resolves to a private/forbidden IP address.
    """
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string.")

    url = url.strip()
    parsed = urlparse(url)

    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Invalid URL scheme '{parsed.scheme}'. Only http and https are supported.")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL does not contain a valid hostname.")

    # Block well-known local aliases
    forbidden_hosts = {"localhost", "localhost.localdomain", "0.0.0.0", "127.0.0.1"}
    if hostname.lower() in forbidden_hosts:
        if not allow_private:
            raise ValueError(f"Access to '{hostname}' is blocked for security (SSRF protection).")

    # Resolve IP address to prevent DNS rebinding and internal network scanning
    if not allow_private:
        try:
            addr_info = socket.getaddrinfo(hostname, None)
            resolved_ips = {item[4][0] for item in addr_info}
            for ip in resolved_ips:
                if is_private_ip(ip):
                    raise ValueError(
                        f"Target host '{hostname}' resolves to private/internal IP {ip}. Request blocked."
                    )
        except socket.gaierror:
            # Domain could not be resolved
            raise ValueError(f"Cannot resolve hostname '{hostname}'. Host is unreachable.")

    return url


def validate_posting_message(message: str) -> Tuple[str, str]:
    """
    Validate posting request constraints:
    1. Message length must not exceed 200 characters.
    2. Exactly one CTA link must be included.
    3. The extracted URL must be valid.
    
    Returns:
        Tuple[str, str]: (sanitized_message, extracted_cta_url)
    
    Raises:
        ValueError: If any constraint is violated.
    """
    if not message or not isinstance(message, str):
        raise ValueError("Message must be a non-empty string.")

    cleaned_msg = message.strip()

    if len(cleaned_msg) > 200:
        raise ValueError(
            f"Message exceeds maximum limit of 200 characters (current length: {len(cleaned_msg)} characters)."
        )

    # Find all URLs in the message
    urls = URL_PATTERN.findall(cleaned_msg)

    if len(urls) == 0:
        raise ValueError("Message must contain exactly one CTA link, but none was found.")
    elif len(urls) > 1:
        raise ValueError(f"Message must contain exactly one CTA link, but found {len(urls)}: {', '.join(urls)}")

    cta_url = urls[0]

    # Validate CTA URL syntax
    parsed = urlparse(cta_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"CTA link '{cta_url}' is not a valid HTTP or HTTPS URL.")

    return cleaned_msg, cta_url
