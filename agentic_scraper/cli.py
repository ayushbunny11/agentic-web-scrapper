
"""
Command Line Interface for Agentic Web Scraper Framework
"""

import click
import asyncio
import json
import os
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from typing import List

from .core.agent_coordinator import AgenticWebScrapingCoordinator
from .core.config_manager import ConfigManager
from .utils.logger import setup_logging

console = Console()

@click.group()
@click.version_option(version="1.0.0")
@click.option('--config', '-c', help='Configuration file path')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.pass_context
def main(ctx, config, verbose):
    """Agentic Web Scraper Framework - AI-Powered Web Scraping"""
    ctx.ensure_object(dict)
    ctx.obj['config_path'] = config
    ctx.obj['verbose'] = verbose
    
    # Setup logging
    setup_logging(verbose)

@main.command()
@click.argument('urls', nargs=-1, required=True)
@click.option('--output', '-o', default='scraped_data', help='Output directory')
@click.option('--ai/--no-ai', default=True, help='Enable/disable AI analysis')
@click.option('--format', 'output_format', default='json', type=click.Choice(['json', 'csv', 'xml']))
@click.option('--config-override', multiple=True, help='Override config values (key=value)')
@click.pass_context
def scrape(ctx, urls, output, ai, output_format, config_override):
    """Scrape websites with AI analysis"""
    
    # Load configuration
    config_manager = ConfigManager(ctx.obj.get('config_path'))
    
    # Apply config overrides
    for override in config_override:
        key, value = override.split('=', 1)
        config_manager.set_config(key, value)
    
    # Initialize coordinator
    coordinator = AgenticWebScrapingCoordinator(
        scraper_config=config_manager.get_scraper_config(),
        ai_config=config_manager.get_ai_config()
    )
    
    console.print(f"[bold green]Starting scraping of {len(urls)} URLs[/bold green]")
    
    # Create output directory
    output_path = Path(output)
    output_path.mkdir(exist_ok=True)
    
    # Run scraping
    asyncio.run(_scrape_urls(coordinator, list(urls), output_path, ai, output_format))

async def _scrape_urls(coordinator, urls, output_path, enable_ai, output_format):
    """Execute scraping with progress tracking"""
    
    with Progress() as progress:
        task = progress.add_task("[green]Scraping...", total=len(urls))
        
        results = await coordinator.process_multiple_urls(
            urls=urls,
            enable_ai=enable_ai,
            save_results=False  # We'll handle saving
        )
        
        progress.update(task, completed=len(urls))
    
    # Save results
    _save_results(results, output_path, output_format)
    
    # Display summary
    _display_summary(results)

def _save_results(results, output_path, output_format):
    """Save results in specified format"""
    timestamp = int(time.time())
    
    if output_format == 'json':
        filename = output_path / f"scraping_results_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    
    console.print(f"[green]Results saved to: {filename}[/green]")

def _display_summary(results):
    """Display scraping results summary"""
    table = Table(title="Scraping Results Summary")
    
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    
    batch_summary = results["batch_summary"]
    table.add_row("Total URLs", str(results["processed_count"]))
    table.add_row("Successful", str(results["success_count"]))
    table.add_row("Images Found", str(batch_summary["total_images_found"]))
    table.add_row("Videos Found", str(batch_summary["total_videos_found"]))
    table.add_row("Average Quality", f"{batch_summary['average_quality_score']}/10")
    
    console.print(table)

@main.command()
@click.option('--template', default='default', help='Configuration template to use')
def init(template):
    """Initialize a new scraping project"""
    config_manager = ConfigManager()
    config_manager.create_project_config(template)
    console.print("[green]Project initialized successfully![/green]")

@main.command()
def plugins():
    """List available plugins"""
    from .plugins.plugin_manager import PluginManager
    
    plugin_manager = PluginManager()
    available_plugins = plugin_manager.list_plugins()
    
    table = Table(title="Available Plugins")
    table.add_column("Name", style="cyan")
    table.add_column("Version", style="magenta")
    table.add_column("Description", style="green")
    
    for plugin in available_plugins:
        table.add_row(plugin.name, plugin.version, plugin.description)
    
    console.print(table)

@main.command()
@click.argument('url')
@click.option('--output', '-o', help='Output file path')
def analyze(url, output):
    """Analyze a single URL in detail"""
    config_manager = ConfigManager()
    coordinator = AgenticWebScrapingCoordinator(
        scraper_config=config_manager.get_scraper_config(),
        ai_config=config_manager.get_ai_config()
    )
    
    console.print(f"[bold blue]Analyzing: {url}[/bold blue]")
    
    result = asyncio.run(coordinator.process_url(url, enable_ai=True))
    
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        console.print(f"[green]Analysis saved to: {output}[/green]")
    else:
        console.print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
