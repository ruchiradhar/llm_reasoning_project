# Quick Start Guide

Get up and running with the LLM Reasoning Benchmark in minutes!

## Prerequisites

- Python 3.8 or higher
- pip package manager
- ~500MB disk space for models
- Internet connection (for downloading models)

## Installation Steps

### 1. Set Up Environment

```bash
# Navigate to project directory
cd llm_reasoning_project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- PyTorch
- Transformers
- HuggingFace Hub
- pandas, numpy, tabulate, tqdm

### 3. Run Your First Benchmark

```bash
# Test with a single tiny model (fastest)
python benchmark.py --models sshleifer/tiny-gpt2

# Or run the full benchmark (all models)
python benchmark.py
```

## What Happens During Benchmark?

1. **Model Download**: Models are downloaded from HuggingFace (cached for future use)
2. **Math Tasks**: 10 math reasoning questions are evaluated
3. **Logic Tasks**: 10 logic reasoning questions are evaluated
4. **Scoring**: Responses are automatically scored
5. **Leaderboard**: Results are ranked and displayed
6. **Save Results**: JSON and CSV files are saved to `results/` directory

## Understanding the Output

### Terminal Output
```
🚀 LLM REASONING BENCHMARK 🚀
Evaluating 2 model(s) on:
  • Math Reasoning: Tests basic arithmetic
  • Logic Reasoning: Tests logical thinking

[1/2] Evaluating model: sshleifer/tiny-gpt2
✓ Loaded model with 10,000 parameters
  ✓ Math Score: 40.00% (4/10)
  ✓ Logic Score: 30.00% (3/10)
  Overall Score: 35.00%
```

### Leaderboard
Models are ranked by overall score (average of math + logic scores)

### Saved Files
- `results/results_<timestamp>.json` - Detailed results
- `results/leaderboard_<timestamp>.csv` - Leaderboard data
- `results/leaderboard_latest.csv` - Always current leaderboard

## Common Commands

```bash
# List available models
python benchmark.py --list-models

# Run on GPU (if available)
python benchmark.py --device cuda

# Run specific models
python benchmark.py --models model1 model2

# Don't save results
python benchmark.py --no-save

# Run example scripts
python examples.py
```

## Troubleshooting

### Model Download Issues
If model download fails:
```bash
# Clear HuggingFace cache
rm -rf ~/.cache/huggingface/

# Try again
python benchmark.py
```

### Out of Memory
If you get memory errors:
- Use smaller models only
- Ensure no other applications are using memory
- Close unnecessary programs

### Import Errors
If you get import errors:
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

## Next Steps

1. **Explore Results**: Check the `results/` directory
2. **Try Examples**: Run `python examples.py`
3. **Add Custom Tasks**: See `CONTRIBUTING.md`
4. **Customize Models**: Edit `src/model_loader.py`

## Support

- Check existing GitHub issues
- Read the full README.md
- Review CONTRIBUTING.md for development help

Happy benchmarking! 🚀
