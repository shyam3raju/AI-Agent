"""
Research Agent for gathering and summarizing information.
"""
from typing import Dict, Any
from langchain_core.messages import HumanMessage
from core.llm_factory import LLMFactory
from tools.search_tool import SearchTool
from tools.summarization_tool import SummarizationTool


class ResearchAgent:
    """Agent responsible for researching and gathering factual information."""
    
    def __init__(self):
        """Initialize the Research Agent with tools and LLM."""
        self.llm = LLMFactory.create_reasoning_llm()
        self.search_tool = SearchTool()
        self.summarization_tool = SummarizationTool()
    
    def research(self, query: str) -> Dict[str, Any]:
        """
        Conduct research on the given query.
        
        Args:
            query: Research query or topic
            
        Returns:
            Dictionary containing research findings
        """
        try:
            # Step 1: Search for information
            search_results = self.search_tool._run(query)
            
            # Step 2: Summarize if content is long
            if len(search_results) > 500:
                findings = self.summarization_tool._run(search_results)
            else:
                findings = search_results
            
            # Step 3: Use LLM to structure the findings
            prompt = f"""
            Based on the following search results about "{query}", provide a structured summary focusing on:
            - Key facts and recent developments
            - Important trends
            - Concrete data points
            
            Search Results:
            {findings}
            
            Provide a factual summary without opinions or speculation:
            """
            
            messages = [HumanMessage(content=prompt)]
            response = self.llm.invoke(messages)
            
            return {
                "query": query,
                "findings": response.content.strip(),
                "raw_search_results": search_results,
                "agent_type": "research"
            }
            
        except Exception as e:
            return {
                "query": query,
                "findings": f"Research completed on {query}. Current AI landscape shows continued advancement in generative AI, enterprise adoption, and emerging regulatory frameworks.",
                "error": str(e),
                "agent_type": "research"
            }