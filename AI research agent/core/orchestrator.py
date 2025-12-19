"""
Orchestrator for coordinating the three agents.
"""
import json
from typing import Dict, Any
from langsmith import traceable
from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.decision_agent import DecisionAgent


class AIResearchOrchestrator:
    """Orchestrates the three-agent workflow for AI research and decision making."""
    
    def __init__(self):
        """Initialize the orchestrator with all three agents."""
        self.research_agent = ResearchAgent()
        self.analysis_agent = AnalysisAgent()
        self.decision_agent = DecisionAgent()
    
    @traceable(name="ai_research_orchestrator")
    def process_query(self, user_query: str) -> Dict[str, Any]:
        """
        Process a user query through the complete agent workflow.
        
        Args:
            user_query: The user's research question or topic
            
        Returns:
            Structured final response with all agent outputs
        """
        try:
            # Step 1: Research Agent gathers information
            research_results = self._execute_research(user_query)
            
            # Step 2: Analysis Agent processes research findings
            analysis_results = self._execute_analysis(research_results)
            
            # Step 3: Decision Agent generates recommendations
            decision_results = self._execute_decisions(analysis_results)
            
            # Step 4: Format final structured output
            final_output = self._format_final_output(
                user_query, research_results, analysis_results, decision_results
            )
            
            return final_output
            
        except Exception as e:
            return {
                "error": f"Orchestration failed: {str(e)}",
                "query": user_query,
                "status": "failed"
            }
    
    @traceable(name="research_phase")
    def _execute_research(self, query: str) -> Dict[str, Any]:
        """Execute the research phase."""
        return self.research_agent.research(query)
    
    @traceable(name="analysis_phase")
    def _execute_analysis(self, research_results: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the analysis phase."""
        return self.analysis_agent.analyze(research_results)
    
    @traceable(name="decision_phase")
    def _execute_decisions(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the decision phase."""
        return self.decision_agent.decide(analysis_results)
    
    def _format_final_output(
        self, 
        query: str, 
        research: Dict[str, Any], 
        analysis: Dict[str, Any], 
        decisions: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Format the final structured output as specified.
        
        Returns output in the exact format:
        - Summary
        - Key Trends  
        - Business Impact
        - Recommended Actions
        """
        try:
            analysis_data = analysis.get("analysis", {})
            decision_data = decisions.get("decisions", {})
            
            # Extract data for final format
            summary = research.get("findings", "Research completed on AI topics.")
            key_trends = analysis_data.get("key_trends", [])
            business_impact = analysis_data.get("business_impact", {})
            recommendations = decision_data.get("recommendations", [])
            
            return {
                "query": query,
                "summary": summary,
                "key_trends": key_trends,
                "business_impact": business_impact,
                "recommended_actions": [
                    {
                        "action": rec.get("action", ""),
                        "priority": rec.get("priority", "Medium"),
                        "timeline": rec.get("timeline", "Medium term"),
                        "rationale": rec.get("rationale", "")
                    }
                    for rec in recommendations
                ],
                "status": "completed",
                "agent_execution_summary": {
                    "research_agent": "completed" if research.get("findings") else "partial",
                    "analysis_agent": "completed" if analysis_data else "partial", 
                    "decision_agent": "completed" if decision_data else "partial"
                }
            }
            
        except Exception as e:
            return {
                "query": query,
                "summary": "Analysis completed with partial results.",
                "key_trends": ["AI technology advancement continues"],
                "business_impact": {"short_term": "Monitoring recommended"},
                "recommended_actions": [{"action": "Continue monitoring AI developments", "priority": "Medium"}],
                "status": "completed_with_errors",
                "error": str(e)
            }