"""Main classification API for IAB toolkit."""

import logging
from typing import Dict, List, Optional

from .models import CategoryResult, PersonaResult
from ._fetch import fetch_page_content_sync
from ._extract import extract_content_hints, extract_main_content
from ._embedding import embed_text_sync, find_similar_categories, get_taxonomy_index
from ._gpt import classify_with_gpt, build_persona_tags

logger = logging.getLogger(__name__)


def classify_url(
    url: str,
    *,
    max_categories: int = 3,
    with_persona: bool = False,
) -> dict:
    """
    Classify a URL into IAB Content Taxonomy v3.1 categories.
    
    Args:
        url: URL to classify
        max_categories: Maximum number of categories to return (≤3)
        with_persona: Whether to generate target reader persona
        
    Returns:
        Dictionary with:
        - 'url': str
        - 'categories_embedding': List[CategoryResult] from embedding classifier
        - 'categories_final': List[CategoryResult] after GPT fallback if needed
        - 'persona': PersonaResult | None
    """
    logger.info(f"Classifying URL: {url}")
    
    # Ensure max_categories is within bounds
    max_categories = min(max_categories, 3)
    
    # Fetch page content
    html = fetch_page_content_sync(url)
    if not html:
        logger.error(f"Failed to fetch content from {url}")
        return {
            'url': url,
            'categories_embedding': [],
            'categories_final': [],
            'persona': None
        }
    
    # Extract content and hints
    main_content = extract_main_content(html)
    content_hints = extract_content_hints(html, url)
    
    if not main_content:
        logger.warning(f"No main content extracted from {url}")
        return {
            'url': url,
            'categories_embedding': [],
            'categories_final': [],
            'persona': None
        }
    
    # Combine content with hints for classification
    classification_text = main_content
    if content_hints.get('title'):
        classification_text = f"{content_hints['title']} {classification_text}"
    if content_hints.get('description'):
        classification_text = f"{classification_text} {content_hints['description']}"
    
    # Classify with embeddings
    try:
        embedding_results = classify_with_embeddings(
            classification_text, 
            max_categories=max_categories
        )
    except Exception as e:
        logger.error(f"Embedding classification failed: {e}")
        embedding_results = []
    
    # Determine if GPT fallback is needed
    use_gpt_fallback = (
        not embedding_results or 
        (embedding_results and embedding_results[0].score < 0.70)
    )
    
    final_results = embedding_results
    
    if use_gpt_fallback:
        logger.info("Using GPT fallback for classification")
        try:
            gpt_results = classify_with_gpt(classification_text, max_categories)
            if gpt_results:
                final_results = gpt_results
        except Exception as e:
            logger.error(f"GPT classification failed: {e}")
    
    # Generate persona if requested
    persona = None
    if with_persona:
        try:
            persona = build_persona_tags(main_content)
        except Exception as e:
            logger.error(f"Persona generation failed: {e}")
    
    return {
        'url': url,
        'categories_embedding': embedding_results,
        'categories_final': final_results,
        'persona': persona
    }


def classify_with_embeddings(
    text: str,
    max_categories: int = 3,
    min_score: float = 0.40
) -> List[CategoryResult]:
    """
    Classify text using embedding similarity.
    
    Args:
        text: Text to classify (first 8k chars used)
        max_categories: Maximum categories to return
        min_score: Minimum similarity score threshold
        
    Returns:
        List of CategoryResult objects sorted by score
    """
    # Limit text to 8k characters for embedding
    if len(text) > 8000:
        text = text[:8000]
    
    # Create embedding
    text_embedding = embed_text_sync(text)
    
    # Find similar categories
    similar_categories = find_similar_categories(
        text_embedding,
        max_categories=max_categories,
        min_score=min_score
    )
    
    # Convert to CategoryResult objects
    results = []
    for category_data, score in similar_categories:
        result = CategoryResult(
            id=str(category_data['unique_id']),
            name=category_data['name'],
            score=score,
            tier_1=category_data.get('tier_1', ''),
            tier_2=category_data.get('tier_2'),
            tier_3=category_data.get('tier_3'),
            tier_4=category_data.get('tier_4')
        )
        results.append(result)
    
    return results
