"""
Example script demonstrating how to use the benchmark components programmatically.
"""

from src.model_loader import ModelLoader
from tasks.math_reasoning import MathReasoningTask
from tasks.logic_reasoning import LogicReasoningTask
from src.evaluator import Evaluator


def example_single_model():
    """Example: Evaluate a single model"""
    print("Example 1: Evaluating a single model\n")
    print("="*60)
    
    # Load model
    model_name = "sshleifer/tiny-gpt2"
    loader = ModelLoader(model_name)
    
    if loader.load_model():
        print(f"✓ Loaded {model_name}")
        print(f"  Parameters: {loader.param_count:,}\n")
        
        # Run tasks
        math_task = MathReasoningTask()
        math_results = math_task.run_task(loader)
        
        logic_task = LogicReasoningTask()
        logic_results = logic_task.run_task(loader)
        
        # Display results
        print(f"Math Score: {math_results['score']:.2f}%")
        print(f"Logic Score: {logic_results['score']:.2f}%")
        print(f"Overall: {(math_results['score'] + logic_results['score']) / 2:.2f}%")


def example_text_generation():
    """Example: Generate text with a model"""
    print("\n\nExample 2: Text generation\n")
    print("="*60)
    
    loader = ModelLoader("sshleifer/tiny-gpt2")
    
    if loader.load_model():
        prompt = "Question: What is 2 + 2?\nAnswer:"
        responses = loader.generate_text(prompt, max_length=30)
        
        print(f"Prompt: {prompt}")
        print(f"Response: {responses[0]}")


def example_compare_models():
    """Example: Compare multiple models"""
    print("\n\nExample 3: Comparing multiple models\n")
    print("="*60)
    
    models = ["sshleifer/tiny-gpt2", "hf-internal-testing/tiny-random-gpt2"]
    evaluator = Evaluator()
    
    math_task = MathReasoningTask()
    logic_task = LogicReasoningTask()
    
    for model_name in models:
        print(f"\nEvaluating {model_name}...")
        loader = ModelLoader(model_name)
        
        if loader.load_model():
            math_results = math_task.run_task(loader)
            logic_results = logic_task.run_task(loader)
            model_info = loader.get_model_info()
            
            evaluator.add_result(model_name, model_info, math_results, logic_results)
    
    # Display leaderboard
    print("\n")
    evaluator.display_leaderboard()


if __name__ == "__main__":
    # Run examples
    # Note: These may take several minutes to complete
    
    print("LLM Reasoning Benchmark - Usage Examples")
    print("="*60)
    
    try:
        example_single_model()
        example_text_generation()
        example_compare_models()
        
        print("\n" + "="*60)
        print("✓ Examples completed successfully!")
        print("\nFor full benchmark, run: python benchmark.py")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("\nMake sure you have installed all dependencies:")
        print("  pip install -r requirements.txt")
