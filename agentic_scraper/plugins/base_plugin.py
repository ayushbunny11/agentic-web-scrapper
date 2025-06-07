
"""
Base Plugin Class for Agentic Web Scraper Framework
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class BasePlugin(ABC):
    """Base class for all plugins"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.name = self.__class__.__name__
        self.version = "1.0.0"
        self.description = "Base plugin"
        self.enabled = True
    
    @abstractmethod
    def process_data(self, scraped_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process scraped data"""
        pass
    
    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """Get plugin metadata"""
        pass
    
    def validate_config(self) -> bool:
        """Validate plugin configuration"""
        return True
    
    def initialize(self) -> bool:
        """Initialize plugin"""
        try:
            if not self.validate_config():
                logger.error(f"Plugin {self.name} configuration validation failed")
                return False
            
            logger.info(f"Plugin {self.name} initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize plugin {self.name}: {e}")
            return False
    
    def finalize(self):
        """Cleanup plugin resources"""
        pass

class AnalyticsPlugin(BasePlugin):
    """Plugin for web analytics extraction"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = "AnalyticsPlugin"
        self.description = "Extract web analytics and tracking information"
    
    def process_data(self, scraped_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract analytics data"""
        analytics_data = {
            "google_analytics": self._extract_ga_tracking(scraped_data),
            "facebook_pixel": self._extract_fb_pixel(scraped_data),
            "tracking_scripts": self._extract_tracking_scripts(scraped_data)
        }
        
        scraped_data["analytics"] = analytics_data
        return scraped_data
    
    def _extract_ga_tracking(self, data: Dict[str, Any]) -> List[str]:
        """Extract Google Analytics tracking codes"""
        # Implementation for GA extraction
        return []
    
    def _extract_fb_pixel(self, data: Dict[str, Any]) -> List[str]:
        """Extract Facebook Pixel codes"""
        # Implementation for FB pixel extraction
        return []
    
    def _extract_tracking_scripts(self, data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extract other tracking scripts"""
        # Implementation for general tracking script extraction
        return []
    
    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "capabilities": ["google_analytics", "facebook_pixel", "tracking_scripts"]
        }

class SEOPlugin(BasePlugin):
    """Plugin for SEO analysis"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = "SEOPlugin"
        self.description = "Analyze SEO elements and provide recommendations"
    
    def process_data(self, scraped_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze SEO elements"""
        seo_data = {
            "title_analysis": self._analyze_title(scraped_data),
            "meta_description": self._analyze_meta_description(scraped_data),
            "heading_structure": self._analyze_headings(scraped_data),
            "image_alt_texts": self._analyze_image_alts(scraped_data),
            "seo_score": self._calculate_seo_score(scraped_data)
        }
        
        scraped_data["seo_analysis"] = seo_data
        return scraped_data
    
    def _analyze_title(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze page title for SEO"""
        title = data.get("title", "")
        return {
            "length": len(title),
            "optimal_length": 50 <= len(title) <= 60,
            "contains_keywords": True  # Simplified
        }
    
    def _analyze_meta_description(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze meta description"""
        metadata = data.get("metadata", {})
        description = metadata.get("description", "")
        return {
            "length": len(description),
            "optimal_length": 150 <= len(description) <= 160,
            "present": bool(description)
        }
    
    def _analyze_headings(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze heading structure"""
        headings = data.get("text_content", {}).get("headings", {})
        return {
            "h1_count": len(headings.get("h1", [])),
            "has_single_h1": len(headings.get("h1", [])) == 1,
            "heading_hierarchy": self._check_heading_hierarchy(headings)
        }
    
    def _analyze_image_alts(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze image alt texts"""
        images = data.get("images", [])
        total_images = len(images)
        images_with_alt = len([img for img in images if img.get("alt")])
        
        return {
            "total_images": total_images,
            "images_with_alt": images_with_alt,
            "alt_coverage": images_with_alt / total_images if total_images > 0 else 0
        }
    
    def _check_heading_hierarchy(self, headings: Dict[str, List]) -> bool:
        """Check if heading hierarchy is proper"""
        # Simplified hierarchy check
        return len(headings.get("h1", [])) == 1
    
    def _calculate_seo_score(self, data: Dict[str, Any]) -> float:
        """Calculate overall SEO score"""
        # Simplified SEO scoring
        score = 0.0
        
        # Title check
        title = data.get("title", "")
        if 50 <= len(title) <= 60:
            score += 20
        
        # Meta description check
        metadata = data.get("metadata", {})
        description = metadata.get("description", "")
        if description and 150 <= len(description) <= 160:
            score += 20
        
        # Heading structure
        headings = data.get("text_content", {}).get("headings", {})
        if len(headings.get("h1", [])) == 1:
            score += 20
        
        # Image alt texts
        images = data.get("images", [])
        if images:
            images_with_alt = len([img for img in images if img.get("alt")])
            alt_ratio = images_with_alt / len(images)
            score += alt_ratio * 20
        
        # Content length
        content_length = len(data.get("text_content", {}).get("full_text", ""))
        if content_length > 300:
            score += 20
        
        return round(score, 2)
    
    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "capabilities": ["title_analysis", "meta_analysis", "heading_structure", "seo_scoring"]
        }
