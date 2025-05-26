#!/usr/bin/env python3
"""
Generates a client-facing report for Japanese text sample classification,
focusing on Tier 2 categories and user profiling.
"""

import time
from pathlib import Path
from datetime import datetime
from .hybrid_iab_classifier import HybridIABClassifier
import sys # Added for stdout redirection
import io # Added for suppressing verbose output

def load_japanese_samples():
    """Load all Japanese sample files."""
    base_path = Path(__file__).parent / "data"
    
    samples = {}
    sample_files = {
        "japanese_beauty_sample.txt": {
            "name": "Beauty & Cosmetics",
            "description": "オーガニック化粧品ブランド"
            # Expected tier1 removed as it's not for client report
        },
        "japanese_text_sample.txt": {
            "name": "Automotive",
            "description": "トヨタRAV4 SUV"
        },
        "japanese_technology_sample.txt": {
            "name": "Technology",
            "description": "iPhone 15 Pro技術"
        },
        "japanese_business_sample.txt": {
            "name": "Business & Finance",
            "description": "東京証券取引所企業"
        },
        "japanese_health_sample.txt": {
            "name": "Health & Wellness",
            "description": "東京大学医学部研究"
        }
    }
    
    for filename, info in sample_files.items():
        file_path = base_path / filename
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read().strip()
                samples[filename] = {
                    "text": text,
                    "name": info["name"],
                    "description": info["description"]
                }
        else:
            # Simplified warning for client script, or could be removed if files are guaranteed
            print(f"Warning: Sample file not found: {filename}")
    
    return samples

def generate_client_report():
    """Generates and prints the client report for Japanese samples."""
    
    original_stdout = sys.stdout
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file_name = f"japanese_text_analysis_client_report_{timestamp}.txt"
    # Assuming Path(__file__).parent is correct
    report_file_path = Path(__file__).resolve().parent / report_file_name

    # Print to console before redirection
    print(f"Generating client report. Output will be saved to: {report_file_path}")

    with open(report_file_path, 'w', encoding='utf-8') as report_file:
        sys.stdout = report_file # Redirect stdout to the report file

        try:
            print("=" * 80)
            print(f"JAPANESE TEXT ANALYSIS REPORT - GENERATED AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 80)
            print("\\nThis report presents an analysis of sample Japanese texts, focusing on estimated Tier 2 content categories and user profiles.\\n")
            
            # Initialize classifier
            print("Initializing Classifier...")
            
            # Suppress stdout for classifier initialization's verbose messages
            current_stdout_for_init = sys.stdout
            temp_stdout_for_init = io.StringIO()
            sys.stdout = temp_stdout_for_init
            try:
                classifier = HybridIABClassifier()
            finally:
                sys.stdout = current_stdout_for_init # Restore stdout to the report file
            
            print("Classifier Initialized.")
            print()
            
            # Load Japanese samples
            samples = load_japanese_samples()
            
            if not samples:
                print("No Japanese sample files found. Report cannot be generated.")
                return
            
            print(f"Loaded {len(samples)} Japanese sample texts for analysis.")
            print("-" * 80 + "\\n")
            
            for i, (filename, sample) in enumerate(samples.items(), 1):
                text = sample["text"]
                name = sample["name"]
                description = sample["description"]
                
                print("=" * 70)
                print(f"サンプル {i}: {name.upper()}")
                print(f"概要: {description}")
                print("=" * 70 + "\\n")
                
                print("--- 全文サンプル ---")
                print(text)
                print("--- サンプル終了 ---\\n")
                
                # Perform classification - suppress verbose output from classify()
                saved_stdout_loop = sys.stdout
                temp_stdout_loop = io.StringIO()
                sys.stdout = temp_stdout_loop
                try:
                    result = classifier.classify(text)
                finally:
                    sys.stdout = saved_stdout_loop # Restore stdout
                
                # Show tier2 categories
                if result.tier2_categories:
                    print(">>> 推定Tier2カテゴリ:")
                    # Sort Tier 2 categories by confidence in descending order
                    sorted_tier2_categories = sorted(result.tier2_categories, key=lambda x: x.get('confidence', 0.0), reverse=True)
                    for j, cat in enumerate(sorted_tier2_categories, 1):
                        name_cat = cat.get('name', 'Unknown')
                        confidence = cat.get('confidence', 0.0)
                        print(f"    {j}. {name_cat} (信頼度: {confidence:.1%})")
                else:
                    print(">>> 推定Tier2カテゴリ: なし")
                print()
                
                # Show user profile
                profile = result.user_profile
                print(">>> 推定ユーザープロファイル:")
                print(f"    年齢層: {profile.age_range}")
                print(f"    ギーク度: {profile.geekiness_level}/10")
                print(f"    コンテンツの洗練度: {profile.content_sophistication}")
                print(f"    推定される属性: {profile.likely_demographics}")
                print()
                
                if i < len(samples):
                    print("-" * 70 + "\\n\\n") # Separator between samples
            
            print("\\n" + "=" * 80)
            print("レポート終了")
            print("=" * 80)
        finally:
            sys.stdout = original_stdout # Restore stdout to console

    # Print to console after generation
    print(f"Client report successfully saved to: {report_file_path}")

def main():
    """Main entry point for the client report generation."""
    generate_client_report()

if __name__ == "__main__":
    main()
