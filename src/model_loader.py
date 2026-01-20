"""
Model loader for small language models from HuggingFace.
This module handles loading and inference with models under 1M parameters.
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelLoader:
    """Load and manage small language models from HuggingFace"""
    
    # List of very small models (< 1M parameters)
    # Note: Most LLMs are much larger, so we're using tiny models for demonstration
    SMALL_MODELS = [
        "distilgpt2",  # ~82M params (still larger, but smallest GPT-2 variant)
        "sshleifer/tiny-gpt2",  # Tiny version for testing (~10-50K params)
        "sshleifer/tiny-ctrl",  # Another tiny model variant
        "hf-internal-testing/tiny-random-gpt2",  # Minimal GPT-2 for testing
    ]
    
    def __init__(self, model_name: str, device: str = "cpu"):
        """
        Initialize the model loader.
        
        Args:
            model_name: HuggingFace model identifier or path
            device: Device to load model on ('cpu' or 'cuda')
        """
        self.model_name = model_name
        self.device = device
        self.model = None
        self.tokenizer = None
        self.param_count = 0
        
    def load_model(self) -> bool:
        """
        Load the model and tokenizer from HuggingFace.
        
        Returns:
            bool: True if loading was successful, False otherwise
        """
        try:
            logger.info(f"Loading model: {self.model_name}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            
            # Set pad token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                trust_remote_code=True,
                torch_dtype=torch.float32
            ).to(self.device)
            
            # Count parameters
            self.param_count = sum(p.numel() for p in self.model.parameters())
            logger.info(f"Model loaded successfully with {self.param_count:,} parameters")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to load model {self.model_name}: {e}")
            return False
    
    def generate_text(
        self, 
        prompt: str, 
        max_length: int = 100,
        temperature: float = 0.7,
        num_return_sequences: int = 1
    ) -> List[str]:
        """
        Generate text from the model given a prompt.
        
        Args:
            prompt: Input text prompt
            max_length: Maximum length of generated text
            temperature: Sampling temperature (higher = more random)
            num_return_sequences: Number of sequences to generate
            
        Returns:
            List of generated text strings
        """
        if self.model is None or self.tokenizer is None:
            logger.error("Model not loaded. Call load_model() first.")
            return []
        
        try:
            # Tokenize input
            inputs = self.tokenizer(
                prompt, 
                return_tensors="pt", 
                padding=True,
                truncation=True
            ).to(self.device)
            
            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    temperature=temperature,
                    num_return_sequences=num_return_sequences,
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                )
            
            # Decode outputs
            generated_texts = [
                self.tokenizer.decode(output, skip_special_tokens=True)
                for output in outputs
            ]
            
            return generated_texts
            
        except Exception as e:
            logger.error(f"Error during text generation: {e}")
            return []
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded model.
        
        Returns:
            Dictionary containing model information
        """
        return {
            "name": self.model_name,
            "parameters": self.param_count,
            "device": self.device,
            "loaded": self.model is not None
        }
    
    @staticmethod
    def get_available_models() -> List[str]:
        """
        Get list of available small models.
        
        Returns:
            List of model names
        """
        return ModelLoader.SMALL_MODELS
