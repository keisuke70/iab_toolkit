#!/usr/bin/env python3
"""
Test individual JSON output functionality for the simplified IAB classification system.
"""

import sys
import os
from pathlib import Path

# Add the current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from enhanced_hybrid_classifier_v2 import enhanced_classify_with_json_output

def test_individual_json_output():
    """Test individual JSON file output for a single sample."""
    
    print("=" * 80)
    print("TESTING INDIVIDUAL JSON OUTPUT")
    print("=" * 80)
    
    # Test with the automotive sample
    sample_file = Path("japanese_text_sample.txt")
    
    if not sample_file.exists():
        print(f"❌ Sample file not found: {sample_file}")
        return
    
    print(f"📄 Reading sample: {sample_file}")
    
    with open(sample_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📊 Content length: {len(content)} characters")
    print(f"🔍 Preview: {content[:100]}...")
    print()
    
    # Classify with JSON output
    print("🚀 Running classification with JSON output...")
    result, json_filename = enhanced_classify_with_json_output(
        text=content,
        sample_name="automotive_test",
        output_filename="individual_test_result.json"
    )
    
    print(f"✅ Classification complete!")
    print(f"💾 JSON saved to: {json_filename}")
    print()
    
    # Display key results
    print("=" * 50)
    print("CLASSIFICATION SUMMARY")
    print("=" * 50)
    
    print("📊 Top 2 Tier 2 Categories:")
    for i, category in enumerate(result.tier2_categories, 1):
        print(f"   {i}. {category['name']} (ID: {category['id']})")
        print(f"      Path: {category['tier_1']} > {category['tier_2']}")
    
    print()
    print("👤 User Profile (3 metrics):")
    profile = result.user_profile.to_dict()
    print(f"   Age Range: {profile['age_range']}")
    print(f"   Geekiness Level: {profile['geekiness_level']}/10")
    print(f"   Content Sophistication: {profile['content_sophistication']}")
    
    print()
    print("🔍 Content Analysis:")
    print(f"   Technical Level: {result.content_analysis.get('technical_level', 'unknown')}")
    print(f"   Tone: {result.content_analysis.get('tone', 'unknown')}")
    
    print()
    print("✅ Individual JSON output test complete!")
    print(f"📁 Check file: {json_filename}")

if __name__ == "__main__":
    test_individual_json_output()
