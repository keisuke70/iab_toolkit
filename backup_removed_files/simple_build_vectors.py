"""Simple script to build vectors directly without module issues."""

import sys
import os
import json
import csv
import numpy as np
import openai
from pathlib import Path

def main():
    print("Building vectors with simple script...")
    
    # Get API key
    try:
        sys.path.append(str(Path(__file__).parent.parent))
        from iab_toolkit._config import config
        api_key = config.get_openai_api_key()
        print("Got API key from config")
    except Exception as e:
        print(f"Config error: {e}")
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            print("Got API key from environment")
        else:
            print("ERROR: No API key found")
            return
    
    client = openai.OpenAI(api_key=api_key)
    
    # Parse TSV
    tsv_path = Path(__file__).parent / "Content Taxonomy 3.1.tsv"
    print(f"Reading TSV from: {tsv_path}")
    
    categories = []
    with open(tsv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader, None)  # Skip header
        
        for row in reader:
            if len(row) < 7:
                continue
            categories.append({
                'unique_id': row[0].strip(),
                'parent': row[1].strip() if row[1].strip() else None,
                'name': row[2].strip(),
                'tier_1': row[3].strip() if row[3].strip() else None,
                'tier_2': row[4].strip() if row[4].strip() else None,
                'tier_3': row[5].strip() if row[5].strip() else None,
                'tier_4': row[6].strip() if row[6].strip() else None
            })
    
    print(f"Parsed {len(categories)} categories")
    
    # Save taxonomy
    data_dir = Path(__file__).parent / "iab_toolkit" / "data"
    data_dir.mkdir(exist_ok=True)
    
    taxonomy_path = data_dir / "taxonomy.json"
    with open(taxonomy_path, 'w', encoding='utf-8') as f:
        json.dump(categories, f, indent=2, ensure_ascii=False)
    print(f"Saved taxonomy to {taxonomy_path}")
    
    # Create embeddings
    print("Creating embeddings...")
    category_names = []
    for cat in categories:
        parts = [cat['name']]
        if cat['tier_1'] and cat['tier_1'] != cat['name']:
            parts.append(f"in {cat['tier_1']}")
        if cat['tier_2'] and cat['tier_2'] != cat['name'] and cat['tier_2'] != cat['tier_1']:
            parts.append(f"category {cat['tier_2']}")
        category_names.append(" ".join(parts))
    
    # Batch processing
    batch_size = 100
    all_embeddings = []
    
    for i in range(0, len(category_names), batch_size):
        batch = category_names[i:i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(category_names) + batch_size - 1) // batch_size
        print(f"Processing batch {batch_num}/{total_batches}")
        
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=batch
        )
        batch_embeddings = [item.embedding for item in response.data]
        all_embeddings.extend(batch_embeddings)
    
    embeddings = np.array(all_embeddings)
    print(f"Created embeddings with shape: {embeddings.shape}")
    
    # Save embeddings
    vectors_path = data_dir / "taxonomy_vec.npy"
    np.save(vectors_path, embeddings)
    print(f"Saved embeddings to {vectors_path}")
    
    print("Vector building complete!")

if __name__ == "__main__":
    main()
