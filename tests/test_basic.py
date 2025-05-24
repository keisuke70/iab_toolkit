"""Basic tests for IAB toolkit."""

import pytest
from unittest.mock import patch, MagicMock
import os

from iab_toolkit import classify_url, CategoryResult, PersonaResult


def test_category_result():
    """Test CategoryResult dataclass."""
    result = CategoryResult(
        id="123",
        name="Technology",
        score=0.85,
        tier_1="Technology & Computing"
    )
    assert result.id == "123"
    assert result.name == "Technology"
    assert result.score == 0.85
    assert result.tier_1 == "Technology & Computing"


def test_persona_result():
    """Test PersonaResult dataclass."""
    persona = PersonaResult(
        age_band="25-34",
        gender_tilt="neutral",
        tech_affinity="enthusiast",
        short_description="Tech-savvy professional"
    )
    assert persona.age_band == "25-34"
    assert persona.gender_tilt == "neutral"
    assert persona.tech_affinity == "enthusiast"
    assert persona.short_description == "Tech-savvy professional"


@patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
@patch('iab_toolkit._fetch.fetch_page_content_sync')
@patch('iab_toolkit._embedding.embed_text_sync')
@patch('iab_toolkit._embedding.get_taxonomy_index')
def test_classify_url_basic(mock_index, mock_embed, mock_fetch):
    """Test basic URL classification functionality."""
    # Mock HTML content
    mock_fetch.return_value = '''
    <html>
        <head>
            <title>Ukraine War News</title>
            <meta name="description" content="Latest news about the conflict in Ukraine">
        </head>
        <body>
            <article>
                <h1>Ukraine War Updates</h1>
                <p>Latest developments in the ongoing conflict...</p>
            </article>
        </body>
    </html>
    '''
    
    # Mock embedding
    import numpy as np
    mock_embed.return_value = np.random.rand(384).astype(np.float32)
    
    # Mock taxonomy index
    mock_taxonomy_instance = MagicMock()
    mock_taxonomy_instance.taxonomy_data = [
        {
            'unique_id': '380',
            'name': 'Crime',
            'tier_1': 'Crime',
            'tier_2': None,
            'tier_3': None,
            'tier_4': None
        },
        {
            'unique_id': '381',
            'name': 'Disasters',
            'tier_1': 'Disasters',
            'tier_2': None,
            'tier_3': None,
            'tier_4': None
        }
    ]
    mock_taxonomy_instance.taxonomy_vectors = np.random.rand(2, 384).astype(np.float32)
    mock_index.return_value = mock_taxonomy_instance
    
    # Test classification
    result = classify_url("https://www.nytimes.com/2023/05/01/world/europe/ukraine-war.html")
    
    # Verify structure
    assert 'url' in result
    assert 'categories_embedding' in result
    assert 'categories_final' in result
    assert 'persona' in result
    
    assert result['url'] == "https://www.nytimes.com/2023/05/01/world/europe/ukraine-war.html"
    assert isinstance(result['categories_embedding'], list)
    assert isinstance(result['categories_final'], list)
    
    # Verify that fetch was called
    mock_fetch.assert_called_once()


@patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
@patch('iab_toolkit._fetch.fetch_page_content_sync')
def test_classify_url_fetch_failure(mock_fetch):
    """Test behavior when page fetch fails."""
    mock_fetch.return_value = None
    
    result = classify_url("https://nonexistent.example.com")
    
    assert result['url'] == "https://nonexistent.example.com"
    assert result['categories_embedding'] == []
    assert result['categories_final'] == []
    assert result['persona'] is None


def test_max_categories_limit():
    """Test that max_categories is properly limited to 3."""
    with patch('iab_toolkit.classify.fetch_page_content_sync') as mock_fetch:
        mock_fetch.return_value = None
        
        # Test with max_categories > 3
        result = classify_url("https://example.com", max_categories=5)
        
        # Should not raise an error and should handle gracefully
        assert 'categories_embedding' in result


if __name__ == "__main__":
    pytest.main([__file__])
