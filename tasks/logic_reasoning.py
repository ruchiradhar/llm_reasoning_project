"""
Logic reasoning tasks for evaluating LLM logical thinking capabilities.
"""

import re
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class LogicReasoningTask:
    """Logic reasoning task evaluator"""
    
    def __init__(self):
        """Initialize logic reasoning task with test cases"""
        self.tasks = [
            {
                "id": 1,
                "question": "If all cats are animals and Fluffy is a cat, is Fluffy an animal? Answer yes or no.",
                "answer": "yes",
                "difficulty": "easy"
            },
            {
                "id": 2,
                "question": "True or False: If it is raining, the ground is wet. It is raining. Therefore, the ground is wet.",
                "answer": "true",
                "difficulty": "easy"
            },
            {
                "id": 3,
                "question": "Which is heavier: a pound of feathers or a pound of bricks? Answer: feathers, bricks, or same.",
                "answer": "same",
                "difficulty": "medium"
            },
            {
                "id": 4,
                "question": "If A is taller than B, and B is taller than C, is A taller than C? Answer yes or no.",
                "answer": "yes",
                "difficulty": "easy"
            },
            {
                "id": 5,
                "question": "Is the following statement logical? 'All birds can fly. Penguins are birds. Therefore penguins can fly.' Answer yes or no.",
                "answer": "no",
                "difficulty": "medium"
            },
            {
                "id": 6,
                "question": "If you flip a fair coin twice, can you get two heads in a row? Answer yes or no.",
                "answer": "yes",
                "difficulty": "easy"
            },
            {
                "id": 7,
                "question": "True or False: If some dogs are brown and Max is brown, then Max is definitely a dog.",
                "answer": "false",
                "difficulty": "medium"
            },
            {
                "id": 8,
                "question": "Which comes next in the pattern: 2, 4, 6, 8, ?",
                "answer": "10",
                "difficulty": "easy"
            },
            {
                "id": 9,
                "question": "If today is Monday, what day will it be in 7 days? Answer with the day name.",
                "answer": "monday",
                "difficulty": "easy"
            },
            {
                "id": 10,
                "question": "Is it possible for something to be both completely red and completely blue at the same time? Answer yes or no.",
                "answer": "no",
                "difficulty": "easy"
            }
        ]
    
    def extract_answer(self, text: str, question_type: str = "general") -> str:
        """
        Extract answer from generated text.
        
        Args:
            text: Generated text from model
            question_type: Type of question (affects extraction)
            
        Returns:
            Extracted answer as string
        """
        text_lower = text.lower()
        
        # Look for yes/no answers
        if "yes" in text_lower:
            return "yes"
        if "no" in text_lower:
            return "no"
        
        # Look for true/false answers
        if "true" in text_lower:
            return "true"
        if "false" in text_lower:
            return "false"
        
        # Look for "same"
        if "same" in text_lower or "equal" in text_lower:
            return "same"
        
        # Look for days of week
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for day in days:
            if day in text_lower:
                return day
        
        # Look for numbers
        numbers = re.findall(r'\b\d+\b', text)
        if numbers:
            return numbers[-1]
        
        # Look for specific words (feathers, bricks)
        if "feather" in text_lower:
            return "feathers"
        if "brick" in text_lower:
            return "bricks"
        
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
        
        # Normalize and compare
        return extracted.lower().strip() == correct_answer.lower().strip()
    
    def run_task(self, model_loader) -> Dict[str, Any]:
        """
        Run logic reasoning task on a model.
        
        Args:
            model_loader: ModelLoader instance with loaded model
            
        Returns:
            Dictionary containing task results
        """
        logger.info(f"Running logic reasoning task on {model_loader.model_name}")
        
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
            "task_type": "logic_reasoning",
            "total_questions": len(self.tasks),
            "correct_answers": correct_count,
            "score": score,
            "details": results
        }
    
    def get_task_description(self) -> str:
        """Get description of the logic reasoning task"""
        return "Logic Reasoning: Tests logical thinking, deduction, and pattern recognition"
