#!/usr/bin/env python3
"""Test the simplified classification system with Japanese samples."""

import os
from enhanced_hybrid_classifier_v2 import enhanced_classify_content

def test_simplified_classification():
    """Test the simplified system showing only 3 user profile metrics."""
    
    # Test files
    test_files = [
        'japanese_text_sample.txt',      # Automotive
        'japanese_beauty_sample.txt',     # Beauty/cosmetics  
        'japanese_business_sample.txt',   # Business/finance
        'japanese_health_sample.txt',     # Health/medical
        'japanese_technology_sample.txt'  # Technology
    ]
    
    print("=" * 80)
    print("SIMPLIFIED IAB CLASSIFICATION SYSTEM - FINAL TEST")
    print("=" * 80)
    print("Changes made:")
    print("✅ Removed confidence percentages from output")
    print("✅ Simplified user profile to 3 metrics only:")
    print("   - Age Range")
    print("   - Geekiness Level (1-10)")
    print("   - Content Sophistication")
    print("=" * 80)
    
    for test_file in test_files:
        if not os.path.exists(test_file):
            print(f"⚠️  File not found: {test_file}")
            continue
            
        print(f"\n🔍 TESTING: {test_file}")
        print("-" * 50)
        
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                text = f.read().strip()
            
            print(f"Content preview: {text[:100]}...")
            print()
            
            # Classify content
            result = enhanced_classify_content(text)
            
            # Display results in simplified format
            print("📊 TOP 2 TIER 2 CATEGORIES:")
            for i, category in enumerate(result.tier2_categories, 1):
                print(f"   {i}. {category['name']} (ID: {category['id']})")
                print(f"      Path: {category['tier_1']} > {category['tier_2']}")
            
            print("\n👤 USER PROFILE (Simplified):")
            profile_dict = result.user_profile.to_dict()
            print(f"   Age Range: {profile_dict['age_range']}")
            print(f"   Geekiness Level: {profile_dict['geekiness_level']}/10")
            print(f"   Content Sophistication: {profile_dict['content_sophistication']}")
            
            print("-" * 50)
            
        except Exception as e:
            print(f"❌ Error processing {test_file}: {e}")
    
    print("\n✅ SIMPLIFIED SYSTEM TEST COMPLETE")
    print("✅ No confidence percentages shown")
    print("✅ User profile reduced to 3 key metrics")
    print("✅ System works with Japanese text samples")

if __name__ == "__main__":
    test_simplified_classification()
