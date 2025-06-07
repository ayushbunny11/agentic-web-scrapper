
"""
Configuration file for the AI-Powered Web Scraping Agent
"""

import os

# AI Agent Configuration
AI_CONFIG = {
    "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
    "model": "gpt-4o-mini",
    "max_tokens": 1000,
    "temperature": 0.3,
    "enable_ai_analysis": True,
    "enable_content_summarization": True,
    "enable_image_analysis": True,
    "enable_video_analysis": True,
    "enable_decision_making": True,
}

# Agent Decision Making Settings
AGENT_DECISIONS = {
    "content_relevance_threshold": 0.7,
    "image_analysis_threshold": 5,  # Analyze if more than 5 images
    "video_analysis_threshold": 3,  # Analyze if more than 3 videos
    "text_summary_length": 200,
    "max_links_to_analyze": 10,
    "priority_content_types": ["article", "news", "blog", "product"],
}

# Default scraping settings
DEFAULT_CONFIG = {
    # Request settings
    "delay_between_requests": 1.0,
    "request_timeout": 10,
    "max_retries": 3,
    
    # User agent string
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    
    # Content extraction settings
    "extract_text": True,
    "extract_images": True,
    "extract_videos": True,
    "extract_links": True,
    "extract_metadata": True,
    
    # Text processing
    "clean_text": True,
    "preserve_whitespace": False,
    
    # Image settings
    "include_image_dimensions": True,
    "resolve_relative_urls": True,
    
    # Video settings
    "include_embedded_videos": True,
    "video_platforms": ["youtube", "vimeo", "dailymotion", "twitch"],
    
    # Output settings
    "output_format": "json",
    "pretty_print": True,
    "include_timestamp": True,
    "include_ai_analysis": True,
    
    # Filtering options
    "min_text_length": 10,
    "exclude_empty_content": True,
    
    # Advanced options
    "follow_redirects": True,
    "verify_ssl": True,
}

# Selectors for different content types
CONTENT_SELECTORS = {
    "headings": ["h1", "h2", "h3", "h4", "h5", "h6"],
    "paragraphs": ["p"],
    "lists": ["ul", "ol"],
    "images": ["img"],
    "videos": ["video", "iframe[src*='youtube']", "iframe[src*='vimeo']"],
    "links": ["a[href]"],
    "articles": ["article", ".article", ".post", ".content"],
    "navigation": ["nav", ".nav", ".menu"],
    "sidebar": [".sidebar", ".aside", "aside"],
}

# Headers for different request types
REQUEST_HEADERS = {
    "default": {
        "User-Agent": DEFAULT_CONFIG["user_agent"],
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
}

# AI Prompts for different analysis tasks
AI_PROMPTS = {
    "content_analysis": """
    Analyze the following web content and provide:
    1. Main topic/theme
    2. Key insights (3-5 bullet points)
    3. Content quality score (1-10)
    4. Target audience
    5. Content type classification
    
    Content: {content}
    """,
    
    "image_analysis": """
    Analyze the following images from a webpage and provide:
    1. Overall visual theme
    2. Image types and purposes
    3. Quality assessment
    4. Relevance to content
    
    Images: {images}
    """,
    
    "video_analysis": """
    Analyze the following videos from a webpage and provide:
    1. Video content types
    2. Platform distribution
    3. Relevance assessment
    4. Engagement potential
    
    Videos: {videos}
    """,
    
    "decision_making": """
    Based on the scraped data, make decisions about:
    1. Should this content be prioritized? (Yes/No and why)
    2. What follow-up actions are recommended?
    3. Content classification and tagging suggestions
    4. Data extraction quality score (1-10)
    
    Data summary: {data_summary}
    """
}
