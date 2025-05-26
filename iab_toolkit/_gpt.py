"""GPT helper for category classification and persona generation (updated for GPT‑4.1 mini).

Highlights
---------
* Centdef classify_with_gpt(content: str, *, max_categories: int = 3) -> List[CategoryResult]:
    client = _get_client()
    resp = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": _SYSTEM_CLS},
            {"role": "user", "content": f"Classify this content into IAB taxonomy categories:\n\n{content[:2000]}"},
        ],
        temperature=0.1,
        max_completion_tokens=500,
    )
    content = resp.choices[0].message.content
    if content is None:
        logger.error("Empty response from GPT")
        return []
    return _parse_categories(content, max_categories)EL_NAME` constant (over‑ridable via `OPENAI_MODEL_NAME` env var) now defaults to **gpt‑4.1‑mini**.
* Uses `max_tokens`, matching the OpenAI SDK ≥ 1.14 parameter name.
* Shared JSON‑parsing utilities to cut repetition.
* Compatible sync/async helpers.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import List, Optional, Dict, Any, Union, overload
from typing_extensions import Literal

import openai
from dotenv import load_dotenv

from .models import CategoryResult, PersonaResult

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------
load_dotenv()
logger = logging.getLogger(__name__)

# You can override via env, but default to the latest small GPT family.
MODEL_NAME: str = os.getenv("OPENAI_MODEL_NAME", "gpt-4.1-mini")

# Load taxonomy data
_TAXONOMY_DATA: Optional[List[Dict[str, Any]]] = None

def _load_taxonomy() -> List[Dict[str, Any]]:
    """Load the taxonomy data once and cache it."""
    global _TAXONOMY_DATA
    if _TAXONOMY_DATA is None:
        try:
            taxonomy_path = Path(__file__).parent / "data" / "taxonomy.json"
            with open(taxonomy_path, 'r', encoding='utf-8') as f:
                _TAXONOMY_DATA = json.load(f)
            # Remove the header row if it exists
            if _TAXONOMY_DATA and _TAXONOMY_DATA[0].get("unique_id") == "Unique ID":
                _TAXONOMY_DATA = _TAXONOMY_DATA[1:]
        except Exception as e:
            logger.error(f"Failed to load taxonomy data: {e}")
            _TAXONOMY_DATA = []
    return _TAXONOMY_DATA or []

def _find_taxonomy_entry(category_name: str) -> Optional[Dict[str, Any]]:
    """Find a taxonomy entry by category name (case-insensitive partial match)."""
    taxonomy = _load_taxonomy()
    category_lower = category_name.lower()
    
    # First try exact match
    for entry in taxonomy:
        if entry["name"].lower() == category_lower:
            return entry
    
    # Then try partial match
    for entry in taxonomy:
        if category_lower in entry["name"].lower():
            return entry
    
    return None

# ---------------------------------------------------------------------------
# Client helpers
# ---------------------------------------------------------------------------

@overload
def _get_client(async_: Literal[False] = False) -> openai.OpenAI: ...

@overload 
def _get_client(async_: Literal[True]) -> openai.AsyncOpenAI: ...

def _get_client(async_: bool = False) -> Union[openai.OpenAI, openai.AsyncOpenAI]:
    """Return a configured OpenAI client (sync or async)."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return (openai.AsyncOpenAI if async_ else openai.OpenAI)(api_key=api_key)


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def _clean_json_response(text: str) -> str:
    """Strip Markdown code fences from a JSON answer, if present."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1])
    return text


def _parse_categories(raw: str, limit: int) -> List[CategoryResult]:
    try:
        data = json.loads(_clean_json_response(raw))
        if not isinstance(data, list):
            raise ValueError("response is not a list")
        out: List[CategoryResult] = []
        for item in data[:limit]:
            if not isinstance(item, dict) or {"id", "name"} - item.keys():
                continue
            
            # Extract confidence score if provided, otherwise use a reasonable default
            confidence = item.get("confidence", 0.75)  # Default to 0.75 if no confidence provided
            if not isinstance(confidence, (int, float)) or not (0.0 <= confidence <= 1.0):
                confidence = 0.75  # Fallback for invalid confidence values
            
            category_name = item["name"]
            
            # Try to find the actual taxonomy entry for this category
            taxonomy_entry = _find_taxonomy_entry(category_name)
            
            if taxonomy_entry:
                # Use real taxonomy data - ensure tier_1 is never None
                tier_1 = taxonomy_entry.get("tier_1") or category_name
                result = CategoryResult(
                    id=taxonomy_entry["unique_id"],
                    name=taxonomy_entry["name"],
                    score=float(confidence),
                    tier_1=tier_1,
                    tier_2=taxonomy_entry.get("tier_2"),
                    tier_3=taxonomy_entry.get("tier_3"),
                    tier_4=taxonomy_entry.get("tier_4")
                )
            else:
                # Fallback if taxonomy entry not found - try to use the provided ID
                # but still attempt to parse tiers from name if it contains " > "
                parts = category_name.split(" > ")
                tier_1 = parts[0] if len(parts) > 0 else category_name
                result = CategoryResult(
                    id=str(item["id"]),
                    name=category_name,
                    score=float(confidence),
                    tier_1=tier_1,
                    tier_2=parts[1] if len(parts) > 1 else None,
                    tier_3=parts[2] if len(parts) > 2 else None,
                    tier_4=parts[3] if len(parts) > 3 else None
                )
                logger.warning(f"Could not find taxonomy entry for category: {category_name}")
            
            out.append(result)
        return out
    except Exception as exc:
        logger.error("Failed to parse category JSON: %s – %s", raw, exc)
        return []


def _parse_persona(raw: str) -> Optional[PersonaResult]:
    try:
        data = json.loads(_clean_json_response(raw))
        if {"age_band", "gender_tilt", "tech_affinity", "short_description"} - data.keys():
            raise ValueError("missing fields")
        return PersonaResult(
            age_band=data["age_band"],
            gender_tilt=data["gender_tilt"],
            tech_affinity=data["tech_affinity"],
            short_description=data["short_description"],
        )
    except Exception as exc:
        logger.error("Failed to parse persona JSON: %s – %s", raw, exc)
        return None


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

_SYSTEM_CLS = (
    "You are an IAB Content Taxonomy v3.1 classifier.\n"
    "Classify content into the most appropriate IAB taxonomy categories.\n"
    "Use real category names from the IAB taxonomy like 'Automotive', 'SUV', 'Auto Body Styles', etc.\n"
    "For automotive content, consider categories like:\n"
    "- Automotive (general automotive topics)\n"
    "- SUV (for SUV-specific content)\n"
    "- Auto Body Styles (for vehicle types)\n"
    "- Off-Road Vehicles (for off-road capable vehicles)\n"
    "Return JSON array of {id: any_number, name: category_name, confidence: float}.\n"
    "Use descriptive category names that match IAB taxonomy structure.\n"
    "Confidence should be 0.0-1.0 representing how well the category matches.\n"
    "Select up to 3 most appropriate categories.\n"
    "Only output JSON."
)

_SYSTEM_PERSONA = (
    "Infer target reader persona from article.\n"
    "Return compact JSON like:\n"
    "{\n"
    "  \"age_band\": \"18-24|25-34|35-49|50+\",\n"
    "  \"gender_tilt\": \"male|female|neutral\",\n"
    "  \"tech_affinity\": \"casual|enthusiast|hardcore\",\n"
    "  \"short_description\": \"...\"\n"
    "}"
)

# ---------------------------------------------------------------------------
# Public API – synchronous helpers
# ---------------------------------------------------------------------------

def classify_with_gpt(content: str, *, max_categories: int = 3) -> List[CategoryResult]:
    client = _get_client()
    resp = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": _SYSTEM_CLS},
            {"role": "user", "content": f"Classify this content into IAB taxonomy categories:\n\n{content[:2000]}"},
        ],
        temperature=0.1,        max_completion_tokens=500,
    )
    response_content = resp.choices[0].message.content
    if response_content is None:
        logger.error("Empty response from GPT")
        return []
    return _parse_categories(response_content, max_categories)


def build_persona_tags(content: str) -> Optional[PersonaResult]:
    client = _get_client()
    resp = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": _SYSTEM_PERSONA},
            {"role": "user", "content": f"Analyze the target persona for this content:\n\n{content[:1500]}"},        ],
        temperature=0.3,
        max_completion_tokens=300,
    )
    response_content = resp.choices[0].message.content
    if response_content is None:
        logger.error("Empty response from GPT")
        return None
    return _parse_persona(response_content)


# ---------------------------------------------------------------------------
# Public API – asynchronous helpers
# ---------------------------------------------------------------------------

async def classify_with_gpt_async(content: str, *, max_categories: int = 3) -> List[CategoryResult]:
    client = _get_client(async_=True)
    resp = await client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": _SYSTEM_CLS},
            {"role": "user", "content": f"Classify this content into IAB taxonomy categories:\n\n{content[:2000]}"},
        ],
        temperature=0.1,        max_completion_tokens=500,
    )
    response_content = resp.choices[0].message.content
    if response_content is None:
        logger.error("Empty response from GPT")
        return []
    return _parse_categories(response_content, max_categories)


async def build_persona_tags_async(content: str) -> Optional[PersonaResult]:
    client = _get_client(async_=True)
    resp = await client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": _SYSTEM_PERSONA},
            {"role": "user", "content": f"Analyze the target persona for this content:\n\n{content[:1500]}"},        ],
        temperature=0.3,
        max_completion_tokens=300,
    )
    response_content = resp.choices[0].message.content
    if response_content is None:
        logger.error("Empty response from GPT")
        return None
    return _parse_persona(response_content)
