"""IAB Content Taxonomy v3.1 Classifier

A Python package for classifying web pages into IAB Content Taxonomy v3.1 categories
using embeddings and GPT fallback.
"""

from .classify import classify_url
from .models import CategoryResult, PersonaResult

__version__ = "0.1.0"
__all__ = ["classify_url", "CategoryResult", "PersonaResult"]
