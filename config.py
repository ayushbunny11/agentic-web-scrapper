
"""
Configuration file for the Web Scraping Agent
"""

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
