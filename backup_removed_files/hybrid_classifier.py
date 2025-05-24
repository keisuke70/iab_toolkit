#!/usr/bin/env python3
"""
Better hybrid classification approach:
1. Use embeddings to find the best Tier 1 category
2. Extract all subcategories from that Tier 1
3. Pass the focused subset to GPT for precise classification
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from iab_toolkit.classify import classify_with_embeddings
from iab_toolkit._gpt import _load_taxonomy

def get_tier1_categories() -> List[Dict[str, Any]]:
    """Get all Tier 1 categories (top-level categories)."""
    taxonomy = _load_taxonomy()
    tier1_categories = []
    
    for entry in taxonomy:
        # Tier 1 categories have no parent or parent equals their own ID
        if (entry.get('tier_2') is None and 
            entry.get('tier_3') is None and 
            entry.get('tier_4') is None):
            tier1_categories.append(entry)
    
    return tier1_categories

def get_all_subcategories_for_tier1(tier1_name: str) -> List[Dict[str, Any]]:
    """Get all subcategories (Tier 2, 3, 4) for a given Tier 1 category."""
    taxonomy = _load_taxonomy()
    subcategories = []
    
    for entry in taxonomy:
        if entry.get('tier_1') == tier1_name:
            subcategories.append(entry)
    
    return subcategories

def create_focused_taxonomy_prompt(tier1_name: str, subcategories: List[Dict[str, Any]]) -> str:
    """Create a focused prompt with just the relevant taxonomy subset."""
    
    prompt = f"""You are classifying content into IAB Content Taxonomy v3.1 categories.

The content appears to be related to: {tier1_name}

Here are ALL the available categories in this taxonomy branch:

TIER 1: {tier1_name}
"""
    
    # Group by tier levels for better organization
    tier2_categories = {}
    tier3_categories = {}
    tier4_categories = {}
    
    for entry in subcategories:
        tier2 = entry.get('tier_2')
        tier3 = entry.get('tier_3') 
        tier4 = entry.get('tier_4')
        
        if tier2 and not tier3:  # Tier 2 category
            tier2_categories[tier2] = entry
        elif tier3 and not tier4:  # Tier 3 category
            if tier2 not in tier3_categories:
                tier3_categories[tier2] = []
            tier3_categories[tier2].append(entry)
        elif tier4:  # Tier 4 category
            if tier2 not in tier4_categories:
                tier4_categories[tier2] = {}
            if tier3 not in tier4_categories[tier2]:
                tier4_categories[tier2][tier3] = []
            tier4_categories[tier2][tier3].append(entry)
    
    # Add Tier 2 categories
    for tier2_name, entry in tier2_categories.items():
        prompt += f"\n  TIER 2: {tier2_name} (ID: {entry['unique_id']})"
    
    # Add Tier 3 categories
    for tier2_name, tier3_list in tier3_categories.items():
        prompt += f"\n  TIER 2: {tier2_name}"
        for entry in tier3_list:
            prompt += f"\n    TIER 3: {entry['tier_3']} (ID: {entry['unique_id']})"
    
    # Add Tier 4 categories  
    for tier2_name, tier3_dict in tier4_categories.items():
        prompt += f"\n  TIER 2: {tier2_name}"
        for tier3_name, tier4_list in tier3_dict.items():
            prompt += f"\n    TIER 3: {tier3_name}"
            for entry in tier4_list:
                prompt += f"\n      TIER 4: {entry['tier_4']} (ID: {entry['unique_id']})"

    prompt += """

Select the 1-3 most specific and appropriate categories from the above list.
Return JSON array: [{"id": actual_id_from_above, "name": "exact_category_name", "confidence": 0.0-1.0}]

Use the EXACT category names and IDs listed above. Choose the most specific tier that applies.
Only output JSON."""
    
    return prompt

def hybrid_classify(text: str, max_categories: int = 3) -> List[Dict[str, Any]]:
    """
    Hybrid classification:
    1. Use embeddings to find best Tier 1
    2. Get focused taxonomy subset
    3. Use GPT with focused prompt for precise classification
    """
    
    print("=== STEP 1: Embedding-based Tier 1 Detection ===")
    
    # Get embedding-based classification (this works well for Tier 1)
    embedding_results = classify_with_embeddings(text, max_categories=5, min_score=0.3)
    
    if not embedding_results:
        print("No embedding results found")
        return []
    
    # Get the top Tier 1 category
    top_result = embedding_results[0]
    tier1_name = top_result.tier_1
    
    print(f"Best Tier 1 category: {tier1_name} (score: {top_result.score:.3f})")
    
    print(f"\n=== STEP 2: Get Focused Taxonomy Subset ===")
    
    # Get all subcategories for this Tier 1
    subcategories = get_all_subcategories_for_tier1(tier1_name)
    print(f"Found {len(subcategories)} subcategories in {tier1_name}")
    
    # Show some examples
    for i, cat in enumerate(subcategories[:5]):
        tier_info = f"T1:{cat.get('tier_1')} T2:{cat.get('tier_2')} T3:{cat.get('tier_3')} T4:{cat.get('tier_4')}"
        print(f"  {cat['unique_id']}: {cat['name']} ({tier_info})")
    if len(subcategories) > 5:
        print(f"  ... and {len(subcategories) - 5} more")
    
    print(f"\n=== STEP 3: Focused GPT Classification ===")
    
    # Create focused prompt
    focused_prompt = create_focused_taxonomy_prompt(tier1_name, subcategories)
    print(f"Prompt length: {len(focused_prompt)} characters")
    print("\\nFirst 200 chars of prompt:")
    print(focused_prompt[:200] + "...")
    
    # TODO: Call GPT with focused prompt
    # For now, let's return the embedding results
    return [{
        'id': result.id,
        'name': result.name,
        'score': result.score,
        'tier_1': result.tier_1,
        'tier_2': result.tier_2,
        'tier_3': result.tier_3,
        'tier_4': result.tier_4,
        'method': 'embedding'
    } for result in embedding_results[:max_categories]]

if __name__ == "__main__":
    # Test with Japanese text
    with open('japanese_text_sample.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    
    print("Testing Hybrid Classification Approach")
    print("=" * 50)
    
    results = hybrid_classify(text)
    
    print(f"\n=== FINAL RESULTS ===")
    for result in results:
        print(f"ID: {result['id']}, Name: {result['name']}, Score: {result['score']:.3f}")
        print(f"  Tiers: {result['tier_1']} > {result['tier_2']} > {result['tier_3']} > {result['tier_4']}")
        print(f"  Method: {result['method']}")
        print()
