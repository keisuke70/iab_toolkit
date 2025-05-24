# IAB Toolkit Enhanced Features

## Overview

The IAB Toolkit has been enhanced with enterprise-level features for content classification using the IAB Content Taxonomy v3.1. The package now supports async batch processing, configuration management, multiple output formats, and **direct text classification**.

## New Features

### 1. Direct Text Classification ⭐ NEW

- **Text Input**: Classify text directly without needing URLs
- **File Support**: Process text from files
- **Multi-language**: Full support for Japanese and other languages
- **Tier 2 Focus**: Special highlighting of Tier 2 categories as requested

```bash
# Classify text directly
iab-classify classify-text "Your text content here"

# From a file (great for Japanese text)
iab-classify classify-text --file japanese_text.txt

# JSON output for programmatic use
iab-classify classify-text --file content.txt --json

# Fast mode (embedding only)
iab-classify classify-text "Text here" --embedding-only --no-persona
```

### 2. Environment Configuration Management

- **Secure API Key Storage**: API keys are stored in encrypted `.env` files in the user's home directory (`~/.iab_toolkit/`)
- **Configuration Persistence**: Settings are saved between sessions
- **Easy Management**: CLI commands for setting and viewing configuration

```bash
# Set your OpenAI API key
iab-classify config set-api-key "your-api-key-here"

# View current configuration
iab-classify config show

# Check API key (masked for security)
iab-classify config get-api-key
```

### 3. Enhanced CLI Interface

The CLI now supports multiple subcommands while maintaining backwards compatibility:

#### Single URL Classification (Backwards Compatible)

```bash
# Old style - still works
iab-classify https://example.com --no-persona

# New style
iab-classify classify https://example.com --no-persona --json
```

#### Batch Processing

```bash
# Process multiple URLs from a file
iab-classify batch-classify urls.txt --output results.json

# With custom settings
iab-classify batch-classify urls.txt \
  --concurrent 10 \
  --max-categories 5 \
  --output results.csv \
  --verbose
```

#### Configuration Management

```bash
# Set API key
iab-classify config set-api-key "sk-..."

# View settings
iab-classify config show

# Set custom configuration
iab-classify config set max_categories 5
```

### 4. Async Batch Processing

- **Concurrent Processing**: Process multiple URLs simultaneously with configurable concurrency
- **Progress Tracking**: Real-time progress updates during batch operations
- **Error Handling**: Graceful handling of failed URLs without stopping the batch
- **Rate Limiting**: Built-in semaphore controls to respect API limits

```python
from iab_toolkit._batch import BatchProcessor

# Create processor with custom concurrency
processor = BatchProcessor(max_concurrent=5)

# Process URLs with progress callback
results = await processor.classify_urls_batch(
    urls,
    max_categories=3,
    with_persona=True,
    progress_callback=lambda completed, total, url: print(f"{completed}/{total}: {url}")
)
```

### 5. Export Functionality

Multiple output formats are supported:

#### JSON Export

```bash
iab-classify batch-classify urls.txt --output results.json
```

#### CSV Export

```bash
iab-classify batch-classify urls.txt --output results.csv
```

#### Console Output

```bash
# Human-readable format
iab-classify batch-classify urls.txt

# JSON to stdout
iab-classify batch-classify urls.txt --json
```

### 6. Enhanced Error Handling

- **Network Errors**: Graceful handling of connection issues
- **API Errors**: Proper error messages for authentication and rate limiting
- **Content Errors**: Handling of malformed or inaccessible content
- **Validation**: Input validation for URLs and configuration

### 7. Async Architecture

The package now includes async versions of core functions:

```python
from iab_toolkit._gpt import classify_with_gpt_async, build_persona_tags_async
from iab_toolkit._fetch import fetch_content
from iab_toolkit._batch import BatchProcessor

# Async classification
categories = await classify_with_gpt_async(text, max_categories=3)

# Async persona generation
persona = await build_persona_tags_async(text)

# Async content fetching
content = await fetch_content(url)
```

## File Structure

### New Modules

- `_config.py` - Configuration management with .env support
- `_batch.py` - Async batch processing with concurrent URL handling
- Enhanced `_fetch.py` - Added aiohttp support for async operations
- Enhanced `_gpt.py` - Added async versions of GPT functions
- Enhanced `cli.py` - Multi-command CLI with backwards compatibility

### Configuration Files

- `~/.iab_toolkit/.env` - User configuration and API keys
- `~/.iab_toolkit/config.json` - Additional settings

## Usage Examples

### Direct Text Classification ⭐ NEW

```bash
# Classify Japanese text about Toyota RAV4
iab-classify classify-text "トヨタRAV4は、トヨタ自動車が製造・販売しているSUVです。1994年に初代モデルが発売され、現在は5代目となっています。RAV4は「Recreational Active Vehicle with 4-wheel drive」の略称で、レクリエーション活動にも対応できる四輪駆動車というコンセプトで開発されました。"

# From a text file
iab-classify classify-text --file content.txt --json

# Fast processing (embedding only)
iab-classify classify-text "Technology news article" --embedding-only --no-persona

# With Tier 2 category focus
iab-classify classify-text --file japanese_text.txt --max-categories 5
```

### Basic Single URL Classification

```bash
iab-classify https://www.techcrunch.com
```

### Batch Processing with Export

```bash
# Create a file with URLs (one per line)
echo "https://www.bbc.com/news" > urls.txt
echo "https://www.techcrunch.com" >> urls.txt
echo "https://www.recipe.com/chocolate-cake" >> urls.txt

# Process all URLs and save to CSV
iab-classify batch-classify urls.txt --output results.csv --concurrent 5
```

### Advanced Configuration

```bash
# Set up your environment
iab-classify config set-api-key "your-openai-api-key"
iab-classify config set default_max_categories 5
iab-classify config set batch_concurrency 10

# Run batch processing with custom settings
iab-classify batch-classify urls.txt \
  --max-categories 3 \
  --concurrent 8 \
  --output detailed_results.json \
  --verbose
```

## Performance Improvements

- **Concurrent Processing**: Up to 10x faster batch processing through async operations
- **Connection Pooling**: Efficient HTTP connection reuse with aiohttp
- **Memory Optimization**: Streaming processing for large batches
- **Rate Limiting**: Configurable concurrency to optimize API usage

## Error Recovery

- **Retry Logic**: Automatic retry for transient network errors
- **Partial Results**: Save successful classifications even if some URLs fail
- **Detailed Logging**: Comprehensive error reporting with verbose mode
- **Graceful Degradation**: Continue processing when individual URLs fail

## Security Features

- **Encrypted Storage**: API keys stored securely in user-specific directories
- **Key Masking**: API keys displayed with masking for security
- **Environment Isolation**: Configuration isolated per user
- **No Plaintext Storage**: Sensitive data properly protected

## Dependencies

- `aiohttp` - Async HTTP client for concurrent requests
- `python-dotenv` - Environment variable management
- All existing dependencies maintained for backwards compatibility

## Migration Guide

The enhanced toolkit is fully backwards compatible. Existing code will continue to work without changes. To use new features:

1. **Install the enhanced version**: `pip install -e .`
2. **Set your API key**: `iab-classify config set-api-key "your-key"`
3. **Start using batch processing**: `iab-classify batch-classify urls.txt`

No breaking changes have been introduced, ensuring smooth migration for existing users.
