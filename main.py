import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Any
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebScrapingAgent:

    def __init__(self, delay: float = 1.0):
        """
        Initialize the web scraping agent
        
        Args:
            delay: Delay between requests to be respectful to servers
        """
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

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
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract structured data
            scraped_data = {
                "url": url,
                "title": self._extract_title(soup),
                "metadata": self._extract_metadata(soup),
                "text_content": self._extract_text_content(soup),
                "images": self._extract_images(soup, url),
                "videos": self._extract_videos(soup, url),
                "links": self._extract_links(soup, url),
                "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }

            logger.info(f"Successfully scraped {url}")
            return scraped_data

        except requests.RequestException as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return {"error": str(e), "url": url}

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
            name = tag.get('name') or tag.get('property') or tag.get(
                'http-equiv')
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
            p.get_text().strip() for p in paragraphs if p.get_text().strip()
        ]

        # Extract lists
        lists = soup.find_all(['ul', 'ol'])
        for list_tag in lists:
            list_items = list_tag.find_all('li')
            text_content["lists"].append({
                "type":
                list_tag.name,
                "items": [li.get_text().strip() for li in list_items]
            })

        # Extract full text (clean)
        for script in soup(["script", "style"]):
            script.decompose()
        text_content["full_text"] = soup.get_text()

        # Clean up whitespace
        text_content["full_text"] = re.sub(r'\s+', ' ',
                                           text_content["full_text"]).strip()

        return text_content

    def _extract_images(self, soup: BeautifulSoup,
                        base_url: str) -> List[Dict[str, str]]:
        """Extract all images from the page"""
        images = []
        img_tags = soup.find_all('img')

        for img in img_tags:
            src = img.get('src')
            if src:
                # Convert relative URLs to absolute
                full_url = urljoin(base_url, src)

                image_data = {
                    "url": full_url,
                    "alt": img.get('alt', ''),
                    "title": img.get('title', ''),
                    "width": img.get('width', ''),
                    "height": img.get('height', '')
                }
                images.append(image_data)

        return images

    def _extract_videos(self, soup: BeautifulSoup,
                        base_url: str) -> List[Dict[str, str]]:
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

        # Extract iframe videos (YouTube, Vimeo, etc.)
        iframe_tags = soup.find_all('iframe')
        for iframe in iframe_tags:
            src = iframe.get('src', '')
            if any(platform in src.lower() for platform in
                   ['youtube', 'vimeo', 'dailymotion', 'twitch']):
                videos.append({
                    "type": "embedded_video",
                    "url": src,
                    "width": iframe.get('width', ''),
                    "height": iframe.get('height', '')
                })

        return videos

    def _extract_links(self, soup: BeautifulSoup,
                       base_url: str) -> List[Dict[str, str]]:
        """Extract all links from the page"""
        links = []
        link_tags = soup.find_all('a', href=True)

        for link in link_tags:
            href = link['href']
            full_url = urljoin(base_url, href)

            link_data = {
                "url": full_url,
                "text": link.get_text().strip(),
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
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"Data saved to {filename}")
        return filename


def main():
    """Main function to demonstrate the web scraping agent"""
    # Initialize the agent
    agent = WebScrapingAgent(delay=1.0)

    # Example usage
    test_urls = ["https://x.com/home"]

    for url in test_urls:
        print(f"\nScraping: {url}")
        print("=" * 50)

        # Scrape the website
        data = agent.scrape_website(url)

        if "error" not in data:
            # Print summary
            print(f"Title: {data['title']}")
            print(
                f"Text paragraphs: {len(data['text_content']['paragraphs'])}")
            print(f"Images found: {len(data['images'])}")
            print(f"Videos found: {len(data['videos'])}")
            print(f"Links found: {len(data['links'])}")

            # Save to JSON
            filename = agent.save_to_json(data)
            print(f"Saved to: {filename}")

            # Pretty print first few items as example
            print("\nSample content:")
            print("-" * 30)

            if data['text_content']['paragraphs']:
                print(
                    f"First paragraph: {data['text_content']['paragraphs'][0][:100]}..."
                )

            if data['images']:
                print(f"First image: {data['images'][0]['url']}")

            if data['videos']:
                print(f"First video: {data['videos'][0]['url']}")

        else:
            print(f"Error: {data['error']}")

        # Respectful delay
        time.sleep(agent.delay)


if __name__ == "__main__":
    main()
