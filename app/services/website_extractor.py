"""Website content scraper and structured information extractor."""

import re
from typing import Dict, List, Optional
import httpx
from app.config import settings

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False
    from html.parser import HTMLParser


class SimpleHTMLTextExtractor(HTMLParser if not HAS_BS4 else object):
    """Fallback HTML text and tag extractor using standard library html.parser."""

    def __init__(self):
        if not HAS_BS4:
            super().__init__()
        self.title: str = ""
        self.meta_description: str = ""
        self.meta_keywords: str = ""
        self.og_title: str = ""
        self.og_site_name: str = ""
        self.headings: List[str] = []
        self.paragraphs: List[str] = []
        self.links: List[str] = []
        self._current_tag: Optional[str] = None
        self._ignore_tags = {"script", "style", "noscript", "svg", "head"}
        self._buffer: List[str] = []

    def handle_starttag(self, tag, attrs):
        self._current_tag = tag.lower()
        attr_dict = {k.lower(): (v or "") for k, v in attrs}

        if tag.lower() == "meta":
            name = attr_dict.get("name", "").lower()
            prop = attr_dict.get("property", "").lower()
            content = attr_dict.get("content", "").strip()

            if name == "description":
                self.meta_description = content
            elif name == "keywords":
                self.meta_keywords = content
            elif prop == "og:title":
                self.og_title = content
            elif prop == "og:site_name":
                self.og_site_name = content
            elif prop == "og:description" and not self.meta_description:
                self.meta_description = content

    def handle_endtag(self, tag):
        t = tag.lower()
        if t in ("h1", "h2", "h3"):
            text = "".join(self._buffer).strip()
            if text:
                self.headings.append(text)
            self._buffer = []
        elif t in ("p", "li", "span", "div"):
            text = "".join(self._buffer).strip()
            if len(text) > 20:
                self.paragraphs.append(text)
            self._buffer = []
        self._current_tag = None

    def handle_data(self, data):
        if self._current_tag in self._ignore_tags:
            return
        cleaned = data.strip()
        if not cleaned:
            return
        if self._current_tag == "title" and not self.title:
            self.title = cleaned
        else:
            self._buffer.append(data)


class ExtractedWebsiteData:
    """Structured container for extracted website information."""

    def __init__(
        self,
        url: str,
        title: str,
        meta_description: str,
        meta_keywords: str,
        og_site_name: str,
        headings: List[str],
        body_text: str,
        services_hint: List[str],
    ):
        self.url = url
        self.title = title
        self.meta_description = meta_description
        self.meta_keywords = meta_keywords
        self.og_site_name = og_site_name
        self.headings = headings
        self.body_text = body_text
        self.services_hint = services_hint

    def to_summary_context(self, max_chars: int = 12000) -> str:
        """Render extracted content as clean context for LLM prompt."""
        parts = [
            f"Website URL: {self.url}",
            f"Page Title: {self.title}",
            f"Meta Description: {self.meta_description}",
            f"Meta Keywords: {self.meta_keywords}",
            f"Site Name: {self.og_site_name}",
        ]
        if self.headings:
            parts.append("Main Headings:\n- " + "\n- ".join(self.headings[:15]))
        if self.services_hint:
            parts.append("Detected Service Highlights:\n- " + "\n- ".join(self.services_hint[:10]))

        body_snippet = self.body_text[:max_chars]
        parts.append(f"Content Body:\n{body_snippet}")
        return "\n\n".join(parts)


class WebsiteExtractor:
    """Fetches and extracts clean structural text from web pages."""

    def __init__(self, timeout: float = settings.SCRAPER_TIMEOUT_SECONDS):
        self.timeout = timeout
        self.headers = {
            "User-Agent": settings.USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

    async def fetch_html(self, url: str) -> str:
        """Fetch raw HTML with timeout and redirect handling."""
        async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
            try:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.text
            except httpx.TimeoutException:
                raise ValueError(f"Website request timed out after {self.timeout}s.")
            except httpx.HTTPStatusError as e:
                raise ValueError(f"Website returned HTTP error {e.response.status_code}: {e.response.reason_phrase}")
            except httpx.RequestError as e:
                raise ValueError(f"Failed to connect to website: {str(e)}")

    def extract_from_html(self, url: str, html_content: str) -> ExtractedWebsiteData:
        """Extract structured content from HTML string."""
        if HAS_BS4:
            return self._extract_with_bs4(url, html_content)
        return self._extract_with_parser(url, html_content)

    def _extract_with_bs4(self, url: str, html_content: str) -> ExtractedWebsiteData:
        soup = BeautifulSoup(html_content, "html.parser")

        # Extract title
        title = soup.title.string.strip() if soup.title and soup.title.string else ""

        # Extract meta tags
        meta_desc = ""
        meta_keys = ""
        og_site_name = ""

        desc_tag = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
        if desc_tag and desc_tag.get("content"):
            meta_desc = desc_tag["content"].strip()
        else:
            og_desc = soup.find("meta", attrs={"property": "og:description"})
            if og_desc and og_desc.get("content"):
                meta_desc = og_desc["content"].strip()

        key_tag = soup.find("meta", attrs={"name": re.compile(r"^keywords$", re.I)})
        if key_tag and key_tag.get("content"):
            meta_keys = key_tag["content"].strip()

        site_tag = soup.find("meta", attrs={"property": "og:site_name"})
        if site_tag and site_tag.get("content"):
            og_site_name = site_tag["content"].strip()

        # Remove noisy tags
        for element in soup(["script", "style", "noscript", "svg", "iframe", "footer", "nav"]):
            element.decompose()

        # Headings
        headings = []
        for tag in soup.find_all(["h1", "h2", "h3"]):
            text = tag.get_text(strip=True)
            if text and text not in headings and len(text) < 150:
                headings.append(text)

        # Service hints
        services_hint = []
        for tag in soup.find_all(["li", "p", "div", "h4"]):
            text = tag.get_text(strip=True)
            if any(k in text.lower() for k in ["service", "solution", "feature", "offering", "pricing"]):
                if 20 < len(text) < 250 and text not in services_hint:
                    services_hint.append(text)

        # Body text
        body_text = soup.get_text(separator=" ", strip=True)
        # Normalize whitespace
        body_text = re.sub(r"\s+", " ", body_text)

        return ExtractedWebsiteData(
            url=url,
            title=title,
            meta_description=meta_desc,
            meta_keywords=meta_keys,
            og_site_name=og_site_name,
            headings=headings[:20],
            body_text=body_text[: settings.SCRAPER_MAX_BODY_CHARS],
            services_hint=services_hint[:10],
        )

    def _extract_with_parser(self, url: str, html_content: str) -> ExtractedWebsiteData:
        parser = SimpleHTMLTextExtractor()
        try:
            parser.feed(html_content)
        except Exception:
            pass

        body_text = " ".join(parser.paragraphs)
        body_text = re.sub(r"\s+", " ", body_text)

        return ExtractedWebsiteData(
            url=url,
            title=parser.title,
            meta_description=parser.meta_description,
            meta_keywords=parser.meta_keywords,
            og_site_name=parser.og_site_name or parser.og_title,
            headings=parser.headings[:20],
            body_text=body_text[: settings.SCRAPER_MAX_BODY_CHARS],
            services_hint=[],
        )

    async def extract(self, url: str) -> ExtractedWebsiteData:
        """Fetch and extract website content."""
        html = await self.fetch_html(url)
        return self.extract_from_html(url, html)
