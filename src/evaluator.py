"""
Evaluation and leaderboard generation for LLM reasoning benchmark.
"""

import json
import pandas as pd
from tabulate import tabulate
from datetime import datetime
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class Evaluator:
    """Evaluate models and generate leaderboard"""
    
    def __init__(self):
        """Initialize evaluator"""
        self.results = []
    
    def add_result(
        self, 
        model_name: str, 
        model_info: Dict[str, Any],
        math_results: Dict[str, Any],
        logic_results: Dict[str, Any]
    ):
        """
        Add evaluation results for a model.
        
        Args:
            model_name: Name of the model
            model_info: Model information dictionary
            math_results: Math reasoning task results
            logic_results: Logic reasoning task results
        """
        result = {
            "model_name": model_name,
            "parameters": model_info.get("parameters", 0),
            "math_score": math_results.get("score", 0),
            "math_correct": math_results.get("correct_answers", 0),
            "math_total": math_results.get("total_questions", 0),
            "logic_score": logic_results.get("score", 0),
            "logic_correct": logic_results.get("correct_answers", 0),
            "logic_total": logic_results.get("total_questions", 0),
            "timestamp": datetime.now().isoformat()
        }
        
        # Calculate overall score (average of both tasks)
        result["overall_score"] = (result["math_score"] + result["logic_score"]) / 2
        
        self.results.append(result)
        logger.info(f"Added results for {model_name}: Overall Score = {result['overall_score']:.2f}%")
    
    def generate_leaderboard(self) -> pd.DataFrame:
        """
        Generate leaderboard from results.
        
        Returns:
            DataFrame containing leaderboard
        """
        if not self.results:
            logger.warning("No results to generate leaderboard")
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = pd.DataFrame(self.results)
        
        # Sort by overall score (descending)
        df = df.sort_values("overall_score", ascending=False)
        
        # Add rank
        df.insert(0, "rank", range(1, len(df) + 1))
        
        return df
    
    def display_leaderboard(self, detailed: bool = False):
        """
        Display leaderboard in terminal.
        
        Args:
            detailed: Whether to show detailed scores
        """
        df = self.generate_leaderboard()
        
        if df.empty:
            print("No results available for leaderboard.")
            return
        
        print("\n" + "="*80)
        print("🏆 LLM REASONING BENCHMARK LEADERBOARD 🏆".center(80))
        print("="*80 + "\n")
        
        if detailed:
            # Detailed view with all columns
            display_cols = [
                "rank", "model_name", "parameters", 
                "overall_score", "math_score", "logic_score",
                "math_correct", "math_total", "logic_correct", "logic_total"
            ]
            display_df = df[display_cols].copy()
            
            # Format numeric columns
            display_df["parameters"] = display_df["parameters"].apply(lambda x: f"{x:,}")
            display_df["overall_score"] = display_df["overall_score"].apply(lambda x: f"{x:.2f}%")
            display_df["math_score"] = display_df["math_score"].apply(lambda x: f"{x:.2f}%")
            display_df["logic_score"] = display_df["logic_score"].apply(lambda x: f"{x:.2f}%")
            display_df["math_correct"] = display_df.apply(lambda x: f"{x['math_correct']}/{x['math_total']}", axis=1)
            display_df["logic_correct"] = display_df.apply(lambda x: f"{x['logic_correct']}/{x['logic_total']}", axis=1)
            
            # Drop individual total columns
            display_df = display_df.drop(["math_total", "logic_total"], axis=1)
            
            # Rename columns for display
            display_df.columns = [
                "Rank", "Model", "Parameters", 
                "Overall", "Math", "Logic",
                "Math Score", "Logic Score"
            ]
        else:
            # Simple view with key columns
            display_cols = ["rank", "model_name", "overall_score", "math_score", "logic_score"]
            display_df = df[display_cols].copy()
            
            # Format scores
            display_df["overall_score"] = display_df["overall_score"].apply(lambda x: f"{x:.2f}%")
            display_df["math_score"] = display_df["math_score"].apply(lambda x: f"{x:.2f}%")
            display_df["logic_score"] = display_df["logic_score"].apply(lambda x: f"{x:.2f}%")
            
            # Rename columns
            display_df.columns = ["Rank", "Model", "Overall Score", "Math Score", "Logic Score"]
        
        print(tabulate(display_df, headers="keys", tablefmt="grid", showindex=False))
        print("\n" + "="*80 + "\n")
    
    def save_results(self, output_dir: str = "results"):
        """
        Save results to files.
        
        Args:
            output_dir: Directory to save results
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed JSON
        json_path = os.path.join(output_dir, f"results_{timestamp}.json")
        with open(json_path, "w") as f:
            json.dump(self.results, f, indent=2)
        logger.info(f"Saved detailed results to {json_path}")
        
        # Save leaderboard CSV
        df = self.generate_leaderboard()
        csv_path = os.path.join(output_dir, f"leaderboard_{timestamp}.csv")
        df.to_csv(csv_path, index=False)
        logger.info(f"Saved leaderboard to {csv_path}")
        
        # Save latest leaderboard (overwrite)
        latest_path = os.path.join(output_dir, "leaderboard_latest.csv")
        df.to_csv(latest_path, index=False)
        logger.info(f"Saved latest leaderboard to {latest_path}")
        
        return {
            "json": json_path,
            "csv": csv_path,
            "latest": latest_path
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics.
        
        Returns:
            Dictionary with summary statistics
        """
        if not self.results:
            return {}
        
        df = pd.DataFrame(self.results)
        
        return {
            "total_models": len(self.results),
            "avg_overall_score": df["overall_score"].mean(),
            "avg_math_score": df["math_score"].mean(),
            "avg_logic_score": df["logic_score"].mean(),
            "best_model": df.loc[df["overall_score"].idxmax(), "model_name"],
            "best_overall_score": df["overall_score"].max(),
            "best_math_model": df.loc[df["math_score"].idxmax(), "model_name"],
            "best_math_score": df["math_score"].max(),
            "best_logic_model": df.loc[df["logic_score"].idxmax(), "model_name"],
            "best_logic_score": df["logic_score"].max()
        }
