#!/usr/bin/env python3
"""
Enhanced Hybrid IAB Classification System v2

This version focuses on:
1. Returning the two most potential Tier 2 categories
2. Advanced user profile estimation (demographics, geekiness, etc.)
3. Better domain detection even without OpenAI API
4. More sophisticated mock classification for testing
"""

import json
import re
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime

# Import from our existing toolkit
try:
    from iab_toolkit._gpt import _load_taxonomy, _get_client
    from iab_toolkit.models import CategoryResult
except ImportError:
    print("Warning: IAB toolkit not available, using simplified version")

class UserProfile:
    """Represents a user profile with demographics and interests."""
    
    def __init__(self):
        self.age_range: str = "unknown"
        self.geekiness_level: int = 5  # 1-10 scale
        self.sophistication: str = "intermediate"  # basic, intermediate, advanced
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "age_range": self.age_range,
            "geekiness_level": self.geekiness_level,
            "content_sophistication": self.sophistication
        }

class EnhancedClassificationResult:
    """Enhanced result focusing on Tier 2 categories with user profiling."""
    
    def __init__(self):
        self.tier2_categories: List[Dict[str, Any]] = []
        self.user_profile: UserProfile = UserProfile()
        self.content_analysis: Dict[str, Any] = {}

def load_taxonomy_data() -> List[Dict[str, Any]]:
    """Load taxonomy data with fallback options."""
    try:
        return _load_taxonomy()
    except:
        # Fallback to direct file loading
        try:
            taxonomy_path = Path(__file__).parent / "iab_toolkit" / "data" / "taxonomy.json"
            with open(taxonomy_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data and data[0].get("unique_id") == "Unique ID":
                    data = data[1:]
                return data
        except:
            print("Warning: Could not load taxonomy data")
            return []

def analyze_content_language_and_style(text: str) -> Dict[str, Any]:
    """Analyze content for language, style, and technical sophistication."""
    
    # Language detection
    japanese_chars = len(re.findall(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]', text))
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    total_chars = len(text)
    
    if japanese_chars > english_chars:
        primary_language = "japanese"
    else:
        primary_language = "english"
    
    # Enhanced technical sophistication analysis
    technical_terms = [
        # Universal technical terms
        'technology', 'system', 'performance', 'specifications', 'analysis',
        'optimization', 'implementation', 'framework', 'algorithm', 'data',
        
        # Automotive technical terms
        'hybrid', 'engine', 'safety', 'features', 'navigation', 'infotainment',
        'transmission', 'acceleration', 'mpg', 'horsepower',
        
        # Technology terms
        'machine learning', 'neural', 'pytorch', 'cuda', 'ai', 'software',
        'programming', 'architecture', 'digital', 'app',
        
        # Business terms
        'strategic', 'investment', 'portfolio', 'market', 'financial',
        'revenue', 'analysis', 'growth', 'budget',
        
        # Health/Beauty terms
        'dermatology', 'organic', 'formulation', 'clinical', 'therapeutic',
        
        # Japanese technical terms
        'テクノロジー', 'システム', 'パフォーマンス', 'ハイブリッド', 'エンジン',
        'デジタル', 'ソフトウェア', 'アプリケーション'
    ]
    
    tech_score = sum(1 for term in technical_terms if term.lower() in text.lower())
    
    # Content tone analysis
    informational_words = ['は', 'です', 'について', 'features', 'specifications', 'performance']
    promotional_words = ['best', 'amazing', 'perfect', '最高', '素晴らしい', 'おすすめ']
    
    info_score = sum(1 for word in informational_words if word in text)
    promo_score = sum(1 for word in promotional_words if word in text)
    
    if info_score > promo_score:
        tone = "informational"
    elif promo_score > info_score:
        tone = "promotional" 
    else:
        tone = "neutral"
    
    # Technical level assessment
    if tech_score >= 5:
        tech_level = "advanced"
    elif tech_score >= 2:
        tech_level = "intermediate"
    else:
        tech_level = "basic"
    
    return {
        "primary_language": primary_language,
        "tone": tone,
        "technical_level": tech_level,
        "technical_term_count": tech_score,
        "character_distribution": {
            "japanese": japanese_chars,
            "english": english_chars,
            "total": total_chars
        }
    }

def estimate_user_profile(text: str, content_analysis: Dict[str, Any], domain: str = "Automotive") -> UserProfile:
    """Estimate user demographics based on content - simplified version."""
    
    profile = UserProfile()
    text_lower = text.lower()
    
    # Enhanced age estimation based on content style and sophistication
    if any(word in text_lower for word in ['family', 'ファミリー', 'children', '子供', 'parent']):
        profile.age_range = "30-45"
    elif any(word in text_lower for word in ['performance', 'racing', 'speed', 'optimization']):
        profile.age_range = "25-35"
    elif any(word in text_lower for word in ['luxury', 'premium', '高級', 'investment', 'portfolio']):
        profile.age_range = "35-55"
    elif any(word in text_lower for word in ['student', 'learning', 'university', '学生', '大学']):
        profile.age_range = "18-25"
    else:
        profile.age_range = "25-45"
    
    # Enhanced geekiness level based on content complexity
    tech_level = content_analysis.get('technical_level', 'basic')
    tech_count = content_analysis.get('technical_term_count', 0)
    
    # Domain-specific geekiness scoring
    if domain == "Technology & Computing":
        base_geekiness = 7
    elif domain == "Business and Finance":
        base_geekiness = 6
    elif domain == "Education":
        base_geekiness = 5
    elif domain == "Medical Health":
        base_geekiness = 5
    else:
        base_geekiness = 4
    
    if any(word in text_lower for word in ['machine learning', 'neural', 'pytorch', 'cuda', 'architecture']):
        profile.geekiness_level = min(10, base_geekiness + 3)
    elif tech_level == "advanced" or tech_count >= 5:
        profile.geekiness_level = min(10, base_geekiness + 2)
    elif tech_level == "intermediate" or tech_count >= 2:
        profile.geekiness_level = min(10, base_geekiness + 1)
    else:
        profile.geekiness_level = base_geekiness
    
    # Sophistication level based on vocabulary and structure
    if content_analysis.get('tone') == 'informational' and tech_count >= 3:
        profile.sophistication = "advanced"
    elif tech_count >= 1 or len(text.split()) > 50:
        profile.sophistication = "intermediate"  
    else:
        profile.sophistication = "basic"
    
    return profile

def intelligent_domain_detection(text: str) -> str:
    """Smart domain detection even without embedding API."""
    
    # Domain keywords mapping (using correct taxonomy names)
    domain_keywords = {
        'Automotive': [
            'car', 'vehicle', 'toyota', 'honda', 'suv', 'sedan', 'truck', 'auto',
            '車', 'トヨタ', 'ホンダ', '自動車', 'ドライブ', 'エンジン',
            'hybrid', 'fuel', 'safety', 'driving', 'automotive', 'rav4',
            'steering', 'brake', 'transmission', 'mpg', 'acceleration'
        ],
        'Technology & Computing': [
            'computer', 'software', 'app', 'digital', 'ai', 'tech', 'algorithm',
            'コンピューター', 'ソフトウェア', 'アプリ', 'デジタル', 'テクノロジー',
            'machine learning', 'neural', 'pytorch', 'framework', 'programming',
            'data', 'analysis', 'optimization', 'implementation', 'architecture'
        ],
        'Medical Health': [
            'health', 'medical', 'doctor', 'medicine', 'fitness', 'wellness',
            '健康', '医療', '医者', '病院', 'フィットネス',
            'skincare', 'beauty', 'organic', 'natural', 'cosmetics',
            'sensitive', 'dermatology', 'treatment', 'therapy'
        ],
        'Business and Finance': [
            'business', 'finance', 'money', 'investment', 'economy', 'market',
            'ビジネス', '金融', 'お金', '投資', '経済',
            'portfolio', 'strategic', 'analysis', 'growth', 'revenue',
            'profit', 'financial', 'budget', 'capital', 'assets'
        ],
        'Education': [
            'education', 'school', 'learning', 'student', 'university', 'academic',
            '教育', '学校', '学習', '学生', '大学',
            'curriculum', 'study', 'research', 'knowledge', 'teaching',
            'training', 'course', 'degree', 'scholarship'
        ],
        'Style & Fashion': [
            'fashion', 'style', 'clothing', 'beauty', 'makeup', 'skincare',
            'ファッション', 'スタイル', '美容', 'メイク',
            'designer', 'trends', 'outfit', 'accessories', 'cosmetics'
        ]
    }
    
    text_lower = text.lower()
    domain_scores = {}
    
    for domain, keywords in domain_keywords.items():
        score = sum(2 if keyword in text_lower else 0 for keyword in keywords)
        # Bonus for exact matches
        exact_matches = sum(1 for keyword in keywords if keyword in text_lower)
        domain_scores[domain] = score + exact_matches
    
    if not domain_scores or max(domain_scores.values()) == 0:
        return "Automotive"  # Default fallback
    
    best_domain = max(domain_scores.keys(), key=lambda k: domain_scores[k])
    
    return best_domain

def get_tier2_categories_for_domain(domain: str) -> List[Dict[str, Any]]:
    """Get all Tier 2 categories for a specific domain."""
    taxonomy = load_taxonomy_data()
    
    tier2_categories = []
    for entry in taxonomy:
        if (entry.get('tier_1') == domain and 
            entry.get('tier_2') and 
            not entry.get('tier_3')):  # Only Tier 2 entries
            tier2_categories.append(entry)
    
    return tier2_categories

def format_tier2_for_gpt(tier2_categories: List[Dict[str, Any]]) -> str:
    """Format Tier 2 categories in ultra-compact format."""
    lines = []
    for entry in tier2_categories:
        lines.append(f"{entry['unique_id']}:{entry['name']}")
    return "\n".join(lines)

def intelligent_tier2_classification(text: str, tier2_categories: List[Dict[str, Any]], 
                                   content_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Smart Tier 2 classification using content analysis."""
    
    # Automotive-specific Tier 2 scoring
    automotive_tier2_scoring = {
        'Auto Body Styles': [
            'suv', 'sedan', 'truck', 'coupe', 'hatchback', 'convertible',
            'SUV', 'セダン', 'トラック', 'クーペ', 'ハッチバック'
        ],
        'Auto Type': [
            'luxury', 'budget', 'hybrid', 'electric', 'green', 'concept',
            '高級', 'ラグジュアリー', 'ハイブリッド', '電気', 'エコ'
        ],
        'Auto Technology': [
            'technology', 'navigation', 'safety', 'smart', 'digital',
            'テクノロジー', 'ナビゲーション', '安全', 'スマート', 'デジタル'
        ],
        'Auto Safety': [
            'safety', 'security', 'protection', 'airbag', 'brake',
            '安全', 'セキュリティ', '保護', 'エアバッグ', 'ブレーキ'
        ],
        'Auto Buying and Selling': [
            'price', 'cost', 'buy', 'sell', 'purchase', 'deal',
            '価格', 'コスト', '購入', '販売', 'お得'
        ]
    }
    
    text_lower = text.lower()
    tier2_scores = []
    
    for category in tier2_categories:
        category_name = category['name']
        score = 0.5  # Base score
        
        # Check if we have specific scoring rules
        if category_name in automotive_tier2_scoring:
            keywords = automotive_tier2_scoring[category_name]
            keyword_matches = sum(2 if keyword in text_lower else 0 for keyword in keywords)
            score += keyword_matches * 0.1
        
        # Boost score based on content analysis
        if content_analysis.get('technical_level') == 'advanced' and 'Technology' in category_name:
            score += 0.2
            
        if content_analysis.get('tone') == 'informational' and 'Body Styles' in category_name:
            score += 0.15
        
        # Vehicle type specific boosting
        if 'rav4' in text_lower and 'Body Styles' in category_name:
            score += 0.3  # RAV4 is primarily about body style (SUV)
            
        if any(word in text_lower for word in ['safety', '安全']) and 'Safety' in category_name:
            score += 0.25
        
        tier2_scores.append({
            'id': category['unique_id'],
            'name': category_name,
            'score': score,  # Keep score for sorting
            'tier_1': category.get('tier_1'),
            'tier_2': category_name
        })
    
    # Sort by score and return top 2
    tier2_scores.sort(key=lambda x: x['score'], reverse=True)
    
    # Remove score from final output
    final_results = []
    for item in tier2_scores[:2]:
        final_results.append({
            'id': item['id'],
            'name': item['name'],
            'tier_1': item['tier_1'],
            'tier_2': item['tier_2']
        })
    
    return final_results

def save_classification_to_json(text: str, result: EnhancedClassificationResult, 
                               filename: str = None, sample_name: str = "text_sample") -> str:
    """Save classification result to JSON file.
    
    Args:
        text: Original text that was classified
        result: EnhancedClassificationResult object
        filename: Optional custom filename (auto-generated if None)
        sample_name: Name identifier for the sample
        
    Returns:
        str: Path to the saved JSON file
    """
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"classification_result_{timestamp}.json"
    
    profile_dict = result.user_profile.to_dict()
    
    output_data = {
        "metadata": {
            "system_version": "Simplified IAB Classification System v2",
            "classification_date": datetime.now().isoformat(),
            "sample_name": sample_name,
            "features": [
                "No confidence percentages in output",
                "3-metric user profile only",
                "Tier 2 category focus",
                "Offline processing"
            ]
        },
        "input": {
            "sample_name": sample_name,
            "content_preview": text[:200] + "..." if len(text) > 200 else text,
            "content_length": len(text)
        },
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
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    return filename

def enhanced_classify_with_json_output(text: str, output_filename: str = None, 
                                     sample_name: str = "text_sample") -> tuple:
    """Enhanced classification with automatic JSON output.
    
    Args:
        text: Text to classify
        output_filename: Optional custom filename for JSON output
        sample_name: Name identifier for the sample
        
    Returns:
        tuple: (EnhancedClassificationResult, json_filename)
    """
    # Perform classification
    result = enhanced_classify_content(text)
    
    # Save to JSON
    json_filename = save_classification_to_json(text, result, output_filename, sample_name)
    
    return result, json_filename

def enhanced_classify_content(text: str) -> EnhancedClassificationResult:
    """
    Enhanced classification focusing on Tier 2 categories and user profiling.
    """
    result = EnhancedClassificationResult()
    
    print("=== ENHANCED HYBRID CLASSIFICATION ===")
    
    # Step 1: Content analysis
    print("Step 1: Analyzing content style and language...")
    content_analysis = analyze_content_language_and_style(text)
    result.content_analysis = content_analysis
    
    # Step 2: Domain detection
    print("Step 2: Detecting primary domain...")
    primary_domain = intelligent_domain_detection(text)
    print(f"Primary domain: {primary_domain}")
    
    # Step 3: Get Tier 2 categories for the domain
    print("Step 3: Getting Tier 2 categories...")
    tier2_categories = get_tier2_categories_for_domain(primary_domain)
    print(f"Found {len(tier2_categories)} Tier 2 categories in {primary_domain}")
    
    # Step 4: Classify into Tier 2 categories
    print("Step 4: Intelligent Tier 2 classification...")
    top_tier2 = intelligent_tier2_classification(text, tier2_categories, content_analysis)
    result.tier2_categories = top_tier2
    
    # Step 5: User profile estimation
    print("Step 5: Estimating user profile...")
    user_profile = estimate_user_profile(text, content_analysis, primary_domain)
    result.user_profile = user_profile
    
    return result

def test_enhanced_classifier():
    """Test the enhanced classifier with the Japanese Toyota RAV4 text."""
    
    # Load test text
    try:
        with open('japanese_text_sample.txt', 'r', encoding='utf-8') as f:
            text = f.read()
    except:
        text = """トヨタRAV4は、トヨタ自動車が製造・販売しているSUVです。1994年に初代モデルが発売され、現在は5代目となっています。RAV4は「Recreational Active Vehicle with 4-wheel drive」の略称で、レクリエーション活動にも対応できる四輪駆動車というコンセプトで開発されました。

最新のRAV4は、力強いデザインと優れた燃費性能を両立しています。ハイブリッドモデルも用意されており、環境性能にも配慮された設計となっています。インテリアは高品質な素材を使用し、快適な乗り心地を提供します。

安全性能では、Toyota Safety Sense 2.0を標準装備し、プリクラッシュセーフティシステムや歩行者検知機能など、先進の安全技術が搭載されています。オフロード走行にも対応しており、アウトドア愛好家にも人気の高い車種です。

価格帯は約300万円から500万円程度で、ファミリー層からアクティブなライフスタイルを楽しむユーザーまで幅広く支持されています。"""
    
    print(f"Testing with text: {text[:100]}...")
    print()
    
    # Run enhanced classification
    result = enhanced_classify_content(text)
    
    # Display results
    print("\n=== TOP 2 TIER 2 CATEGORIES ===")
    for i, category in enumerate(result.tier2_categories, 1):
        print(f"{i}. {category['name']} (ID: {category['id']})")
        print(f"   Full Path: {category['tier_1']} > {category['tier_2']}")
        print()
    
    print("=== USER PROFILE ANALYSIS ===")
    profile_dict = result.user_profile.to_dict()
    for key, value in profile_dict.items():
        if isinstance(value, list):
            print(f"{key.replace('_', ' ').title()}: {', '.join(value)}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")
    print()
    
    print("=== CONTENT ANALYSIS ===")
    for key, value in result.content_analysis.items():
        if isinstance(value, dict):
            continue  # Skip nested dicts for cleaner output
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    # Additional insights
    print("\n=== CLASSIFICATION INSIGHTS ===")
    print(f"Primary Language: {result.content_analysis.get('primary_language', 'unknown')}")
    print(f"Content Sophistication: {result.content_analysis.get('technical_level', 'unknown')}")
    
    # Keywords that influenced classification
    automotive_keywords_found = []
    text_lower = text.lower()
    key_automotive_terms = ['rav4', 'toyota', 'suv', '自動車', 'ハイブリッド', '安全']
    for term in key_automotive_terms:
        if term in text_lower:
            automotive_keywords_found.append(term)
    
    print(f"Key Automotive Keywords Found: {', '.join(automotive_keywords_found)}")

if __name__ == "__main__":
    print("Enhanced Hybrid IAB Classification System v2")
    print("=" * 50)
    print("Features:")
    print("✓ Focus on top 2 Tier 2 categories")
    print("✓ Advanced user profile estimation")
    print("✓ Intelligent domain detection (no API required)")
    print("✓ Content sophistication analysis")
    print("✓ Multilingual support (Japanese/English)")
    print()
    
    test_enhanced_classifier()
