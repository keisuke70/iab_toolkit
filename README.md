# IAB Toolkit - Hybrid Text Classifier

A high-performance hybrid text classification package for IAB (Interactive Advertising Bureau) content categorization. This package uses advanced AI techniques to classify text content according to IAB taxonomy standards with exceptional accuracy.

## Features

- **Hybrid Classification**: Combines multiple AI techniques for optimal accuracy
- **Tier 1 Detection**: Specialized detector for top-level IAB categories
- **Multi-language Support**: Works with English, Japanese, and other languages
- **Fast Processing**: Optimized for performance and efficiency
- **Easy Integration**: Simple API for seamless integration into existing workflows
- **CLI Interface**: Command-line tool for batch processing and testing

## Installation

```bash
pip install iab-toolkit
```

## Quick Start

### Basic Usage

```python
from iab_toolkit import HybridIABClassifier

# Initialize the classifier
classifier = HybridIABClassifier()

# Classify text content
text = "Learn Python programming with our comprehensive online courses and tutorials."
result = classifier.classify(text)

print(f"Category: {result.category}")
print(f"Confidence: {result.confidence:.2f}")
print(f"Tier 1: {result.tier1}")
```

### Advanced Usage with Custom Configuration

```python
from iab_toolkit import HybridIABClassifier, OptimizedTier1Detector

# Initialize with custom settings
classifier = HybridIABClassifier(
    confidence_threshold=0.8,
    use_embeddings=True,
    max_retries=3
)

# For specialized Tier 1 detection
tier1_detector = OptimizedTier1Detector()
tier1_result = tier1_detector.detect(text)
```

## Command Line Interface

The package includes a powerful CLI for batch processing and testing:

### Basic CLI Usage

```bash
# Classify text directly
iab-hybrid "Your text content here"

# Read from file
iab-hybrid --file input.txt

# Output as JSON
iab-hybrid "Your text" --json

# Verbose output with detailed information
iab-hybrid "Your text" --verbose
```

### CLI Options

- `--file, -f`: Read text from a file
- `--json, -j`: Output results in JSON format
- `--verbose, -v`: Show detailed classification information
- `--test`: Run built-in test suite with sample data

### Example CLI Commands

```bash
# Test with sample data
iab-hybrid --test

# Process a file with JSON output
iab-hybrid --file content.txt --json

# Classify text with verbose output
iab-hybrid "Technology news and updates" --verbose
```

## API Reference

### HybridIABClassifier

The main classification class that provides comprehensive IAB content categorization.

#### Methods

##### `classify(text: str) -> FinalClassificationResult`

Classifies the given text and returns detailed results.

**Parameters:**
- `text` (str): The text content to classify

**Returns:**
- `FinalClassificationResult`: Object containing:
  - `category` (str): The classified IAB category
  - `confidence` (float): Confidence score (0.0 to 1.0)
  - `tier1` (str): Top-level IAB category
  - `subcategory` (str, optional): Subcategory if applicable
  - `reasoning` (str): AI reasoning for the classification

**Example:**
```python
result = classifier.classify("Breaking news about renewable energy developments")
print(f"Category: {result.category}")
print(f"Confidence: {result.confidence:.2f}")
print(f"Reasoning: {result.reasoning}")
```

### OptimizedTier1Detector

Specialized detector for identifying top-level IAB categories with high accuracy.

#### Methods

##### `detect(text: str) -> Tier1DetectionResult`

Detects the Tier 1 category for the given text.

**Parameters:**
- `text` (str): The text content to analyze

**Returns:**
- `Tier1DetectionResult`: Object containing tier 1 classification details

## Configuration

The package uses environment variables for configuration:

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Optional: Set custom API base URL
export OPENAI_API_BASE="https://your-custom-endpoint.com"
```

You can also create a `.env` file in your project directory:

```env
OPENAI_API_KEY=your-api-key-here
OPENAI_API_BASE=https://your-custom-endpoint.com
```

## IAB Taxonomy Support

This package supports the complete IAB Content Taxonomy, including:

- **Tier 1 Categories**: 26 top-level categories (Arts & Entertainment, Automotive, Business, etc.)
- **Tier 2 Categories**: Detailed subcategories for precise classification
- **Multi-level Classification**: Automatic detection of appropriate classification depth

### Supported Categories Include:

- Arts & Entertainment
- Automotive  
- Business and Finance
- Careers
- Education
- Family and Parenting
- Health & Fitness
- Food & Drink
- Hobbies & Interests
- Home & Garden
- Law, Government & Politics
- News
- Personal Finance
- Pets
- Real Estate
- Religion & Spirituality
- Science
- Shopping
- Sports
- Style & Fashion
- Technology & Computing
- Travel
- And more...

## Performance

The hybrid approach delivers exceptional accuracy:

- **Tier 1 Accuracy**: >95% on standard benchmarks
- **Overall Accuracy**: >90% across all categories
- **Processing Speed**: <2 seconds per classification
- **Multi-language**: Supports English, Japanese, and other major languages

## Examples

### Processing Multiple Texts

```python
from iab_toolkit import HybridIABClassifier

classifier = HybridIABClassifier()

texts = [
    "Latest smartphone reviews and tech news",
    "Healthy recipes for family dinners",
    "Stock market analysis and investment tips",
    "Travel guides for European destinations"
]

for text in texts:
    result = classifier.classify(text)
    print(f"Text: {text[:50]}...")
    print(f"Category: {result.category}")
    print(f"Confidence: {result.confidence:.2f}")
    print("-" * 50)
```

### Batch Processing with CLI

```bash
# Create a file with multiple texts
echo "Tech news and gadget reviews" > texts.txt
echo "Cooking recipes and food tips" >> texts.txt
echo "Financial planning advice" >> texts.txt

# Process each line
while IFS= read -r line; do
    echo "Text: $line"
    iab-hybrid "$line" --json
done < texts.txt
```

## Error Handling

The package includes robust error handling:

```python
from iab_toolkit import HybridIABClassifier
from iab_toolkit.exceptions import ClassificationError

classifier = HybridIABClassifier()

try:
    result = classifier.classify("Your text here")
    print(f"Success: {result.category}")
except ClassificationError as e:
    print(f"Classification failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for API calls

### Dependencies

- `openai` - For AI-powered classification
- `numpy` - For numerical computations
- `python-dotenv` - For environment variable management

## Contributing

We welcome contributions! Please see our contributing guidelines for details on how to submit pull requests, report issues, and suggest improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, questions, or feature requests:

- Open an issue on GitHub
- Check the documentation
- Review the examples in this README

## Changelog

### Version 0.3.0 (Current)
- Simplified package to focus solely on hybrid classification
- Removed legacy URL-based classifiers
- Improved performance and accuracy
- Enhanced CLI interface
- Better error handling and type annotations

### Version 0.2.0
- Added hybrid classification capabilities
- Introduced Tier 1 detection
- Multi-language support

### Version 0.1.0
- Initial release with basic classification features

---

**Note**: This package requires an OpenAI API key for operation. Make sure to set up your API credentials before using the classifier.