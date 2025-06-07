
# Agentic Web Scraper Framework

A powerful, AI-driven web scraping framework that combines intelligent content extraction with advanced decision-making capabilities. Built for developers who need more than just basic web scraping.

## 🚀 Features

- **AI-Powered Analysis**: Leverages OpenAI's GPT models for content summarization and decision making
- **Intelligent Content Extraction**: Automatically extracts text, images, videos, links, and metadata
- **Plugin Architecture**: Extensible framework with built-in plugins for analytics and SEO analysis
- **Command Line Interface**: Professional CLI with rich output formatting
- **Configuration Management**: Flexible configuration system with environment variable support
- **Agentic Decision Making**: AI agent makes intelligent decisions about content prioritization
- **Multiple Output Formats**: JSON, CSV, and XML export options
- **Async Processing**: High-performance asynchronous processing for multiple URLs

## 📦 Installation

### From Source (Development)

```bash
# Clone the repository
git clone https://github.com/yourusername/agentic-web-scraper.git
cd agentic-web-scraper

# Install in development mode
pip install -e .
```

### Via pip (Production)

```bash
pip install agentic-web-scraper
```

## 🔧 Quick Start

### 1. Initialize a Project

```bash
agentic-scraper init --template default
```

### 2. Set up API Key (Optional but Recommended)

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

### 3. Scrape a Website

```bash
# Basic scraping
agentic-scraper scrape https://example.com

# With AI analysis
agentic-scraper scrape https://example.com --ai

# Multiple URLs
agentic-scraper scrape https://example.com https://another-site.com --output ./results
```

### 4. Analyze Content

```bash
# Detailed analysis of a single URL
agentic-scraper analyze https://example.com --output analysis.json
```

## 🎯 Usage Examples

### Python API

```python
from agentic_scraper import AgenticWebScrapingCoordinator
import asyncio

async def main():
    # Initialize coordinator
    coordinator = AgenticWebScrapingCoordinator()
    
    # Scrape with AI analysis
    result = await coordinator.process_url(
        "https://example.com", 
        enable_ai=True
    )
    
    print(f"Quality Score: {result['agent_metadata']['data_quality_score']}")
    print(f"AI Summary: {result.get('ai_analysis', {}).get('content_analysis', {}).get('summary', 'N/A')}")

# Run the async function
asyncio.run(main())
```

### Configuration File

Create `agentic_scraper_config.yaml`:

```yaml
scraper:
  delay_between_requests: 2.0
  extract_images: true
  extract_videos: true
  user_agent: "Custom Bot 1.0"

ai:
  model: "gpt-4"
  temperature: 0.3
  enable_ai_analysis: true

output:
  format: "json"
  save_individual_files: true
  output_directory: "./scraped_data"

plugins:
  enabled: ["analytics", "seo"]
```

### Environment Variables

```bash
export OPENAI_API_KEY="your-api-key"
export SCRAPER_DELAY="1.5"
export AI_MODEL="gpt-4"
export OUTPUT_FORMAT="json"
```

## 🔌 Plugin System

### Available Plugins

- **Analytics Plugin**: Extract Google Analytics, Facebook Pixel, and other tracking codes
- **SEO Plugin**: Analyze SEO elements and provide optimization recommendations

### Creating Custom Plugins

```python
from agentic_scraper.plugins.base_plugin import BasePlugin

class CustomPlugin(BasePlugin):
    def __init__(self, config=None):
        super().__init__(config)
        self.name = "CustomPlugin"
        self.description = "My custom plugin"
    
    def process_data(self, scraped_data):
        # Your custom processing logic
        scraped_data["custom_analysis"] = {"processed": True}
        return scraped_data
    
    def get_metadata(self):
        return {
            "name": self.name,
            "version": "1.0.0",
            "description": self.description
        }
```

## 📊 Output Examples

### Basic Scraping Output

```json
{
  "url": "https://example.com",
  "title": "Example Domain",
  "text_content": {
    "headings": {"h1": ["Example Domain"]},
    "paragraphs": ["This domain is for use in illustrative examples..."],
    "full_text": "Example Domain This domain is for use..."
  },
  "images": [
    {
      "url": "https://example.com/image.jpg",
      "alt": "Example image",
      "title": "Example"
    }
  ],
  "agent_metadata": {
    "data_quality_score": 8.5,
    "content_richness": "Rich",
    "ai_analysis_available": true
  }
}
```

### AI Analysis Output

```json
{
  "ai_analysis": {
    "content_analysis": {
      "summary": "This is a sample website demonstrating...",
      "main_topics": ["web development", "examples"],
      "content_quality_score": 7.8,
      "target_audience": "developers"
    },
    "agent_decisions": {
      "priority_score": 8.5,
      "recommended_actions": [
        "Consider creating a summary for lengthy content",
        "High quality content - suitable for archiving"
      ]
    }
  }
}
```

## ⚙️ Configuration Options

### Scraper Settings

- `delay_between_requests`: Delay between HTTP requests
- `request_timeout`: HTTP request timeout
- `max_retries`: Maximum retry attempts
- `extract_*`: Control what content types to extract
- `user_agent`: Custom user agent string

### AI Settings

- `model`: OpenAI model to use (gpt-4, gpt-3.5-turbo, etc.)
- `temperature`: AI creativity level (0.0-1.0)
- `max_tokens`: Maximum tokens per AI request
- `enable_*_analysis`: Control AI analysis features

### Output Settings

- `format`: Output format (json, csv, xml)
- `save_individual_files`: Save each URL result separately
- `output_directory`: Directory for output files
- `compress_output`: Compress output files

## 🚀 Deployment

### Deploy on Replit

This framework is optimized for Replit deployment:

1. Fork the repository on Replit
2. Set your `OPENAI_API_KEY` in Secrets
3. Run the scraper using the integrated terminal or Run button

### Production Deployment

```bash
# Install production dependencies
pip install agentic-web-scraper[production]

# Run with production settings
agentic-scraper scrape --config production_config.yaml https://target-site.com
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Commit your changes: `git commit -am 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🛠️ Advanced Usage

### Custom Configuration

```python
from agentic_scraper.core.config_manager import ConfigManager

# Create custom configuration
config_manager = ConfigManager()
config_manager.set_config("scraper.delay_between_requests", 2.0)
config_manager.set_config("ai.model", "gpt-4")

# Save configuration
config_manager.save_config("my_config.yaml")
```

### Batch Processing

```python
import asyncio
from agentic_scraper import AgenticWebScrapingCoordinator

async def batch_scrape():
    urls = [
        "https://site1.com",
        "https://site2.com",
        "https://site3.com"
    ]
    
    coordinator = AgenticWebScrapingCoordinator()
    results = await coordinator.process_multiple_urls(urls)
    
    print(f"Processed {results['processed_count']} URLs")
    print(f"Success rate: {results['success_count']}/{results['processed_count']}")

asyncio.run(batch_scrape())
```

## 📈 Performance Tips

1. **Adjust delays**: Reduce `delay_between_requests` for faster scraping (be respectful)
2. **Disable unused features**: Turn off AI analysis or specific content extraction for speed
3. **Use async processing**: Process multiple URLs concurrently
4. **Configure timeouts**: Set appropriate `request_timeout` values
5. **Enable compression**: Use `compress_output` for large datasets

## 🔍 Troubleshooting

### Common Issues

1. **OpenAI API errors**: Check your API key and quota
2. **Timeout errors**: Increase `request_timeout` setting
3. **Memory issues**: Process URLs in smaller batches
4. **SSL errors**: Set `verify_ssl: false` in config (not recommended for production)

### Getting Help

- Check the [documentation](https://github.com/yourusername/agentic-web-scraper/wiki)
- Open an [issue](https://github.com/yourusername/agentic-web-scraper/issues)
- Join our [Discord community](https://discord.gg/your-server)

---

**Made with ❤️ for the developer community**
