# 🧠 LLM Reasoning Benchmark

A comprehensive benchmark suite for evaluating small language models on reasoning tasks. This project tests multiple LLMs from HuggingFace on mathematical and logical reasoning challenges, generating comparative leaderboards to assess their capabilities.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Project Overview

This project demonstrates:
- **Model Loading & Management**: Efficient loading of HuggingFace transformer models
- **Task-Based Evaluation**: Structured evaluation framework for reasoning tasks
- **Automated Scoring**: Intelligent answer extraction and scoring algorithms
- **Results Visualization**: Clean leaderboard generation and results tracking
- **Production-Ready Code**: Modular architecture with proper logging and error handling

## 📊 Features

- ✅ **Multiple Model Support**: Evaluate various small LLMs (< 1M parameters)
- ✅ **Dual Task Evaluation**: 
  - Math Reasoning (10 questions)
  - Logic Reasoning (10 questions)
- ✅ **Automated Leaderboard**: Ranked comparison of model performance
- ✅ **Result Persistence**: JSON and CSV output formats
- ✅ **CLI Interface**: Easy-to-use command-line interface
- ✅ **Extensible Architecture**: Simple to add new tasks or models

## 🏗️ Project Structure

```
llm_reasoning_project/
├── benchmark.py              # Main benchmark script
├── requirements.txt          # Project dependencies
├── setup.py                 # Package setup configuration
├── README.md                # Project documentation
├── LICENSE                  # MIT license
├── .gitignore              # Git ignore rules
│
├── src/                     # Source code
│   ├── __init__.py
│   ├── model_loader.py      # HuggingFace model loader
│   └── evaluator.py         # Evaluation and leaderboard generation
│
├── tasks/                   # Task implementations
│   ├── __init__.py
│   ├── math_reasoning.py    # Math reasoning tasks
│   └── logic_reasoning.py   # Logic reasoning tasks
│
└── results/                 # Output directory (generated)
    ├── results_<timestamp>.json
    ├── leaderboard_<timestamp>.csv
    └── leaderboard_latest.csv
```

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd llm_reasoning_project

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Benchmark

```bash
# Run benchmark on all default models
python benchmark.py

# Run on specific models
python benchmark.py --models sshleifer/tiny-gpt2 hf-internal-testing/tiny-random-gpt2

# List available models
python benchmark.py --list-models

# Run on GPU (if available)
python benchmark.py --device cuda

# Run without saving results
python benchmark.py --no-save
```

## 📋 Available Models

The benchmark includes several tiny models suitable for testing:

- `sshleifer/tiny-gpt2` - Minimal GPT-2 variant (~10-50K parameters)
- `hf-internal-testing/tiny-random-gpt2` - Random initialized tiny GPT-2
- `sshleifer/tiny-ctrl` - Tiny CTRL model variant
- `distilgpt2` - Distilled GPT-2 (~82M parameters)

**Note**: Finding models under 1M parameters is challenging as most production LLMs are much larger. The included models represent the smallest available variants for demonstration purposes.

## 🧪 Task Details

### Math Reasoning (10 Questions)
Tests basic arithmetic and mathematical problem-solving:
- Addition, subtraction, multiplication, division
- Word problems
- Area calculations
- Speed/distance problems

**Example**: "If you have 3 apples and buy 5 more, how many apples do you have in total?"

### Logic Reasoning (10 Questions)
Tests logical thinking, deduction, and pattern recognition:
- Syllogistic reasoning
- Pattern completion
- True/false logic evaluation
- Temporal reasoning

**Example**: "If A is taller than B, and B is taller than C, is A taller than C?"

## 📈 Evaluation Metrics

Each model receives:
- **Math Score**: Percentage correct on math tasks (0-100%)
- **Logic Score**: Percentage correct on logic tasks (0-100%)
- **Overall Score**: Average of math and logic scores

Results are ranked in a leaderboard format showing comparative performance.

## 🎨 Example Output

```
================================================================================
                  🏆 LLM REASONING BENCHMARK LEADERBOARD 🏆                     
================================================================================

╔══════╦═══════════════════════════════════╦══════════╦═════════╦═════════╗
║ Rank ║ Model                             ║ Overall  ║ Math    ║ Logic   ║
╠══════╬═══════════════════════════════════╬══════════╬═════════╬═════════╣
║    1 ║ sshleifer/tiny-gpt2              ║ 35.00%   ║ 40.00%  ║ 30.00%  ║
║    2 ║ hf-internal-testing/tiny-random-  ║ 25.00%   ║ 20.00%  ║ 30.00%  ║
║      ║ gpt2                              ║          ║         ║         ║
╚══════╩═══════════════════════════════════╩══════════╩═════════╩═════════╝
```

## 🔧 Technical Implementation

### Key Components

1. **ModelLoader** (`src/model_loader.py`)
   - Loads models from HuggingFace Hub
   - Manages tokenization and text generation
   - Provides parameter counting and model info

2. **Task Evaluators** (`tasks/`)
   - `MathReasoningTask`: Math problem evaluation
   - `LogicReasoningTask`: Logic problem evaluation
   - Answer extraction using regex and heuristics
   - Automated scoring with detailed results

3. **Evaluator** (`src/evaluator.py`)
   - Aggregates results across models and tasks
   - Generates ranked leaderboards
   - Exports results to JSON and CSV formats

4. **Benchmark Script** (`benchmark.py`)
   - CLI interface for running evaluations
   - Orchestrates model loading and task execution
   - Displays results and saves outputs

## 📦 Dependencies

- **torch**: PyTorch for model execution
- **transformers**: HuggingFace transformers library
- **huggingface-hub**: HuggingFace Hub integration
- **pandas**: Data manipulation and analysis
- **tabulate**: Pretty table formatting
- **numpy**: Numerical operations
- **tqdm**: Progress bars

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:

- Add more reasoning tasks (coding, common sense, etc.)
- Support for larger model variants
- Implement caching for faster re-evaluation
- Add confidence scoring for answers
- Create web interface for results
- Add more sophisticated answer extraction

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

Created as a demonstration of LLM evaluation capabilities and software engineering best practices.

## 🙏 Acknowledgments

- HuggingFace for providing model infrastructure
- The open-source ML community for model development
- PyTorch and Transformers teams for excellent libraries

## 🎯 Skills Demonstrated

This project showcases:
- Machine Learning model integration and evaluation
- Python software architecture and design patterns
- Task automation and benchmark frameworks
- Data analysis and visualization
- CLI tool development
- Comprehensive documentation
- Git version control and professional project organization
A project to compare to setup and compare common LLMs on reasoning tasks
