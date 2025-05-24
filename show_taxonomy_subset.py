#!/usr/bin/env python3
"""Show what the focused taxonomy subset looks like."""

from hybrid_classifier_v2 import get_taxonomy_subset_for_tier1, format_taxonomy_for_gpt

print("=== AUTOMOTIVE TAXONOMY SUBSET ===")
automotive_subset = get_taxonomy_subset_for_tier1("Automotive")
print(f"Found {len(automotive_subset)} automotive categories")

formatted = format_taxonomy_for_gpt(automotive_subset)
print("\nFormatted for GPT:")
print("=" * 50)
print(formatted)
print("=" * 50)
print(f"\nTotal characters: {len(formatted)}")
print("This is MUCH smaller than the full taxonomy file!")
