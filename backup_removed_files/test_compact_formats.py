#!/usr/bin/env python3
"""Test different compact formats for taxonomy data."""

import json
from iab_toolkit._gpt import _load_taxonomy

def get_automotive_subset():
    """Get automotive taxonomy subset."""
    taxonomy = _load_taxonomy()
    automotive_entries = []
    
    for entry in taxonomy:
        if (entry.get('tier_1') == 'Automotive' or 
            (entry.get('tier_1') is None and entry.get('name') == 'Automotive')):
            automotive_entries.append(entry)
    
    return automotive_entries

def format_current(entries):
    """Current format from show_taxonomy_subset.py"""
    lines = ["Available IAB taxonomy categories for this content:", ""]
    
    # Group by tier
    tier1 = [e for e in entries if e.get('tier_2') is None and e.get('tier_3') is None]
    tier2 = [e for e in entries if e.get('tier_2') is not None and e.get('tier_3') is None and e.get('tier_4') is None]
    tier3 = [e for e in entries if e.get('tier_3') is not None and e.get('tier_4') is None]
    
    if tier1:
        lines.append("Tier 1 (General):")
        for entry in tier1:
            lines.append(f"  [{entry['unique_id']}] {entry['name']}")
        lines.append("")
    
    if tier2:
        lines.append("Tier 2 (Specific):")
        for entry in tier2:
            lines.append(f"  [{entry['unique_id']}] {entry['tier_1']} > {entry['name']}")
        lines.append("")
    
    if tier3:
        lines.append("Tier 3 (Very Specific):")
        for entry in tier3:
            lines.append(f"  [{entry['unique_id']}] {entry['tier_1']} > {entry['tier_2']} > {entry['name']}")
        lines.append("")
    
    return "\n".join(lines)

def format_compact_v1(entries):
    """Ultra compact format - remove descriptions, use abbreviations"""
    lines = ["IAB categories:", ""]
    
    # Group by tier
    tier1 = [e for e in entries if e.get('tier_2') is None and e.get('tier_3') is None]
    tier2 = [e for e in entries if e.get('tier_2') is not None and e.get('tier_3') is None and e.get('tier_4') is None]
    tier3 = [e for e in entries if e.get('tier_3') is not None and e.get('tier_4') is None]
    
    if tier1:
        lines.append("T1:")
        for entry in tier1:
            lines.append(f"[{entry['unique_id']}] {entry['name']}")
        lines.append("")
    
    if tier2:
        lines.append("T2:")
        for entry in tier2:
            lines.append(f"[{entry['unique_id']}] {entry['name']}")
        lines.append("")
    
    if tier3:
        lines.append("T3:")
        for entry in tier3:
            lines.append(f"[{entry['unique_id']}] {entry['name']}")
        lines.append("")
    
    return "\n".join(lines)

def format_compact_v2(entries):
    """Single line per entry format"""
    lines = ["IAB taxonomy:"]
    
    for entry in entries:
        tier_info = ""
        if entry.get('tier_3'):
            tier_info = "T3"
        elif entry.get('tier_2'):
            tier_info = "T2"
        else:
            tier_info = "T1"
        
        lines.append(f"{entry['unique_id']}:{tier_info}:{entry['name']}")
    
    return "\n".join(lines)

def format_compact_v3(entries):
    """JSON-like compact format"""
    data = {}
    
    for entry in entries:
        if entry.get('tier_3'):
            tier = "t3"
        elif entry.get('tier_2'):
            tier = "t2"
        else:
            tier = "t1"
        
        if tier not in data:
            data[tier] = {}
        
        data[tier][str(entry['unique_id'])] = entry['name']
    
    # Format as compact string
    lines = ["Categories:"]
    for tier, items in data.items():
        tier_items = [f"{k}:{v}" for k, v in items.items()]
        lines.append(f"{tier.upper()}: {', '.join(tier_items)}")
    
    return "\n".join(lines)

def format_compact_v4(entries):
    """Hierarchical compact format - only show unique parts"""
    lines = ["Automotive taxonomy:"]
    
    # Group by tier
    tier1 = [e for e in entries if e.get('tier_2') is None and e.get('tier_3') is None]
    tier2 = [e for e in entries if e.get('tier_2') is not None and e.get('tier_3') is None and e.get('tier_4') is None]
    tier3 = [e for e in entries if e.get('tier_3') is not None and e.get('tier_4') is None]
    
    if tier1:
        for entry in tier1:
            lines.append(f"[{entry['unique_id']}] {entry['name']}")
    
    if tier2:
        for entry in tier2:
            lines.append(f"  [{entry['unique_id']}] {entry['name']}")
    
    if tier3:
        for entry in tier3:
            lines.append(f"    [{entry['unique_id']}] {entry['name']}")
    
    return "\n".join(lines)

def format_compact_v5(entries):
    """Ultra minimal - just ID and name"""
    lines = []
    for entry in entries:
        lines.append(f"{entry['unique_id']}:{entry['name']}")
    return "\n".join(lines)

def main():
    entries = get_automotive_subset()
    print(f"Testing {len(entries)} automotive entries\n")
    
    formats = [
        ("Current Format", format_current),
        ("Compact V1 (remove descriptions)", format_compact_v1),
        ("Compact V2 (single line)", format_compact_v2),
        ("Compact V3 (JSON-like)", format_compact_v3),
        ("Compact V4 (hierarchical)", format_compact_v4),
        ("Compact V5 (ultra minimal)", format_compact_v5),
    ]
    
    results = []
    
    for name, formatter in formats:
        formatted = formatter(entries)
        char_count = len(formatted)
        results.append((name, char_count, formatted))
        
        print(f"=== {name} ===")
        print(f"Characters: {char_count}")
        print(f"Sample:")
        print(formatted[:300] + "..." if len(formatted) > 300 else formatted)
        print("\n" + "="*50 + "\n")
    
    # Summary
    print("SUMMARY:")
    print("Format Name | Characters | Reduction")
    print("-" * 40)
    baseline = results[0][1]  # Current format
    for name, char_count, _ in results:
        reduction = f"{((baseline - char_count) / baseline * 100):.1f}%" if char_count != baseline else "baseline"
        print(f"{name:<25} | {char_count:>9} | {reduction:>9}")

if __name__ == "__main__":
    main()
