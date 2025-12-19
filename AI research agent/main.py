"""
Main application for AI Research & Decision Assistant.
"""
import os
import json
import datetime
from typing import Dict, Any
from dotenv import load_dotenv
from langsmith import traceable
from core.orchestrator import AIResearchOrchestrator


def setup_environment() -> None:
    """Setup environment variables and LangSmith tracing."""
    load_dotenv()
    
    # Verify required environment variables
    required_vars = ["GROQ_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {missing_vars}")
    
    # Setup LangSmith tracing
    os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
    os.environ.setdefault("LANGCHAIN_PROJECT", "ai-research-assistant")
    
    print("✅ Environment setup complete")
    print(f"📊 LangSmith Project: {os.getenv('LANGCHAIN_PROJECT', 'ai-research-assistant')}")


def format_output(result: Dict[str, Any]) -> str:
    """
    Format the final output in the required structure.
    
    Args:
        result: Orchestrator output
        
    Returns:
        Formatted string output
    """
    output_lines = []
    
    # Summary
    output_lines.append("📋 SUMMARY")
    output_lines.append("=" * 50)
    output_lines.append(result.get("summary", "No summary available"))
    output_lines.append("")
    
    # Key Trends
    output_lines.append("📈 KEY TRENDS")
    output_lines.append("=" * 50)
    trends = result.get("key_trends", [])
    if trends:
        for i, trend in enumerate(trends, 1):
            output_lines.append(f"{i}. {trend}")
    else:
        output_lines.append("No specific trends identified")
    output_lines.append("")
    
    # Business Impact
    output_lines.append("💼 BUSINESS IMPACT")
    output_lines.append("=" * 50)
    impact = result.get("business_impact", {})
    if impact:
        for timeframe, description in impact.items():
            output_lines.append(f"• {timeframe.replace('_', ' ').title()}: {description}")
    else:
        output_lines.append("Business impact assessment pending")
    output_lines.append("")
    
    # Recommended Actions
    output_lines.append("🎯 RECOMMENDED ACTIONS")
    output_lines.append("=" * 50)
    actions = result.get("recommended_actions", [])
    if actions:
        for i, action in enumerate(actions, 1):
            output_lines.append(f"{i}. {action.get('action', 'No action specified')}")
            output_lines.append(f"   Priority: {action.get('priority', 'Medium')}")
            output_lines.append(f"   Timeline: {action.get('timeline', 'Medium term')}")
            if action.get('rationale'):
                output_lines.append(f"   Rationale: {action.get('rationale')}")
            output_lines.append("")
    else:
        output_lines.append("No specific actions recommended")
    
    return "\n".join(output_lines)


def get_user_query() -> str:
    """
    Get query from user input or example selection.
    
    Returns:
        Selected or entered query string
    """
    example_queries = [
        "Current trends in generative AI and large language models",
        "AI safety and regulatory developments in 2024", 
        "Enterprise AI adoption and business transformation",
        "Impact of multimodal AI on business operations",
        "Open-source AI models vs proprietary solutions",
        "AI governance and compliance frameworks for enterprises",
        "Future of AI in healthcare and medical research",
        "AI-powered automation in manufacturing and supply chain"
    ]
    
    print("\n🎯 AI RESEARCH & DECISION ASSISTANT")
    print("=" * 50)
    print("Choose an option:")
    print("1. Enter your own research query")
    print("2. Select from example queries")
    print("3. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                print("\n📝 Enter your AI research query:")
                query = input("Query: ").strip()
                if query:
                    return query
                else:
                    print("❌ Please enter a valid query.")
                    continue
                    
            elif choice == "2":
                print("\n📋 Example Queries:")
                print("-" * 30)
                for i, example in enumerate(example_queries, 1):
                    print(f"{i}. {example}")
                
                while True:
                    try:
                        example_choice = input(f"\nSelect example (1-{len(example_queries)}): ").strip()
                        example_idx = int(example_choice) - 1
                        
                        if 0 <= example_idx < len(example_queries):
                            return example_queries[example_idx]
                        else:
                            print(f"❌ Please enter a number between 1 and {len(example_queries)}")
                    except ValueError:
                        print("❌ Please enter a valid number")
                        
            elif choice == "3":
                print("👋 Goodbye!")
                exit(0)
                
            else:
                print("❌ Please enter 1, 2, or 3")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            exit(0)
        except Exception as e:
            print(f"❌ Error: {e}")


@traceable(name="main_application")
def main() -> None:
    """Main application entry point."""
    try:
        # Setup environment
        setup_environment()
        
        # Initialize orchestrator
        print("🤖 Initializing AI Research & Decision Assistant...")
        orchestrator = AIResearchOrchestrator()
        
        # Get query from user
        query = get_user_query()
        
        print(f"\n🔍 Processing your query...")
        print(f"📋 Query: {query}")
        print("\n⏳ This may take 15-30 seconds...")
        
        # Process the query
        result = orchestrator.process_query(query)
        
        # Format and display output
        print("\n" + "="*60)
        print("🎯 AI RESEARCH & DECISION ASSISTANT RESULTS")
        print("="*60)
        print(format_output(result))
        
        # Save results to file with timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"results_{timestamp}.json"
        
        with open(filename, "w") as f:
            json.dump(result, f, indent=2)
        
        # Also save as latest results
        with open("results.json", "w") as f:
            json.dump(result, f, indent=2)
        
        print(f"💾 Results saved to {filename} and results.json")
        print("📊 Check LangSmith for detailed traces and performance metrics")
        
        # Ask if user wants to run another query
        print("\n" + "="*60)
        while True:
            try:
                another = input("🔄 Would you like to analyze another query? (y/n): ").strip().lower()
                if another in ['y', 'yes']:
                    print("\n" + "="*60)
                    main()  # Recursive call for another query
                    break
                elif another in ['n', 'no']:
                    print("👋 Thank you for using AI Research & Decision Assistant!")
                    break
                else:
                    print("❌ Please enter 'y' for yes or 'n' for no")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
        
    except Exception as e:
        print(f"❌ Application error: {str(e)}")
        print("🔧 Please check your API keys and try again")
        raise


if __name__ == "__main__":
    main()