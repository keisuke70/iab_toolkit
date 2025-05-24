"""Batch processing utilities with async support."""

import asyncio
import aiohttp
import json
import csv
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import logging

from iab_toolkit._fetch import fetch_content
from iab_toolkit._extract import extract_main_content
from iab_toolkit._embedding import embed_text, find_similar_categories
from iab_toolkit._gpt import classify_with_gpt_async, build_persona_tags_async
from iab_toolkit.models import CategoryResult, PersonaResult

logger = logging.getLogger(__name__)


class BatchProcessor:
    """Async batch processor for URL classification."""
    
    def __init__(self, max_concurrent: int = 5):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def classify_url_async(
        self,
        url: str,
        max_categories: int = 3,
        with_persona: bool = False,
        session: Optional[aiohttp.ClientSession] = None
    ) -> Dict[str, Any]:
        """
        Asynchronously classify a single URL.
        
        Args:
            url: URL to classify
            max_categories: Maximum number of categories to return
            with_persona: Whether to generate persona
            session: Optional aiohttp session for reuse
            
        Returns:
            Classification result dictionary
        """
        async with self.semaphore:
            try:
                logger.info(f"Classifying URL: {url}")
                
                # Fetch and extract content
                content = await fetch_content(url, session=session)
                if not content:
                    return {
                        'url': url,
                        'error': 'Failed to fetch content',
                        'categories_embedding': [],
                        'categories_final': [],
                        'persona': None
                    }
                
                text_content = extract_main_content(content)
                if not text_content or len(text_content.strip()) < 50:
                    return {
                        'url': url,
                        'error': 'Insufficient text content',
                        'categories_embedding': [],
                        'categories_final': [],
                        'persona': None
                    }
                
                # Embedding-based classification
                embedding_categories = []
                try:
                    embedding = await embed_text(text_content)
                    similar_cats = find_similar_categories(embedding, max_categories)
                    embedding_categories = [
                        CategoryResult(
                            id=str(cat_data['id']),
                            name=cat_data['name'],
                            score=score,
                            tier_1=cat_data.get('tier_1', cat_data['name']),
                            tier_2=cat_data.get('tier_2'),
                            tier_3=cat_data.get('tier_3'),
                            tier_4=cat_data.get('tier_4')
                        )
                        for cat_data, score in similar_cats
                    ]
                except Exception as e:
                    logger.error(f"Embedding classification failed: {e}")
                
                # GPT-based refinement
                final_categories = embedding_categories
                try:
                    if embedding_categories:
                        gpt_categories = await classify_with_gpt_async(
                            text_content, max_categories
                        )
                        if gpt_categories:
                            final_categories = gpt_categories
                except Exception as e:
                    logger.error(f"GPT classification failed: {e}")
                
                # Persona generation
                persona = None
                if with_persona:
                    try:
                        persona = await build_persona_tags_async(text_content)
                    except Exception as e:
                        logger.error(f"Persona generation failed: {e}")
                
                return {
                    'url': url,
                    'categories_embedding': embedding_categories,
                    'categories_final': final_categories,
                    'persona': persona,
                    'timestamp': datetime.now().isoformat()
                }
            
            except Exception as e:
                logger.error(f"Error classifying {url}: {e}")
                return {
                    'url': url,
                    'error': str(e),
                    'categories_embedding': [],
                    'categories_final': [],
                    'persona': None,
                    'timestamp': datetime.now().isoformat()
                }
    
    async def classify_urls_batch(
        self,
        urls: List[str],
        max_categories: int = 3,
        with_persona: bool = False,
        progress_callback: Optional[callable] = None
    ) -> List[Dict[str, Any]]:
        """
        Classify multiple URLs concurrently.
        
        Args:
            urls: List of URLs to classify
            max_categories: Maximum number of categories per URL
            with_persona: Whether to generate personas
            progress_callback: Optional callback for progress updates
            
        Returns:
            List of classification results
        """
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in urls:
                task = self.classify_url_async(
                    url, max_categories, with_persona, session
                )
                tasks.append(task)
            
            results = []
            for i, coro in enumerate(asyncio.as_completed(tasks)):
                result = await coro
                results.append(result)
                
                if progress_callback:
                    progress_callback(i + 1, len(urls), result['url'])
            
            return results


def load_urls_from_file(file_path: Path) -> List[str]:
    """Load URLs from a text file (one URL per line)."""
    urls = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            url = line.strip()
            if url and not url.startswith('#'):
                urls.append(url)
    return urls


def save_results_to_json(results: List[Dict[str, Any]], output_path: Path) -> None:
    """Save classification results to JSON file."""
    # Convert results to JSON-serializable format
    json_results = []
    for result in results:
        json_result = {
            'url': result['url'],
            'timestamp': result.get('timestamp'),
            'error': result.get('error'),
            'categories_embedding': [
                {
                    'id': cat.id,
                    'name': cat.name,
                    'score': cat.score,
                    'tier_1': cat.tier_1,
                    'tier_2': cat.tier_2,
                    'tier_3': cat.tier_3,
                    'tier_4': cat.tier_4
                }
                for cat in result['categories_embedding']
            ],
            'categories_final': [
                {
                    'id': cat.id,
                    'name': cat.name,
                    'score': cat.score,
                    'tier_1': cat.tier_1,
                    'tier_2': cat.tier_2,
                    'tier_3': cat.tier_3,
                    'tier_4': cat.tier_4
                }
                for cat in result['categories_final']
            ],
            'persona': {
                'age_band': result['persona'].age_band,
                'gender_tilt': result['persona'].gender_tilt,
                'tech_affinity': result['persona'].tech_affinity,
                'short_description': result['persona'].short_description
            } if result['persona'] else None
        }
        json_results.append(json_result)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(json_results, f, indent=2, ensure_ascii=False)


def save_results_to_csv(results: List[Dict[str, Any]], output_path: Path) -> None:
    """Save classification results to CSV file."""
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow([
            'url', 'timestamp', 'error', 'top_category_id', 'top_category_name',
            'top_category_score', 'all_categories', 'persona_age', 'persona_gender',
            'persona_tech', 'persona_description'
        ])
        
        # Write data
        for result in results:
            categories = result['categories_final'] or result['categories_embedding']
            top_cat = categories[0] if categories else None
            
            all_cats = '; '.join([
                f"{cat.name} ({cat.score:.2f})" for cat in categories
            ])
            
            persona = result['persona']
            
            writer.writerow([
                result['url'],
                result.get('timestamp', ''),
                result.get('error', ''),
                top_cat.id if top_cat else '',
                top_cat.name if top_cat else '',
                top_cat.score if top_cat else '',
                all_cats,
                persona.age_band if persona else '',
                persona.gender_tilt if persona else '',
                persona.tech_affinity if persona else '',
                persona.short_description if persona else ''
            ])
