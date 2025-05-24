#!/usr/bin/env python3
"""Demonstrate the two-stage classification process."""

# Simulate what GPT might return for automotive content
print("=== STEP 1: What GPT Returns ===")
gpt_response = '''[
    {"id": 999, "name": "SUV", "confidence": 0.95},
    {"id": 888, "name": "Automotive", "confidence": 0.85},
    {"id": 777, "name": "Off-Road Vehicles", "confidence": 0.75}
]'''

print("GPT's raw response (with fake IDs):")
print(gpt_response)

print("\n=== STEP 2: Local Taxonomy Lookup ===")
from iab_toolkit._gpt import _find_taxonomy_entry

# For each category GPT suggested, look up the real taxonomy data
categories = ["SUV", "Automotive", "Off-Road Vehicles"]

for category in categories:
    entry = _find_taxonomy_entry(category)
    if entry:
        print(f"\nCategory: {category}")
        print(f"  GPT suggested ID: 999/888/777 (fake)")
        print(f"  Real taxonomy ID: {entry['unique_id']}")
        print(f"  Real name: {entry['name']}")
        print(f"  Tier 1: {entry.get('tier_1')}")
        print(f"  Tier 2: {entry.get('tier_2')}")
        print(f"  Tier 3: {entry.get('tier_3')}")
        print(f"  Tier 4: {entry.get('tier_4')}")

print("\n=== STEP 3: The Magic Happens ===")
print("The system replaces GPT's fake IDs with real taxonomy data!")
