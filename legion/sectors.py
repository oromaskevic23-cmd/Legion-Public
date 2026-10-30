"""Extensible, legal-first online work taxonomy (not job listings or earnings).

An industry classification never grants website, customer or account access.
"""
SECTORS = frozenset({
    "software-development", "website-development", "quality-assurance",
    "defensive-cybersecurity", "research", "data-analysis",
    "data-cleaning", "business-analytics", "graphic-design",
    "video-production", "animation", "audio-production",
    "copywriting", "translation", "localization",
    "content-management", "ethical-seo", "digital-marketing",
    "customer-support", "crm-operations", "sales-research",
    "ecommerce-operations", "product-documentation",
    "education-content", "virtual-assistance", "project-management",
    "workflow-automation", "real-estate-research",
    "recruiting-administration", "accessibility-testing",
    "financial-reporting-research", "community-moderation",
    "ux-research", "market-research", "digital-product-development",
    "technical-support", "business-process-analysis"
})
SAFE_DEMO_ONLY = True

HIGH_RISK_BOUNDARIES = frozenset({
    "account-login", "outbound-publication", "customer-messages",
    "financial-transaction", "token-transfer", "order-placement",
    "paid-service-activation", "personal-data-export",
    "unauthorized-scraping", "bulk-unsolicited-outreach",
    "security-intrusion", "contract-signing"
})
