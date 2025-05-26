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
MODEL_NAME: str = os.getenv("OPENAI_MODEL_NAME", "gpt-4.1-nano")

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


# Functions below are removed as they are unused or superseded by hybrid_iab_classifier.py
# _parse_categories
# _parse_persona
# _SYSTEM_CLS
# _SYSTEM_PERSONA
# classify_with_gpt
# build_persona_tags
# classify_with_gpt_async
# build_persona_tags_async

# Keeping:
# _load_taxonomy
# _find_taxonomy_entry
# _get_client
# _clean_json_response
