#!/usr/bin/env python3
"""Test edge cases and limitations of the taxonomy lookup."""

from iab_toolkit._gpt import _find_taxonomy_entry

print("=== TESTING EDGE CASES ===")

# Test cases that might be problematic
test_cases = [
    "Business Banking & Finance",  # Tier 3 category
    "Angel Investment",           # Tier 4 category
    "Commercial Trucks",          # Tier 3 category
    "vehicle",                    # Generic term
    "car",                        # Generic term
    "Toyota",                     # Brand name (won't be found)
    "RAV4"                       # Model name (won't be found)
]

for category in test_cases:
    entry = _find_taxonomy_entry(category)
    if entry:
        print(f"\n✅ FOUND: {category}")
        print(f"  Real ID: {entry['unique_id']}")
        print(f"  Real name: {entry['name']}")
        print(f"  Tier 1: {entry.get('tier_1')}")
        print(f"  Tier 2: {entry.get('tier_2')}")
        print(f"  Tier 3: {entry.get('tier_3')}")
        print(f"  Tier 4: {entry.get('tier_4')}")
    else:
        print(f"\n❌ NOT FOUND: {category}")

print("\n=== THE REAL LIMITATION ===")
print("GPT can only suggest categories that exist in the taxonomy.")
print("If GPT suggests 'Toyota RAV4', the lookup will fail.")
print("This is why the prompt is crucial - it guides GPT toward valid categories.")
