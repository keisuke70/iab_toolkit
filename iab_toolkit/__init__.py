"""IAB Content Taxonomy v3.1 Hybrid Classifier

A Python package for classifying text content into IAB Content Taxonomy v3.1 categories
using optimized hybrid approach with embeddings and GPT.

Features:
- Fast and accurate tier 1 domain detection using precomputed embeddings
- Intelligent tier 2 classification with GPT-4o-mini
- Comprehensive user profiling and content analysis
- Multi-language support including Japanese
"""

from .hybrid import HybridIABClassifier, OptimizedTier1Detector

__version__ = "0.3.0"
__all__ = [
    "HybridIABClassifier",
    "OptimizedTier1Detector"
]
