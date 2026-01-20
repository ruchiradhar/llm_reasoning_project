# Contributing to LLM Reasoning Benchmark

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit: `git commit -m "Add your feature"`
7. Push: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Keep functions focused and modular
- Write descriptive variable names

## Testing

Before submitting a PR:
- Test with multiple models
- Verify results are saved correctly
- Check that leaderboard displays properly
- Ensure CLI arguments work as expected

## Adding New Tasks

To add a new reasoning task:

1. Create a new file in `tasks/` directory
2. Implement a class with these methods:
   - `__init__()`: Initialize task with questions
   - `run_task(model_loader)`: Execute the task
   - `evaluate_response()`: Score responses
   - `get_task_description()`: Return task description

3. Update `benchmark.py` to include the new task
4. Add documentation to README.md

## Adding New Models

To add models:
- Update `SMALL_MODELS` list in `src/model_loader.py`
- Ensure models are compatible with HuggingFace transformers
- Verify models can run on CPU

## Pull Request Guidelines

- Provide clear description of changes
- Include examples if adding features
- Update documentation as needed
- Ensure code follows project style
- Test thoroughly before submitting

## Questions?

Open an issue for:
- Bug reports
- Feature requests
- Questions about implementation
- Suggestions for improvement

Thank you for contributing!
