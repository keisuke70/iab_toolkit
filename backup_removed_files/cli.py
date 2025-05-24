"""Command-line interface for IAB classifier."""

import argparse
import json
import sys
import logging
from typing import Dict, Any

from iab_toolkit import classify_url


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


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Classify web pages using IAB Content Taxonomy v3.1"
    )
    parser.add_argument("url", help="URL to classify")
    parser.add_argument(
        "--no-persona",
        action="store_true",
        help="Skip persona generation"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON instead of formatted text"
    )
    parser.add_argument(
        "--max-categories",
        type=int,
        default=3,
        help="Maximum number of categories to return (default: 3)"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Set up logging
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)
    
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
    
    except KeyboardInterrupt:
        print("\nClassification interrupted by user.")
        sys.exit(1)
    except Exception as e:
        if args.verbose:
            import traceback
            traceback.print_exc()
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
