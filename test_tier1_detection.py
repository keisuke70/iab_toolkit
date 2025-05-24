#!/usr/bin/env python3
"""Test tier 1 category detection."""

from iab_toolkit._gpt import _load_taxonomy

taxonomy = _load_taxonomy()
print(f'Loaded {len(taxonomy)} taxonomy entries')

# Test tier 1 detection
tier1_categories = []
for entry in taxonomy:
    if (entry.get('tier_2') is None and 
        entry.get('tier_3') is None and 
        entry.get('tier_4') is None):
        tier1_categories.append(entry)

print(f'Found {len(tier1_categories)} Tier 1 categories:')
for cat in tier1_categories[:10]:
    print(f'  {cat["unique_id"]}: {cat["name"]}')

print('\nAll Tier 1 categories:')
for cat in tier1_categories:
    print(f'  - {cat["name"]} (ID: {cat["unique_id"]})')
