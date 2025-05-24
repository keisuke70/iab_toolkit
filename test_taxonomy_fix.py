#!/usr/bin/env python3
"""Test the taxonomy lookup functionality."""

from iab_toolkit._gpt import _load_taxonomy, _find_taxonomy_entry

print('=== TESTING TAXONOMY LOOKUP ===')

# Load taxonomy data
taxonomy = _load_taxonomy()
print(f'Loaded {len(taxonomy)} taxonomy entries')

# Test finding automotive categories
test_categories = ['SUV', 'Automotive', 'Auto Body Styles', 'Off-Road Vehicles']

for category in test_categories:
    entry = _find_taxonomy_entry(category)
    if entry:
        print(f'\nFound {category}:')
        print(f'  ID: {entry["unique_id"]}')
        print(f'  Name: {entry["name"]}')
        print(f'  Tier 1: {entry.get("tier_1")}')
        print(f'  Tier 2: {entry.get("tier_2")}')
        print(f'  Tier 3: {entry.get("tier_3")}')
        print(f'  Tier 4: {entry.get("tier_4")}')
    else:
        print(f'\nNOT FOUND: {category}')

# Test the category parsing logic
print('\n=== TESTING CATEGORY PARSING ===')
from iab_toolkit._gpt import _parse_categories

# Mock GPT response with real category names
mock_gpt_response = '''[
    {"id": 123, "name": "SUV", "confidence": 0.95},
    {"id": 456, "name": "Automotive", "confidence": 0.85},
    {"id": 789, "name": "Auto Body Styles", "confidence": 0.75}
]'''

results = _parse_categories(mock_gpt_response, 3)
print(f'Parsed {len(results)} categories:')
for result in results:
    print(f'\nCategory: {result.name}')
    print(f'  ID: {result.id}')
    print(f'  Score: {result.score}')
    print(f'  Tier 1: {result.tier_1}')
    print(f'  Tier 2: {result.tier_2}')
    print(f'  Tier 3: {result.tier_3}')
    print(f'  Tier 4: {result.tier_4}')
