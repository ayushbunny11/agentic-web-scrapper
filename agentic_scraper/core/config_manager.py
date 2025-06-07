
"""
Configuration Manager for the Agentic Web Scraper Framework
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ConfigManager:
    """Centralized configuration management"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.config_data = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file or environment"""
        # Default configuration
        self.config_data = self._get_default_config()
        
        # Load from file if specified
        if self.config_path and os.path.exists(self.config_path):
            self._load_from_file(self.config_path)
        
        # Override with environment variables
        self._load_from_environment()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "scraper": {
                "delay_between_requests": 1.0,
                "request_timeout": 10,
                "max_retries": 3,
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "extract_text": True,
                "extract_images": True,
                "extract_videos": True,
                "extract_links": True,
                "extract_metadata": True,
                "clean_text": True,
                "resolve_relative_urls": True,
                "include_embedded_videos": True,
                "video_platforms": ["youtube", "vimeo", "dailymotion", "twitch"],
                "min_text_length": 10,
                "exclude_empty_content": True,
                "follow_redirects": True,
                "verify_ssl": True,
                "pretty_print": True
            },
            "ai": {
                "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
                "model": "gpt-4o-mini",
                "max_tokens": 1000,
                "temperature": 0.3,
                "enable_ai_analysis": True,
                "enable_content_summarization": True,
                "enable_image_analysis": True,
                "enable_video_analysis": True,
                "enable_decision_making": True
            },
            "agent": {
                "content_relevance_threshold": 0.7,
                "image_analysis_threshold": 5,
                "video_analysis_threshold": 3,
                "text_summary_length": 200,
                "max_links_to_analyze": 10,
                "priority_content_types": ["article", "news", "blog", "product"]
            },
            "output": {
                "format": "json",
                "save_individual_files": True,
                "output_directory": "scraped_data",
                "include_timestamp": True,
                "compress_output": False
            },
            "plugins": {
                "enabled": [],
                "plugin_directory": "plugins"
            }
        }
    
    def _load_from_file(self, config_path: str):
        """Load configuration from file (JSON or YAML)"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                    file_config = yaml.safe_load(f)
                else:
                    file_config = json.load(f)
            
            # Merge with existing config
            self._deep_merge(self.config_data, file_config)
            logger.info(f"Configuration loaded from {config_path}")
            
        except Exception as e:
            logger.warning(f"Failed to load config from {config_path}: {e}")
    
    def _load_from_environment(self):
        """Load configuration from environment variables"""
        env_mappings = {
            "OPENAI_API_KEY": ("ai", "openai_api_key"),
            "SCRAPER_DELAY": ("scraper", "delay_between_requests"),
            "SCRAPER_TIMEOUT": ("scraper", "request_timeout"),
            "AI_MODEL": ("ai", "model"),
            "OUTPUT_FORMAT": ("output", "format"),
            "OUTPUT_DIR": ("output", "output_directory")
        }
        
        for env_var, (section, key) in env_mappings.items():
            value = os.getenv(env_var)
            if value:
                # Convert string values to appropriate types
                if key in ["delay_between_requests", "request_timeout", "temperature"]:
                    value = float(value)
                elif key in ["max_retries", "max_tokens", "image_analysis_threshold"]:
                    value = int(value)
                elif key in ["extract_text", "enable_ai_analysis", "save_individual_files"]:
                    value = value.lower() in ('true', '1', 'yes', 'on')
                
                self.config_data[section][key] = value
    
    def _deep_merge(self, base: Dict[str, Any], update: Dict[str, Any]):
        """Deep merge two dictionaries"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def get_scraper_config(self) -> Dict[str, Any]:
        """Get scraper configuration"""
        return self.config_data.get("scraper", {})
    
    def get_ai_config(self) -> Dict[str, Any]:
        """Get AI configuration"""
        return self.config_data.get("ai", {})
    
    def get_agent_config(self) -> Dict[str, Any]:
        """Get agent configuration"""
        return self.config_data.get("agent", {})
    
    def get_output_config(self) -> Dict[str, Any]:
        """Get output configuration"""
        return self.config_data.get("output", {})
    
    def get_plugin_config(self) -> Dict[str, Any]:
        """Get plugin configuration"""
        return self.config_data.get("plugins", {})
    
    def get_config(self, section: str, key: str = None) -> Any:
        """Get specific configuration value"""
        if key:
            return self.config_data.get(section, {}).get(key)
        return self.config_data.get(section, {})
    
    def set_config(self, path: str, value: Any):
        """Set configuration value using dot notation"""
        keys = path.split('.')
        current = self.config_data
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    def save_config(self, output_path: str):
        """Save current configuration to file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            if output_path.endswith('.yaml') or output_path.endswith('.yml'):
                yaml.dump(self.config_data, f, default_flow_style=False, indent=2)
            else:
                json.dump(self.config_data, f, indent=2)
        
        logger.info(f"Configuration saved to {output_path}")
    
    def create_project_config(self, template: str = "default"):
        """Create a project configuration file"""
        config_templates = {
            "default": self._get_default_config(),
            "minimal": self._get_minimal_config(),
            "advanced": self._get_advanced_config()
        }
        
        template_config = config_templates.get(template, self._get_default_config())
        
        # Save to project directory
        config_path = Path("agentic_scraper_config.yaml")
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(template_config, f, default_flow_style=False, indent=2)
        
        logger.info(f"Project configuration created: {config_path}")
    
    def _get_minimal_config(self) -> Dict[str, Any]:
        """Get minimal configuration template"""
        return {
            "scraper": {
                "extract_text": True,
                "extract_images": False,
                "extract_videos": False,
                "extract_links": False
            },
            "ai": {
                "enable_ai_analysis": False
            },
            "output": {
                "format": "json",
                "save_individual_files": True
            }
        }
    
    def _get_advanced_config(self) -> Dict[str, Any]:
        """Get advanced configuration template"""
        config = self._get_default_config()
        config["scraper"]["include_analytics"] = True
        config["scraper"]["extract_performance_metrics"] = True
        config["ai"]["enable_advanced_analysis"] = True
        config["plugins"]["enabled"] = ["analytics", "performance", "seo"]
        return config
