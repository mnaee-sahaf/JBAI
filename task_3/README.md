# Support Ticket Classifier - Local AI

A Python script that classifies support tickets into categories using zero-shot classification with a local AI model.

## Model Information

**Model:** `MoritzLaurer/deberta-v3-base-zeroshot-v2.0`

This is a DeBERTa-v3 model fine-tuned specifically for zero-shot classification tasks. It provides:
- **Size:** ~500 MB
- **Type:** Zero-shot text classification
- **Performance:** High accuracy with low memory footprint
- **Optimization:** Intent-based label engineering with descriptive labels for better classification

### Label Engineering Approach

Instead of using simple category names, this implementation uses descriptive labels that help the model better understand the intent:
- `"a technical failure, crash, error, or incorrect data"` → **bug**
- `"a billing, payment, invoice, or subscription issue"` → **billing**
- `"a suggestion to implement a new feature or improvement"` → **feature_request**
- `"a question asking for assistance or instructions on how to use the software or settings"` → **account_help**
- `"irrelevant text"` → **other**

### Additional Logic

The script includes heuristic-based refinement for ambiguous cases:
- If a message contains phrases like "How can I", "How do I", or "Can I" and the model's confidence is below 80%, it's re-routed from **feature_request** to **account_help**
- This helps distinguish between usage questions and actual feature suggestions

## Installation

### Prerequisites
- Python 3.8-3.12
- pip package manager
- At least 2GB of free RAM
- At least 1GB of free disk space

### Install Dependencies

```bash
pip install transformers torch
```

**Alternative:** Use the provided requirements file:

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
transformers>=4.30.0
torch>=2.0.0
```

## Usage

### Run the Script

```bash
python classify_tickets.py
```

### Using Custom Messages

Create a `messages.txt` file in the same directory with one message per line:

```
My custom support ticket 1
My custom support ticket 2
My custom support ticket 3
```

The script will automatically detect and use this file.

## Output

### JSON File: `classified_local.json`

```json
[
  {
    "text": "The app is not tracking my time on Android anymore.",
    "category": "bug",
    "score": 0.9234,
    "ai_logic": "a technical failure, crash, error, or incorrect data"
  },
  ...
]
```

### Terminal Summary

```
==================================================
CLASSIFICATION SUMMARY
==================================================
account_help: 4
billing: 4
bug: 6
feature_request: 6
other: 0
==================================================
```

## Classification Categories

- **bug** - Technical issues, crashes, errors, incorrect data
- **billing** - Payment, invoices, charges, subscriptions
- **feature_request** - New feature suggestions, improvements
- **account_help** - Usage questions, how-to, settings assistance
- **other** - Irrelevant or unclassified text

## Performance

- **First run:** ~2-3 minutes (model download + classification)
- **Subsequent runs:** ~30-40 seconds for 20 messages
- **Memory usage:** ~2GB RAM
- **Per message:** ~1-2 seconds on CPU

## Features

✅ Descriptive label engineering for better accuracy  
✅ Heuristic-based refinement for ambiguous cases  
✅ Automatic file detection (`messages.txt`)  
✅ Detailed output with AI reasoning  
✅ Real-time progress indicators  
✅ Lightweight and memory-efficient  

## Known Limitations

The model sometimes confuses **feature_request** and **account_help** tickets, which is why additional heuristic logic has been implemented to improve accuracy for these cases.

## Troubleshooting

### Issue: Out of memory
**Solution:** Close other applications or use a machine with more RAM

### Issue: Slow classification
**Solution:** This is normal on CPU. Consider using a GPU-enabled environment like Google Colab

### Issue: Model download fails
**Solution:** Check internet connection. The model will resume if interrupted

### Issue: Python 3.13 compatibility
**Solution:** Use Python 3.8-3.12 for best compatibility

## Project Structure

```
.
├── classify_tickets.py          # Main script
├── classified_local.json        # Output (generated)
├── messages.txt                 # Optional input file
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Example Output

```
Loading specialized zero-shot model...
Using: MoritzLaurer/deberta-v3-base-zeroshot-v2.0
Model loaded successfully!

File messages.txt not found, using built-in messages.
Classifying tickets...

[01] BUG             | The app is not tracking my time on Android anymore....
[02] BILLING        | I would like to upgrade my plan from Free to Pro....
[03] ACCOUNT_HELP   | How can I export all my timesheets to Excel?...
...
```

## License

This project uses the DeBERTa model from Hugging Face, which is licensed under Apache 2.0.

## Support

For issues or questions:
- Check Transformers documentation: https://huggingface.co/docs/transformers
- Model card: https://huggingface.co/MoritzLaurer/deberta-v3-base-zeroshot-v2.0

---

**Note:** The model runs entirely on your local machine. No API keys or external services required.