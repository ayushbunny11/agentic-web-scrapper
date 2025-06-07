
"""
AI Agent for Web Scraping Analysis and Decision Making
"""

import openai
import json
import logging
from typing import Dict, List, Any, Optional
from config import AI_CONFIG, AGENT_DECISIONS, AI_PROMPTS

logger = logging.getLogger(__name__)

class AIScrapingAgent:
    """AI-powered agent for web scraping analysis and decision making"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or AI_CONFIG
        self.client = None
        
        if self.config.get("openai_api_key"):
            self.client = openai.OpenAI(api_key=self.config["openai_api_key"])
        else:
            logger.warning("OpenAI API key not provided. AI features will be disabled.")
    
    def is_ai_enabled(self) -> bool:
        """Check if AI features are enabled and configured"""
        return self.client is not None and self.config.get("enable_ai_analysis", False)
    
    async def analyze_content(self, scraped_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze scraped content using AI"""
        if not self.is_ai_enabled():
            return {"ai_analysis": "AI analysis disabled"}
        
        analysis_results = {}
        
        try:
            # Content Analysis
            if self.config.get("enable_content_summarization", True):
                content_analysis = await self._analyze_text_content(scraped_data.get("text_content", {}))
                analysis_results["content_analysis"] = content_analysis
            
            # Image Analysis
            if (self.config.get("enable_image_analysis", True) and 
                len(scraped_data.get("images", [])) >= AGENT_DECISIONS["image_analysis_threshold"]):
                image_analysis = await self._analyze_images(scraped_data.get("images", []))
                analysis_results["image_analysis"] = image_analysis
            
            # Video Analysis
            if (self.config.get("enable_video_analysis", True) and 
                len(scraped_data.get("videos", [])) >= AGENT_DECISIONS["video_analysis_threshold"]):
                video_analysis = await self._analyze_videos(scraped_data.get("videos", []))
                analysis_results["video_analysis"] = video_analysis
            
            # Decision Making
            if self.config.get("enable_decision_making", True):
                decisions = await self._make_decisions(scraped_data, analysis_results)
                analysis_results["agent_decisions"] = decisions
            
            # Generate Overall Score
            analysis_results["overall_score"] = self._calculate_overall_score(analysis_results)
            
        except Exception as e:
            logger.error(f"AI analysis failed: {str(e)}")
            analysis_results["error"] = f"AI analysis failed: {str(e)}"
        
        return analysis_results
    
    async def _analyze_text_content(self, text_content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze text content using AI"""
        full_text = text_content.get("full_text", "")
        
        if len(full_text) < 100:
            return {"summary": "Content too short for analysis"}
        
        # Truncate if too long
        content_sample = full_text[:3000] if len(full_text) > 3000 else full_text
        
        prompt = AI_PROMPTS["content_analysis"].format(content=content_sample)
        
        try:
            response = self.client.chat.completions.create(
                model=self.config["model"],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.config["max_tokens"],
                temperature=self.config["temperature"]
            )
            
            analysis = response.choices[0].message.content
            
            return {
                "summary": analysis,
                "word_count": len(full_text.split()),
                "character_count": len(full_text),
                "readability_score": self._calculate_readability_score(full_text)
            }
            
        except Exception as e:
            logger.error(f"Text analysis failed: {str(e)}")
            return {"error": f"Text analysis failed: {str(e)}"}
    
    async def _analyze_images(self, images: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze images using AI"""
        if not images:
            return {"analysis": "No images to analyze"}
        
        # Create summary of images for analysis
        image_summary = []
        for img in images[:10]:  # Analyze first 10 images
            image_summary.append({
                "url": img.get("url", ""),
                "alt_text": img.get("alt", ""),
                "title": img.get("title", "")
            })
        
        prompt = AI_PROMPTS["image_analysis"].format(images=json.dumps(image_summary, indent=2))
        
        try:
            response = self.client.chat.completions.create(
                model=self.config["model"],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.config["max_tokens"],
                temperature=self.config["temperature"]
            )
            
            return {
                "analysis": response.choices[0].message.content,
                "total_images": len(images),
                "analyzed_images": len(image_summary)
            }
            
        except Exception as e:
            logger.error(f"Image analysis failed: {str(e)}")
            return {"error": f"Image analysis failed: {str(e)}"}
    
    async def _analyze_videos(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze videos using AI"""
        if not videos:
            return {"analysis": "No videos to analyze"}
        
        video_summary = []
        for video in videos:
            video_summary.append({
                "url": video.get("url", ""),
                "type": video.get("type", ""),
                "platform": self._identify_video_platform(video.get("url", ""))
            })
        
        prompt = AI_PROMPTS["video_analysis"].format(videos=json.dumps(video_summary, indent=2))
        
        try:
            response = self.client.chat.completions.create(
                model=self.config["model"],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.config["max_tokens"],
                temperature=self.config["temperature"]
            )
            
            return {
                "analysis": response.choices[0].message.content,
                "total_videos": len(videos),
                "platforms": list(set([v["platform"] for v in video_summary]))
            }
            
        except Exception as e:
            logger.error(f"Video analysis failed: {str(e)}")
            return {"error": f"Video analysis failed: {str(e)}"}
    
    async def _make_decisions(self, scraped_data: Dict[str, Any], analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Make intelligent decisions about the scraped content"""
        data_summary = {
            "url": scraped_data.get("url", ""),
            "title": scraped_data.get("title", ""),
            "content_length": len(scraped_data.get("text_content", {}).get("full_text", "")),
            "images_count": len(scraped_data.get("images", [])),
            "videos_count": len(scraped_data.get("videos", [])),
            "links_count": len(scraped_data.get("links", [])),
            "has_analysis": bool(analysis_results)
        }
        
        prompt = AI_PROMPTS["decision_making"].format(data_summary=json.dumps(data_summary, indent=2))
        
        try:
            response = self.client.chat.completions.create(
                model=self.config["model"],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.config["max_tokens"],
                temperature=self.config["temperature"]
            )
            
            return {
                "decisions": response.choices[0].message.content,
                "priority_score": self._calculate_priority_score(data_summary),
                "recommended_actions": self._generate_recommendations(data_summary)
            }
            
        except Exception as e:
            logger.error(f"Decision making failed: {str(e)}")
            return {"error": f"Decision making failed: {str(e)}"}
    
    def _calculate_readability_score(self, text: str) -> float:
        """Calculate a simple readability score"""
        if not text:
            return 0.0
        
        words = text.split()
        sentences = text.count('.') + text.count('!') + text.count('?')
        
        if sentences == 0:
            return 0.0
        
        avg_sentence_length = len(words) / sentences
        
        # Simple readability score (lower is better)
        score = max(0, 10 - (avg_sentence_length / 10))
        return round(score, 2)
    
    def _identify_video_platform(self, url: str) -> str:
        """Identify video platform from URL"""
        url_lower = url.lower()
        for platform in ["youtube", "vimeo", "dailymotion", "twitch"]:
            if platform in url_lower:
                return platform
        return "unknown"
    
    def _calculate_priority_score(self, data_summary: Dict[str, Any]) -> float:
        """Calculate priority score for content"""
        score = 0.0
        
        # Content length scoring
        content_length = data_summary.get("content_length", 0)
        if content_length > 1000:
            score += 3.0
        elif content_length > 500:
            score += 2.0
        elif content_length > 100:
            score += 1.0
        
        # Media content scoring
        if data_summary.get("images_count", 0) > 5:
            score += 2.0
        if data_summary.get("videos_count", 0) > 0:
            score += 3.0
        
        # Links scoring
        if data_summary.get("links_count", 0) > 10:
            score += 1.0
        
        return min(10.0, score)
    
    def _generate_recommendations(self, data_summary: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on data"""
        recommendations = []
        
        if data_summary.get("content_length", 0) > 2000:
            recommendations.append("Consider creating a summary for lengthy content")
        
        if data_summary.get("images_count", 0) > 10:
            recommendations.append("High image count - consider image optimization analysis")
        
        if data_summary.get("videos_count", 0) > 0:
            recommendations.append("Video content detected - analyze for engagement potential")
        
        if data_summary.get("links_count", 0) > 20:
            recommendations.append("High link density - consider link analysis for SEO insights")
        
        return recommendations
    
    def _calculate_overall_score(self, analysis_results: Dict[str, Any]) -> float:
        """Calculate overall content quality score"""
        scores = []
        
        # Content analysis score
        if "content_analysis" in analysis_results:
            readability = analysis_results["content_analysis"].get("readability_score", 0)
            scores.append(readability)
        
        # Priority score
        if "agent_decisions" in analysis_results:
            priority = analysis_results["agent_decisions"].get("priority_score", 0)
            scores.append(priority)
        
        return round(sum(scores) / len(scores) if scores else 0.0, 2)
