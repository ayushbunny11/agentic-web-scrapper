
"""
Example usage of the Web Scraping Agent
"""

from main import WebScrapingAgent
import json

def scrape_single_url():
    """Example: Scrape a single URL"""
    agent = WebScrapingAgent(delay=1.0)
    
    url = "https://example.com"
    print(f"Scraping: {url}")
    
    data = agent.scrape_website(url)
    
    if "error" not in data:
        # Save to file
        filename = agent.save_to_json(data)
        print(f"Data saved to: {filename}")
        
        # Print summary
        print(f"Title: {data['title']}")
        print(f"Images: {len(data['images'])}")
        print(f"Videos: {len(data['videos'])}")
        print(f"Paragraphs: {len(data['text_content']['paragraphs'])}")
    else:
        print(f"Error: {data['error']}")

def scrape_multiple_urls():
    """Example: Scrape multiple URLs"""
    agent = WebScrapingAgent(delay=2.0)
    
    urls = [
        "https://example.com",
        "https://httpbin.org/html",
        # Add more URLs here
    ]
    
    results = []
    
    for url in urls:
        print(f"\nScraping: {url}")
        data = agent.scrape_website(url)
        results.append(data)
        
        if "error" not in data:
            print(f"✓ Successfully scraped {data['title']}")
        else:
            print(f"✗ Failed to scrape: {data['error']}")
    
    # Save all results
    with open("batch_scraping_results.json", "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nBatch results saved to: batch_scraping_results.json")

def analyze_scraped_data():
    """Example: Analyze scraped data"""
    agent = WebScrapingAgent()
    
    url = "https://news.ycombinator.com"
    data = agent.scrape_website(url)
    
    if "error" not in data:
        print("Data Analysis:")
        print("=" * 40)
        print(f"Website: {data['url']}")
        print(f"Title: {data['title']}")
        print(f"Total text length: {len(data['text_content']['full_text'])}")
        print(f"Number of headings: {sum(len(headings) for headings in data['text_content']['headings'].values())}")
        print(f"Number of paragraphs: {len(data['text_content']['paragraphs'])}")
        print(f"Number of images: {len(data['images'])}")
        print(f"Number of videos: {len(data['videos'])}")
        print(f"Number of links: {len(data['links'])}")
        
        # Show sample content
        if data['text_content']['paragraphs']:
            print(f"\nSample paragraph: {data['text_content']['paragraphs'][0][:200]}...")
        
        if data['images']:
            print(f"\nSample image: {data['images'][0]['url']}")

if __name__ == "__main__":
    print("Web Scraping Agent Examples")
    print("=" * 50)
    
    # Run examples
    print("\n1. Scraping single URL:")
    scrape_single_url()
    
    print("\n2. Analyzing scraped data:")
    analyze_scraped_data()
