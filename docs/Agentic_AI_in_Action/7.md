## 7. Debugging and Tracing with LangSmith
Building complex agentic systems with LangChain and LangGraph involves many moving parts. LangSmith is a platform designed to help you debug, trace, monitor, and evaluate your language model applications, making it an invaluable tool for developing robust agents.

### 7.1. Why LangSmith?
- **Visibility:** Get a clear view of what your agent is doing at each step. See the inputs and outputs of LLM calls, tool executions, and graph node transitions.
- **Debugging:** Quickly identify errors, unexpected behavior, or inefficient paths in your agent's logic.
- **Collaboration:** Share traces with team members to troubleshoot issues.
- **Evaluation:** Log results, gather feedback, and run evaluations to measure and improve agent performance.
- **Monitoring:** Keep an eye on your agents in production (though this tutorial focuses on development).

### 7.2. Setting up LangSmith
To get started with LangSmith, you typically need to: 
1. Sign up at smith.langchain.com.
2. Create an API key.
3. Set a few environment variables in your development environment:

```python
import os
import getpass # To securely get API key if not set as env var

# Best practice: Set these in your shell environment (e.g., .env file or export commands)
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = "YOUR_LANGSMITH_API_KEY"
# os.environ["LANGCHAIN_PROJECT"] = "My Agentic AI Project" # Optional: organize runs into projects

# Example of setting them programmatically if not already set (useful for notebooks)
def setup_langsmith_env():
    if "LANGCHAIN_TRACING_V2" not in os.environ:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        print("Set LANGCHAIN_TRACING_V2 to true")

    if "LANGCHAIN_API_KEY" not in os.environ:
        api_key = getpass.getpass("Enter your LangSmith API key: ")
        os.environ["LANGCHAIN_API_KEY"] = api_key
        print("LangSmith API key set from input.")
    else:
        print("LangSmith API key found in environment.")

    if "LANGCHAIN_PROJECT" not in os.environ:
        os.environ["LANGCHAIN_PROJECT"] = "Default Agentic Tutorial Project"
        print(f"Using LangSmith project: {os.environ['LANGCHAIN_PROJECT']}")

# Call this at the beginning of your script or notebook
# setup_langsmith_env()
```
Once these environment variables are set, LangChain and LangGraph will automatically start sending trace data to your LangSmith project.

### 7.3. Tracing LangChain Components and LangGraph Runs
When you execute your LangGraph application (e.g., `research_app.invoke(...)` or `research_app.stream(...)` from our example), LangSmith captures:

- **Overall Graph Execution:** The entry into the graph and its final output.
- **Node Executions:** Each time a node in your `StateGraph` is run, LangSmith records its inputs (the part of the state it received) and its outputs (the state updates it returned).
- **LangChain Component Calls:** If a node internally uses LangChain components (like an `AgentExecutor`, an LLM call, a specific chain, or a tool), these are also traced as nested operations.
  - You'll see the exact prompts sent to LLMs.
  - The arguments passed to tools and the data they returned.
  - The flow within `create_openai_tools_agent` or other agent runnables.
- **Visualizing Graphs:** LangSmith provides a visual representation of your LangGraph executions, making it much easier to understand the flow of control, especially with conditional edges and loops. You can see which path was taken through the graph for a given input.

### 7.4. Example: Inspecting the Research Assistant in LangSmith
If you run the Research Assistant agent (from Section 4) with LangSmith configured:

1. Go to your LangSmith project.
2. You will see a new trace for each invocation of `research_app.invoke()` or `research_app.stream()`.
3. Clicking on a trace will show you:
   - The initial input to the graph.
   - A timeline of nodes executed (planner, tool_executor).
   - For the `planner` node, you can expand it to see the internal call to your `planner_agent_runnable` (the `create_openai_tools_agent`). Further expanding this will show the LLM call, the prompt, and the model's response (including any tool calls it decided to make).
   - For the `tool_executor` node, you'll see which tool was called (e.g., `web_search` or `summarize_text_tool`) and the arguments and output of that tool.
   - If you used a checkpointer, the state at each step might also be visible or inferable from the inputs/outputs of the nodes.

This detailed, hierarchical view is crucial for understanding why your agent made certain decisions, how tools performed, and where potential improvements can be made.

### 7.5. Logging Feedback and Annotations
LangSmith also allows you to programmatically or manually add feedback to runs.

```python
from langsmith import Client

# client = Client() # Initialize if you need to interact with LangSmith API directly

# Example: After a run, you might log feedback (this usually requires the run_id)
# This is more for evaluation workflows, but shows the capability.

# run_id = "some_run_id_from_a_trace" # You'd get this from a trace or programmatically
# if client and run_id:
#     try:
#         client.create_feedback(
#             run_id=run_id,
#             key="user_satisfaction", # Arbitrary key for the feedback type
#             score=0.8, # Numerical score (e.g., 0.0 to 1.0)
#             comment="The summary was good but a bit too verbose."
#         )
#         print(f"Feedback added for run {run_id}")
#     except Exception as e:
#         print(f"Could not log feedback: {e}")
```
This feedback can be used to evaluate agent performance over time and identify areas for improvement.
By integrating LangSmith into your development workflow from the start, you gain powerful observability that significantly speeds up the development and refinement of complex agentic AI systems.

## Comprehensive Testing and Monitoring for Agentic Systems

While LangSmith provides excellent observability for development and debugging, production agentic systems require a comprehensive testing strategy and monitoring framework that goes beyond trace visualization. This section covers systematic approaches to testing, monitoring, and maintaining agentic AI systems in production environments.

### Testing Strategies for Agentic Systems

**Unit Testing for Agent Components**:
Testing individual components in isolation ensures reliability at the foundation level.

```python
import pytest
from unittest.mock import Mock, patch
from langchain_core.messages import HumanMessage, AIMessage
from your_agent.tools import SearchTool, SummarizeTool
from your_agent.state import ResearchAgentState

class TestAgentComponents:
    
    def test_search_tool_basic_functionality(self):
        """Test search tool with valid input."""
        search_tool = SearchTool()
        
        # Mock the external API call
        with patch('your_agent.tools.tavily_api') as mock_tavily:
            mock_tavily.search.return_value = [
                {"content": "Test result 1", "url": "http://example.com/1"},
                {"content": "Test result 2", "url": "http://example.com/2"}
            ]
            
            result = search_tool.invoke("test query")
            
            assert len(result) == 2
            assert "Test result 1" in str(result)
            mock_tavily.search.assert_called_once_with("test query")
    
    def test_search_tool_error_handling(self):
        """Test search tool handles API failures gracefully."""
        search_tool = SearchTool()
        
        with patch('your_agent.tools.tavily_api') as mock_tavily:
            mock_tavily.search.side_effect = Exception("API Error")
            
            result = search_tool.invoke("test query")
            
            # Should return error message, not raise exception
            assert "error" in str(result).lower()
    
    def test_state_update_logic(self):
        """Test state transitions work correctly."""
        initial_state = ResearchAgentState(
            input_question="test question",
            messages=[HumanMessage(content="test")],
            search_results=None,
            summary=None,
            next_node=None
        )
        
        # Test state update after search
        updated_state = update_state_after_search(
            initial_state, 
            ["result1", "result2"]
        )
        
        assert updated_state["search_results"] == ["result1", "result2"]
        assert updated_state["next_node"] == "summarizer"

class TestAgentBehaviors:
    """Test higher-level agent behaviors and decision patterns."""
    
    def test_tool_selection_logic(self):
        """Test agent selects appropriate tools based on context."""
        agent = ResearchAgent()
        
        # Test search selection
        search_decision = agent.decide_next_action(
            query="What is the capital of France?",
            context={"has_search_results": False}
        )
        assert search_decision["tool"] == "search"
        
        # Test summarization selection
        summary_decision = agent.decide_next_action(
            query="What is the capital of France?",
            context={"has_search_results": True, "search_complete": True}
        )
        assert summary_decision["tool"] == "summarize"
    
    def test_error_recovery_behavior(self):
        """Test agent recovers gracefully from tool failures."""
        agent = ResearchAgent()
        
        with patch.object(agent.search_tool, 'invoke') as mock_search:
            mock_search.side_effect = Exception("Search failed")
            
            result = agent.handle_search_step("test query")
            
            # Should fallback or provide helpful error message
            assert result["status"] == "error"
            assert "fallback" in result or "alternative" in result
```

**Integration Testing for Multi-Component Interactions**:
Test how different agent components work together.

```python
class TestAgentIntegration:
    
    @pytest.fixture
    def agent_system(self):
        """Setup a test agent system with mocked external dependencies."""
        return TestAgentSystem(
            llm=MockLLM(),
            search_tool=MockSearchTool(),
            config=TestConfig()
        )
    
    def test_complete_research_workflow(self, agent_system):
        """Test end-to-end research workflow."""
        initial_state = {
            "input_question": "Recent developments in AI",
            "messages": [HumanMessage(content="Recent developments in AI")]
        }
        
        # Run the complete workflow
        final_state = agent_system.run_workflow(initial_state)
        
        # Verify workflow completion
        assert final_state["summary"] is not None
        assert len(final_state["messages"]) > 1
        assert final_state["next_node"] == "__end__"
        
        # Verify intermediate steps occurred
        message_types = [type(msg).__name__ for msg in final_state["messages"]]
        assert "AIMessage" in message_types  # Agent decision
        assert "ToolMessage" in message_types  # Tool execution
    
    def test_state_persistence_across_nodes(self, agent_system):
        """Test state is properly maintained across graph nodes."""
        state = agent_system.execute_planner_node({
            "input_question": "test",
            "messages": []
        })
        
        # Verify state structure
        assert "messages" in state
        assert "next_node" in state
        
        # Execute next node with updated state
        next_state = agent_system.execute_tool_node(state)
        
        # Verify state continuity
        assert len(next_state["messages"]) > len(state["messages"])
```

**End-to-End Testing with Realistic Scenarios**:
Test complete user journeys and edge cases.

```python
class TestEndToEndScenarios:
    
    @pytest.mark.integration
    def test_complex_research_scenario(self):
        """Test agent handling complex, multi-step research."""
        scenarios = [
            {
                "query": "Compare renewable energy trends in 2024",
                "expected_tools": ["search", "summarize"],
                "expected_duration": 30,  # seconds
                "quality_threshold": 0.8
            },
            {
                "query": "What are the privacy implications of AI?",
                "expected_tools": ["search", "summarize"],
                "expected_keywords": ["privacy", "AI", "implications"]
            }
        ]
        
        for scenario in scenarios:
            with self.subTest(scenario=scenario["query"]):
                start_time = time.time()
                
                result = self.agent.research(scenario["query"])
                
                duration = time.time() - start_time
                
                # Performance assertions
                assert duration < scenario["expected_duration"]
                
                # Quality assertions
                if "quality_threshold" in scenario:
                    quality_score = self.evaluate_response_quality(
                        result["summary"], scenario["query"]
                    )
                    assert quality_score >= scenario["quality_threshold"]
                
                # Content assertions
                if "expected_keywords" in scenario:
                    summary_lower = result["summary"].lower()
                    for keyword in scenario["expected_keywords"]:
                        assert keyword.lower() in summary_lower
```

### Performance Testing and Benchmarking

**Load Testing for Agent Systems**:
```python
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

class AgentPerformanceTester:
    
    def __init__(self, agent_system):
        self.agent_system = agent_system
        self.results = []
    
    async def test_concurrent_requests(self, num_requests=50, max_concurrent=10):
        """Test agent performance under concurrent load."""
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def single_request(request_id):
            async with semaphore:
                start_time = time.time()
                try:
                    result = await self.agent_system.aresearch(
                        f"Test query {request_id}"
                    )
                    success = True
                    error = None
                except Exception as e:
                    result = None
                    success = False
                    error = str(e)
                
                end_time = time.time()
                
                return {
                    "request_id": request_id,
                    "duration": end_time - start_time,
                    "success": success,
                    "error": error,
                    "timestamp": start_time
                }
        
        # Execute concurrent requests
        tasks = [single_request(i) for i in range(num_requests)]
        self.results = await asyncio.gather(*tasks)
        
        return self.analyze_performance_results()
    
    def analyze_performance_results(self):
        """Analyze performance test results."""
        successful_requests = [r for r in self.results if r["success"]]
        failed_requests = [r for r in self.results if not r["success"]]
        
        if successful_requests:
            durations = [r["duration"] for r in successful_requests]
            
            performance_metrics = {
                "total_requests": len(self.results),
                "successful_requests": len(successful_requests),
                "failed_requests": len(failed_requests),
                "success_rate": len(successful_requests) / len(self.results),
                "average_duration": sum(durations) / len(durations),
                "min_duration": min(durations),
                "max_duration": max(durations),
                "p95_duration": sorted(durations)[int(0.95 * len(durations))],
                "requests_per_second": len(successful_requests) / max(durations)
            }
        else:
            performance_metrics = {
                "total_requests": len(self.results),
                "successful_requests": 0,
                "failed_requests": len(failed_requests),
                "success_rate": 0.0,
                "error_summary": {}
            }
            
            # Analyze error patterns
            for result in failed_requests:
                error_type = type(result["error"]).__name__
                performance_metrics["error_summary"][error_type] = (
                    performance_metrics["error_summary"].get(error_type, 0) + 1
                )
        
        return performance_metrics
```

### Production Monitoring Framework

**Real-Time Performance Monitoring**:
```python
import prometheus_client
from prometheus_client import Counter, Histogram, Gauge
import logging
import structlog

class AgentMetricsCollector:
    
    def __init__(self):
        # Performance metrics
        self.request_duration = Histogram(
            'agent_request_duration_seconds',
            'Time spent processing agent requests',
            ['agent_type', 'endpoint']
        )
        
        self.request_total = Counter(
            'agent_requests_total',
            'Total number of agent requests',
            ['agent_type', 'status']
        )
        
        self.tool_usage = Counter(
            'agent_tool_usage_total',
            'Number of tool invocations',
            ['tool_name', 'status']
        )
        
        self.active_sessions = Gauge(
            'agent_active_sessions',
            'Number of active agent sessions',
            ['agent_type']
        )
        
        # Quality metrics
        self.response_quality = Histogram(
            'agent_response_quality_score',
            'Response quality scores',
            ['agent_type']
        )
        
        # Cost metrics
        self.token_usage = Counter(
            'agent_token_usage_total',
            'Total tokens consumed',
            ['model', 'type']  # type: input/output
        )
        
        self.api_costs = Counter(
            'agent_api_costs_total',
            'Total API costs in USD',
            ['provider', 'model']
        )
    
    def record_request(self, agent_type, duration, status, endpoint="default"):
        """Record metrics for a completed request."""
        self.request_duration.labels(
            agent_type=agent_type, 
            endpoint=endpoint
        ).observe(duration)
        
        self.request_total.labels(
            agent_type=agent_type, 
            status=status
        ).inc()
    
    def record_tool_usage(self, tool_name, status="success"):
        """Record tool usage metrics."""
        self.tool_usage.labels(
            tool_name=tool_name, 
            status=status
        ).inc()
    
    def record_quality_score(self, agent_type, score):
        """Record response quality metrics."""
        self.response_quality.labels(agent_type=agent_type).observe(score)
    
    def record_token_usage(self, model, input_tokens, output_tokens):
        """Record token consumption."""
        self.token_usage.labels(model=model, type="input").inc(input_tokens)
        self.token_usage.labels(model=model, type="output").inc(output_tokens)
    
    def update_active_sessions(self, agent_type, count):
        """Update active session count."""
        self.active_sessions.labels(agent_type=agent_type).set(count)

class AgentLogger:
    
    def __init__(self):
        self.logger = structlog.get_logger("agent_system")
    
    def log_agent_decision(self, agent_id, decision_context, decision_result):
        """Log agent decision-making process."""
        self.logger.info(
            "agent_decision",
            agent_id=agent_id,
            context=decision_context,
            decision=decision_result,
            timestamp=time.time()
        )
    
    def log_tool_execution(self, tool_name, input_args, output_result, duration):
        """Log tool execution details."""
        self.logger.info(
            "tool_execution",
            tool_name=tool_name,
            input_args=input_args,
            output_result=output_result,
            duration=duration,
            timestamp=time.time()
        )
    
    def log_error(self, error_type, error_message, context, agent_id=None):
        """Log errors with full context."""
        self.logger.error(
            "agent_error",
            error_type=error_type,
            error_message=error_message,
            context=context,
            agent_id=agent_id,
            timestamp=time.time()
        )
```

**Health Check System**:
```python
class AgentHealthChecker:
    
    def __init__(self, agent_system):
        self.agent_system = agent_system
        self.health_status = {
            "overall": "unknown",
            "components": {},
            "last_check": None
        }
    
    async def run_health_checks(self):
        """Execute comprehensive health checks."""
        checks = {
            "llm_connectivity": self.check_llm_health,
            "tool_availability": self.check_tools_health,
            "memory_system": self.check_memory_health,
            "external_apis": self.check_external_apis_health
        }
        
        results = {}
        overall_healthy = True
        
        for check_name, check_func in checks.items():
            try:
                result = await check_func()
                results[check_name] = result
                if not result["healthy"]:
                    overall_healthy = False
            except Exception as e:
                results[check_name] = {
                    "healthy": False,
                    "error": str(e),
                    "timestamp": time.time()
                }
                overall_healthy = False
        
        self.health_status = {
            "overall": "healthy" if overall_healthy else "unhealthy",
            "components": results,
            "last_check": time.time()
        }
        
        return self.health_status
    
    async def check_llm_health(self):
        """Check LLM availability and response quality."""
        try:
            start_time = time.time()
            response = await self.agent_system.llm.ainvoke("Health check: respond with 'OK'")
            duration = time.time() - start_time
            
            return {
                "healthy": "OK" in response.content and duration < 5.0,
                "response_time": duration,
                "response_content": response.content[:100],
                "timestamp": time.time()
            }
        except Exception as e:
            return {
                "healthy": False,
                "error": str(e),
                "timestamp": time.time()
            }
    
    async def check_tools_health(self):
        """Check availability of critical tools."""
        tool_results = {}
        overall_healthy = True
        
        for tool_name, tool in self.agent_system.tools.items():
            try:
                # Lightweight health check for each tool
                result = await tool.health_check()
                tool_results[tool_name] = result
                if not result.get("healthy", False):
                    overall_healthy = False
            except Exception as e:
                tool_results[tool_name] = {"healthy": False, "error": str(e)}
                overall_healthy = False
        
        return {
            "healthy": overall_healthy,
            "tools": tool_results,
            "timestamp": time.time()
        }
```

**Alert System Configuration**:
```python
class AgentAlertManager:
    
    def __init__(self, metrics_collector, notification_channels):
        self.metrics = metrics_collector
        self.channels = notification_channels
        self.alert_rules = self.setup_alert_rules()
    
    def setup_alert_rules(self):
        """Define alerting rules for agent systems."""
        return {
            "high_error_rate": {
                "condition": lambda: self.get_error_rate() > 0.05,
                "severity": "high",
                "message": "Agent error rate exceeds 5%",
                "cooldown": 300  # 5 minutes
            },
            "slow_response_time": {
                "condition": lambda: self.get_avg_response_time() > 10.0,
                "severity": "medium",
                "message": "Average response time exceeds 10 seconds",
                "cooldown": 600  # 10 minutes
            },
            "tool_failure_spike": {
                "condition": lambda: self.get_tool_failure_rate() > 0.10,
                "severity": "high",
                "message": "Tool failure rate exceeds 10%",
                "cooldown": 180  # 3 minutes
            },
            "cost_threshold": {
                "condition": lambda: self.get_hourly_cost() > 50.0,
                "severity": "medium", 
                "message": "Hourly API costs exceed $50",
                "cooldown": 3600  # 1 hour
            }
        }
    
    def check_alerts(self):
        """Check all alert conditions and send notifications."""
        for alert_name, rule in self.alert_rules.items():
            if rule["condition"]():
                if self.should_send_alert(alert_name, rule["cooldown"]):
                    self.send_alert(alert_name, rule)
    
    def send_alert(self, alert_name, rule):
        """Send alert through configured channels."""
        alert_data = {
            "alert_name": alert_name,
            "severity": rule["severity"],
            "message": rule["message"],
            "timestamp": time.time(),
            "metrics_snapshot": self.get_metrics_snapshot()
        }
        
        for channel in self.channels:
            try:
                channel.send_alert(alert_data)
            except Exception as e:
                logging.error(f"Failed to send alert via {channel}: {e}")
```

This comprehensive testing and monitoring framework ensures that agentic systems maintain high quality, performance, and reliability in production environments. The combination of systematic testing, real-time monitoring, and proactive alerting enables teams to identify and resolve issues quickly while continuously improving system performance.

# Debugging with LangSmith

⏱️ **Estimated reading time: 10 minutes** 