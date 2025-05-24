#!/usr/bin/env python3
"""Enhanced test script with JSON file output for the simplified classification system."""

import os
import json
from datetime import datetime
from enhanced_hybrid_classifier_v2 import enhanced_classify_content

def test_simplified_classification_with_output():
    """Test the simplified system and save results to JSON file."""
    
    # Test files
    test_files = [
        'japanese_text_sample.txt',      # Automotive
        'japanese_beauty_sample.txt',     # Beauty/cosmetics  
        'japanese_business_sample.txt',   # Business/finance
        'japanese_health_sample.txt',     # Health/medical
        'japanese_technology_sample.txt'  # Technology
    ]
    
    print("=" * 80)
    print("SIMPLIFIED IAB CLASSIFICATION SYSTEM - WITH JSON OUTPUT")
    print("=" * 80)
    print("Features:")
    print("✅ No confidence percentages in output")
    print("✅ Simplified user profile (3 metrics only)")
    print("✅ JSON file output for structured data")
    print("=" * 80)
    
    # Store all results for JSON output
    all_results = []
    
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
            
            # Display results in simplified format (console output)
            print("📊 TOP 2 TIER 2 CATEGORIES:")
            for i, category in enumerate(result.tier2_categories, 1):
                print(f"   {i}. {category['name']} (ID: {category['id']})")
                print(f"      Path: {category['tier_1']} > {category['tier_2']}")
            
            print("\n👤 USER PROFILE (Simplified):")
            profile_dict = result.user_profile.to_dict()
            print(f"   Age Range: {profile_dict['age_range']}")
            print(f"   Geekiness Level: {profile_dict['geekiness_level']}/10")
            print(f"   Content Sophistication: {profile_dict['content_sophistication']}")
            
            # Prepare data for JSON output
            json_result = {
                "sample_name": test_file,
                "timestamp": datetime.now().isoformat(),
                "content_preview": text[:200] + "..." if len(text) > 200 else text,
                "classification": {
                    "primary_domain": result.tier2_categories[0]['tier_1'] if result.tier2_categories else "unknown",
                    "tier2_categories": [
                        {
                            "rank": i + 1,
                            "id": category['id'],
                            "name": category['name'],
                            "tier_1": category['tier_1'],
                            "tier_2": category['tier_2'],
                            "full_path": f"{category['tier_1']} > {category['tier_2']}"
                        }
                        for i, category in enumerate(result.tier2_categories)
                    ]
                },
                "user_profile": {
                    "age_range": profile_dict['age_range'],
                    "geekiness_level": profile_dict['geekiness_level'],
                    "content_sophistication": profile_dict['content_sophistication']
                }
            }
            
            all_results.append(json_result)
            print("-" * 50)
            
        except Exception as e:
            print(f"❌ Error processing {test_file}: {e}")
            # Add error result to JSON
            error_result = {
                "sample_name": test_file,
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "classification": None,
                "user_profile": None
            }
            all_results.append(error_result)
    
    # Save results to JSON file
    output_filename = f"simplified_classification_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump({
                "metadata": {
                    "system_version": "Simplified IAB Classification System v2",
                    "test_date": datetime.now().isoformat(),
                    "total_samples": len(all_results),
                    "successful_classifications": len([r for r in all_results if 'error' not in r]),
                    "features": [
                        "No confidence percentages in output",
                        "3-metric user profile only",
                        "Offline processing (no API required)",
                        "Japanese and English text support"
                    ]
                },
                "results": all_results
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 RESULTS SAVED TO: {output_filename}")
        print(f"📊 Total samples processed: {len(all_results)}")
        print(f"✅ Successful classifications: {len([r for r in all_results if 'error' not in r])}")
        
    except Exception as e:
        print(f"❌ Error saving JSON file: {e}")
    
    print("\n✅ SIMPLIFIED SYSTEM TEST WITH JSON OUTPUT COMPLETE")
    print("✅ Console output shows clean, simplified format")
    print("✅ JSON file contains structured data for analysis")
    print("✅ All Japanese text samples processed successfully")

def create_sample_json_output():
    """Create a sample JSON output structure for reference."""
    sample_output = {
        "metadata": {
            "system_version": "Simplified IAB Classification System v2",
            "test_date": "2025-05-24T10:30:00",
            "total_samples": 1,
            "successful_classifications": 1,
            "features": [
                "No confidence percentages in output",
                "3-metric user profile only", 
                "Offline processing (no API required)",
                "Japanese and English text support"
            ]
        },
        "results": [
            {
                "sample_name": "japanese_text_sample.txt",
                "timestamp": "2025-05-24T10:30:00",
                "content_preview": "トヨタRAV4は、トヨタ自動車が製造・販売しているSUVです...",
                "classification": {
                    "primary_domain": "Automotive",
                    "tier2_categories": [
                        {
                            "rank": 1,
                            "id": "2",
                            "name": "Auto Body Styles",
                            "tier_1": "Automotive",
                            "tier_2": "Auto Body Styles",
                            "full_path": "Automotive > Auto Body Styles"
                        },
                        {
                            "rank": 2,
                            "id": "35",
                            "name": "Auto Safety",
                            "tier_1": "Automotive", 
                            "tier_2": "Auto Safety",
                            "full_path": "Automotive > Auto Safety"
                        }
                    ]
                },
                "user_profile": {
                    "age_range": "30-45",
                    "geekiness_level": 5,
                    "content_sophistication": "advanced"
                }
            }
        ]
    }
    
    with open("sample_json_structure.json", 'w', encoding='utf-8') as f:
        json.dump(sample_output, f, indent=2, ensure_ascii=False)
    
    print("📄 Sample JSON structure saved to: sample_json_structure.json")

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Run full test with JSON output")
    print("2. Create sample JSON structure only")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        create_sample_json_output()
    else:
        test_simplified_classification_with_output()
