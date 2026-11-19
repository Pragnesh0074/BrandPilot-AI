
# BrandPilot AI

**AI-Powered Website Intelligence & Multi-Platform Social Media Automation API**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi)
![Async](https://img.shields.io/badge/Async-Supported-success)
![License](https://img.shields.io/badge/License-MIT-green)

BrandPilot AI is a Python-based backend platform built with FastAPI that combines AI-powered website analysis, business intelligence, SEO recommendations, competitor research, and automated social media publishing.

The platform analyzes publicly accessible websites to generate actionable business insights and provides a unified API for distributing content across multiple social media platforms.

## Features

### AI-Powered Website Analysis

- Extract website content, metadata, and brand information.
- Identify competitors and analyze their market positioning.
- Discover business strengths, weaknesses, and opportunities.
- Generate structured business intelligence reports.
- Identify target industries and customer segments.

### SEO Intelligence

- Generate primary, secondary, and long-tail keywords.
- Recommend SEO-friendly page titles and meta descriptions.
- Identify relevant search queries.
- Suggest content improvements and SEO opportunities.

### Business Intelligence

Generates five structured analysis sections:

1. **Competitor Analysis** – Competitor identification, strengths, weaknesses, and competitive advantages.
2. **Search Query Recommendations** – Relevant search queries for Google, Facebook, Instagram, LinkedIn, and X.
3. **SEO Improvements** – Keywords, metadata, and content recommendations.
4. **Business Services** – Recommended services, target industries, customer profiles, and benefits.
5. **Target Audience Analysis** – Customer personas, business types, locations, interests, and requirements.

### Multi-Platform Social Media Publishing

Publish content across multiple platforms through a single API endpoint.

Supported platforms:

- Telegram
- Discord
- Slack
- Mastodon
- Bluesky
- X (Twitter)

Additional capabilities:

- Maximum message length of 200 characters.
- Exactly one valid CTA link per message.
- Asynchronous concurrent publishing.
- Independent platform error handling.
- Simulation mode for testing without live credentials.

### Security

- URL protocol validation (HTTP/HTTPS).
- DNS-based SSRF protection.
- Private and reserved IP address blocking.
- Pydantic request and response validation.
- Modular platform integration architecture.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI | REST API framework |
| Pydantic | Data validation and schemas |
| asyncio | Asynchronous processing |
| HTTPX | HTTP communication |
| BeautifulSoup / HTML Parsing | Website content extraction |
| Google Gemini | Cloud AI integration |
| Groq | Cloud AI integration |
| Local AI Engine | Local semantic analysis |
| unittest | Automated testing |

## Project Structure

```text
BrandPilot-AI/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── link_analysis.py
│   │   └── posting.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── link_analysis.py
│   │   └── posting.py
│   │
│   ├── services/
│   │   ├── website_extractor.py
│   │   ├── llm_service.py
│   │   ├── analysis_service.py
│   │   └── posting_service.py
│   │
│   ├── platforms/
│   │   ├── base.py
│   │   ├── telegram.py
│   │   ├── discord.py
│   │   ├── slack.py
│   │   ├── mastodon.py
│   │   ├── bluesky.py
│   │   └── twitter.py
│   │
│   └── utils/
│       └── validators.py
│
├── tests/
│   ├── test_validators.py
│   ├── test_posting.py
│   └── test_link_analysis.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation & Setup

### Prerequisites

- Python 3.10 or later
- pip
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/brandpilot-ai.git

cd brandpilot-ai
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate the environment:

**macOS / Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create your environment configuration:

```bash
cp .env.example .env
```

Update the `.env` file with your required configuration.

By default, the project supports local AI processing and social media simulation mode, allowing local execution without mandatory external API credentials.

### 5. Start the Application

```bash
uvicorn app.main:app --host 0.0.0.0 --port 4000 --reload
```

The API will be available at:

| Resource | URL |
|---|---|
| Base URL | http://localhost:4000 |
| Swagger Documentation | http://localhost:4000/docs |
| ReDoc Documentation | http://localhost:4000/redoc |

## API Documentation

### 1. Website Link Analysis

**Endpoint:** `POST /link-analysis`

Analyzes a website and generates structured business intelligence and SEO recommendations.

**Request:**

```json
{
  "url": "https://example.com"
}
```

**Response Overview:**

```json
{
  "success": true,
  "website": "https://example.com",
  "brand": {
    "name": "Example",
    "category": "Business Services",
    "summary": "Website brand overview"
  },
  "analysis": {
    "competitor_analysis": {},
    "target_search_queries": [],
    "seo_improvements": {},
    "top_services": [],
    "target_audience": {}
  },
  "model_used": "free-local-ai-engine",
  "processing_time_ms": 3.82
}
```

The analysis response contains five sections covering competitors, search queries, SEO improvements, business services, and target audiences.

### 2. Multi-Platform Social Media Publishing

**Endpoint:** `POST /posting`

Publishes a validated message across supported social media platforms.

**Request:**

```json
{
  "message": "Discover our latest business solutions and grow your online presence. https://example.com"
}
```

**Validation Rules:**

- Maximum 200 characters.
- Exactly one valid CTA link.
- CTA link must use HTTP or HTTPS.

**Response Overview:**

```json
{
  "success": true,
  "results": [
    {
      "platform": "Telegram",
      "status": "success",
      "posted_url": "https://t.me/channel/example",
      "public_access": true,
      "error": null
    },
    {
      "platform": "Discord",
      "status": "success",
      "posted_url": "https://discord.com/channels/example",
      "public_access": true,
      "error": null
    }
  ]
}
```

Each platform returns its individual publishing status. A failure on one platform does not interrupt publishing to other platforms.

### 3. Health Check

**Endpoint:** `GET /health`

Checks the application status and configured execution modes.

**Response:**

```json
{
  "status": "healthy",
  "free_ai_ready": true,
  "posting_simulation_mode": true
}
```

## AI Engine Configuration

The application supports multiple AI processing providers.

| Provider | Description |
|---|---|
| FreeLocalAIEngine | Default local semantic analysis |
| Google Gemini Flash | Cloud-based AI processing |
| Groq Cloud | Cloud-based inference |

### Local AI Processing

The built-in local engine uses structural website extraction, semantic pattern matching, and keyword clustering to generate analysis results without requiring an external AI API.

### Cloud AI Processing

Google Gemini and Groq integrations provide alternative AI processing options through configurable providers.

The active provider and associated credentials can be configured through environment variables.

## Security & SSRF Protection

Website analysis accepts externally supplied URLs, so request validation is an important part of the application.

The URL validation layer:

1. Allows only HTTP and HTTPS protocols.
2. Resolves domain names through DNS.
3. Checks resolved IP addresses.
4. Blocks loopback addresses.
5. Blocks private network ranges.
6. Blocks link-local and reserved IP addresses.
7. Prevents requests to restricted internal network resources.

## Testing

The project includes automated tests covering:

- URL validation and SSRF protection.
- Social media message validation.
- Platform publishing and error handling.
- Link analysis response validation.
- API functionality.

Run the test suite:

```bash
python3 -m unittest discover tests
```

## Configuration

Environment variables are managed through the `.env` file.

Refer to `.env.example` for the available configuration options, including AI provider settings, platform credentials, and publishing simulation mode.

## License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.
