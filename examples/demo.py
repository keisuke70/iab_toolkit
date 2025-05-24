#!/usr/bin/env python3
"""
Example script demonstrating the enhanced IAB Toolkit features.

This script shows how to use the new async batch processing,
configuration management, and export functionality.
"""

import asyncio
import json
from pathlib import Path
from typing import List

from iab_toolkit._config import config
from iab_toolkit._batch import BatchProcessor, save_results_to_json, save_results_to_csv
from iab_toolkit import classify_url

async def demo_batch_processing():
    """Demonstrate async batch processing."""
    print("=== Async Batch Processing Demo ===\n")
    
    # Sample URLs for demonstration
    urls = [
        "https://www.bbc.com/news",
        "https://www.techcrunch.com", 
        "https://www.cnn.com/sport",
        "https://www.foodnetwork.com/recipes"
    ]
    
    print(f"Processing {len(urls)} URLs concurrently...")
    
    # Create batch processor with 3 concurrent requests
    processor = BatchProcessor(max_concurrent=3)
    
    def progress_callback(completed: int, total: int, current_url: str):
        print(f"  Progress: {completed}/{total} - {current_url}")
    
    try:
        # Process URLs with progress tracking
        results = await processor.classify_urls_batch(
            urls,
            max_categories=3,
            with_persona=True,
            progress_callback=progress_callback
        )
        
        print(f"\nProcessed {len(results)} URLs")
        
        # Show results summary
        for result in results:
            if result.get('error'):
                print(f"❌ {result['url']}: {result['error']}")
            else:
                categories_count = len(result.get('categories_final', []))
                print(f"✅ {result['url']}: {categories_count} categories")
        
        # Export to files
        save_results_to_json(results, Path("demo_results.json"))
        save_results_to_csv(results, Path("demo_results.csv"))
        print("\n📁 Results saved to demo_results.json and demo_results.csv")
        
        return results
        
    except Exception as e:
        print(f"❌ Batch processing failed: {e}")
        return []

def demo_configuration():
    """Demonstrate configuration management."""
    print("\n=== Configuration Management Demo ===\n")
    
    # Show current configuration
    current_config = config.get_config()
    print("Current configuration:")
    for key, value in current_config.items():
        print(f"  {key}: {value}")
    
    # Check API key status
    api_key = config.get_openai_api_key()
    if api_key:
        masked_key = f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else "***"
        print(f"\n🔑 API Key: {masked_key}")
    else:
        print("\n⚠️  No API key set. Use: iab-classify config set-api-key 'your-key'")
    
    # Demonstrate configuration updates
    print("\n📝 Configuration can be updated programmatically:")
    print("  config.update_config(default_max_categories=5)")
    print("  config.set_openai_api_key('your-api-key')")

def demo_single_classification():
    """Demonstrate single URL classification."""
    print("\n=== Single URL Classification Demo ===\n")
    
    url = "https://www.bbc.com/news"
    print(f"Classifying: {url}")
    
    try:
        result = classify_url(url, max_categories=3, with_persona=True)
        
        print("✅ Classification successful!")
        print(f"📊 Categories found: {len(result.get('categories_final', []))}")
        print(f"👤 Persona generated: {'Yes' if result.get('persona') else 'No'}")
        
        # Show top category if available
        if result.get('categories_final'):
            top_category = result['categories_final'][0]
            print(f"🏆 Top category: {top_category.name} (score: {top_category.score:.3f})")
        
        return result
        
    except Exception as e:
        print(f"❌ Classification failed: {e}")
        return None

async def main():
    """Main demo function."""
    print("🚀 IAB Toolkit Enhanced Features Demo")
    print("=" * 50)
    
    # Configuration demo
    demo_configuration()
    
    # Single classification demo
    demo_single_classification()
    
    # Batch processing demo
    await demo_batch_processing()
    
    print("\n" + "=" * 50)
    print("✨ Demo completed!")
    print("\nNext steps:")
    print("1. Set your OpenAI API key: iab-classify config set-api-key 'your-key'")
    print("2. Try batch processing: iab-classify batch-classify urls.txt")
    print("3. Explore the CLI: iab-classify --help")

if __name__ == "__main__":
    asyncio.run(main())
