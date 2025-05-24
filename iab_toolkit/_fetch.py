"""Robust HTML fetcher with proper error handling."""

import asyncio
import httpx
import aiohttp
from typing import Optional
import logging

logger = logging.getLogger(__name__)


async def fetch_content(url: str, session: Optional[aiohttp.ClientSession] = None) -> Optional[str]:
    """
    Fetch HTML content from a URL using aiohttp with robust error handling.
    
    Args:
        url: The URL to fetch
        session: Optional aiohttp session for reuse
        
    Returns:
        HTML content as string, or None if failed
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        if session:
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                response.raise_for_status()
                return await response.text()
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    response.raise_for_status()
                    return await response.text()
    except (asyncio.TimeoutError, aiohttp.ServerTimeoutError):
        logger.error(f"Timeout fetching {url}")
        return None
    except aiohttp.ClientResponseError as e:
        logger.error(f"HTTP error {e.status} fetching {url}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching {url}: {e}")
        return None


async def fetch_page_content(url: str) -> Optional[str]:
    """
    Fetch HTML content from a URL with robust error handling.
    
    Args:
        url: The URL to fetch
        
    Returns:
        HTML content as string, or None if failed
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        async with httpx.AsyncClient(timeout=5.0, follow_redirects=True) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.text
    except httpx.TimeoutException:
        logger.error(f"Timeout fetching {url}")
        return None
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error {e.response.status_code} fetching {url}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching {url}: {e}")
        return None


def fetch_page_content_sync(url: str) -> Optional[str]:
    """
    Synchronous version of fetch_page_content.
    
    Args:
        url: The URL to fetch
        
    Returns:
        HTML content as string, or None if failed
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        with httpx.Client(timeout=5.0, follow_redirects=True) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            return response.text
    except httpx.TimeoutException:
        logger.error(f"Timeout fetching {url}")
        return None
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error {e.response.status_code} fetching {url}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching {url}: {e}")
        return None
