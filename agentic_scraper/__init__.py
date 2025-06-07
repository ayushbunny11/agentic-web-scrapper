
"""
Agentic Web Scraper Framework
AI-Powered Web Scraping with Decision Making Capabilities
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .core.scraper_engine import WebScrapingEngine
from .core.ai_agent import AIScrapingAgent
from .core.agent_coordinator import AgenticWebScrapingCoordinator
from .core.config_manager import ConfigManager
from .plugins.base_plugin import BasePlugin

__all__ = [
    "WebScrapingEngine",
    "AIScrapingAgent", 
    "AgenticWebScrapingCoordinator",
    "ConfigManager",
    "BasePlugin"
]
