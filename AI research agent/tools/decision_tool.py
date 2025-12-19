"""
Decision tool for generating strategic recommendations.
"""
import json
from typing import Dict, Any
from langchain.tools import BaseTool
from langchain_core.messages import HumanMessage
from core.llm_factory import LLMFactory


class DecisionTool(BaseTool):
    """Tool for generating strategic business recommendations."""
    
    name: str = "decision_tool"
    description: str = (
        "Generate strategic business recommendations based on analysis data. "
        "Input should be analysis results as a dictionary or JSON string. "
        "Returns structured recommendations with rationale and priority."
    )
    
    def _run(self, analysis: str) -> str:
        """
        Generate strategic recommendations from analysis.
        
        Args:
            analysis: Analysis results as string or JSON
            
        Returns:
            Structured recommendations as JSON string
        """
        try:
            llm = LLMFactory.create_reasoning_llm()
            
            prompt = f"""
            Based on the following AI market analysis, generate strategic business recommendations.
            
            Analysis Data:
            {analysis}
            
            Provide recommendations in this exact JSON format:
            {{
                "recommendations": [
                    {{
                        "action": "Specific actionable recommendation",
                        "rationale": "Why this recommendation makes sense",
                        "priority": "High/Medium/Low",
                        "timeline": "Short/Medium/Long term"
                    }}
                ],
                "key_considerations": ["consideration1", "consideration2"],
                "risk_mitigation": ["risk1_mitigation", "risk2_mitigation"]
            }}
            
            Focus on practical, business-ready actions.
            """
            
            messages = [HumanMessage(content=prompt)]
            response = llm.invoke(messages)
            
            return response.content.strip()
            
        except Exception as e:
            # Fallback structured response
            fallback = {
                "recommendations": [
                    {
                        "action": "Monitor AI technology developments closely",
                        "rationale": "Rapid pace of AI advancement requires continuous awareness",
                        "priority": "High",
                        "timeline": "Short term"
                    }
                ],
                "key_considerations": ["Technology adoption costs", "Competitive landscape"],
                "risk_mitigation": ["Gradual implementation", "Staff training programs"]
            }
            return json.dumps(fallback, indent=2)
    
    async def _arun(self, analysis: str) -> str:
        """Async version of the decision tool."""
        return self._run(analysis)