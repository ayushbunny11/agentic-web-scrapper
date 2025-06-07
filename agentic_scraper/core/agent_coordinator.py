
"""
Agent Coordinator - Orchestrates web scraping and AI analysis
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from scraper_engine import WebScrapingEngine
from ai_agent import AIScrapingAgent
from config import DEFAULT_CONFIG, AI_CONFIG, AGENT_DECISIONS

logger = logging.getLogger(__name__)

class AgenticWebScrapingCoordinator:
    """
    Main coordinator that orchestrates web scraping and AI analysis
    """
    
    def __init__(self, scraper_config: Dict[str, Any] = None, ai_config: Dict[str, Any] = None):
        self.scraper_config = scraper_config or DEFAULT_CONFIG
        self.ai_config = ai_config or AI_CONFIG
        
        # Initialize engines
        self.scraper_engine = WebScrapingEngine(self.scraper_config)
        self.ai_agent = AIScrapingAgent(self.ai_config)
        
        logger.info("Agentic Web Scraping Coordinator initialized")
    
    async def process_url(self, url: str, enable_ai: bool = True) -> Dict[str, Any]:
        """
        Process a single URL with scraping and AI analysis
        
        Args:
            url: URL to process
            enable_ai: Whether to enable AI analysis
            
        Returns:
            Complete analysis results
        """
        logger.info(f"Processing URL: {url}")
        
        # Step 1: Scrape the website
        scraped_data = self.scraper_engine.scrape_website(url)
        
        if "error" in scraped_data:
            logger.error(f"Scraping failed for {url}: {scraped_data['error']}")
            return scraped_data
        
        # Step 2: AI Analysis (if enabled and configured)
        if enable_ai and self.ai_agent.is_ai_enabled():
            try:
                ai_analysis = await self.ai_agent.analyze_content(scraped_data)
                scraped_data["ai_analysis"] = ai_analysis
                logger.info(f"AI analysis completed for {url}")
            except Exception as e:
                logger.error(f"AI analysis failed for {url}: {str(e)}")
                scraped_data["ai_analysis"] = {"error": f"AI analysis failed: {str(e)}"}
        
        # Step 3: Agent Decision Making
        agent_metadata = self._generate_agent_metadata(scraped_data)
        scraped_data["agent_metadata"] = agent_metadata
        
        return scraped_data
    
    async def process_multiple_urls(self, urls: List[str], enable_ai: bool = True, save_results: bool = True) -> List[Dict[str, Any]]:
        """
        Process multiple URLs concurrently
        
        Args:
            urls: List of URLs to process
            enable_ai: Whether to enable AI analysis
            save_results: Whether to save results to files
            
        Returns:
            List of analysis results
        """
        logger.info(f"Processing {len(urls)} URLs")
        
        results = []
        
        for url in urls:
            try:
                result = await self.process_url(url, enable_ai)
                results.append(result)
                
                # Save individual results if requested
                if save_results and "error" not in result:
                    filename = self.scraper_engine.save_to_json(result)
                    result["saved_to_file"] = filename
                
                # Respectful delay between requests
                await asyncio.sleep(self.scraper_config.get("delay_between_requests", 1.0))
                
            except Exception as e:
                logger.error(f"Failed to process {url}: {str(e)}")
                results.append({"url": url, "error": str(e)})
        
        # Generate batch summary
        batch_summary = self._generate_batch_summary(results)
        
        return {
            "results": results,
            "batch_summary": batch_summary,
            "processed_count": len(results),
            "success_count": len([r for r in results if "error" not in r])
        }
    
    def _generate_agent_metadata(self, scraped_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate metadata about agent processing"""
        metadata = {
            "processing_timestamp": scraped_data.get("scraped_at"),
            "data_quality_score": self._calculate_data_quality(scraped_data),
            "content_richness": self._assess_content_richness(scraped_data),
            "extraction_completeness": self._check_extraction_completeness(scraped_data),
            "ai_analysis_available": "ai_analysis" in scraped_data and "error" not in scraped_data.get("ai_analysis", {}),
        }
        
        return metadata
    
    def _calculate_data_quality(self, data: Dict[str, Any]) -> float:
        """Calculate overall data quality score"""
        score = 0.0
        max_score = 10.0
        
        # Title presence
        if data.get("title"):
            score += 1.0
        
        # Content presence and length
        text_content = data.get("text_content", {})
        full_text = text_content.get("full_text", "")
        if len(full_text) > 100:
            score += 2.0
        elif len(full_text) > 50:
            score += 1.0
        
        # Structured content
        if text_content.get("headings"):
            score += 1.0
        if text_content.get("paragraphs"):
            score += 1.0
        
        # Media content
        if data.get("images"):
            score += 1.5
        if data.get("videos"):
            score += 1.5
        
        # Links
        if data.get("links"):
            score += 1.0
        
        # Metadata
        if data.get("metadata"):
            score += 1.0
        
        return round((score / max_score) * 10, 2)
    
    def _assess_content_richness(self, data: Dict[str, Any]) -> str:
        """Assess content richness level"""
        text_length = len(data.get("text_content", {}).get("full_text", ""))
        image_count = len(data.get("images", []))
        video_count = len(data.get("videos", []))
        
        score = 0
        if text_length > 1000:
            score += 3
        elif text_length > 500:
            score += 2
        elif text_length > 100:
            score += 1
        
        if image_count > 5:
            score += 2
        elif image_count > 0:
            score += 1
        
        if video_count > 0:
            score += 2
        
        if score >= 6:
            return "Very Rich"
        elif score >= 4:
            return "Rich"
        elif score >= 2:
            return "Moderate"
        else:
            return "Minimal"
    
    def _check_extraction_completeness(self, data: Dict[str, Any]) -> Dict[str, bool]:
        """Check completeness of data extraction"""
        return {
            "title_extracted": bool(data.get("title")),
            "text_extracted": bool(data.get("text_content", {}).get("full_text")),
            "images_extracted": bool(data.get("images")),
            "videos_extracted": bool(data.get("videos")),
            "links_extracted": bool(data.get("links")),
            "metadata_extracted": bool(data.get("metadata"))
        }
    
    def _generate_batch_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary for batch processing"""
        successful_results = [r for r in results if "error" not in r]
        
        if not successful_results:
            return {"summary": "No successful extractions"}
        
        total_images = sum(len(r.get("images", [])) for r in successful_results)
        total_videos = sum(len(r.get("videos", [])) for r in successful_results)
        total_links = sum(len(r.get("links", [])) for r in successful_results)
        
        avg_quality = sum(r.get("agent_metadata", {}).get("data_quality_score", 0) for r in successful_results) / len(successful_results)
        
        return {
            "total_processed": len(results),
            "successful_extractions": len(successful_results),
            "total_images_found": total_images,
            "total_videos_found": total_videos,
            "total_links_found": total_links,
            "average_quality_score": round(avg_quality, 2),
            "ai_analysis_performed": len([r for r in successful_results if r.get("agent_metadata", {}).get("ai_analysis_available", False)])
        }
    
    def get_configuration(self) -> Dict[str, Any]:
        """Get current configuration"""
        return {
            "scraper_config": self.scraper_config,
            "ai_config": self.ai_config,
            "ai_enabled": self.ai_agent.is_ai_enabled()
        }
    
    def update_configuration(self, scraper_config: Dict[str, Any] = None, ai_config: Dict[str, Any] = None):
        """Update configuration dynamically"""
        if scraper_config:
            self.scraper_config.update(scraper_config)
            self.scraper_engine = WebScrapingEngine(self.scraper_config)
            logger.info("Scraper configuration updated")
        
        if ai_config:
            self.ai_config.update(ai_config)
            self.ai_agent = AIScrapingAgent(self.ai_config)
            logger.info("AI configuration updated")
