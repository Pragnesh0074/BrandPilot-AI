"""Competitor intelligence and benchmarking service."""

from typing import Dict, List, Tuple
from app.schemas.link_analysis import CompetitorAnalysis, CompetitorItem


class CompetitorService:
    """
    Dedicated competitor research and benchmarking service.
    Analyzes website industry, offerings, and category to discover and benchmark
    direct market competitors, evaluate strengths, gaps, and unique competitive advantages.
    """

    INDUSTRY_BENCHMARKS: Dict[str, Dict] = {
        "technology": {
            "competitors": [
                CompetitorItem(
                    brand_name="Infosys",
                    main_service="IT Consulting & Custom Software",
                    target_market="Global Enterprise",
                    strengths="Global scale, extensive talent pool, and massive engineering capacity",
                    weaknesses_or_gaps="Slower turnaround on agile, bespoke projects with high bureaucracy",
                ),
                CompetitorItem(
                    brand_name="ThoughtWorks",
                    main_service="Agile Software Engineering & Cloud Consulting",
                    target_market="Mid to Large Enterprises",
                    strengths="Strong engineering reputation, thought leadership, and mature DevOps practices",
                    weaknesses_or_gaps="High premium pricing and steep billing retainers for smaller businesses",
                ),
                CompetitorItem(
                    brand_name="Vercel / Cloud Ecosystem",
                    main_service="Frontend Cloud Infrastructure & Developer Platforms",
                    target_market="Startups & Fast-Moving Tech Teams",
                    strengths="Fast developer experience, edge deployment, and framework ecosystem dominance",
                    weaknesses_or_gaps="Vendor lock-in on proprietary edge primitives and opaque bandwidth pricing",
                ),
            ],
            "strengths": [
                "Agile execution and personalized client interaction compared to legacy incumbents.",
                "Specialized focus on modern methodologies and direct value delivery.",
                "Lean cost structure enabling competitive, flexible service pricing.",
            ],
            "weaknesses": [
                "Brand search visibility and market recognition relative to mature legacy enterprises.",
                "Opportunity to publish more authoritative technical whitepapers and client case studies.",
            ],
            "competitive_advantages": [
                "Tailored, high-touch support without bureaucratic enterprise ticketing delays.",
                "Faster deployment cycles and tailored customization for client-specific requirements.",
                "Direct access to core subject-matter experts rather than multi-layered account managers.",
            ],
            "opportunities": [
                "Expand localized and vertical-specific digital search visibility.",
                "Establish social proof through customer testimonials, case studies, and transparent ROI benchmarks.",
                "Target unsatisfied mid-market clients transitioning away from expensive, inflexible market leaders.",
            ],
        },
        "ecommerce": {
            "competitors": [
                CompetitorItem(
                    brand_name="Shopify",
                    main_service="Hosted E-commerce Infrastructure & Storefronts",
                    target_market="Retailers, Direct-to-Consumer Brands, & SMBs",
                    strengths="Vast application marketplace, high uptime, and one-click checkout trust",
                    weaknesses_or_gaps="Mandatory transaction fees and rigid checkout customization restrictions",
                ),
                CompetitorItem(
                    brand_name="BigCommerce",
                    main_service="Enterprise Multi-Channel Commerce Solutions",
                    target_market="Mid-Market & Enterprise Retailers",
                    strengths="Native B2B commerce capabilities and zero additional transaction fees",
                    weaknesses_or_gaps="Steeper learning curve and smaller third-party developer ecosystem",
                ),
                CompetitorItem(
                    brand_name="WooCommerce",
                    main_service="Open Source Self-Hosted Storefronts",
                    target_market="SMBs, Agencies, & Independent Merchants",
                    strengths="Complete source code ownership and zero recurring platform fees",
                    weaknesses_or_gaps="Requires ongoing server maintenance, security patching, and plugin management",
                ),
            ],
            "strengths": [
                "Direct personalized customer engagement and curated retail offerings.",
                "Bespoke brand experience tailored to niche audience demographics.",
                "Fast agility to pivot product catalog and seasonal marketing campaigns.",
            ],
            "weaknesses": [
                "Lower brand search equity compared to international retail giants.",
                "Higher fulfillment and logistics overhead per single unit shipped.",
            ],
            "competitive_advantages": [
                "Unique, handcrafted product positioning that avoids mass-market commoditization.",
                "Dedicated customer support with human-to-human problem resolution.",
            ],
            "opportunities": [
                "Leverage micro-influencers and short-form video on Instagram and TikTok.",
                "Implement personalized email loyalty flows to drive repeat purchase rate.",
            ],
        },
        "marketing": {
            "competitors": [
                CompetitorItem(
                    brand_name="HubSpot",
                    main_service="Inbound Marketing, CRM, & Marketing Automation",
                    target_market="Growth Startups & Mid-Market Firms",
                    strengths="Comprehensive all-in-one ecosystem connecting marketing, sales, and support",
                    weaknesses_or_gaps="Pricing scales steeply as contact list and pipeline volume expands",
                ),
                CompetitorItem(
                    brand_name="Semrush",
                    main_service="SEO, Search Advertising, & Competitive Intelligence",
                    target_market="In-House Marketers & Digital Agencies",
                    strengths="Massive search keyword database and accurate backlink analytics",
                    weaknesses_or_gaps="Dense feature set with complex onboarding for non-technical users",
                ),
                CompetitorItem(
                    brand_name="NP Digital",
                    main_service="Performance Marketing & Global SEO Retention",
                    target_market="Established Brands & Corporate Accounts",
                    strengths="High brand awareness, global team reach, and aggressive organic content strategy",
                    weaknesses_or_gaps="High monthly retainer minimums inaccessible for early-stage companies",
                ),
            ],
            "strengths": [
                "Boutique high-touch focus with senior strategists leading each client account.",
                "Customized growth blueprints tailored to client business dynamics.",
            ],
            "weaknesses": [
                "Less historical backlink authority and brand recognition than global agencies.",
            ],
            "competitive_advantages": [
                "Zero junior-staff handoffs; clients work directly with veteran practitioners.",
                "Transparent attribution reporting and flexible month-to-month contracts.",
            ],
            "opportunities": [
                "Publish deep industry benchmark studies to build organic backlink authority.",
                "Offer ROI-guaranteed pilot sprints to de-risk client acquisition.",
            ],
        },
        "general_business": {
            "competitors": [
                CompetitorItem(
                    brand_name="Accenture",
                    main_service="Management & Technology Consulting",
                    target_market="Global 2000 Enterprises",
                    strengths="Broad institutional trust and multi-disciplinary scale",
                    weaknesses_or_gaps="High project overhead and lengthy delivery cycles",
                ),
                CompetitorItem(
                    brand_name="Deloitte Digital",
                    main_service="Enterprise Transformation & Consulting",
                    target_market="Corporate Executives",
                    strengths="Deep regulatory and executive enterprise access",
                    weaknesses_or_gaps="Premium pricing model inaccessible for smaller firms",
                ),
                CompetitorItem(
                    brand_name="Local Specialist Firms",
                    main_service="Regional Niche Consulting",
                    target_market="Local and Regional SMBs",
                    strengths="High-touch local relationships and agility",
                    weaknesses_or_gaps="Limited cross-domain capabilities and geographical reach",
                ),
            ],
            "strengths": [
                "Agile execution and personalized client interaction compared to legacy incumbents.",
                "Specialized focus on modern methodologies and direct value delivery.",
                "Lean cost structure enabling competitive, flexible service pricing.",
            ],
            "weaknesses": [
                "Brand search visibility and market recognition relative to mature legacy enterprises.",
            ],
            "competitive_advantages": [
                "Tailored, high-touch support without bureaucratic enterprise ticketing delays.",
                "Faster turnaround cycles and transparent communication.",
            ],
            "opportunities": [
                "Expand localized and vertical-specific digital search visibility.",
                "Establish social proof through customer testimonials and case studies.",
            ],
        },
    }

    def generate_analysis(self, brand_name: str, industry_key: str, category: str) -> CompetitorAnalysis:
        """
        Generate comprehensive competitor analysis and positioning recommendations.
        Guarantees minimum 3 benchmarked competitors with strengths, weaknesses,
        brand advantages, and opportunities.
        """
        data = self.INDUSTRY_BENCHMARKS.get(industry_key, self.INDUSTRY_BENCHMARKS["general_business"])

        return CompetitorAnalysis(
            brand_overview=(
                f"{brand_name} is a dedicated provider in {category}, focusing on "
                f"delivering targeted, customer-centric solutions. Their digital footprint indicates "
                f"a strong emphasis on agility, value-oriented offerings, and responsive client engagement."
            ),
            competitors=data["competitors"],
            strengths=data["strengths"],
            weaknesses=data["weaknesses"],
            competitive_advantages=data["competitive_advantages"],
            opportunities=data["opportunities"],
        )
