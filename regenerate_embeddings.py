#!/usr/bin/env python3
"""
Regenerate embeddings from the cleaned tier1_taxonomy.json file.
"""

import json
import numpy as np
from pathlib import Path
import os
import sys

# Add the iab_toolkit to the path
sys.path.append(str(Path(__file__).parent / "iab_toolkit"))

try:
    from iab_toolkit._embedding import embed_text_sync
    from iab_toolkit._config import config
    REAL_API_AVAILABLE = True
    print("✅ Real embedding API available")
except ImportError:
    REAL_API_AVAILABLE = False
    print("❌ Real embedding API not available")

def regenerate_embeddings():
    """Generate embeddings from the cleaned taxonomy file."""
    
    # Paths
    taxonomy_file = Path(__file__).parent / "final" / "data" / "tier1_taxonomy.json"
    output_dir = Path(__file__).parent / "final" / "data"
    embeddings_file = output_dir / "tier1_embeddings.npy"
    domains_file = output_dir / "tier1_domains.json"
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load the cleaned taxonomy
    print(f"📖 Loading taxonomy from: {taxonomy_file}")
    if not taxonomy_file.exists():
        print(f"❌ Error: {taxonomy_file} not found")
        return False
    
    with open(taxonomy_file, 'r', encoding='utf-8') as f:
        taxonomy_data = json.load(f)
    
    print(f"📊 Found {len(taxonomy_data)} domains")
    
    if not REAL_API_AVAILABLE:
        print("❌ Cannot generate embeddings without API access")
        return False
    
    # Extract descriptions and names
    descriptions = []
    domain_names = []
    
    for entry in taxonomy_data:
        domain_name = entry['name']
        description = entry['description']
        
        descriptions.append(description)
        domain_names.append(domain_name)
        print(f"  {len(domain_names)}. {domain_name}")
    
    print(f"\n🔧 Generating embeddings for {len(descriptions)} descriptions...")
    
    # Generate embeddings
    embeddings = []
    for i, description in enumerate(descriptions):
        print(f"  Processing {i+1}/{len(descriptions)}: {domain_names[i]}")
        try:
            embedding = embed_text_sync(description)
            embeddings.append(embedding)
        except Exception as e:
            print(f"❌ Error embedding {domain_names[i]}: {e}")
            return False
    
    # Convert to numpy array
    embeddings_array = np.array(embeddings)
    print(f"📐 Embeddings shape: {embeddings_array.shape}")
    
    # Save embeddings
    np.save(embeddings_file, embeddings_array)
    print(f"💾 Saved embeddings: {embeddings_file}")
    
    # Save domain names
    with open(domains_file, 'w', encoding='utf-8') as f:
        json.dump(domain_names, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved domains: {domains_file}")
    
    print(f"\n✅ Successfully generated embeddings!")
    print(f"📊 {len(domain_names)} domains")
    print(f"📐 Embedding dimension: {embeddings_array.shape[1]}")
    print(f"📁 Files saved in: {output_dir}")
    
    return True

if __name__ == "__main__":
    success = regenerate_embeddings()
    if success:
        print("\n🎉 Embedding generation complete!")
    else:
        print("\n💥 Embedding generation failed!")
