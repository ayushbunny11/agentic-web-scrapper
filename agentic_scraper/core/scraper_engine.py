
"""
Core Web Scraping Engine
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Any
import time
import logging

logger = logging.getLogger(__name__)

class WebScrapingEngine:
    """Core web scraping engine with configurable extraction"""
    
    def __init__(self, config: Dict[str, Any] = None):
        from ..core.config_manager import ConfigManager
        
        if config is None:
            config_manager = ConfigManager()
            config = config_manager.get_scraper_config()
            
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(config.get("request_headers", {}))
        
        # Update user agent if provided in config
        if config and "user_agent" in config:
            self.session.headers["User-Agent"] = config["user_agent"]
    
    def scrape_website(self, url: str) -> Dict[str, Any]:
        """
        Scrape a website and extract all content in structured format
        
        Args:
            url: The URL to scrape
            
        Returns:
            Dictionary containing structured data
        """
        logger.info(f"Starting to scrape: {url}")

        try:
            response = self._make_request(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract structured data based on config
            scraped_data = {
                "url": url,
                "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Conditional extraction based on config
            if self.config.get("extract_text", True):
                scraped_data["title"] = self._extract_title(soup)
                scraped_data["text_content"] = self._extract_text_content(soup)
            
            if self.config.get("extract_metadata", True):
                scraped_data["metadata"] = self._extract_metadata(soup)
            
            if self.config.get("extract_images", True):
                scraped_data["images"] = self._extract_images(soup, url)
            
            if self.config.get("extract_videos", True):
                scraped_data["videos"] = self._extract_videos(soup, url)
            
            if self.config.get("extract_links", True):
                scraped_data["links"] = self._extract_links(soup, url)

            logger.info(f"Successfully scraped {url}")
            return scraped_data

        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return {"error": str(e), "url": url}
    
    def _make_request(self, url: str) -> requests.Response:
        """Make HTTP request with retry logic"""
        max_retries = self.config.get("max_retries", 3)
        
        for attempt in range(max_retries):
            try:
                response = self.session.get(
                    url, 
                    timeout=self.config.get("request_timeout", 10),
                    verify=self.config.get("verify_ssl", True),
                    allow_redirects=self.config.get("follow_redirects", True)
                )
                response.raise_for_status()
                return response
                
            except requests.RequestException as e:
                if attempt == max_retries - 1:
                    raise e
                logger.warning(f"Request attempt {attempt + 1} failed, retrying...")
                time.sleep(self.config.get("delay_between_requests", 1.0))
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        title_tag = soup.find('title')
        return title_tag.get_text().strip() if title_tag else ""

    def _extract_metadata(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract metadata from meta tags"""
        metadata = {}

        # Extract meta tags
        meta_tags = soup.find_all('meta')
        for tag in meta_tags:
            name = tag.get('name') or tag.get('property') or tag.get('http-equiv')
            content = tag.get('content')
            if name and content:
                metadata[name] = content

        return metadata

    def _extract_text_content(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract text content organized by structure"""
        text_content = {
            "headings": {},
            "paragraphs": [],
            "lists": [],
            "full_text": ""
        }

        # Extract headings
        for i in range(1, 7):
            headings = soup.find_all(f'h{i}')
            if headings:
                text_content["headings"][f"h{i}"] = [
                    h.get_text().strip() for h in headings
                ]

        # Extract paragraphs
        paragraphs = soup.find_all('p')
        text_content["paragraphs"] = [
            p.get_text().strip() for p in paragraphs 
            if p.get_text().strip() and len(p.get_text().strip()) >= self.config.get("min_text_length", 10)
        ]

        # Extract lists
        lists = soup.find_all(['ul', 'ol'])
        for list_tag in lists:
            list_items = list_tag.find_all('li')
            text_content["lists"].append({
                "type": list_tag.name,
                "items": [li.get_text().strip() for li in list_items]
            })

        # Extract full text (clean)
        for script in soup(["script", "style"]):
            script.decompose()
        text_content["full_text"] = soup.get_text()

        # Clean up whitespace
        if self.config.get("clean_text", True):
            text_content["full_text"] = re.sub(r'\s+', ' ', text_content["full_text"]).strip()

        return text_content

    def _extract_images(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        """Extract all images from the page"""
        images = []
        img_tags = soup.find_all('img')

        for img in img_tags:
            src = img.get('src')
            if src:
                # Convert relative URLs to absolute
                if self.config.get("resolve_relative_urls", True):
                    full_url = urljoin(base_url, src)
                else:
                    full_url = src

                image_data = {
                    "url": full_url,
                    "alt": img.get('alt', ''),
                    "title": img.get('title', ''),
                }
                
                if self.config.get("include_image_dimensions", True):
                    image_data.update({
                        "width": img.get('width', ''),
                        "height": img.get('height', '')
                    })
                
                images.append(image_data)

        return images

    def _extract_videos(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        """Extract all videos from the page"""
        videos = []

        # Extract video tags
        video_tags = soup.find_all('video')
        for video in video_tags:
            src = video.get('src')
            if src:
                videos.append({
                    "type": "video",
                    "url": urljoin(base_url, src),
                    "controls": video.get('controls', ''),
                    "autoplay": video.get('autoplay', ''),
                    "poster": video.get('poster', '')
                })

            # Check for source tags within video
            sources = video.find_all('source')
            for source in sources:
                src = source.get('src')
                if src:
                    videos.append({
                        "type": "video_source",
                        "url": urljoin(base_url, src),
                        "type_attr": source.get('type', '')
                    })

        # Extract iframe videos (YouTube, Vimeo, etc.) if enabled
        if self.config.get("include_embedded_videos", True):
            iframe_tags = soup.find_all('iframe')
            video_platforms = self.config.get("video_platforms", ["youtube", "vimeo", "dailymotion", "twitch"])
            
            for iframe in iframe_tags:
                src = iframe.get('src', '')
                if any(platform in src.lower() for platform in video_platforms):
                    videos.append({
                        "type": "embedded_video",
                        "url": src,
                        "width": iframe.get('width', ''),
                        "height": iframe.get('height', '')
                    })

        return videos

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        """Extract all links from the page"""
        links = []
        link_tags = soup.find_all('a', href=True)

        for link in link_tags:
            href = link['href']
            if self.config.get("resolve_relative_urls", True):
                full_url = urljoin(base_url, href)
            else:
                full_url = href

            link_text = link.get_text().strip()
            
            # Filter out empty links if configured
            if self.config.get("exclude_empty_content", True) and not link_text:
                continue

            link_data = {
                "url": full_url,
                "text": link_text,
                "title": link.get('title', ''),
                "target": link.get('target', '')
            }
            links.append(link_data)

        return links

    def save_to_json(self, data: Dict[str, Any], filename: str = None) -> str:
        """Save scraped data to JSON file"""
        if filename is None:
            # Generate filename from URL
            parsed_url = urlparse(data.get('url', 'unknown'))
            domain = parsed_url.netloc.replace('.', '_')
            filename = f"scraped_{domain}_{int(time.time())}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            if self.config.get("pretty_print", True):
                json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                json.dump(data, f, ensure_ascii=False)

        logger.info(f"Data saved to {filename}")
        return filename
