#!/usr/bin/env python3
"""
Main benchmark script for evaluating small LLMs on reasoning tasks.

This script loads small language models from HuggingFace and evaluates them
on math and logic reasoning tasks, then generates a leaderboard.
"""

import argparse
import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src.model_loader import ModelLoader
from tasks.math_reasoning import MathReasoningTask
from tasks.logic_reasoning import LogicReasoningTask
from src.evaluator import Evaluator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_benchmark(models: list, device: str = "cpu", save_results: bool = True):
    """
    Run benchmark on specified models.
    
    Args:
        models: List of model names to evaluate
        device: Device to run models on ('cpu' or 'cuda')
        save_results: Whether to save results to files
    """
    # Initialize tasks
    math_task = MathReasoningTask()
    logic_task = LogicReasoningTask()
    
    # Initialize evaluator
    evaluator = Evaluator()
    
    print("\n" + "="*80)
    print("🚀 LLM REASONING BENCHMARK 🚀".center(80))
    print("="*80)
    print(f"\nEvaluating {len(models)} model(s) on:")
    print(f"  • {math_task.get_task_description()}")
    print(f"  • {logic_task.get_task_description()}")
    print("="*80 + "\n")
    
    # Evaluate each model
    for i, model_name in enumerate(models, 1):
        print(f"\n[{i}/{len(models)}] Evaluating model: {model_name}")
        print("-" * 80)
        
        try:
            # Load model
            loader = ModelLoader(model_name, device=device)
            if not loader.load_model():
                logger.error(f"Failed to load model: {model_name}")
                continue
            
            model_info = loader.get_model_info()
            print(f"✓ Loaded model with {model_info['parameters']:,} parameters")
            
            # Run math reasoning task
            print(f"\n  Running math reasoning task...")
            math_results = math_task.run_task(loader)
            print(f"  ✓ Math Score: {math_results['score']:.2f}% ({math_results['correct_answers']}/{math_results['total_questions']})")
            
            # Run logic reasoning task
            print(f"\n  Running logic reasoning task...")
            logic_results = logic_task.run_task(loader)
            print(f"  ✓ Logic Score: {logic_results['score']:.2f}% ({logic_results['correct_answers']}/{logic_results['total_questions']})")
            
            # Add to evaluator
            evaluator.add_result(model_name, model_info, math_results, logic_results)
            
            print(f"\n  Overall Score: {(math_results['score'] + logic_results['score']) / 2:.2f}%")
            print("-" * 80)
            
        except Exception as e:
            logger.error(f"Error evaluating {model_name}: {e}", exc_info=True)
            continue
    
    # Display leaderboard
    evaluator.display_leaderboard(detailed=True)
    
    # Display summary
    summary = evaluator.get_summary()
    if summary:
        print("📊 BENCHMARK SUMMARY")
        print("="*80)
        print(f"Total Models Evaluated: {summary['total_models']}")
        print(f"Average Overall Score: {summary['avg_overall_score']:.2f}%")
        print(f"Average Math Score: {summary['avg_math_score']:.2f}%")
        print(f"Average Logic Score: {summary['avg_logic_score']:.2f}%")
        print(f"\n🏆 Best Overall: {summary['best_model']} ({summary['best_overall_score']:.2f}%)")
        print(f"🧮 Best Math: {summary['best_math_model']} ({summary['best_math_score']:.2f}%)")
        print(f"🧩 Best Logic: {summary['best_logic_model']} ({summary['best_logic_score']:.2f}%)")
        print("="*80 + "\n")
    
    # Save results
    if save_results:
        print("💾 Saving results...")
        paths = evaluator.save_results()
        print(f"  ✓ Detailed results: {paths['json']}")
        print(f"  ✓ Leaderboard CSV: {paths['csv']}")
        print(f"  ✓ Latest leaderboard: {paths['latest']}")
        print()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Benchmark small LLMs on reasoning tasks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run benchmark on all default models
  python benchmark.py

  # Run on specific models
  python benchmark.py --models sshleifer/tiny-gpt2 hf-internal-testing/tiny-random-gpt2

  # Run on GPU
  python benchmark.py --device cuda

  # Don't save results to file
  python benchmark.py --no-save
        """
    )
    
    parser.add_argument(
        "--models",
        nargs="+",
        help="List of model names to evaluate (default: all small models)"
    )
    
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        choices=["cpu", "cuda"],
        help="Device to run models on (default: cpu)"
    )
    
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't save results to files"
    )
    
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List available models and exit"
    )
    
    args = parser.parse_args()
    
    # List models if requested
    if args.list_models:
        print("\nAvailable small models:")
        for model in ModelLoader.get_available_models():
            print(f"  • {model}")
        print()
        return
    
    # Determine which models to evaluate
    if args.models:
        models = args.models
    else:
        models = ModelLoader.get_available_models()
    
    # Run benchmark
    try:
        run_benchmark(
            models=models,
            device=args.device,
            save_results=not args.no_save
        )
    except KeyboardInterrupt:
        print("\n\n⚠️  Benchmark interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Benchmark failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
