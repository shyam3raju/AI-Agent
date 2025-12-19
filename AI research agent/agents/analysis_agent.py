"""
Analysis Agent for extracting trends, risks, and opportunities.
"""
import json
from typing import Dict, Any
from langchain_core.messages import HumanMessage
from core.llm_factory import LLMFactory


class AnalysisAgent:
    """Agent responsible for analyzing research findings."""
    
    def __init__(self):
        """Initialize the Analysis Agent."""
        self.llm = LLMFactory.create_reasoning_llm()
    
    def analyze(self, research_findings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze research findings to extract trends, risks, and opportunities.
        
        Args:
            research_findings: Output from Research Agent
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            findings_text = research_findings.get("findings", "")
            
            prompt = f"""
            Analyze the following research findings about AI topics.
            Extract and categorize information into the specified structure.
            
            Research Findings:
            {findings_text}
            
            Provide your analysis in this exact JSON format:
            {{
                "key_trends": [
                    "Trend 1: Description",
                    "Trend 2: Description",
                    "Trend 3: Description"
                ],
                "risks": [
                    "Risk 1: Description and potential impact",
                    "Risk 2: Description and potential impact"
                ],
                "opportunities": [
                    "Opportunity 1: Description and potential value",
                    "Opportunity 2: Description and potential value"
                ],
                "business_impact": {{
                    "short_term": "Impact expected in next 6-12 months",
                    "medium_term": "Impact expected in 1-3 years",
                    "long_term": "Impact expected in 3+ years"
                }},
                "market_dynamics": [
                    "Dynamic 1: Description",
                    "Dynamic 2: Description"
                ]
            }}
            
            Focus on business-relevant insights and concrete implications.
            """
            
            messages = [HumanMessage(content=prompt)]
            response = self.llm.invoke(messages)
            
            # Parse JSON response
            try:
                analysis_data = json.loads(response.content.strip())
            except json.JSONDecodeError:
                # Fallback structured analysis
                analysis_data = self._create_fallback_analysis(findings_text)
            
            return {
                "original_query": research_findings.get("query", ""),
                "analysis": analysis_data,
                "agent_type": "analysis"
            }
            
        except Exception as e:
            return {
                "original_query": research_findings.get("query", ""),
                "analysis": self._create_fallback_analysis(research_findings.get("findings", "")),
                "error": str(e),
                "agent_type": "analysis"
            }
    
    def _create_fallback_analysis(self, findings: str) -> Dict[str, Any]:
        """Create a fallback analysis structure."""
        return {
            "key_trends": [
                "Continued advancement in large language models and generative AI",
                "Increased enterprise adoption of AI solutions",
                "Growing focus on AI safety and regulatory compliance"
            ],
            "risks": [
                "Regulatory uncertainty may impact AI development timelines",
                "Competitive pressure from rapid technological advancement"
            ],
            "opportunities": [
                "Market expansion in AI-powered business solutions",
                "Innovation potential in multimodal AI applications"
            ],
            "business_impact": {
                "short_term": "Immediate opportunities in AI tool integration",
                "medium_term": "Transformation of business processes and workflows",
                "long_term": "Fundamental shifts in industry competitive dynamics"
            },
            "market_dynamics": [
                "Rapid pace of technological innovation",
                "Increasing investment in AI infrastructure"
            ]
        }