"""
Test script to demonstrate the Agentic AI IT Support System
"""
import asyncio
import sys
from rag_system import RAGSystem


def test_rag_system():
    """Test RAG system with sample queries"""
    print("\n" + "="*70)
    print("TESTING RAG SYSTEM")
    print("="*70 + "\n")
    
    rag = RAGSystem()
    
    test_queries = [
        "I forgot my password and can't login to my account",
        "My WiFi is not working and I can't connect to the internet",
        "I need to install Microsoft Office on my computer",
        "The printer is not responding when I try to print documents",
        "I can't access the shared drive folder",
        "My laptop screen is cracked and not working",
        "I'm getting a virus warning on my computer",
        "Can't connect to VPN from home"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: {query}")
        print("-" * 70)
        
        result = rag.get_best_match(query)
        
        if result:
            print(f"   Category: {result['category']}")
            print(f"   Priority: {result['priority']}")
            print(f"   Auto-resolvable: {result['auto_resolvable']}")
            print(f"   Relevance Score: {result['relevance_score']:.3f}")
            print(f"   Confidence: {'HIGH' if result['relevance_score'] > 0.7 else 'MEDIUM' if result['relevance_score'] > 0.5 else 'LOW'}")
        else:
            print("   No match found")


def test_agents():
    """Test individual agents"""
    print("\n" + "="*70)
    print("TESTING AI AGENTS")
    print("="*70 + "\n")
    
    from agents import UIAgent, ClassificationAgent, DecisionAgent, ResolutionAgent, EscalationAgent
    from rag_system import RAGSystem
    
    rag = RAGSystem()
    
    # Test UI Agent
    print("\n1. UI AGENT TEST")
    print("-" * 70)
    ui_agent = UIAgent()
    ui_result = ui_agent.capture_request(
        issue_description="I forgot my password",
        user_id=1
    )
    print(f"   Success: {ui_result['success']}")
    print(f"   Issue: {ui_result['issue_description']}")
    
    # Test Classification Agent
    print("\n2. CLASSIFICATION AGENT TEST (RAG-powered)")
    print("-" * 70)
    classification_agent = ClassificationAgent(rag)
    classification = classification_agent.classify("I forgot my password and can't login")
    print(f"   Success: {classification['success']}")
    print(f"   Category: {classification.get('category')}")
    print(f"   Priority: {classification.get('priority')}")
    print(f"   Confidence: {classification.get('confidence_score', 0):.3f}")
    print(f"   Auto-resolvable: {classification.get('auto_resolvable')}")
    
    # Test Decision Agent
    print("\n3. DECISION AGENT TEST")
    print("-" * 70)
    decision_agent = DecisionAgent()
    decision = decision_agent.decide(classification)
    print(f"   Action: {decision['action']}")
    print(f"   Reasoning: {decision['reasoning']}")
    print(f"   Requires Human: {decision['requires_human']}")
    
    # Test Resolution Agent
    if decision['action'] == 'auto_resolve':
        print("\n4. RESOLUTION AGENT TEST")
        print("-" * 70)
        resolution_agent = ResolutionAgent()
        resolution = resolution_agent.resolve(classification, "I forgot my password")
        print(f"   Status: {resolution['status']}")
        print(f"   Success: {resolution['success']}")
        print(f"   Has Solution: {'solution' in resolution and resolution['solution'] is not None}")
    
    # Test Escalation Agent
    else:
        print("\n4. ESCALATION AGENT TEST")
        print("-" * 70)
        escalation_agent = EscalationAgent()
        escalation = escalation_agent.escalate("Complex issue", classification, "IT-TEST-001")
        print(f"   Status: {escalation['status']}")
        print(f"   Assigned to: {escalation['assigned_to']}")
        print(f"   Priority: {escalation['priority']}")


def print_system_info():
    """Print system information"""
    print("\n" + "="*70)
    print("SYSTEM INFORMATION")
    print("="*70 + "\n")
    
    print("✓ Application: Agentic AI IT Support System")
    print("✓ Architecture: Multi-Agent with RAG")
    print("✓ Backend: FastAPI (Async)")
    print("✓ Database: SQLite with SQLAlchemy")
    print("✓ RAG: Sentence Transformers + ChromaDB")
    print("✓ Authentication: JWT-based")
    
    print("\n" + "="*70)
    print("AGENTS")
    print("="*70 + "\n")
    
    agents = [
        ("UI Agent", "Captures and validates user input"),
        ("Classification Agent", "RAG-powered issue classification"),
        ("Decision Agent", "Determines resolution path"),
        ("Resolution Agent", "Provides automatic solutions"),
        ("Escalation Agent", "Escalates to human IT staff"),
        ("Logging Agent", "Maintains audit trail")
    ]
    
    for name, description in agents:
        print(f"✓ {name:25} - {description}")
    
    print("\n" + "="*70)
    print("FEATURES")
    print("="*70 + "\n")
    
    features = [
        "Multi-agent architecture",
        "RAG-based semantic search",
        "Auto-resolution of common issues",
        "Smart escalation to humans",
        "Complete audit trail",
        "Real-time analytics dashboard",
        "Role-based access control",
        "RESTful API with Swagger docs"
    ]
    
    for feature in features:
        print(f"✓ {feature}")


def main():
    """Main test function"""
    print("\n" + "="*70)
    print("AGENTIC AI IT SUPPORT SYSTEM - TEST SUITE")
    print("="*70)
    
    try:
        # Print system info
        print_system_info()
        
        # Test RAG system
        test_rag_system()
        
        # Test agents
        test_agents()
        
        print("\n" + "="*70)
        print("ALL TESTS COMPLETED")
        print("="*70 + "\n")
        
        print("To start the application, run:")
        print("  python main.py")
        print("\nOr use the convenience script:")
        print("  run.bat    (Windows)")
        print("  ./run.sh   (Linux/Mac)")
        print("\nThen access:")
        print("  http://localhost:8000        - Main interface")
        print("  http://localhost:8000/docs   - API documentation")
        print("  http://localhost:8000/dashboard - Admin dashboard")
        print("\nDefault login: admin / admin123")
        print("\n" + "="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
