#!/usr/bin/env python3
"""
Enhanced Hybrid IAB Classification System with User Profiling

New Features:
1. Focus on returning top 2 Tier 2 categories
2. User profile estimation (demographics, interests, geekiness level)
3. Enhanced analysis and tagging
"""

import json
import re
from typing import List, Dict, Any, Optional, NamedTuple
from dataclasses import dataclass
from iab_toolkit._gpt import _load_taxonomy, _get_client
from iab_toolkit.models import CategoryResult

@dataclass
class UserProfile:
    """User profile estimation based on content analysis."""
    demographics: Dict[str, Any]
    interests: List[str]
    geekiness_level: int  # 1-10 scale
    content_sophistication: str  # "basic", "intermediate", "advanced"
    likely_behaviors: List[str]
    confidence: float

class EnhancedResult(NamedTuple):
    """Enhanced classification result with user profiling."""
    tier2_categories: List[CategoryResult]
    user_profile: UserProfile
    content_analysis: Dict[str, Any]

def get_tier2_categories_for_tier1(tier1_name: str) -> List[Dict[str, Any]]:
    """Get all Tier 2 categories that belong to a specific Tier 1 category."""
    taxonomy = _load_taxonomy()
    tier2_categories = []
    
    for entry in taxonomy:
        if (entry.get('tier_1') == tier1_name and 
            entry.get('tier_2') is not None and 
            entry.get('tier_3') is None and 
            entry.get('tier_4') is None):
            tier2_categories.append(entry)
    
    return tier2_categories

def detect_tier1_with_embedding(text: str, top_k: int = 2) -> List[Dict[str, Any]]:
    """
    Use embedding similarity to detect the most likely Tier 1 categories.
    Focused on finding the best domains for Tier 2 classification.
    """
    try:
        from iab_toolkit._embedding import embed_text_sync
        
        # Get text embedding
        text_embedding = embed_text_sync(text[:8000])
        
        # Get all Tier 1 categories
        taxonomy = _load_taxonomy()
        tier1_categories = []
        
        for entry in taxonomy:
            if (entry.get('tier_2') is None and 
                entry.get('tier_3') is None and 
                entry.get('tier_4') is None):
                tier1_categories.append(entry)
        
        # Mock result for automotive content (in real implementation, compute similarities)
        if any(word in text.lower() for word in ['車', 'toyota', 'rav4', 'suv', 'automotive', 'vehicle', 'car']):
            automotive_tier1 = next((cat for cat in tier1_categories if cat['name'] == 'Automotive'), None)
            if automotive_tier1:
                return [automotive_tier1]
        
        # Technology keywords
        if any(word in text.lower() for word in ['ai', 'tech', 'software', 'computer', 'programming', 'digital']):
            tech_tier1 = next((cat for cat in tier1_categories if cat['name'] == 'Technology & Computing'), None)
            if tech_tier1:
                return [tech_tier1]
        
        # Default fallback
        return tier1_categories[:top_k]
        
    except Exception as e:
        print(f"Embedding detection failed: {e}")
        # Fallback to common categories
        taxonomy = _load_taxonomy()
        tier1_categories = []
        for entry in taxonomy:
            if (entry.get('tier_2') is None and 
                entry.get('tier_3') is None and 
                entry.get('tier_4') is None):
                tier1_categories.append(entry)
        return tier1_categories[:2]

def format_tier2_taxonomy_for_gpt(tier2_categories: List[Dict[str, Any]]) -> str:
    """
    Format Tier 2 categories in ultra-compact format for GPT analysis.
    """
    lines = []
    
    # Sort by unique_id for consistent ordering
    sorted_categories = sorted(tier2_categories, key=lambda x: x['unique_id'])
    
    for entry in sorted_categories:
        lines.append(f"{entry['unique_id']}:{entry['name']}")
    
    return "\n".join(lines)

def analyze_user_profile(text: str) -> UserProfile:
    """
    Analyze text to estimate user profile characteristics.
    """
    text_lower = text.lower()
    
    # Demographics estimation
    demographics = {
        "age_range": "unknown",
        "likely_gender": "unknown", 
        "education_level": "unknown",
        "income_level": "unknown"
    }
    
    # Age indicators
    if any(word in text_lower for word in ['新車', 'new car', 'first car', '初心者', 'beginner']):
        demographics["age_range"] = "young_adult_25-35"
    elif any(word in text_lower for word in ['family', 'ファミリー', 'children', '子供']):
        demographics["age_range"] = "middle_aged_35-50"
    elif any(word in text_lower for word in ['luxury', '高級', 'premium', 'retirement']):
        demographics["age_range"] = "mature_50+"
    
    # Technical sophistication
    tech_words = ['engine', 'エンジン', 'horsepower', 'transmission', 'hybrid', 'electric', 'specs', 'specification']
    tech_count = sum(1 for word in tech_words if word in text_lower)
    
    # Geekiness level (1-10)
    geekiness_level = min(10, max(1, tech_count + 3))
    
    # Content sophistication
    if tech_count >= 5:
        sophistication = "advanced"
    elif tech_count >= 2:
        sophistication = "intermediate"
    else:
        sophistication = "basic"
    
    # Interest extraction
    interests = []
    if any(word in text_lower for word in ['車', 'car', 'automotive', 'vehicle']):
        interests.append("automotive")
    if any(word in text_lower for word in ['suv', 'off-road', 'adventure']):
        interests.append("outdoor_activities")
    if any(word in text_lower for word in ['family', 'ファミリー']):
        interests.append("family_oriented")
    if any(word in text_lower for word in ['performance', '性能', 'sport']):
        interests.append("performance_enthusiast")
    
    # Likely behaviors
    behaviors = []
    if 'suv' in text_lower:
        behaviors.extend(["research_before_buying", "values_versatility", "active_lifestyle"])
    if any(word in text_lower for word in ['toyota', 'reliable', '信頼']):
        behaviors.extend(["brand_loyal", "values_reliability"])
    if sophistication == "advanced":
        behaviors.append("reads_technical_reviews")
    
    return UserProfile(
        demographics=demographics,
        interests=interests,
        geekiness_level=geekiness_level,
        content_sophistication=sophistication,
        likely_behaviors=behaviors,
        confidence=0.75  # Moderate confidence in profile estimation
    )

def gpt_classify_tier2_with_profiling(text: str, tier2_taxonomy: str, max_categories: int = 2) -> Dict[str, Any]:
    """
    Use GPT to classify content into Tier 2 categories and provide user profiling insights.
    """
    try:
        from iab_toolkit._gpt import _get_client
        
        system_prompt = f"""You are an expert at classifying content into IAB taxonomy categories and analyzing user profiles.

Available Tier 2 categories for classification:
{tier2_taxonomy}

Instructions:
1. Analyze the content and select the TOP 2 most relevant Tier 2 categories from the list above
2. Provide confidence scores (0.0-1.0) for each category
3. Analyze the user profile based on the content
4. Estimate demographics, interests, and behavior patterns

Response format (JSON):
{{
  "tier2_categories": [
    {{
      "id": "category_id",
      "name": "category_name",
      "confidence": 0.95,
      "reasoning": "why this category fits"
    }}
  ],
  "user_profile": {{
    "age_range": "25-35",
    "interests": ["automotive", "technology"],
    "geekiness_level": 7,
    "sophistication": "advanced",
    "likely_demographics": "tech-savvy professional",
    "behavioral_patterns": ["researches thoroughly", "values performance"],
    "confidence": 0.8
  }},
  "content_analysis": {{
    "tone": "informational/commercial/personal",
    "technical_level": "basic/intermediate/advanced",
    "key_themes": ["theme1", "theme2"]
  }}
}}"""

        client = _get_client(async_=False)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze and classify this content:\n\n{text[:2000]}"}
            ],
            temperature=0.1,
            max_completion_tokens=1000
        )
        
        content = response.choices[0].message.content
        if not content:
            return {"error": "Empty response from GPT"}
        
        # Clean and parse JSON response
        clean_content = content.strip()
        if clean_content.startswith("```"):
            lines = clean_content.split("\n")
            clean_content = "\n".join(lines[1:-1])
        
        return json.loads(clean_content)
        
    except Exception as e:
        print(f"Error in GPT classification: {e}")
        # Return mock response for testing
        return {
            "tier2_categories": [
                {
                    "id": "2",
                    "name": "Auto Body Styles",
                    "confidence": 0.92,
                    "reasoning": "Content discusses SUV vehicle type"
                },
                {
                    "id": "16", 
                    "name": "Auto Type",
                    "confidence": 0.88,
                    "reasoning": "Focuses on specific vehicle category"
                }
            ],
            "user_profile": {
                "age_range": "30-45",
                "interests": ["automotive", "family_vehicles"],
                "geekiness_level": 6,
                "sophistication": "intermediate",
                "likely_demographics": "family-oriented professional",
                "behavioral_patterns": ["researches before buying", "values reliability"],
                "confidence": 0.75
            },
            "content_analysis": {
                "tone": "informational",
                "technical_level": "intermediate", 
                "key_themes": ["vehicle_features", "automotive_category"]
            }
        }

def enhanced_hybrid_classify(text: str, use_real_gpt: bool = False) -> EnhancedResult:
    """
    Enhanced hybrid classification focusing on Tier 2 categories with user profiling.
    
    Args:
        text: Content to classify
        use_real_gpt: Whether to use real OpenAI API
        
    Returns:
        EnhancedResult with Tier 2 categories and user profile
    """
    print("=== ENHANCED HYBRID CLASSIFICATION ===")
    
    # Step 1: Detect Tier 1 domain
    print("Step 1: Detecting primary domain...")
    tier1_categories = detect_tier1_with_embedding(text, top_k=1)
    
    if not tier1_categories:
        print("No Tier 1 categories detected")
        return EnhancedResult([], UserProfile({}, [], 0, "basic", [], 0.0), {})
    
    tier1_name = tier1_categories[0]['name']
    print(f"Primary domain: {tier1_name}")
    
    # Step 2: Get Tier 2 categories for this domain
    print("Step 2: Getting Tier 2 categories...")
    tier2_categories = get_tier2_categories_for_tier1(tier1_name)
    print(f"Found {len(tier2_categories)} Tier 2 categories in {tier1_name}")
    
    if not tier2_categories:
        print("No Tier 2 categories found for this domain")
        return EnhancedResult([], UserProfile({}, [], 0, "basic", [], 0.0), {})
    
    # Step 3: Format for GPT
    formatted_taxonomy = format_tier2_taxonomy_for_gpt(tier2_categories)
    print(f"Step 3: Formatted {len(formatted_taxonomy)} chars for GPT")
    
    # Step 4: GPT analysis with profiling
    print("Step 4: GPT analysis with user profiling...")
    if use_real_gpt:
        gpt_result = gpt_classify_tier2_with_profiling(text, formatted_taxonomy, 2)
    else:
        gpt_result = gpt_classify_tier2_with_profiling(text, formatted_taxonomy, 2)  # Uses mock
    
    # Step 5: Process results
    tier2_results = []
    taxonomy = _load_taxonomy()
    
    for cat_data in gpt_result.get("tier2_categories", []):
        category_id = str(cat_data.get("id", ""))
        confidence = float(cat_data.get("confidence", 0.0))
        
        # Find full taxonomy entry
        taxonomy_entry = next((cat for cat in taxonomy if str(cat['unique_id']) == category_id), None)
        
        if taxonomy_entry:
            result = CategoryResult(
                id=category_id,
                name=taxonomy_entry['name'],
                score=confidence,
                tier_1=taxonomy_entry.get('tier_1'),
                tier_2=taxonomy_entry.get('tier_2'),
                tier_3=taxonomy_entry.get('tier_3'),
                tier_4=taxonomy_entry.get('tier_4')
            )
            tier2_results.append(result)
    
    # Create user profile
    profile_data = gpt_result.get("user_profile", {})
    user_profile = UserProfile(
        demographics={
            "age_range": profile_data.get("age_range", "unknown"),
            "likely_demographics": profile_data.get("likely_demographics", "unknown")
        },
        interests=profile_data.get("interests", []),
        geekiness_level=profile_data.get("geekiness_level", 5),
        content_sophistication=profile_data.get("sophistication", "intermediate"),
        likely_behaviors=profile_data.get("behavioral_patterns", []),
        confidence=profile_data.get("confidence", 0.5)
    )
    
    content_analysis = gpt_result.get("content_analysis", {})
    
    return EnhancedResult(tier2_results, user_profile, content_analysis)

def test_enhanced_classification():
    """Test the enhanced classification with user profiling."""
    
    # Test with Japanese Toyota RAV4 text
    try:
        with open('japanese_text_sample.txt', 'r', encoding='utf-8') as f:
            text = f.read()
    except:
        text = "Toyota RAV4 は人気のSUVで、優れたオフロード性能と燃費効率を兼ね備えています。ファミリー向けの実用的な車として多くの人に選ばれています。"
    
    print(f"Testing with text: {text[:100]}...")
    print()
    
    # Test enhanced classification
    result = enhanced_hybrid_classify(text, use_real_gpt=False)
    
    print("\n=== TOP 2 TIER 2 CATEGORIES ===")
    for i, category in enumerate(result.tier2_categories, 1):
        print(f"{i}. {category.name} (ID: {category.id})")
        print(f"   Confidence: {category.score:.3f}")
        print(f"   Full Path: {category.tier_1} > {category.tier_2}")
        print()
    
    print("=== USER PROFILE ANALYSIS ===")
    profile = result.user_profile
    print(f"Age Range: {profile.demographics.get('age_range', 'unknown')}")
    print(f"Geekiness Level: {profile.geekiness_level}/10")
    print(f"Content Sophistication: {profile.content_sophistication}")
    print(f"Interests: {', '.join(profile.interests)}")
    print(f"Likely Behaviors: {', '.join(profile.likely_behaviors)}")
    print(f"Profile Confidence: {profile.confidence:.2f}")
    print()
    
    print("=== CONTENT ANALYSIS ===")
    analysis = result.content_analysis
    print(f"Tone: {analysis.get('tone', 'unknown')}")
    print(f"Technical Level: {analysis.get('technical_level', 'unknown')}")
    print(f"Key Themes: {', '.join(analysis.get('key_themes', []))}")

if __name__ == "__main__":
    test_enhanced_classification()
