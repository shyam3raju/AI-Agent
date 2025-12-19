"""
LLM Factory for creating configured Groq LLM instances.
"""
import os
from typing import Optional
from langchain_groq import ChatGroq


class LLMFactory:
    """Factory for creating configured LLM instances."""
    
    @staticmethod
    def create_groq_llm(
        model: str = "llama-3.3-70b-versatile",
        temperature: float = 0.1,
        max_tokens: Optional[int] = 1024,
        timeout: Optional[int] = 60
    ) -> ChatGroq:
        """
        Create a Groq LLM instance with conservative settings.
        
        Args:
            model: Model name (llama-3.3-70b-versatile or llama-3.1-8b-instant)
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            timeout: Request timeout in seconds
            
        Returns:
            Configured ChatGroq instance
        """
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
            
        return ChatGroq(
            groq_api_key=api_key,
            model_name=model,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout
        )
    
    @staticmethod
    def create_fast_llm() -> ChatGroq:
        """Create a fast LLM for latency-sensitive operations."""
        return LLMFactory.create_groq_llm(
            model="llama-3.1-8b-instant",
            temperature=0.0,
            max_tokens=512
        )
    
    @staticmethod
    def create_reasoning_llm() -> ChatGroq:
        """Create a reasoning LLM for complex analysis."""
        return LLMFactory.create_groq_llm(
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            max_tokens=2048
        )