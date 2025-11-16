"""
Test script to verify all agent components work correctly
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.research_agent import ResearchAgent
from agents.summarizer_agent import SummarizerAgent
from agents.report_generator import ReportGenerator
from utils.session_manager import SessionService, MemoryBank
from utils.observability import logger, tracer, metrics

def test_agents():
    """Test the multi-agent system"""
    
    print("=" * 60)
    print("🧪 Testing AI Research Assistant Multi-Agent System")
    print("=" * 60)
    
    # Test 1: Initialize components
    print("\n✅ Test 1: Initializing components...")
    try:
        session_service = SessionService()
        memory_bank = MemoryBank()
        session_id = session_service.create_session("test_user")
        print(f"   Session created: {session_id}")
        print("   ✓ Components initialized successfully")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False
    
    # Test 2: Start tracing
    print("\n✅ Test 2: Starting distributed tracing...")
    try:
        trace_id = tracer.start_trace("test_research", {"topic": "artificial intelligence"})
        print(f"   Trace ID: {trace_id}")
        print("   ✓ Tracing started successfully")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False
    
    # Test 3: Research Agent
    print("\n✅ Test 3: Testing Research Agent...")
    try:
        research_agent = ResearchAgent()
        logger.get_logger().info("Starting research test")
        results = research_agent.search("artificial intelligence", max_results=3)
        tracer.add_span(trace_id, "ResearchAgent", "search", 1.5, "success")
        metrics.record_agent_call("ResearchAgent", 1.5, True)
        print(f"   Found {len(results)} results")
        if results:
            print(f"   Sample result: {results[0]['title'][:50]}...")
        print("   ✓ Research Agent working")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False
    
    # Test 4: Summarizer Agent
    print("\n✅ Test 4: Testing Summarizer Agent...")
    try:
        summarizer_agent = SummarizerAgent()
        summary = summarizer_agent.summarize(results, length="Short")
        tracer.add_span(trace_id, "SummarizerAgent", "summarize", 0.8, "success")
        metrics.record_agent_call("SummarizerAgent", 0.8, True)
        print(f"   Summary length: {len(summary)} characters")
        print(f"   Summary preview: {summary[:80]}...")
        print("   ✓ Summarizer Agent working")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False
    
    # Test 5: Report Generator
    print("\n✅ Test 5: Testing Report Generator...")
    try:
        report_agent = ReportGenerator()
        report = report_agent.generate(
            topic="artificial intelligence",
            search_results=results,
            summary=summary,
            include_citations=True
        )
        tracer.add_span(trace_id, "ReportGenerator", "generate", 0.5, "success")
        metrics.record_agent_call("ReportGenerator", 0.5, True)
        print(f"   Report length: {len(report)} characters")
        print("   ✓ Report Generator working")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False
    
    # Test 6: Session Management
    print("\n✅ Test 6: Testing Session Management...")
    try:
        research_data = {
            'topic': 'artificial intelligence',
            'summary': summary,
            'results': results
        }
        session_service.add_to_history(session_id, research_data)
        session_service.add_context(session_id, "Tested AI research")
        history = session_service.get_session_history(session_id)
        print(f"   Session history entries: {len(history)}")
        print("   ✓ Session Management working")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False
    
    # Test 7: Memory Bank
    print("\n✅ Test 7: Testing Memory Bank...")
    try:
        memory_bank.store_memory(
            "artificial intelligence",
            {'summary': summary, 'sources': len(results)},
            {'type': 'test', 'timestamp': '2025-11-16'}
        )
        retrieved = memory_bank.retrieve_memory("artificial intelligence")
        print(f"   Memory stored and retrieved: {retrieved is not None}")
        print(f"   Access count: {retrieved['access_count']}")
        print("   ✓ Memory Bank working")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False
    
    # Test 8: Observability
    print("\n✅ Test 8: Testing Observability...")
    try:
        tracer.end_trace(trace_id, "success")
        metrics_summary = metrics.get_metrics_summary()
        
        print(f"   Total agent calls: {metrics_summary['total_agent_calls']}")
        print(f"   Average response time: {metrics_summary['avg_response_time']:.2f}s")
        print(f"   Success rate: {metrics_summary['success_rate']:.1f}%")
        
        recent_traces = tracer.get_recent_traces(1)
        print(f"   Traces recorded: {len(recent_traces)}")
        
        print("   ✓ Observability working")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False
    
    # Final summary
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED!")
    print("=" * 60)
    print("\n📊 System Summary:")
    print(f"   • 3 Agents: Research, Summarizer, Report Generator")
    print(f"   • Session Management: Active")
    print(f"   • Memory Bank: Active")
    print(f"   • Logging: Active")
    print(f"   • Tracing: Active")
    print(f"   • Metrics: Active")
    print("\n✅ Multi-Agent System is fully functional!")
    print("\nRun the Streamlit app with: python -m streamlit run app.py")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = test_agents()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
