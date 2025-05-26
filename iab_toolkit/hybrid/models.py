"""Data models for IAB toolkit results."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class CategoryResult:
    """Represents a classified IAB category with confidence score."""
    id: str
    name: str
    score: float
    tier_1: str
    tier_2: Optional[str] = None
    tier_3: Optional[str] = None
    tier_4: Optional[str] = None


@dataclass
class PersonaResult:
    """Represents a target reader persona inference."""
    age_band: str  # "18-24", "25-34", "35-49", "50+"
    gender_tilt: str  # "male", "female", "neutral"
    tech_affinity: str  # "casual", "enthusiast", "hardcore"
    short_description: str
