#!/usr/bin/env python3
"""
Simple CLI for IAB Hybrid Classifier
"""

import argparse
import sys
from pathlib import Path
from .hybrid_iab_classifier import HybridIABClassifier


def main():
    """Main CLI entry point for hybrid classifier."""
    parser = argparse.ArgumentParser(
        description="IAB Content Taxonomy v3.1 Hybrid Classifier",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  iab-hybrid "Your text content here"
  iab-hybrid --file content.txt
  iab-hybrid --test  # Run Japanese sample tests
        """
    )
    
    parser.add_argument(
        "text", 
        nargs='?', 
        help="Text content to classify (optional if using --file or --test)"
    )
    parser.add_argument(
        "--file", "-f",
        help="Path to text file to classify"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run the Japanese sample test suite"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Handle test mode
    if args.test:
        from .test_japanese_samples import main as test_main
        return test_main()
    
    # Get text content
    text_content = None
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {file_path}")
            return 1
        try:
            text_content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Error reading file: {e}")
            return 1
    elif args.text:
        text_content = args.text
    else:
        parser.print_help()
        return 1
    
    if not text_content or not text_content.strip():
        print("Error: No text content provided")
        return 1
    
    try:
        # Initialize classifier
        if args.verbose:
            print("Initializing HybridIABClassifier...")
        
        classifier = HybridIABClassifier()
        
        # Classify content
        if args.verbose:
            print(f"Classifying text ({len(text_content)} characters)...")
        
        result = classifier.classify(text_content)
        
        # Output results
        if args.json:
            import json
            from dataclasses import asdict
            result_dict = asdict(result)
            print(json.dumps(result_dict, indent=2, ensure_ascii=False))
        else:
            print_readable_results(result, text_content)
        
        return 0
        
    except Exception as e:
        if args.verbose:
            import traceback
            traceback.print_exc()
        else:
            print(f"Error: {e}")
        return 1


def print_readable_results(result, text_content):
    """Print results in human-readable format."""
    print("\n" + "="*60)
    print("IAB HYBRID CLASSIFICATION RESULTS")
    print("="*60)
    
    # Text preview
    preview = text_content[:100] + "..." if len(text_content) > 100 else text_content
    print(f"📖 Text Preview: {preview}")
    print(f"📏 Text Length: {len(text_content)} characters")
    print()
    
    # Tier 1 Domain
    print(f"🎯 Primary Domain: {result.primary_tier1_domain}")
    
    # Tier 2 Categories
    if result.tier2_categories:
        print(f"\n🏷️  Top Tier 2 Categories:")
        for i, cat in enumerate(result.tier2_categories, 1):
            confidence = cat.get('confidence', 0) * 100
            print(f"   {i}. {cat['name']} ({confidence:.1f}%)")
    
    # User Profile
    if result.user_profile:
        profile = result.user_profile
        print(f"\n👤 User Profile:")
        print(f"   Age Range: {profile.age_range}")
        print(f"   Tech Level: {profile.geekiness_level}/10")
        print(f"   Sophistication: {profile.content_sophistication}")
        
        if profile.interests:
            interests = ', '.join(profile.interests)
            print(f"   Interests: {interests}")
    
    # Processing info
    if result.processing_time:
        print(f"\n⏱️  Processing Time: {result.processing_time:.3f} seconds")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    sys.exit(main())
