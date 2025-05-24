# -*- coding: utf-8 -*-
"""Build taxonomy vectors from TSV file."""

print("Script starting - imports begin")
import csv
import json
import os
import numpy as np
import openai
import logging
from typing import List, Dict
from pathlib import Path
print("All imports successful")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_tsv_file(tsv_path: str) -> List[Dict]:
    """Parse the IAB Content Taxonomy v3.1 TSV file."""
    categories = []
    
    with open(tsv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader, None)  # Skip header row
        
        for row in reader:
            if len(row) < 7:
                continue
                
            unique_id = row[0].strip()
            parent = row[1].strip() if row[1].strip() else None
            name = row[2].strip()
            tier_1 = row[3].strip() if row[3].strip() else None
            tier_2 = row[4].strip() if row[4].strip() else None
            tier_3 = row[5].strip() if row[5].strip() else None
            tier_4 = row[6].strip() if row[6].strip() else None
            
            if not unique_id or not name:
                continue
            
            category = {
                'unique_id': unique_id,
                'parent': parent,
                'name': name,
                'tier_1': tier_1,
                'tier_2': tier_2,
                'tier_3': tier_3,
                'tier_4': tier_4
            }
            categories.append(category)
    
    return categories


def create_embeddings(categories: List[dict]) -> np.ndarray:
    """Create embeddings for IAB categories using OpenAI API."""
    # Try to get API key from config first
    api_key = None
    
    try:
        from iab_toolkit._config import config
        api_key = config.get_openai_api_key()
    except ImportError:
        pass
    
    if not api_key:
        api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        raise ValueError("OpenAI API key not found. Please set it using: iab-classify config set-api-key 'your-key'")
    
    client = openai.OpenAI(api_key=api_key)
    
    # Prepare category names for embedding
    category_names = []
    for cat in categories:
        description_parts = [cat['name']]
        if cat['tier_1'] and cat['tier_1'] != cat['name']:
            description_parts.append(f"in {cat['tier_1']}")
        if cat['tier_2'] and cat['tier_2'] != cat['name'] and cat['tier_2'] != cat['tier_1']:
            description_parts.append(f"category {cat['tier_2']}")
        category_names.append(" ".join(description_parts))
    
    logger.info(f"Creating embeddings for {len(category_names)} categories...")
    
    # Batch the requests
    batch_size = 100
    all_embeddings = []
    
    for i in range(0, len(category_names), batch_size):
        batch = category_names[i:i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(category_names) + batch_size - 1) // batch_size
        logger.info(f"Processing batch {batch_num}/{total_batches}")
        
        try:
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=batch
            )
            batch_embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(batch_embeddings)
        except Exception as e:
            logger.error(f"Error creating embeddings for batch {batch_num}: {e}")
            raise
    
    logger.info(f"Created {len(all_embeddings)} embeddings")
    return np.array(all_embeddings)


def main():
    """Main entry point."""
    try:
        print("Starting build_vectors script...")
        project_root = Path(__file__).parent.parent
        print(f"Project root: {project_root}")
        tsv_path = project_root / "Content Taxonomy 3.1.tsv"
        data_dir = project_root / "iab_toolkit" / "data"
        taxonomy_json_path = data_dir / "taxonomy.json"
        embeddings_path = data_dir / "taxonomy_vec.npy"
        
        print(f"Looking for TSV file at: {tsv_path}")
        if not tsv_path.exists():
            raise FileNotFoundError(f"TSV file not found: {tsv_path}")
        
        print("TSV file found, parsing...")
        logger.info(f"Parsing TSV file: {tsv_path}")
        categories = parse_tsv_file(str(tsv_path))
        logger.info(f"Parsed {len(categories)} categories from TSV")
        print(f"Parsed {len(categories)} categories")
        
        # Save taxonomy data
        print("Creating data directory...")
        os.makedirs(data_dir, exist_ok=True)
        print("Saving taxonomy JSON...")
        with open(taxonomy_json_path, 'w', encoding='utf-8') as f:
            json.dump(categories, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved taxonomy data to {taxonomy_json_path}")
        print(f"Saved taxonomy data to {taxonomy_json_path}")
        
        # Create and save embeddings
        print("Creating embeddings...")
        logger.info("Creating embeddings...")
        embeddings = create_embeddings(categories)
        print(f"Got embeddings shape: {embeddings.shape}")
        np.save(embeddings_path, embeddings)
        logger.info(f"Saved embeddings to {embeddings_path}")
        print(f"Saved embeddings to {embeddings_path}")
        
        logger.info("Vector building complete!")
        print("Vector building complete!")
        logger.info(f"Files created:")
        logger.info(f"  - {taxonomy_json_path}")
        logger.info(f"  - {embeddings_path}")
        print(f"Files created:")
        print(f"  - {taxonomy_json_path}")
        print(f"  - {embeddings_path}")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
