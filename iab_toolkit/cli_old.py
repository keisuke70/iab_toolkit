"""Command-line interface for IAB classifier."""

import argparse
import json
import sys
import logging
import asyncio
import csv
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
import os

from iab_toolkit import classify_url
from iab_toolkit._config import config
from iab_toolkit._batch import BatchProcessor, load_urls_from_file, save_results_to_json, save_results_to_csv
from iab_toolkit._embedding import embed_text_sync


def format_categories_output(categories, title="Categories"):
    """Format categories for human-readable output."""
    if not categories:
        return f"{title}: None found"
    
    lines = [f"{title}:"]
    for i, cat in enumerate(categories, 1):
        score_str = f"score={cat.score:.2f}" if hasattr(cat, 'score') and cat.score > 0 else ""
        lines.append(f"  {i}. {cat.name} ({cat.id}) {score_str}")
    
    return "\n".join(lines)


def format_persona_output(persona):
    """Format persona for human-readable output."""
    if not persona:
        return "Persona: None generated"
    
    return f"""Persona:
  {persona.age_band} / {persona.gender_tilt} / {persona.tech_affinity}
  {persona.short_description}"""


def progress_callback(completed: int, total: int, current_url: str):
    """Progress callback for batch processing."""
    print(f"Progress: {completed}/{total} - {current_url}")


async def cmd_batch_classify(args):
    """Handle batch classification command."""
    urls_file = Path(args.urls_file)
    if not urls_file.exists():
        print(f"Error: URLs file not found: {urls_file}")
        return 1
    
    try:
        urls = load_urls_from_file(urls_file)
        if not urls:
            print("Error: No URLs found in file")
            return 1
        
        print(f"Found {len(urls)} URLs to classify")
        
        # Create batch processor
        processor = BatchProcessor(max_concurrent=args.concurrent)
        
        # Process URLs
        results = await processor.classify_urls_batch(
            urls,
            max_categories=args.max_categories,
            with_persona=not args.no_persona,
            progress_callback=progress_callback if args.verbose else None
        )
        
        # Save results
        if args.output:
            output_path = Path(args.output)
            if output_path.suffix.lower() == '.csv':
                save_results_to_csv(results, output_path)
                print(f"Results saved to {output_path}")
            else:
                save_results_to_json(results, output_path)
                print(f"Results saved to {output_path}")
        else:
            # Print results to stdout
            if args.json:
                print(json.dumps(results, indent=2, ensure_ascii=False))
            else:
                for result in results:
                    print(f"\nURL: {result['url']}")
                    if 'error' in result:
                        print(f"Error: {result['error']}")
                    else:
                        categories = result['categories_final'] or result['categories_embedding']
                        print(format_categories_output(categories))
                        if not args.no_persona and result['persona']:
                            print(format_persona_output(result['persona']))
        
        return 0
    
    except Exception as e:
        if args.verbose:
            import traceback
            traceback.print_exc()
        else:
            print(f"Error: {e}")
        return 1


def cmd_classify(args):
    """Handle single URL classification command."""
    try:
        # Classify the URL
        result = classify_url(
            args.url,
            max_categories=min(args.max_categories, 3),
            with_persona=not args.no_persona
        )
        
        if args.json:
            # Convert results to JSON-serializable format
            json_result = {
                'url': result['url'],
                'categories_embedding': [
                    {
                        'id': cat.id,
                        'name': cat.name,
                        'score': cat.score,
                        'tier_1': cat.tier_1,
                        'tier_2': cat.tier_2,
                        'tier_3': cat.tier_3,
                        'tier_4': cat.tier_4
                    }
                    for cat in result['categories_embedding']
                ],
                'categories_final': [
                    {
                        'id': cat.id,
                        'name': cat.name,
                        'score': cat.score,
                        'tier_1': cat.tier_1,
                        'tier_2': cat.tier_2,
                        'tier_3': cat.tier_3,
                        'tier_4': cat.tier_4
                    }
                    for cat in result['categories_final']
                ],
                'persona': {
                    'age_band': result['persona'].age_band,
                    'gender_tilt': result['persona'].gender_tilt,
                    'tech_affinity': result['persona'].tech_affinity,
                    'short_description': result['persona'].short_description
                } if result['persona'] else None
            }
            print(json.dumps(json_result, indent=2, ensure_ascii=False))
        else:
            # Format for human reading
            print(format_categories_output(result['categories_embedding'], "Embedding"))
            print()
            
            # Show final results if different from embedding
            if (result['categories_final'] != result['categories_embedding']):
                print(format_categories_output(result['categories_final'], "Final (after GPT)"))
            else:
                print("Final (after GPT): Same as embedding results")
            
            if not args.no_persona:
                print()
                print(format_persona_output(result['persona']))
        
        return 0
    
    except Exception as e:
        if args.verbose:
            import traceback
            traceback.print_exc()
        else:
            print(f"Error: {e}")
        return 1


def cmd_config(args):
    """Handle configuration commands."""
    try:
        if args.config_action == 'set-api-key':
            if not args.value:
                print("Error: API key value required")
                return 1
            config.set_openai_api_key(args.value)
            print("OpenAI API key set successfully")
            
        elif args.config_action == 'get-api-key':
            api_key = config.get_openai_api_key()
            if api_key:
                # Show only first and last 4 characters for security
                masked = f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else "***"
                print(f"OpenAI API key: {masked}")
            else:
                print("OpenAI API key: Not set")
                
        elif args.config_action == 'show':
            cfg = config.get_config()
            print("Configuration:")
            for key, value in cfg.items():
                print(f"  {key}: {value}")
                
        elif args.config_action == 'set':
            if not args.key or args.value is None:
                print("Error: Both key and value required for set command")
                return 1
            config.update_config(**{args.key: args.value})
            print(f"Configuration updated: {args.key} = {args.value}")
            
        return 0
    
    except Exception as e:
        print(f"Error: {e}")
        return 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="IAB Content Taxonomy v3.1 classifier",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Single URL classification
    classify_parser = subparsers.add_parser('classify', help='Classify a single URL')
    classify_parser.add_argument("url", help="URL to classify")
    classify_parser.add_argument("--no-persona", action="store_true", help="Skip persona generation")
    classify_parser.add_argument("--json", action="store_true", help="Output raw JSON instead of formatted text")
    classify_parser.add_argument("--max-categories", type=int, default=3, help="Maximum number of categories to return (default: 3)")
    classify_parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    # Batch classification
    batch_parser = subparsers.add_parser('batch-classify', help='Classify multiple URLs from a file')
    batch_parser.add_argument("urls_file", help="File containing URLs (one per line)")
    batch_parser.add_argument("--output", "-o", help="Output file (JSON or CSV based on extension)")
    batch_parser.add_argument("--no-persona", action="store_true", help="Skip persona generation")
    batch_parser.add_argument("--json", action="store_true", help="Output raw JSON instead of formatted text")
    batch_parser.add_argument("--max-categories", type=int, default=3, help="Maximum number of categories to return (default: 3)")
    batch_parser.add_argument("--concurrent", type=int, default=5, help="Number of concurrent requests (default: 5)")
    batch_parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    # Configuration management
    config_parser = subparsers.add_parser('config', help='Manage configuration')
    config_subparsers = config_parser.add_subparsers(dest='config_action', help='Configuration actions')
    
    # Config set-api-key
    set_api_parser = config_subparsers.add_parser('set-api-key', help='Set OpenAI API key')
    set_api_parser.add_argument('value', help='API key value')
    
    # Config get-api-key
    config_subparsers.add_parser('get-api-key', help='Show current API key (masked)')
    
    # Config show
    config_subparsers.add_parser('show', help='Show all configuration')
    
    # Config set
    set_config_parser = config_subparsers.add_parser('set', help='Set configuration value')
    set_config_parser.add_argument('key', help='Configuration key')
    set_config_parser.add_argument('value', help='Configuration value')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle case where no command is provided (backwards compatibility)
    if not args.command:
        # Try to parse as old-style single URL command
        parser = argparse.ArgumentParser(description="Classify web pages using IAB Content Taxonomy v3.1")
        parser.add_argument("url", help="URL to classify")
        parser.add_argument("--no-persona", action="store_true", help="Skip persona generation")
        parser.add_argument("--json", action="store_true", help="Output raw JSON instead of formatted text")
        parser.add_argument("--max-categories", type=int, default=3, help="Maximum number of categories to return (default: 3)")
        parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
        
        args = parser.parse_args()
        args.command = 'classify'
    
    # Set up logging
    if hasattr(args, 'verbose') and args.verbose:
        logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
    else:
        logging.basicConfig(level=logging.WARNING)
    
    # Execute command
    try:
        if args.command == 'classify':
            return cmd_classify(args)
        elif args.command == 'batch-classify':
            return asyncio.run(cmd_batch_classify(args))
        elif args.command == 'config':
            return cmd_config(args)
        else:
            parser.print_help()
            return 1
    except KeyboardInterrupt:
        print("\nOperation interrupted by user.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
