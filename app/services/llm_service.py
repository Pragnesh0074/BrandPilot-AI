"""Free AI / LLM Service supporting Free Local NLP Engine, Groq (Free Tier), and Gemini (Free Tier)."""

import json
import re
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse
import httpx

from app.config import settings
from app.services.website_extractor import ExtractedWebsiteData
from app.services.competitor_service import CompetitorService
from app.schemas.link_analysis import (
    BrandDetails,
    CompetitorAnalysis,
    CompetitorItem,
    TargetSearchQuery,
    SEOImprovements,
    ServiceItem,
    TargetAudience,
    AnalysisContent,
)


class FreeLocalAIEngine:
    """
    100% Free, offline, zero-API-cost AI intelligence engine.
    Analyzes website structural content, semantics, headings, and meta tags
    to generate complete, deep, and structured business intelligence.
    """

    # Industry / Category knowledge base for competitor analysis & classification
    INDUSTRY_KNOWLEDGE = {
        "technology": {
            "category": "Technology & Software Solutions",
            "competitors": [
                ("Infosys", "IT Consulting & Custom Software", "Global Enterprise", "Global scale and massive engineering headcount", "Slower turnaround on agile, bespoke projects"),
                ("ThoughtWorks", "Agile Software & Cloud Consulting", "Mid to Large Enterprises", "Strong engineering reputation and thought leadership", "High pricing and premium billing rates"),
                ("Vercel / Next.js Ecosystem", "Frontend Cloud & Developer Experience", "Startups & Tech Teams", "Developer ecosystem dominance and fast deployments", "Vendor lock-in on edge infrastructure"),
            ],
            "default_keywords": ["software engineering", "cloud infrastructure", "digital transformation", "API integration", "enterprise software"],
            "platforms_queries": [
                ("best enterprise software development company", ["Google"], "Service Search", "High-intent lead generation for IT buyers", "CTOs and IT Directors"),
                ("modern scalable web application architecture", ["LinkedIn"], "B2B Search", "Establishing technical authority", "VP of Engineering and Product Leads"),
                ("tech stack and UI engineering tips", ["Instagram", "Facebook"], "Inspiration", "Community building and developer talent attraction", "Developers and Tech Enthusiasts"),
                ("reliable API development agency for startups", ["X"], "Service Discovery", "Startup founder outreach", "Early-stage founders"),
                ("custom cloud application development services", ["Google", "LinkedIn"], "Commercial Evaluation", "Capturing RFP evaluations", "Procurement & IT Managers"),
            ],
        },
        "ecommerce": {
            "category": "E-Commerce & Retail",
            "competitors": [
                ("Shopify", "Hosted E-commerce Infrastructure", "Retailers & SMBs", "Vast app ecosystem and one-click checkout", "Transaction fees and customization limitations"),
                ("BigCommerce", "Enterprise Multi-channel Commerce", "Mid-market & Enterprises", "Native B2B commerce capabilities", "Steeper learning curve and smaller app marketplace"),
                ("WooCommerce", "Open Source Self-hosted Storefront", "SMBs & Developers", "Complete ownership and zero recurring platform fees", "Requires ongoing hosting, security, and maintenance overhead"),
            ],
            "default_keywords": ["online shopping", "ecommerce platform", "direct to consumer", "secure checkout", "fast shipping"],
            "platforms_queries": [
                ("best online store platform for growing brands", ["Google"], "Service Search", "Attracting merchants seeking scale", "E-commerce Managers"),
                ("trending consumer products and store deals", ["Instagram", "Facebook"], "Discovery", "Driving viral social consumer sales", "Online Shoppers & Trendsetters"),
                ("omnichannel retail fulfillment and logistics", ["LinkedIn"], "B2B Search", "B2B partnership and vendor engagement", "Retail Operations Executives"),
                ("top customer retention strategies for D2C", ["X"], "Inspiration", "Thought leadership among DTC founders", "Store Owners & Marketers"),
                ("affordable fast shipping online store", ["Google"], "Transactional", "Direct commercial conversion", "High-intent Retail Buyers"),
            ],
        },
        "marketing": {
            "category": "Digital Marketing & Brand Strategy",
            "competitors": [
                ("HubSpot", "Inbound Marketing & CRM Automation", "SMBs & Scaleups", "All-in-one CRM, content, and automation platform", "Tiered pricing escalates rapidly with contact volume"),
                ("Semrush", "SEO & Competitive Intelligence Suite", "Digital Marketers", "Deep keyword databases and backlink tracking", "Complex UI with feature overload for non-specialists"),
                ("Neil Patel Digital / NP Digital", "Full-Funnel Performance Marketing Agency", "Mid to Large Brands", "Strong organic search branding and global reach", "Higher retainer minimums for small accounts"),
            ],
            "default_keywords": ["digital marketing", "SEO optimization", "social media strategy", "conversion rate optimization", "brand growth"],
            "platforms_queries": [
                ("best digital marketing agency for ROI growth", ["Google"], "Service Search", "High conversion inbound lead capture", "CMOs and Growth Leaders"),
                ("creative social media campaign ideas", ["Instagram", "Facebook"], "Inspiration", "Visual brand awareness and engagement", "Social Media Managers"),
                ("B2B lead generation pipeline strategies", ["LinkedIn"], "B2B Search", "Commercial outreach to enterprise buyers", "Sales & Marketing Directors"),
                ("viral marketing and growth hacking case studies", ["X"], "Discovery", "Establishing viral thought leadership", "Founders & Growth Marketers"),
                ("how to improve organic search ranking fast", ["Google"], "Informational", "Top-of-funnel educational authority", "Marketing Specialists"),
            ],
        },
        "general_business": {
            "category": "Professional Business Services",
            "competitors": [
                ("Accenture", "Management & Technology Consulting", "Global 2000 Enterprises", "Broad institutional trust and multi-disciplinary scale", "High project overhead and lengthy delivery cycles"),
                ("Deloitte Digital", "Enterprise Transformation & Consulting", "Corporate Executives", "Deep regulatory and executive enterprise access", "Premium pricing model inaccessible for smaller firms"),
                ("Local Specialist Firms", "Regional Niche Consulting", "Local and Regional SMBs", "High-touch local relationships and agility", "Limited cross-domain capabilities and geographical reach"),
            ],
            "default_keywords": ["professional consulting", "business strategy", "client solutions", "quality service", "operational excellence"],
            "platforms_queries": [
                ("trusted business consulting and solutions provider", ["Google"], "Service Search", "High-intent buyer discovery", "Business Owners & Directors"),
                ("client success stories and business impact", ["LinkedIn"], "B2B Search", "Credential verification and trust building", "Procurement Executives"),
                ("behind the scenes business team culture", ["Instagram", "Facebook"], "Brand Trust", "Humanizing brand identity and hiring", "Prospective Clients & Talent"),
                ("business transformation insights and trends", ["X"], "Thought Leadership", "Industry discourse and peer engagement", "Industry Analysts & C-Suite"),
                ("affordable business consulting services", ["Google"], "Commercial Intent", "Capturing price-sensitive mid-market buyers", "SMB Executives"),
            ],
        },
    }

    def _extract_brand_name(self, data: ExtractedWebsiteData) -> str:
        if data.og_site_name and len(data.og_site_name.strip()) > 1:
            return data.og_site_name.strip()
        if data.title:
            # Often Title is "Brand Name | Tagline" or "Brand Name - Services"
            parts = re.split(r"[\-|–|—|:|•|\|]", data.title)
            if parts and parts[0].strip():
                candidate = parts[0].strip()
                if len(candidate) <= 40:
                    return candidate

        # Fallback to domain name capitalization
        parsed = urlparse(data.url)
        domain = parsed.hostname or data.url
        clean_domain = re.sub(r"^www\.", "", domain)
        name_part = clean_domain.split(".")[0]
        return name_part.capitalize()

    def _detect_industry(self, text: str) -> str:
        low = text.lower()
        if any(w in low for w in ["software", "api", "tech", "cloud", "developer", "code", "ai", "app", "saas"]):
            return "technology"
        elif any(w in low for w in ["shop", "cart", "product", "checkout", "store", "ecommerce", "retail", "buy"]):
            return "ecommerce"
        elif any(w in low for w in ["marketing", "seo", "agency", "advertising", "traffic", "branding", "leads"]):
            return "marketing"
        return "general_business"

    def _extract_top_services(self, data: ExtractedWebsiteData, category: str) -> List[ServiceItem]:
        services: List[ServiceItem] = []

        # Check headings for service-like names
        for heading in data.headings:
            clean_h = heading.strip()
            if 4 <= len(clean_h) <= 50 and not any(clean_h.lower() == s.service_name.lower() for s in services):
                # Avoid generic headers
                if clean_h.lower() not in {"about us", "contact us", "privacy policy", "terms of service", "home", "menu"}:
                    services.append(
                        ServiceItem(
                            service_name=clean_h,
                            description=f"Tailored {clean_h.lower()} delivering high-impact operational value and measurable performance.",
                            target_industry=category,
                            target_customer="Organizations and decision-makers seeking quality execution",
                            main_benefit=f"Accelerates growth and streamlines execution with professional {clean_h.lower()}.",
                        )
                    )
            if len(services) >= 5:
                break

        # If fewer than 5 discovered from headings, fill with contextual service defaults
        defaults = [
            ("Custom Solution Development", "Tailored end-to-end design and delivery to match bespoke client requirements.", "Organizations with unique operational needs", "Higher adaptability and customized outcomes"),
            ("Strategic Consultation", "Expert guidance and discovery workshops to identify gaps and optimization opportunities.", "Business leaders and department heads", "De-risks decision making with clear roadmaps"),
            ("Performance Optimization", "Continuous monitoring, refining, and tuning to ensure peak performance and stability.", "Teams requiring maximum reliability and uptime", "Enhanced speed, user satisfaction, and efficiency"),
            ("Integration & Onboarding", "Frictionless setup and connection with existing third-party platforms and tools.", "Growing teams modernizing their operations", "Reduces transition friction and saves onboarding time"),
            ("Ongoing Maintenance & Support", "Reliable 24/7 proactive maintenance, security patches, and SLA support.", "Enterprises prioritizing operational continuity", "Guarantees peace of mind and long-term uptime"),
        ]

        for name, desc, target, benefit in defaults:
            if len(services) >= 5:
                break
            if not any(s.service_name == name for s in services):
                services.append(
                    ServiceItem(
                        service_name=name,
                        description=desc,
                        target_industry=category,
                        target_customer=target,
                        main_benefit=benefit,
                    )
                )

        return services[:5]

    def __init__(self):
        self.competitor_service = CompetitorService()

    def analyze(self, data: ExtractedWebsiteData) -> AnalysisContent:
        combined_text = f"{data.title} {data.meta_description} {data.meta_keywords} {' '.join(data.headings)} {data.body_text[:4000]}"
        industry_key = self._detect_industry(combined_text)
        industry_info = self.INDUSTRY_KNOWLEDGE[industry_key]
        brand_name = self._extract_brand_name(data)

        # 1. Competitor Analysis (delegated to CompetitorService)
        comp_analysis = self.competitor_service.generate_analysis(
            brand_name=brand_name,
            industry_key=industry_key,
            category=industry_info["category"],
        )

        # 2. Top 5 Target Search Queries across Google, Facebook, Instagram, LinkedIn, X
        queries: List[TargetSearchQuery] = []
        for q_text, platforms, intent, relevance, audience in industry_info["platforms_queries"]:
            queries.append(
                TargetSearchQuery(
                    query=f"{q_text} {brand_name}".strip() if "best" not in q_text else q_text,
                    platforms=platforms,
                    intent=intent,
                    business_relevance=relevance,
                    target_audience=audience,
                )
            )

        # 3. SEO Improvements
        primary_kw = data.meta_keywords.split(",")[0].strip() if data.meta_keywords else industry_info["default_keywords"][0]
        secondary_kws = [k.strip() for k in data.meta_keywords.split(",")[1:4] if k.strip()] or industry_info["default_keywords"][1:4]

        recommended_title = f"{brand_name} | Top {primary_kw.title()} & Solutions"
        if len(recommended_title) > 60:
            recommended_title = recommended_title[:57] + "..."

        recommended_meta_desc = (
            f"Discover premier {primary_kw} with {brand_name}. We empower businesses with "
            f"innovative, reliable, and cost-effective services. Get started today!"
        )
        if len(recommended_meta_desc) > 160:
            recommended_meta_desc = recommended_meta_desc[:157] + "..."

        seo_improvements = SEOImprovements(
            primary_keyword=primary_kw,
            secondary_keywords=secondary_kws,
            long_tail_keywords=[
                f"affordable {primary_kw} for growing businesses",
                f"best {primary_kw} provider reviews",
                f"custom {primary_kw} implementation guide",
            ],
            business_keywords=industry_info["default_keywords"],
            recommended_title=recommended_title,
            meta_description=recommended_meta_desc,
            supporting_content=[
                "Comprehensive Service Landing Pages with explicit conversion funnels",
                "Frequently Asked Questions (FAQ) addressing pricing, onboarding, and SLAs",
                "Industry-specific case studies demonstrating quantifiable ROI metrics",
                "Educational blog series covering industry trends, best practices, and actionable tutorials",
                "Comparison landing pages highlighting key differentiators versus alternatives",
            ],
        )

        # 4. Top 5 Services
        top_services = self._extract_top_services(data, industry_info["category"])

        # 5. Target Audience Identification
        target_audience = TargetAudience(
            primary_audience=[
                "Small to medium-sized business owners and technical leaders seeking reliable execution",
                "Department heads and project leaders needing specialized agile domain expertise",
            ],
            secondary_audience=[
                "Startup founders in need of rapid prototype-to-production scale",
                "Procurement officers looking for cost-effective alternatives to Tier-1 firms",
            ],
            industries=[
                industry_info["category"],
                "B2B Professional Services",
                "Digital Commerce & Technology",
                "Emerging Startups & Growth Scaleups",
            ],
            business_types=[
                "Small & Medium Enterprises (SMBs)",
                "Early-stage to Series-B Startups",
                "Mid-market Commercial Firms",
            ],
            customer_profiles=[
                "Decision Maker: CTO / VP of Technology / Head of Digital Operations",
                "Budget Holder: Managing Director / Founder / Business Unit VP",
                "Evaluator: Senior Product Manager / Technical Lead",
            ],
            location="Global digital market with primary reach in English-speaking commercial hubs",
            customer_needs=[
                "Rapid, predictable turnaround without lengthy negotiation bottlenecks",
                "Cost transparency with clear deliverables and no hidden fees",
                "High quality standards and accessible ongoing communication",
            ],
            potential_interests=[
                "Digital efficiency, operational automation, cost reduction, modern tech tools, growth marketing",
            ],
            recommended_segments=[
                "High-growth startups requiring agile outsourced specialized capabilities",
                "Established regional businesses modernizing legacy processes",
                "Performance-focused teams searching for high ROI service partners",
            ],
        )

        return AnalysisContent(
            competitor_analysis=comp_analysis,
            target_search_queries=queries,
            seo_improvements=seo_improvements,
            top_services=top_services,
            target_audience=target_audience,
        )


class LLMService:
    """
    Unified AI orchestration service.
    Prioritizes Free Local AI Engine by default (0 cost, no API keys needed),
    with optional support for Free Tier Google Gemini and Free Tier Groq Cloud.
    """

    def __init__(self):
        self.local_engine = FreeLocalAIEngine()
        self.provider = settings.LLM_PROVIDER.lower()

    async def analyze_website(self, data: ExtractedWebsiteData) -> Dict[str, Any]:
        """Analyze extracted website data and return structured analysis result."""
        # Check if external free tier is explicitly configured with an API key
        if self.provider == "gemini" and settings.GEMINI_API_KEY:
            try:
                return await self._analyze_with_gemini_free_tier(data)
            except Exception as e:
                # Graceful fallback to Free Local AI Engine
                return self._fallback_local_analysis(data, fallback_reason=f"Gemini error: {str(e)}")

        elif self.provider == "groq":
            try:
                return await self._analyze_with_groq_free_tier(data)
            except Exception as e:
                return self._fallback_local_analysis(data, fallback_reason=f"Groq error: {str(e)}")

        # Default: 100% Free Local AI Engine
        return self._fallback_local_analysis(data)

    def _fallback_local_analysis(self, data: ExtractedWebsiteData, fallback_reason: Optional[str] = None) -> Dict[str, Any]:
        analysis_content = self.local_engine.analyze(data)
        brand_name = self.local_engine._extract_brand_name(data)
        combined_text = f"{data.title} {data.meta_description} {data.body_text[:1000]}"
        industry_key = self.local_engine._detect_industry(combined_text)
        category = self.local_engine.INDUSTRY_KNOWLEDGE[industry_key]["category"]
        summary = data.meta_description or f"{brand_name} is an established organization providing specialized {category.lower()}."

        brand = BrandDetails(
            name=brand_name,
            category=category,
            summary=summary,
        )

        model_name = "free-local-ai-engine"
        if fallback_reason:
            model_name += f" (fallback: {fallback_reason})"

        return {
            "brand": brand,
            "analysis": analysis_content,
            "model_used": model_name,
        }

    async def _analyze_with_gemini_free_tier(self, data: ExtractedWebsiteData) -> Dict[str, Any]:
        """Call Google Gemini Free Tier endpoint."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent?key={settings.GEMINI_API_KEY}"
        context = data.to_summary_context(max_chars=8000)

        prompt = (
            "You are an expert AI business and SEO analyst. Analyze the following website content "
            "and output STRICT JSON matching this schema:\n"
            "{\n"
            '  "brand": {"name": "...", "category": "...", "summary": "..."},\n'
            '  "competitor_analysis": {"brand_overview": "...", "competitors": [{"brand_name": "...", "main_service": "...", "target_market": "...", "strengths": "...", "weaknesses_or_gaps": "..."}], "strengths": ["..."], "weaknesses": ["..."], "competitive_advantages": ["..."], "opportunities": ["..."]},\n'
            '  "target_search_queries": [{"query": "...", "platforms": ["Google", "LinkedIn"], "intent": "...", "business_relevance": "...", "target_audience": "..."}],\n'
            '  "seo_improvements": {"primary_keyword": "...", "secondary_keywords": ["..."], "long_tail_keywords": ["..."], "business_keywords": ["..."], "recommended_title": "...", "meta_description": "...", "supporting_content": ["..."]},\n'
            '  "top_services": [{"service_name": "...", "description": "...", "target_industry": "...", "target_customer": "...", "main_benefit": "..."}],\n'
            '  "target_audience": {"primary_audience": ["..."], "secondary_audience": ["..."], "industries": ["..."], "business_types": ["..."], "customer_profiles": ["..."], "location": "...", "customer_needs": ["..."], "potential_interests": ["..."], "recommended_segments": ["..."]}\n'
            "}\n\n"
            f"Website Context:\n{context}"
        )

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"response_mime_type": "application/json"},
        }

        async with httpx.AsyncClient(timeout=25.0) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            res_data = resp.json()
            raw_text = res_data["candidates"][0]["content"]["parts"][0]["text"]
            parsed_json = json.loads(raw_text)

            brand = BrandDetails(**parsed_json["brand"])
            analysis = AnalysisContent(
                competitor_analysis=CompetitorAnalysis(**parsed_json["competitor_analysis"]),
                target_search_queries=[TargetSearchQuery(**q) for q in parsed_json["target_search_queries"]],
                seo_improvements=SEOImprovements(**parsed_json["seo_improvements"]),
                top_services=[ServiceItem(**s) for s in parsed_json["top_services"]],
                target_audience=TargetAudience(**parsed_json["target_audience"]),
            )
            return {
                "brand": brand,
                "analysis": analysis,
                "model_used": f"google-gemini-free-tier ({settings.GEMINI_MODEL})",
            }

    async def _analyze_with_groq_free_tier(self, data: ExtractedWebsiteData) -> Dict[str, Any]:
        """Call Groq Cloud Free Tier."""
        import os
        from groq import AsyncGroq

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is not configured.")

        client = AsyncGroq(api_key=api_key)
        context = data.to_summary_context(max_chars=6000)

        prompt = (
            "You are an expert AI business and SEO analyst. Output STRICT JSON:\n"
            f"{context}"
        )
        completion = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        raw_text = completion.choices[0].message.content
        parsed = json.loads(raw_text)
        brand = BrandDetails(**parsed["brand"])
        analysis = AnalysisContent(**parsed["analysis"])
        return {
            "brand": brand,
            "analysis": analysis,
            "model_used": "groq-free-tier (llama-3.3-70b-versatile)",
        }
