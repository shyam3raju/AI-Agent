"""
Decision Agent for producing actionable recommendations.
"""
import json
from typing import Dict, Any
from langchain_core.messages import HumanMessage
from core.llm_factory import LLMFactory
from tools.decision_tool import DecisionTool


class DecisionAgent:
    """Agent responsible for generating business-ready recommendations."""
    
    def __init__(self):
        """Initialize the Decision Agent with decision tool."""
        self.llm = LLMFactory.create_reasoning_llm()
        self.decision_tool = DecisionTool()
    
    def decide(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate actionable recommendations based on analysis.
        
        Args:
            analysis_results: Output from Analysis Agent
            
        Returns:
            Dictionary containing recommendations and decisions
        """
        try:
            analysis_data = json.dumps(analysis_results.get("analysis", {}), indent=2)
            
            # Use the decision tool to generate structured recommendations
            decision_output = self.decision_tool._run(analysis_data)
            
            # Parse the decision output
            try:
                decisions = json.loads(decision_output)
            except json.JSONDecodeError:
                # If JSON parsing fails, use LLM to structure the output
                prompt = f"""
                Based on this analysis, provide strategic recommendations in JSON format:
                
                Analysis: {analysis_data}
                Decision Tool Output: {decision_output}
                
                Format as:
                {{
                    "recommendations": [
                        {{
                            "action": "Specific action",
                            "rationale": "Why this makes sense",
                            "priority": "High/Medium/Low",
                            "timeline": "Short/Medium/Long term"
                        }}
                    ],
                    "key_considerations": ["consideration1", "consideration2"],
                    "risk_mitigation": ["mitigation1", "mitigation2"]
                }}
                """
                
                messages = [HumanMessage(content=prompt)]
                response = self.llm.invoke(messages)
                
                try:
                    decisions = json.loads(response.content.strip())
                except json.JSONDecodeError:
                    decisions = self._create_fallback_decisions()
            
            return {
                "original_query": analysis_results.get("original_query", ""),
                "decisions": decisions,
                "agent_type": "decision"
            }
            
        except Exception as e:
            return {
                "original_query": analysis_results.get("original_query", ""),
                "decisions": self._create_fallback_decisions(),
                "error": str(e),
                "agent_type": "decision"
            }
    
    def _create_fallback_decisions(self) -> Dict[str, Any]:
        """Create fallback decision structure."""
        return {
            "recommendations": [
                {
                    "action": "Establish AI monitoring and evaluation framework",
                    "rationale": "Stay informed about AI developments to make timely strategic decisions",
                    "priority": "High",
                    "timeline": "Short term"
                },
                {
                    "action": "Assess current business processes for AI integration opportunities",
                    "rationale": "Identify areas where AI can provide competitive advantage",
                    "priority": "Medium",
                    "timeline": "Medium term"
                }
            ],
            "key_considerations": [
                "Budget allocation for AI initiatives",
                "Staff training and change management"
            ],
            "risk_mitigation": [
                "Gradual implementation approach",
                "Regular technology assessment reviews"
            ]
        }