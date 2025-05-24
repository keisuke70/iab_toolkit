"""Content extraction from HTML pages."""

import json
import re
from typing import Dict, Optional, List
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from selectolax.parser import HTMLParser


def extract_content_hints(html: str, url: str) -> Dict[str, str]:
    """
    Extract content hints from HTML including meta tags, slug, and JSON-LD.
    
    Args:
        html: Raw HTML content
        url: Original URL for context
        
    Returns:
        Dictionary with extracted hints
    """
    soup = BeautifulSoup(html, 'html.parser')
    hints = {}
    
    # Extract title
    title_tag = soup.find('title')
    if title_tag:
        hints['title'] = title_tag.get_text().strip()
    
    # Extract meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc and meta_desc.get('content'):
        hints['description'] = meta_desc['content'].strip()
    
    # Extract meta keywords
    meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
    if meta_keywords and meta_keywords.get('content'):
        hints['keywords'] = meta_keywords['content'].strip()
    
    # Extract Open Graph tags
    og_title = soup.find('meta', property='og:title')
    if og_title and og_title.get('content'):
        hints['og_title'] = og_title['content'].strip()
    
    og_desc = soup.find('meta', property='og:description')
    if og_desc and og_desc.get('content'):
        hints['og_description'] = og_desc['content'].strip()
    
    og_type = soup.find('meta', property='og:type')
    if og_type and og_type.get('content'):
        hints['og_type'] = og_type['content'].strip()
    
    # Extract URL slug
    parsed_url = urlparse(url)
    path_parts = [part for part in parsed_url.path.split('/') if part]
    if path_parts:
        hints['url_slug'] = path_parts[-1].replace('-', ' ').replace('_', ' ')
    
    # Extract JSON-LD structured data
    json_ld_scripts = soup.find_all('script', type='application/ld+json')
    for script in json_ld_scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict):
                if data.get('@type'):
                    hints['jsonld_type'] = data['@type']
                if data.get('articleSection'):
                    hints['jsonld_section'] = data['articleSection']
                if data.get('keywords'):
                    keywords = data['keywords']
                    if isinstance(keywords, list):
                        hints['jsonld_keywords'] = ', '.join(keywords)
                    else:
                        hints['jsonld_keywords'] = str(keywords)
        except (json.JSONDecodeError, AttributeError):
            continue
    
    return hints


def extract_main_content(html: str) -> str:
    """
    Extract the main article content from HTML.
    
    Args:
        html: Raw HTML content
        
    Returns:
        Cleaned main content text
    """
    # Use selectolax for faster parsing
    tree = HTMLParser(html)
    
    # Remove script and style elements
    for tag in tree.css('script, style, nav, header, footer, aside, .sidebar, .navigation'):
        tag.decompose()
    
    # Try to find main content containers
    content_selectors = [
        'article',
        '[role="main"]',
        'main',
        '.content',
        '.post-content',
        '.article-content',
        '.entry-content',
        '#content',
        '.main-content'
    ]
    
    main_content = ""
    for selector in content_selectors:
        elements = tree.css(selector)
        if elements:
            main_content = elements[0].text(deep=True)
            break
    
    # Fallback to body if no main content found
    if not main_content:
        body = tree.css_first('body')
        if body:
            main_content = body.text(deep=True)
    
    # Clean up the text
    main_content = re.sub(r'\s+', ' ', main_content).strip()
    
    # Limit to first 8000 characters for embedding
    if len(main_content) > 8000:
        main_content = main_content[:8000]
    
    return main_content
