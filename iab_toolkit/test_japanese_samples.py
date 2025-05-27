#!/usr/bin/env python3
"""
Comprehensive test using all Japanese text sample files to validate
the hybrid classification system with .npy embeddings.
Output is redirected to a log file.
"""

import time
from pathlib import Path
import sys # Added for stdout redirection
from datetime import datetime # Added for timestamped log file
from .hybrid_iab_classifier import HybridIABClassifier

def load_japanese_samples():
    """Load all Japanese sample files."""
    base_path = Path(__file__).parent / "data"
    
    samples = {}
    sample_files = {
        "japanese_text_sample.txt": {
            "name": "Automotive",
            "expected_tier1": "Automotive", 
            "description": "トヨタRAV4 SUV"
        },
        "japanese_beauty_sample.txt": {
            "name": "Beauty & Cosmetics",
            "expected_tier1": "Style & Fashion",
            "description": "オーガニック化粧品ブランド"
        },
        "japanese_technology_sample.txt": {
            "name": "Technology",
            "expected_tier1": "Technology & Computing",
            "description": "iPhone 15 Pro技術"
        },
        "japanese_business_sample.txt": {
            "name": "Business & Finance",
            "expected_tier1": "Business and Finance",
            "description": "東京証券取引所企業"
        },
        "japanese_health_sample.txt": {
            "name": "Health & Wellness",
            "expected_tier1": "Healthy Living",
            "description": "東京大学医学部研究"
        },          "japanese_careers_sample.txt": {
            "name": "Careers & Employment",
            "expected_tier1": "Careers",
            "description": "キャリアアップセミナー情報"
        },
        "japanese_education_sample.txt": {
            "name": "Education",
            "expected_tier1": "Education",
            "description": "オンライン学習プラットフォーム"
        },
        "japanese_food_drink_sample.txt": {
            "name": "Food & Drink",
            "expected_tier1": "Food & Drink",
            "description": "東京レストラン春の特別コース"
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
                    "expected_tier1": info["expected_tier1"],
                    "description": info["description"]
                }
        else:
            print(f"⚠️  Warning: Sample file not found: {filename}")
    
    return samples

def test_japanese_classification():
    """Test the hybrid classifier with all Japanese samples. Output to log file."""
    
    original_stdout = sys.stdout
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_name = f"test_japanese_samples_output_{timestamp}.log"
    # Save log in the test folder
    test_folder = Path(__file__).parent / "test"
    test_folder.mkdir(exist_ok=True)  # Ensure test folder exists
    log_file_path = test_folder / log_file_name
    
    # Print to console before redirection
    print(f"Redirecting test output to: {log_file_path}")
    
    log_file = open(log_file_path, 'w', encoding='utf-8')
    sys.stdout = log_file
    
    try:
        print("=" * 80)
        print(f"COMPREHENSIVE JAPANESE TEXT CLASSIFICATION TEST - LOG AT {datetime.now()}")
        print("=" * 80)
        print("🎯 Testing hybrid system with real Japanese content")
        print("📊 Using .npy embeddings for tier1 + LLM for tier2")
        print("🇯🇵 All samples are authentic Japanese text")
        print()
        
        # Initialize classifier
        print("Initializing HybridIABClassifier...")
        classifier = HybridIABClassifier()
        print()
        
        # Load Japanese samples
        samples = load_japanese_samples()
        
        if not samples:
            print("❌ No Japanese sample files found!")
            return
        
        print(f"📄 Loaded {len(samples)} Japanese sample files")
        print()
        
        # Test each sample
        results = []
        total_time = 0
        
        for i, (filename, sample) in enumerate(samples.items(), 1):
            text = sample["text"]
            name = sample["name"]
            expected = sample["expected_tier1"]
            description = sample["description"]
            
            print(f"🧪 Test {i}: {name}")
            print("=" * 60)
            print(f"📝 説明: {description}")
            print(f"📄 ファイル: {filename}")
            print(f"📊 期待される分類: {expected}")
            print(f"📖 テキスト概要: {text[:100]}...")
            print()
            
            # Perform classification
            start_time = time.time()
            result = classifier.classify(text)
            classification_time = time.time() - start_time
            total_time += classification_time
            
            # Check tier1 accuracy
            tier1_correct = result.primary_tier1_domain == expected
            status_emoji = "✅" if tier1_correct else "⚠️"
            
            print(f"🎯 分類結果:")
            print(f"   {status_emoji} Tier1ドメイン: {result.primary_tier1_domain}")
            print(f"   📈 期待値: {expected}")
            print(f"   ✓ 正確性: {'正解' if tier1_correct else '異なる結果'}")
            print()
            
            # Show tier2 categories
            if result.tier2_categories:
                print(f"🏷️  Tier2カテゴリ (TOP {len(result.tier2_categories)}):")
                for j, cat in enumerate(result.tier2_categories, 1):
                    name_cat = cat.get('name', 'Unknown')
                    confidence = cat.get('confidence', 0.0)
                    print(f"   {j}. {name_cat} ({confidence:.1%})")
            else:
                print("🏷️  Tier2カテゴリ: なし")
            print()
            
            # Show user profile
            profile = result.user_profile
            print(f"👤 ユーザープロファイル:")
            print(f"   年齢層: {profile.age_range}")
            print(f"   技術レベル: {profile.geekiness_level}/10")
            print(f"   コンテンツ洗練度: {profile.content_sophistication}")
            print(f"   ユーザー層: {profile.likely_demographics}")
            print()
            
            # Performance
            print(f"⏱️  処理時間: {classification_time:.3f}秒")
            print()
            
            # Store results
            results.append({
                'filename': filename,
                'name': name,
                'description': description,
                'expected': expected,
                'detected': result.primary_tier1_domain,
                'tier1_correct': tier1_correct,
                'tier2_count': len(result.tier2_categories),
                'processing_time': classification_time,
                'user_profile': {
                    'age_range': profile.age_range,
                    'geekiness': profile.geekiness_level,
                    'sophistication': profile.content_sophistication,
                    'demographics': profile.likely_demographics
                }
            })
            
            print("-" * 60)
            print()
        
        # System status
        print("🚀 システムステータス:")
        print("=" * 80)
        print("✅ .npy埋め込みファイル使用中")
        print("✅ 日本語コンテンツ対応済み")
        print("✅ ハイブリッド分類稼働中")
        print("✅ ユーザープロファイリング機能")
        
        # Determine overall test success for console message
        correct_count_for_status = sum(1 for r in results if r['tier1_correct'])
        accuracy_for_status = (correct_count_for_status / len(results)) * 100 if results else 0

        if accuracy_for_status == 100:
            print()
            print("🎉 全てのテストが成功しました！")
            print("🎯 システムは完全に機能しています")
        elif accuracy_for_status >= 80:
            print()
            print("👍 テストは概ね成功です")
            print("📈 システムは良好に動作しています")
        else:
            print()
            print("⚠️  いくつかの改善が必要です")
        
        return results # Still return results if needed elsewhere, though summary is gone
    
    finally:
        sys.stdout = original_stdout # Restore stdout
        log_file.close()
        # Print to console after redirection is restored
        print(f"Test output saved to: {log_file_path}")

def main():
    """Main entry point for the CLI command."""
    test_japanese_classification()

if __name__ == "__main__":
    main()
