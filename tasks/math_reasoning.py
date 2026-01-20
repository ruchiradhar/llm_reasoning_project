"""
Math reasoning tasks for evaluating LLM mathematical capabilities.
"""

import re
from typing import List, Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class MathReasoningTask:
    """Math reasoning task evaluator"""
    
    def __init__(self):
        """Initialize math reasoning task with test cases"""
        self.tasks = [
            {
                "id": 1,
                "question": "What is 15 + 27?",
                "answer": "42",
                "difficulty": "easy"
            },
            {
                "id": 2,
                "question": "If you have 3 apples and buy 5 more, how many apples do you have in total?",
                "answer": "8",
                "difficulty": "easy"
            },
            {
                "id": 3,
                "question": "What is 12 * 3?",
                "answer": "36",
                "difficulty": "easy"
            },
            {
                "id": 4,
                "question": "If a book costs $15 and you have $50, how much money will you have left after buying the book?",
                "answer": "35",
                "difficulty": "medium"
            },
            {
                "id": 5,
                "question": "What is 100 - 47?",
                "answer": "53",
                "difficulty": "easy"
            },
            {
                "id": 6,
                "question": "If you divide 48 by 6, what do you get?",
                "answer": "8",
                "difficulty": "medium"
            },
            {
                "id": 7,
                "question": "A rectangle has a length of 8 and width of 5. What is its area?",
                "answer": "40",
                "difficulty": "medium"
            },
            {
                "id": 8,
                "question": "What is 7 + 8 + 5?",
                "answer": "20",
                "difficulty": "easy"
            },
            {
                "id": 9,
                "question": "If a train travels 60 miles in 2 hours, what is its speed in miles per hour?",
                "answer": "30",
                "difficulty": "medium"
            },
            {
                "id": 10,
                "question": "What is 25 * 4?",
                "answer": "100",
                "difficulty": "easy"
            }
        ]
    
    def extract_answer(self, text: str) -> str:
        """
        Extract numerical answer from generated text.
        
        Args:
            text: Generated text from model
            
        Returns:
            Extracted answer as string
        """
        # Look for numbers in the response
        numbers = re.findall(r'\b\d+\.?\d*\b', text)
        
        if numbers:
            # Return the last number found (often the final answer)
            return numbers[-1].rstrip('.')
        
        return ""
    
    def evaluate_response(self, response: str, correct_answer: str) -> bool:
        """
        Evaluate if the model's response contains the correct answer.
        
        Args:
            response: Model's generated response
            correct_answer: Correct answer
            
        Returns:
            True if correct, False otherwise
        """
        extracted = self.extract_answer(response)
        
        # Check if extracted answer matches correct answer
        try:
            # Try numeric comparison
            return float(extracted) == float(correct_answer)
        except (ValueError, TypeError):
            # Fall back to string comparison
            return extracted.lower().strip() == correct_answer.lower().strip()
    
    def run_task(self, model_loader) -> Dict[str, Any]:
        """
        Run math reasoning task on a model.
        
        Args:
            model_loader: ModelLoader instance with loaded model
            
        Returns:
            Dictionary containing task results
        """
        logger.info(f"Running math reasoning task on {model_loader.model_name}")
        
        results = []
        correct_count = 0
        
        for task in self.tasks:
            question = task["question"]
            correct_answer = task["answer"]
            
            # Create prompt
            prompt = f"Question: {question}\nAnswer:"
            
            # Generate response
            responses = model_loader.generate_text(
                prompt,
                max_length=50,
                temperature=0.3,  # Lower temperature for more focused answers
                num_return_sequences=1
            )
            
            if responses:
                response = responses[0]
                is_correct = self.evaluate_response(response, correct_answer)
                
                if is_correct:
                    correct_count += 1
                
                results.append({
                    "task_id": task["id"],
                    "question": question,
                    "correct_answer": correct_answer,
                    "model_response": response,
                    "extracted_answer": self.extract_answer(response),
                    "is_correct": is_correct,
                    "difficulty": task["difficulty"]
                })
            else:
                results.append({
                    "task_id": task["id"],
                    "question": question,
                    "correct_answer": correct_answer,
                    "model_response": "ERROR: No response generated",
                    "extracted_answer": "",
                    "is_correct": False,
                    "difficulty": task["difficulty"]
                })
        
        score = (correct_count / len(self.tasks)) * 100
        
        return {
            "task_type": "math_reasoning",
            "total_questions": len(self.tasks),
            "correct_answers": correct_count,
            "score": score,
            "details": results
        }
    
    def get_task_description(self) -> str:
        """Get description of the math reasoning task"""
        return "Math Reasoning: Tests basic arithmetic and mathematical problem-solving"
