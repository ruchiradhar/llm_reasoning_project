# Example Results

This directory contains benchmark results in JSON and CSV formats.

## File Naming Convention

- `results_YYYYMMDD_HHMMSS.json` - Detailed results with all model responses
- `leaderboard_YYYYMMDD_HHMMSS.csv` - Leaderboard snapshot
- `leaderboard_latest.csv` - Most recent leaderboard (always up to date)

## Result Structure

### JSON Results
```json
{
  "model_name": "model-identifier",
  "parameters": 50000,
  "math_score": 40.0,
  "math_correct": 4,
  "math_total": 10,
  "logic_score": 30.0,
  "logic_correct": 3,
  "logic_total": 10,
  "overall_score": 35.0,
  "timestamp": "2026-01-20T10:30:00"
}
```

### CSV Leaderboard Columns
- `rank`: Model ranking (1 = best)
- `model_name`: HuggingFace model identifier
- `parameters`: Total model parameters
- `overall_score`: Average score across all tasks
- `math_score`: Math reasoning task score
- `logic_score`: Logic reasoning task score
- `math_correct`: Number of correct math answers
- `math_total`: Total math questions
- `logic_correct`: Number of correct logic answers
- `logic_total`: Total logic questions
- `timestamp`: Evaluation timestamp
