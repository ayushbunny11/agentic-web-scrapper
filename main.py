"""
Main entry point for the AI-Powered Agentic Web Scraping Framework
"""

import asyncio
import logging
import os
from dotenv import load_dotenv
from agent_coordinator import AgenticWebScrapingCoordinator
from config import DEFAULT_CONFIG, AI_CONFIG

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Main execution function"""
    logger.info("Starting AI-Powered Agentic Web Scraping Framework")

    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    logger.info(api_key)
    if not api_key:
        logger.warning("OPENAI_API_KEY not found. AI features will be disabled.")
        logger.warning("To enable AI features, add your OpenAI API key to the Secrets tab.")

    # Initialize the coordinator
    coordinator = AgenticWebScrapingCoordinator()

    # Example URLs to scrape
    test_urls = [
        "https://medium.com/age-of-awareness/they-know-a-collapse-is-coming-39a53e2ecd80"
    ]

    logger.info(f"Processing {len(test_urls)} URLs with AI analysis")

    # Process URLs with AI analysis
    results = await coordinator.process_multiple_urls(
        urls=test_urls,
        enable_ai=bool(api_key),  # Enable AI only if API key is available
        save_results=True
    )

    # Display results summary
    print("\n" + "="*80)
    print("AGENTIC WEB SCRAPING RESULTS SUMMARY")
    print("="*80)

    batch_summary = results["batch_summary"]
    print(f"Total URLs processed: {results['processed_count']}")
    print(f"Successful extractions: {results['success_count']}")
    print(f"Total images found: {batch_summary['total_images_found']}")
    print(f"Total videos found: {batch_summary['total_videos_found']}")
    print(f"Total links found: {batch_summary['total_links_found']}")
    print(f"Average quality score: {batch_summary['average_quality_score']}/10")

    if api_key:
        print(f"AI analyses performed: {batch_summary['ai_analysis_performed']}")
    else:
        print("AI analysis: DISABLED (no API key)")

    # Display individual results
    print("\n" + "-"*50)
    print("INDIVIDUAL RESULTS:")
    print("-"*50)

    for i, result in enumerate(results["results"], 1):
        if "error" not in result:
            print(f"\n{i}. {result['url']}")
            print(f"   Title: {result.get('title', 'N/A')}")
            print(f"   Quality Score: {result.get('agent_metadata', {}).get('data_quality_score', 'N/A')}/10")
            print(f"   Content Richness: {result.get('agent_metadata', {}).get('content_richness', 'N/A')}")

            if result.get('agent_metadata', {}).get('ai_analysis_available'):
                ai_analysis = result.get('ai_analysis', {})
                if 'content_analysis' in ai_analysis:
                    print(f"   AI Summary Available: Yes")
                if 'agent_decisions' in ai_analysis:
                    priority_score = ai_analysis['agent_decisions'].get('priority_score', 'N/A')
                    print(f"   AI Priority Score: {priority_score}/10")

            if result.get('saved_to_file'):
                print(f"   Saved to: {result['saved_to_file']}")
        else:
            print(f"\n{i}. ERROR - {result['url']}: {result['error']}")

    print("\n" + "="*80)
    print("Framework execution completed!")

    # Show configuration info
    config_info = coordinator.get_configuration()
    print(f"\nAI Features Enabled: {config_info['ai_enabled']}")
    print("To modify configurations, edit config.py or use environment variables.")

if __name__ == "__main__":
    asyncio.run(main())