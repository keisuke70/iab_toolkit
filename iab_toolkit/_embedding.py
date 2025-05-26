"""Vector utilities and lazy loading of taxonomy embeddings."""

import json
import os
import numpy as np
from typing import List, Tuple, Optional
from pathlib import Path
import logging

import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class TaxonomyIndex:
    """Singleton class for lazy-loading and caching taxonomy vectors."""
    
    _instance: Optional['TaxonomyIndex'] = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.taxonomy_data = None
            self.taxonomy_vectors = None
            self._initialized = True
    
    def load_index(self):
        """Load taxonomy data and vectors if not already loaded."""
        if self.taxonomy_data is not None and self.taxonomy_vectors is not None:
            return
        
        # Get the path to the data directory
        package_dir = Path(__file__).parent
        data_dir = package_dir / 'data'
        
        taxonomy_path = data_dir / 'taxonomy.json'
        vectors_path = data_dir / 'taxonomy_vec.npy'
        
        if not taxonomy_path.exists():
            raise FileNotFoundError(
                f"Taxonomy data not found at {taxonomy_path}. "
                "Please run 'python -m scripts.build_vectors' first."
            )
        
        if not vectors_path.exists():
            raise FileNotFoundError(
                f"Taxonomy vectors not found at {vectors_path}. "
                "Please run 'python -m scripts.build_vectors' first."
            )
        
        # Load taxonomy data
        with open(taxonomy_path, 'r', encoding='utf-8') as f:
            self.taxonomy_data = json.load(f)
        
        # Load vectors
        self.taxonomy_vectors = np.load(vectors_path).astype(np.float32)
        
        logger.info(f"Loaded {len(self.taxonomy_data)} taxonomy categories with vectors")


def get_taxonomy_index() -> TaxonomyIndex:
    """Get the singleton taxonomy index instance."""
    return TaxonomyIndex()


def normalize_vector(vector: np.ndarray) -> np.ndarray:
    """Normalize a vector to unit length."""
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    return float(np.dot(a, b))


async def embed_text(text: str) -> np.ndarray:
    """
    Create embedding for text using OpenAI API.
    
    Args:
        text: Text to embed
        
    Returns:
        Normalized embedding vector
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    client = openai.OpenAI(api_key=api_key)
    
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        embedding = np.array(response.data[0].embedding, dtype=np.float32)
        return normalize_vector(embedding)
    except Exception as e:
        logger.error(f"Error creating embedding: {e}")
        raise


def embed_text_sync(text: str) -> np.ndarray:
    """
    Synchronous version of embed_text.
    
    Args:
        text: Text to embed
        
    Returns:
        Normalized embedding vector
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    client = openai.OpenAI(api_key=api_key)
    
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        embedding = np.array(response.data[0].embedding, dtype=np.float32)
        return normalize_vector(embedding)
    except Exception as e:
        logger.error(f"Error creating embedding: {e}")
        raise


def find_similar_categories(
    text_embedding: np.ndarray,
    max_categories: int = 3,
    min_score: float = 0.40
) -> List[Tuple[dict, float]]:
    """
    Find similar categories using cosine similarity.
    
    Args:
        text_embedding: Normalized embedding vector for the text
        max_categories: Maximum number of categories to return
        min_score: Minimum similarity score threshold
        
    Returns:
        List of (category_data, score) tuples sorted by score descending
    """
    index = get_taxonomy_index()
    index.load_index()
    
    # Compute similarities
    similarities = []
    if not index.taxonomy_data or index.taxonomy_vectors is None:
        logger.error("Taxonomy data or vectors are not loaded.")
        return []
    for i, category in enumerate(index.taxonomy_data):
        category_vector = normalize_vector(index.taxonomy_vectors[i])
        score = cosine_similarity(text_embedding, category_vector)
        if score >= min_score:
            similarities.append((category, score))
    
    # Sort by score descending and limit
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:max_categories]
