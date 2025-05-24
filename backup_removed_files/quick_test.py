#!/usr/bin/env python3

from enhanced_hybrid_classifier_v2 import enhanced_classify_content

# Test with a simple automotive text
test_text = 'Looking for a reliable family SUV with good safety features and fuel efficiency'
result = enhanced_classify_content(test_text)

print('=== ENHANCED CLASSIFICATION RESULTS ===')

print('Top 2 Tier 2 Categories:')
for i, cat in enumerate(result.tier2_categories[:2], 1):
    print(f'{i}. {cat["name"]} (Confidence: {cat["confidence"]:.1%})')

print('')
print('User Profile:')
print('Age Range:', result.user_profile.age_range)
print('Geekiness Level:', result.user_profile.geekiness_level, '/10')
print('Interests:', result.user_profile.interests)
print('Content Sophistication:', result.user_profile.sophistication)
print('Likely Behaviors:', result.user_profile.likely_behaviors)
print('Profile Confidence:', f'{result.user_profile.confidence:.1%}')

print('')
print('Content Analysis:')
for key, value in result.content_analysis.items():
    print(f'{key}: {value}')
