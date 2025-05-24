# Text Classification Feature

## Overview

The IAB Toolkit now supports direct text classification without needing URLs. This is perfect for classifying content you already have as text, including text in different languages like Japanese.

## Usage

### Command: `classify-text`

The new `classify-text` command allows you to classify text directly in two ways:

1. **Direct text input:**

```bash
iab-classify classify-text "Your text content here"
```

2. **From a file:**

```bash
iab-classify classify-text --file your_text_file.txt
```

### Examples

#### Basic Text Classification

```bash
# Classify Japanese text about Toyota RAV4
iab-classify classify-text "トヨタRAV4は、トヨタ自動車が製造・販売しているSUVです。1994年に初代モデルが発売され、現在は5代目となっています。" --embedding-only --no-persona
```

#### From File

```bash
# Create a text file with your content
echo "Toyota RAV4 is a compact SUV manufactured by Toyota. It features advanced safety technology and hybrid engine options." > content.txt

# Classify the content
iab-classify classify-text --file content.txt
```

#### With JSON Output

```bash
# Get structured JSON output
iab-classify classify-text --file content.txt --json
```

### Options

- `--file` / `-f`: Read text from a file instead of command line
- `--json`: Output results in JSON format for programmatic use
- `--max-categories N`: Return up to N categories (default: 3)
- `--embedding-only`: Use only embedding-based classification (faster, no GPT)
- `--no-persona`: Skip persona generation
- `--verbose` / `-v`: Enable detailed logging

### Output Format

#### Human-Readable Output

```
==================================================
TEXT CLASSIFICATION RESULTS
==================================================
Embedding Categories:
  1. Automotive (Score: 0.85)
  2. Technology (Score: 0.78)
  3. Consumer Electronics (Score: 0.72)

Final Categories (after GPT): Same as embedding results

==============================
TIER 2 CATEGORIES (Client Focus)
==============================
1. Automotive Technology (Score: 0.850)
2. Consumer Electronics (Score: 0.720)

Persona:
  25-34 / neutral / enthusiast
  Tech-savvy automotive enthusiast interested in hybrid vehicles
```

#### JSON Output

```json
{
  "text_length": 450,
  "categories_embedding": [
    {
      "id": "123",
      "name": "Automotive",
      "score": 0.85,
      "tier_1": "Automotive",
      "tier_2": "Automotive Technology",
      "tier_3": "Hybrid Vehicles",
      "tier_4": null
    }
  ],
  "categories_final": [...],
  "persona": {
    "age_band": "25-34",
    "gender_tilt": "neutral",
    "tech_affinity": "enthusiast",
    "short_description": "Tech-savvy automotive enthusiast"
  }
}
```

## Special Features for Your Use Case

### Tier 2 Categories

The output specifically highlights Tier 2 categories as requested, showing them in a dedicated section for easy identification.

### Japanese Text Support

The system fully supports Japanese text classification. The embedding model can understand Japanese content and classify it appropriately into IAB categories.

### Performance Modes

- **Fast Mode**: Use `--embedding-only --no-persona` for quick results
- **Full Mode**: Default behavior includes GPT refinement and persona generation
- **Structured Mode**: Use `--json` for programmatic processing

## Cross-Language Classification

### Japanese Text Support

The system supports Japanese text classification by adjusting the similarity threshold:

```bash
# Default threshold (0.40) may be too high for cross-language classification
iab-classify classify-text -f japanese_text.txt --min-score 0.20

# For better results with Japanese text, use lower thresholds
iab-classify classify-text "トヨタRAV4は、トヨタ自動車が製造・販売しているSUVです。" --min-score 0.15 --max-categories 5
```

**Recommended Settings for Japanese Text:**

- `--min-score 0.20` - Good balance for most Japanese content
- `--min-score 0.15` - More permissive, catches more categories
- `--max-categories 5` - Get more classification options

**Example Results for Japanese Toyota RAV4 Text:**

- Embedding: SUV (0.32), Off-Road Vehicles (0.32), Minivan (0.28)
- GPT Enhancement: Automotive (0.85), Vehicles (0.85), SUVs (0.85)
- Persona: 25-34|35-49 / neutral / enthusiast

## Integration Examples

### Python Script

```python
import subprocess
import json

def classify_text(text):
    result = subprocess.run([
        'iab-classify', 'classify-text', text,
        '--json', '--embedding-only', '--no-persona'
    ], capture_output=True, text=True)

    return json.loads(result.stdout)

# Use it
categories = classify_text("Your Japanese text here")
for cat in categories['categories_final']:
    print(f"Category: {cat['name']} (Tier 2: {cat['tier_2']})")
```

### Batch Processing Text Files

```bash
# Process multiple text files
for file in *.txt; do
    echo "Processing $file"
    iab-classify classify-text --file "$file" --json > "${file%.txt}_results.json"
done
```
