"""GPT helper for category classification and persona generation."""

import json
import os
from typing import List, Optional
import logging

import openai
from dotenv import load_dotenv

from .models import CategoryResult, PersonaResult

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


def get_openai_client() -> openai.OpenAI:
    """Get configured OpenAI client."""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return openai.OpenAI(api_key=api_key)


def get_async_openai_client() -> openai.AsyncOpenAI:
    """Get configured async OpenAI client."""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return openai.AsyncOpenAI(api_key=api_key)


def clean_json_response(response_text: str) -> str:
    """Clean GPT response by removing markdown code blocks."""
    response_text = response_text.strip()
    # Remove markdown code blocks if present
    if response_text.startswith('```'):
        lines = response_text.split('\n')
        # Remove first and last lines (the ``` markers)
        response_text = '\n'.join(lines[1:-1])
    return response_text


def classify_with_gpt(
    content: str,
    max_categories: int = 3
) -> List[CategoryResult]:
    """
    Classify content using o4-mini-2025-04-16.
    
    Args:
        content: Text content to classify
        max_categories: Maximum number of categories to return
        
    Returns:
        List of CategoryResult objects
    """
    client = get_openai_client()
    
    system_prompt = """You are an IAB Content Taxonomy v3.1 classifier.
Select up to 3 most appropriate categories.
Return JSON array of {id:int, name:str}.
Only output JSON."""
    
    user_prompt = f"Classify this content into IAB taxonomy categories:\n\n{content[:2000]}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            max_completion_tokens=500
        )
        
        response_text = response.choices[0].message.content
        if not response_text:
            logger.error("Empty response from GPT")
            return []
        response_text = clean_json_response(response_text)
        
        # Parse JSON response
        try:
            categories_data = json.loads(response_text)
            if not isinstance(categories_data, list):
                logger.error(f"GPT response is not a list: {response_text}")
                return []
            
            results = []
            for item in categories_data[:max_categories]:
                if isinstance(item, dict) and 'id' in item and 'name' in item:
                    # Create CategoryResult with basic info
                    # We don't have tier information from GPT, so set score to 0.85
                    result = CategoryResult(
                        id=str(item['id']),
                        name=item['name'],
                        score=0.85,  # Default score for GPT results
                        tier_1=item['name'].split(' > ')[0] if ' > ' in item['name'] else item['name']
                    )
                    results.append(result)
            
            return results
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse GPT JSON response: {response_text}, error: {e}")
            return []
    
    except Exception as e:
        logger.error(f"Error in GPT classification: {e}")
        return []


def build_persona_tags(content: str) -> Optional[PersonaResult]:
    """
    Generate target reader persona from content using GPT.
    
    Args:
        content: Text content to analyze
        
    Returns:
        PersonaResult object or None if failed
    """
    client = get_openai_client()
    
    system_prompt = """Infer target reader persona from article.
Return compact JSON:
{
"age_band": "18-24|25-34|35-49|50+",
"gender_tilt": "male|female|neutral",
"tech_affinity": "casual|enthusiast|hardcore",
"short_description": "..."
}"""
    
    user_prompt = f"Analyze the target persona for this content:\n\n{content[:1500]}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_completion_tokens=300
        )
        
        response_text = response.choices[0].message.content
        if not response_text:
            logger.error("Empty response from GPT")
            return None
        response_text = clean_json_response(response_text)
        
        # Parse JSON response
        try:
            persona_data = json.loads(response_text)
            
            if not isinstance(persona_data, dict):
                logger.error(f"Persona response is not a dict: {response_text}")
                return None
            
            required_fields = ['age_band', 'gender_tilt', 'tech_affinity', 'short_description']
            if not all(field in persona_data for field in required_fields):
                logger.error(f"Missing required fields in persona response: {response_text}")
                return None
            
            return PersonaResult(
                age_band=persona_data['age_band'],
                gender_tilt=persona_data['gender_tilt'],
                tech_affinity=persona_data['tech_affinity'],
                short_description=persona_data['short_description']
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse persona JSON response: {response_text}, error: {e}")
            return None
    
    except Exception as e:
        logger.error(f"Error in persona generation: {e}")
        return None


async def classify_with_gpt_async(
    content: str,
    max_categories: int = 3
) -> List[CategoryResult]:
    """
    Asynchronously classify content using GPT-4o-mini.
    
    Args:
        content: Text content to classify
        max_categories: Maximum number of categories to return
        
    Returns:
        List of CategoryResult objects
    """
    client = get_async_openai_client()
    
    system_prompt = """You are an IAB Content Taxonomy v3.1 classifier.
Select up to 3 most appropriate categories.
Return JSON array of {id:int, name:str}.
Only output JSON."""
    
    user_prompt = f"Classify this content into IAB taxonomy categories:\n\n{content[:2000]}"
    
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            max_completion_tokens=500
        )
        
        response_text = response.choices[0].message.content
        if not response_text:
            logger.error("Empty response from GPT")
            return []
        response_text = clean_json_response(response_text)
        
        # Parse JSON response
        try:
            categories_data = json.loads(response_text)
            if not isinstance(categories_data, list):
                logger.error(f"GPT response is not a list: {response_text}")
                return []
            
            results = []
            for item in categories_data[:max_categories]:
                if isinstance(item, dict) and 'id' in item and 'name' in item:
                    # Create CategoryResult with basic info
                    # We don't have tier information from GPT, so set score to 0.85
                    result = CategoryResult(
                        id=str(item['id']),
                        name=item['name'],
                        score=0.85,  # Default score for GPT results
                        tier_1=item['name'].split(' > ')[0] if ' > ' in item['name'] else item['name']
                    )
                    results.append(result)
            
            return results
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse GPT JSON response: {response_text}, error: {e}")
            return []
    
    except Exception as e:
        logger.error(f"Error in GPT classification: {e}")
        return []


async def build_persona_tags_async(content: str) -> Optional[PersonaResult]:
    """
    Asynchronously generate target reader persona from content using GPT.
    
    Args:
        content: Text content to analyze
        
    Returns:
        PersonaResult object or None if failed
    """
    client = get_async_openai_client()
    
    system_prompt = """Infer target reader persona from article.
Return compact JSON:
{
"age_band": "18-24|25-34|35-49|50+",
"gender_tilt": "male|female|neutral",
"tech_affinity": "casual|enthusiast|hardcore",
"short_description": "..."
}"""
    
    user_prompt = f"Analyze the target persona for this content:\n\n{content[:1500]}"
    
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_completion_tokens=300
        )
        
        response_text = response.choices[0].message.content
        if not response_text:
            logger.error("Empty response from GPT")
            return None
        response_text = clean_json_response(response_text)
        
        # Parse JSON response
        try:
            persona_data = json.loads(response_text)
            
            if not isinstance(persona_data, dict):
                logger.error(f"Persona response is not a dict: {response_text}")
                return None
            
            required_fields = ['age_band', 'gender_tilt', 'tech_affinity', 'short_description']
            if not all(field in persona_data for field in required_fields):
                logger.error(f"Missing required fields in persona response: {response_text}")
                return None
            
            return PersonaResult(
                age_band=persona_data['age_band'],
                gender_tilt=persona_data['gender_tilt'],
                tech_affinity=persona_data['tech_affinity'],
                short_description=persona_data['short_description']
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse persona JSON response: {response_text}, error: {e}")
            return None
    
    except Exception as e:
        logger.error(f"Error in persona generation: {e}")
        return None
