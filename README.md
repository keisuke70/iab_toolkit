# IAB Toolkit

A Python package for classifying web pages into IAB Content Taxonomy v3.1 categories using embeddings and GPT fallback, with optional target reader persona generation.

## Features

- **Dual Classification**: Uses OpenAI embeddings for fast classification with GPT-4o-mini fallback for complex cases
- **IAB Content Taxonomy v3.1**: Complete support for the latest IAB taxonomy
- **Direct Text Classification**: Classify text directly without URLs, supports multiple languages including Japanese
- **Persona Generation**: Optional target reader persona inference
- **Robust Content Extraction**: Handles various HTML structures and extracts meaningful content
- **CLI and Library**: Use as a command-line tool or Python library
- **Performance Optimized**: Lazy-loading of taxonomy vectors with caching
- **Batch Processing**: Async processing of multiple URLs concurrently
- **Multiple Output Formats**: JSON and CSV export options

## Setup

### 1. Install the package

```bash
pip install -e .
```

### 2. Set up OpenAI API key

Set your OpenAI API key as an environment variable:

```bash
# Windows PowerShell
$env:OPENAI_API_KEY = "your-api-key-here"

# Or create a .env file in the project root
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

### 3. Build taxonomy vectors

Generate the taxonomy embeddings (one-time setup):

```bash
python -m scripts.build_vectors
```

This will process the `Content Taxonomy 3.1.tsv` file and create:
- `iab_toolkit/data/taxonomy.json` - Structured category data
- `iab_toolkit/data/taxonomy_vec.npy` - Embedding vectors

## Usage

### Command Line Interface

#### URL Classification
Basic classification:
```bash
iab-classify https://www.theverge.com/2025/05/22/ai-video-tools-roundup
```

Output:
```
Embedding:
  1. Technology & Computing (596)      score=0.91
  2. Arts & Entertainment (JLBCU7)     score=0.88

Final (after GPT): Same as embedding results

Persona:
  25-34 / neutral / enthusiast
  Tech-savvy professionals interested in creative tools and AI innovations
```

Available options:
```bash
iab-classify --help
iab-classify https://example.com --no-persona    # Skip persona generation
iab-classify https://example.com --json          # Output raw JSON
iab-classify https://example.com --max-categories 2  # Limit categories
iab-classify https://example.com --verbose       # Enable verbose logging
```

#### Direct Text Classification ⭐ NEW
Classify text directly (great for Japanese content):
```bash
# Direct text input
iab-classify classify-text "Your text content here"

# From a file
iab-classify classify-text --file your_text.txt

# Japanese text example
iab-classify classify-text "トヨタRAV4は、トヨタ自動車が製造・販売しているSUVです。" --json

# Fast mode (embedding only)
iab-classify classify-text --file content.txt --embedding-only --no-persona
```

#### Batch Processing
```bash
# Process multiple URLs
iab-classify batch-classify urls.txt --output results.csv --concurrent 5
```

Output:
```
https://www.theverge.com/2025/05/22/ai-video-tools-roundup,Technology & Computing (596),0.91,Arts & Entertainment (JLBCU7),0.88
https://www.example.com,Shopping (IAB19),0.85,Home & Garden (IAB7),0.80
```

### Python Library

```python
from iab_toolkit import classify_url

# Basic classification
result = classify_url("https://www.example.com")

# With options
result = classify_url(
    "https://www.example.com",
    max_categories=2,
    with_persona=True
)

# Access results
print(f"URL: {result['url']}")
print(f"Embedding categories: {len(result['categories_embedding'])}")
print(f"Final categories: {len(result['categories_final'])}")

for category in result['categories_final']:
    print(f"- {category.name} (ID: {category.id}, Score: {category.score:.2f})")

if result['persona']:
    persona = result['persona']
    print(f"Target audience: {persona.age_band}, {persona.gender_tilt}, {persona.tech_affinity}")
    print(f"Description: {persona.short_description}")
```

### Return Format

The `classify_url` function returns a dictionary with:

```python
{
    'url': str,                           # Original URL
    'categories_embedding': [CategoryResult],  # Results from embedding classifier
    'categories_final': [CategoryResult],      # Final results (after GPT fallback if needed)
    'persona': PersonaResult | None            # Target reader persona (if requested)
}
```

#### CategoryResult

```python
@dataclass
class CategoryResult:
    id: str              # Unique category ID
    name: str            # Category name
    score: float         # Confidence score (0.0-1.0)
    tier_1: str          # Top-level category
    tier_2: str | None   # Second-level category
    tier_3: str | None   # Third-level category
    tier_4: str | None   # Fourth-level category
```

#### PersonaResult

```python
@dataclass
class PersonaResult:
    age_band: str         # "18-24", "25-34", "35-49", "50+"
    gender_tilt: str      # "male", "female", "neutral"
    tech_affinity: str    # "casual", "enthusiast", "hardcore"
    short_description: str # Human-readable description
```

## How It Works

1. **Content Extraction**: Fetches and parses HTML, extracting main content, meta tags, and structured data
2. **Embedding Classification**: Creates embeddings for the content and finds similar categories using cosine similarity
3. **GPT Fallback**: If embedding confidence is low (<0.70), uses GPT-4o-mini for classification
4. **Persona Generation**: Optionally analyzes content to infer target reader demographics and interests

## Performance & Costs

### Latency
- **Embedding classification**: ~1-2 seconds
- **With GPT fallback**: ~3-5 seconds
- **With persona**: +1-2 seconds

### OpenAI API Costs (approximate)
- **Embeddings**: ~$0.00002 per classification
- **GPT fallback**: ~$0.001-0.003 per classification
- **Persona generation**: ~$0.0005-0.001 per request

### Optimization
- Taxonomy vectors are lazy-loaded and cached in memory
- Content is limited to 8k characters for embeddings
- Batch processing available for multiple URLs

## Development

### Running Tests

```bash
pip install -e ".[dev]"
pytest tests/
```

### File Structure

```
iab_toolkit/
├── iab_toolkit/           # Main package
│   ├── __init__.py       # Package exports
│   ├── classify.py       # Main classification API
│   ├── _fetch.py         # HTML fetching
│   ├── _extract.py       # Content extraction
│   ├── _embedding.py     # Vector operations
│   ├── _gpt.py          # GPT integration
│   ├── models.py        # Data classes
│   └── data/            # Generated taxonomy data
├── scripts/
│   └── build_vectors.py # Taxonomy vector builder
├── cli.py               # Command-line interface
└── tests/
    └── test_basic.py    # Unit tests
```

## Requirements

- Python 3.10+
- OpenAI API key
- Internet connection for web scraping and API calls

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## Troubleshooting

### Common Issues

**"OPENAI_API_KEY environment variable not set"**
- Set the environment variable or create a `.env` file with your API key

**"Taxonomy data not found"**
- Run `python -m scripts.build_vectors` to generate the taxonomy vectors

**"Failed to fetch content"**
- Check internet connection and URL accessibility
- Some sites may block automated requests

**"No main content extracted"**
- The page may have unusual HTML structure
- Check if the page requires JavaScript to load content

### Logging

Enable verbose logging for debugging:

```bash
iab-classify https://example.com --verbose
```

Or in Python:
```python
import logging
logging.basicConfig(level=logging.INFO)
```
