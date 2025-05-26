#!/usr/bin/env python3
"""
Test the optimized detector with the Japanese beauty content specifically.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from optimized_tier1_detector import OptimizedTier1Detector

def test_japanese_beauty():
    """Test with the specific Japanese beauty content that was misclassified."""
    
    detector = OptimizedTier1Detector()
    
    # The Japanese beauty text that should be Style & Fashion
    japanese_text = """オーガニック化粧品ブランド「ナチュラルビューティー」は、敏感肌の方にも安心してお使いいただける自然由来の美容製品を提供しています。特に人気の高いスキンケアシリーズは、化学合成成分を一切使用せず、植物エキスのみで構成されています。

主力商品である保湿クリームは、ホホバオイルとシアバターを主成分とし、乾燥肌や敏感肌の改善に効果的です。皮膚科医による臨床試験も実施されており、安全性と効果の両方が科学的に証明されています。

また、メイクアップ製品も充実しており、ファンデーションやリップスティックなども天然成分で作られています。環境に配慮したパッケージングを採用し、持続可能な美容をコンセプトとしています。

価格帯は3,000円から15,000円程度で、健康志向の高い女性や、化学成分に敏感な方々から支持されています。オンラインストアでの販売が中心で、全国どこでも購入が可能です。"""
    
    print("🧪 TESTING JAPANESE BEAUTY CONTENT CLASSIFICATION")
    print("="*60)
    print("Expected: Style & Fashion")
    print("Previous result: Medical Health")
    print()
    print("Text content (translated):")
    print("Organic cosmetics brand providing natural beauty products,")
    print("skincare series, moisturizing cream, makeup products,")
    print("foundation, lipstick, sustainable beauty concept...")
    print()
    
    # Test classification
    domain, confidence = detector.detect_tier1_domain(japanese_text)
    
    print(f"🔍 CLASSIFICATION RESULT:")
    print(f"   Detected: {domain}")
    print(f"   Confidence: {confidence:.3f}")
    print()
    
    if domain == "Style & Fashion":
        print("✅ SUCCESS! Correctly classified as Style & Fashion")
    elif domain == "Medical Health":
        print("❌ STILL WRONG! Still classifying as Medical Health")
        print("   The optimization didn't fix the core issue")
    else:
        print(f"⚠️  DIFFERENT RESULT: Now classifying as {domain}")
        print("   This might be better or worse than Medical Health")
    
    # Let's also get the top 3 matches to see the competition
    print(f"\n🏆 Getting top matches to understand the decision...")
    
    domain, confidence, top_matches = detector.detect_tier1_domain_with_top_matches(japanese_text, top_n=5)
    
    print(f"\n📊 TOP 5 CLASSIFICATION RESULTS:")
    for i, (match_domain, match_score) in enumerate(top_matches, 1):
        icon = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "📍"
        print(f"   {icon} {i}. {match_domain}: {match_score:.3f}")
    
    print(f"\n📋 ANALYSIS:")
    if top_matches[0][0] == "Style & Fashion":
        print("✅ Style & Fashion is the clear winner!")
        if len(top_matches) > 1:
            second_place = top_matches[1]
            gap = top_matches[0][1] - second_place[1]
            print(f"   Gap to 2nd place ({second_place[0]}): {gap:.3f}")
            if gap < 0.05:
                print("   ⚠️  Close competition - small margin")
            else:
                print("   ✅ Confident classification - good margin")
    
    return domain, confidence

if __name__ == "__main__":
    test_japanese_beauty()
