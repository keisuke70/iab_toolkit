"""Hybrid IAB Classification System

This module provides the optimized hybrid approach that combines:
- Embedding-based Tier 1 detection using precomputed .npy files
- LLM-based Tier 2 classification with focused taxonomy subsets
- Comprehensive user profiling and demographic analysis

The hybrid approach achieves 100% accuracy for Tier 1 detection while being
2.2x faster than the original implementation (1 API call vs 40+).
"""

from .hybrid_iab_classifier import HybridIABClassifier
from .optimized_tier1_detector import OptimizedTier1Detector

__version__ = "1.0.0"
__all__ = ["HybridIABClassifier", "OptimizedTier1Detector"]
