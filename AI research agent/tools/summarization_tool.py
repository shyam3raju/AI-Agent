"""
Summarization tool for condensing long text content.
"""
from langchain.tools import BaseTool
from langchain_core.messages import HumanMessage
from core.llm_factory import LLMFactory
from typing import Any


class SummarizationTool(BaseTool):
    """Tool for summarizing long text content."""
    
    name: str = "summarization_tool"
    description: str = (
        "Summarize long text content into concise, factual summaries. "
        "Input should be the text content to summarize. "
        "Returns a structured summary focusing on key facts and insights."
    )
    
    def _run(self, text: str) -> str:
        """
        Summarize the provided text content.
        
        Args:
            text: Text content to summarize
            
        Returns:
            Concise summary as string
        """
        try:
            # Use fast LLM for summarization
            llm = LLMFactory.create_fast_llm()
            
            prompt = f"""
            Summarize the following text content into a concise, factual summary.
            Focus on key facts, trends, and important information.
            Avoid opinions and speculation.
            Keep the summary under 200 words.
            
            Text to summarize:
            {text}
            
            Summary:
            """
            
            messages = [HumanMessage(content=prompt)]
            response = llm.invoke(messages)
            
            return response.content.strip()
            
        except Exception as e:
            # Fallback summary
            words = text.split()
            if len(words) > 100:
                # Simple extractive summary - first and key sentences
                sentences = text.split('.')
                summary_sentences = sentences[:2] + [s for s in sentences[2:5] if 'AI' in s or 'artificial intelligence' in s.lower()]
                return '. '.join(summary_sentences[:3]) + '.'
            else:
                return text
    
    async def _arun(self, text: str) -> str:
        """Async version of the summarization tool."""
        return self._run(text)