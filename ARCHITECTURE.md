# Project Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     LLM Reasoning Benchmark                      │
│                     benchmark.py (Main Entry)                    │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ├─────────────────┬──────────────────┬────────────┐
                 │                 │                  │            │
        ┌────────▼────────┐  ┌────▼─────┐   ┌───────▼───────┐    │
        │  Model Loader   │  │  Tasks   │   │  Evaluator    │    │
        │  (src/)         │  │ (tasks/) │   │  (src/)       │    │
        └────────┬────────┘  └────┬─────┘   └───────┬───────┘    │
                 │                 │                  │            │
                 │                 │                  │            │
        ┌────────▼────────┐  ┌────▼──────┐  ┌────────▼────────┐  │
        │ HuggingFace Hub │  │ Math Task │  │  Leaderboard    │  │
        │  (Models)       │  │Logic Task │  │  Generation     │  │
        └─────────────────┘  └───────────┘  └─────────────────┘  │
                                                                   │
                                                          ┌────────▼────────┐
                                                          │ Results Output  │
                                                          │ (results/)      │
                                                          │ - JSON          │
                                                          │ - CSV           │
                                                          └─────────────────┘
```

## Component Details

### 1. Model Loader (`src/model_loader.py`)
**Purpose**: Manage LLM loading and inference
**Key Functions**:
- Load models from HuggingFace Hub
- Generate text from prompts
- Count model parameters
- Provide model information

**Design Pattern**: Adapter Pattern (wraps HuggingFace API)

### 2. Task Modules (`tasks/`)
**Purpose**: Define and evaluate reasoning tasks

#### Math Reasoning (`math_reasoning.py`)
- 10 arithmetic and word problems
- Answer extraction via regex
- Scoring algorithm

#### Logic Reasoning (`logic_reasoning.py`)
- 10 logical deduction problems
- Pattern recognition
- Boolean logic evaluation

**Design Pattern**: Strategy Pattern (interchangeable tasks)

### 3. Evaluator (`src/evaluator.py`)
**Purpose**: Aggregate results and generate leaderboards
**Key Functions**:
- Collect results from multiple models
- Calculate scores and rankings
- Generate pandas DataFrame
- Export to multiple formats

**Design Pattern**: Facade Pattern (simplifies result handling)

### 4. Main Script (`benchmark.py`)
**Purpose**: CLI interface and orchestration
**Features**:
- Argument parsing
- Model loading loop
- Progress reporting
- Result display and saving

**Design Pattern**: Command Pattern (CLI commands)

## Data Flow

```
User Input (CLI)
    │
    ▼
Parse Arguments ──────► Select Models
    │
    ▼
For Each Model:
    │
    ├─► Load Model ────────► ModelLoader
    │
    ├─► Run Math Task ─────► MathReasoningTask
    │       │
    │       └─► Generate Responses
    │       └─► Extract Answers
    │       └─► Score Results
    │
    ├─► Run Logic Task ────► LogicReasoningTask
    │       │
    │       └─► Generate Responses
    │       └─► Extract Answers
    │       └─► Score Results
    │
    └─► Add to Evaluator ──► Store Results
    
Evaluator
    │
    ├─► Generate Leaderboard
    │
    ├─► Display Results
    │
    └─► Save to Files
            │
            ├─► JSON (detailed)
            └─► CSV (leaderboard)
```

## Class Diagram

```
┌─────────────────────────┐
│    ModelLoader          │
├─────────────────────────┤
│ - model_name            │
│ - device                │
│ - model                 │
│ - tokenizer             │
│ - param_count           │
├─────────────────────────┤
│ + load_model()          │
│ + generate_text()       │
│ + get_model_info()      │
└─────────────────────────┘
            │
            │ uses
            ▼
┌─────────────────────────┐       ┌──────────────────────────┐
│  MathReasoningTask      │       │  LogicReasoningTask      │
├─────────────────────────┤       ├──────────────────────────┤
│ - tasks[]               │       │ - tasks[]                │
├─────────────────────────┤       ├──────────────────────────┤
│ + run_task()            │       │ + run_task()             │
│ + extract_answer()      │       │ + extract_answer()       │
│ + evaluate_response()   │       │ + evaluate_response()    │
│ + get_task_description()│       │ + get_task_description() │
└─────────────────────────┘       └──────────────────────────┘
            │                                 │
            │                                 │
            └─────────┬───────────────────────┘
                      │ results
                      ▼
            ┌─────────────────────────┐
            │     Evaluator           │
            ├─────────────────────────┤
            │ - results[]             │
            ├─────────────────────────┤
            │ + add_result()          │
            │ + generate_leaderboard()│
            │ + display_leaderboard() │
            │ + save_results()        │
            │ + get_summary()         │
            └─────────────────────────┘
```

## Key Design Decisions

### 1. Modular Architecture
- Separate concerns: loading, evaluation, presentation
- Easy to extend with new tasks
- Simple to swap model sources

### 2. Task-Based Evaluation
- Each task is independent
- Tasks can be run in any order
- Easy to add new task types

### 3. Flexible Output
- Multiple export formats (JSON, CSV)
- Both detailed and summary views
- Timestamped for history tracking

### 4. Error Handling
- Graceful failure per model
- Logging throughout
- Continues on individual failures

### 5. CLI-First Design
- Command-line interface for automation
- Can be imported as library
- Suitable for CI/CD integration

## Extension Points

To extend the benchmark:

1. **Add New Tasks**: Create new class in `tasks/`
2. **Add New Models**: Update `SMALL_MODELS` list
3. **Change Scoring**: Modify evaluator scoring logic
4. **Add Metrics**: Extend result dictionaries
5. **New Output Formats**: Add methods to Evaluator

## Performance Considerations

- Models loaded one at a time (memory efficient)
- Results stored in memory (not disk until save)
- Generation is synchronous (no async yet)
- CPU-first design (GPU optional)

## Testing Strategy

Current: Manual testing with example models
Future: Unit tests for each component
- Mock model responses
- Test answer extraction
- Validate scoring logic
- Check leaderboard generation
