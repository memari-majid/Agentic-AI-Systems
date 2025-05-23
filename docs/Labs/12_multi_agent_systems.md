# Lab 12: Multi-Agent Systems

⏱️ **Estimated completion time: 60 minutes**

## Overview

This lab demonstrates building multi-agent systems with LangGraph, including agent communication, coordination, and collaborative problem-solving patterns.

## Learning Objectives

- Understanding multi-agent architectures
- Implementing agent communication protocols
- Coordinating distributed agent workflows

## Key Concepts

### Multi-Agent Patterns
1. **Coordinator-Worker**: Central coordination of specialized agents
2. **Peer-to-Peer**: Direct agent-to-agent communication
3. **Hierarchical**: Layered agent organization structures

## Lab Code

```python
#!/usr/bin/env python3
"""
Multi-Agent Systems Demo
Demonstrate coordinated multi-agent workflows with LangGraph.
"""
from typing import Dict, List, TypedDict, Optional
from langgraph.graph import StateGraph
import json
import time

# Agent state definitions
class MultiAgentState(TypedDict, total=False):
    user_request: str
    task_assignments: Dict[str, str]
    agent_results: Dict[str, Dict]
    coordination_log: List[str]
    final_response: str

class Agent:
    """Base agent class with communication capabilities."""
    
    def __init__(self, name: str, specialization: str):
        self.name = name
        self.specialization = specialization
        self.capabilities = []
    
    def process_task(self, task: str, context: Dict = None) -> Dict:
        """Process assigned task and return results."""
        print(f"🤖 {self.name} processing: {task}")
        time.sleep(0.1)  # Simulate processing time
        
        return {
            "agent": self.name,
            "task": task,
            "result": self._generate_result(task, context),
            "confidence": 0.85,
            "timestamp": time.time()
        }
    
    def _generate_result(self, task: str, context: Dict = None) -> str:
        """Generate task-specific result."""
        return f"{self.specialization} result for: {task}"

class ResearchAgent(Agent):
    """Agent specialized in research and information gathering."""
    
    def __init__(self):
        super().__init__("ResearchAgent", "Research & Analysis")
        self.capabilities = ["web_search", "data_analysis", "fact_checking"]
    
    def _generate_result(self, task: str, context: Dict = None) -> str:
        if "research" in task.lower():
            return f"Research findings: Found 15 relevant sources on {task}. Key insights include current trends and best practices."
        elif "analyze" in task.lower():
            return f"Analysis complete: {task} shows positive indicators with 87% confidence."
        else:
            return f"Information gathered on {task} with comprehensive details."

class PlanningAgent(Agent):
    """Agent specialized in planning and strategy."""
    
    def __init__(self):
        super().__init__("PlanningAgent", "Strategic Planning")
        self.capabilities = ["strategic_planning", "resource_allocation", "scheduling"]
    
    def _generate_result(self, task: str, context: Dict = None) -> str:
        if "plan" in task.lower():
            return f"Strategic plan developed for {task} with 5 phases and timeline."
        elif "schedule" in task.lower():
            return f"Schedule created for {task} optimizing for efficiency and deadlines."
        else:
            return f"Planning framework established for {task}."

class ExecutionAgent(Agent):
    """Agent specialized in task execution and implementation."""
    
    def __init__(self):
        super().__init__("ExecutionAgent", "Implementation & Execution")
        self.capabilities = ["task_execution", "monitoring", "reporting"]
    
    def _generate_result(self, task: str, context: Dict = None) -> str:
        if "execute" in task.lower():
            return f"Execution initiated for {task} with monitoring dashboard active."
        elif "implement" in task.lower():
            return f"Implementation completed for {task} meeting all specifications."
        else:
            return f"Execution plan ready for {task} with quality assurance."

class CoordinatorAgent(Agent):
    """Master coordinator agent managing other agents."""
    
    def __init__(self):
        super().__init__("CoordinatorAgent", "Multi-Agent Coordination")
        self.managed_agents = {
            "research": ResearchAgent(),
            "planning": PlanningAgent(), 
            "execution": ExecutionAgent()
        }
    
    def analyze_request(self, request: str) -> Dict[str, str]:
        """Analyze user request and assign tasks to appropriate agents."""
        assignments = {}
        
        if any(word in request.lower() for word in ["research", "find", "analyze", "study"]):
            assignments["research"] = f"Research and analyze: {request}"
        
        if any(word in request.lower() for word in ["plan", "strategy", "organize", "schedule"]):
            assignments["planning"] = f"Create strategic plan for: {request}"
        
        if any(word in request.lower() for word in ["execute", "implement", "build", "create"]):
            assignments["execution"] = f"Execute and implement: {request}"
        
        # Default: assign to all agents for comprehensive handling
        if not assignments:
            assignments = {
                "research": f"Research background for: {request}",
                "planning": f"Plan approach for: {request}",
                "execution": f"Prepare execution for: {request}"
            }
        
        return assignments

# Multi-agent workflow nodes
coordinator = CoordinatorAgent()

def task_coordination_node(state: MultiAgentState) -> MultiAgentState:
    """Coordinate task assignment across agents."""
    request = state["user_request"]
    
    # Analyze request and assign tasks
    assignments = coordinator.analyze_request(request)
    state["task_assignments"] = assignments
    
    log_entry = f"Coordinator assigned {len(assignments)} tasks to agents"
    state["coordination_log"] = state.get("coordination_log", []) + [log_entry]
    
    print(f"📋 Task Coordination:")
    for agent, task in assignments.items():
        print(f"   {agent}: {task}")
    
    return state

def research_agent_node(state: MultiAgentState) -> MultiAgentState:
    """Execute research agent tasks."""
    assignments = state.get("task_assignments", {})
    
    if "research" in assignments:
        research_task = assignments["research"]
        result = coordinator.managed_agents["research"].process_task(research_task)
        
        if "agent_results" not in state:
            state["agent_results"] = {}
        state["agent_results"]["research"] = result
        
        log_entry = f"Research agent completed task with {result['confidence']:.0%} confidence"
        state["coordination_log"] = state.get("coordination_log", []) + [log_entry]
    
    return state

def planning_agent_node(state: MultiAgentState) -> MultiAgentState:
    """Execute planning agent tasks."""
    assignments = state.get("task_assignments", {})
    
    if "planning" in assignments:
        planning_task = assignments["planning"]
        
        # Get research context if available
        context = {}
        if "agent_results" in state and "research" in state["agent_results"]:
            context["research"] = state["agent_results"]["research"]
        
        result = coordinator.managed_agents["planning"].process_task(planning_task, context)
        
        if "agent_results" not in state:
            state["agent_results"] = {}
        state["agent_results"]["planning"] = result
        
        log_entry = f"Planning agent completed task with strategic framework"
        state["coordination_log"] = state.get("coordination_log", []) + [log_entry]
    
    return state

def execution_agent_node(state: MultiAgentState) -> MultiAgentState:
    """Execute implementation agent tasks."""
    assignments = state.get("task_assignments", {})
    
    if "execution" in assignments:
        execution_task = assignments["execution"]
        
        # Get context from other agents
        context = {}
        if "agent_results" in state:
            if "research" in state["agent_results"]:
                context["research"] = state["agent_results"]["research"]
            if "planning" in state["agent_results"]:
                context["planning"] = state["agent_results"]["planning"]
        
        result = coordinator.managed_agents["execution"].process_task(execution_task, context)
        
        if "agent_results" not in state:
            state["agent_results"] = {}
        state["agent_results"]["execution"] = result
        
        log_entry = f"Execution agent completed implementation tasks"
        state["coordination_log"] = state.get("coordination_log", []) + [log_entry]
    
    return state

def result_synthesis_node(state: MultiAgentState) -> MultiAgentState:
    """Synthesize results from all agents into final response."""
    agent_results = state.get("agent_results", {})
    
    # Combine results from all agents
    final_response = f"Multi-agent system response to: {state['user_request']}\n\n"
    
    for agent_name, result in agent_results.items():
        final_response += f"🤖 {result['agent']}:\n"
        final_response += f"   {result['result']}\n\n"
    
    final_response += f"Coordination Summary:\n"
    for log_entry in state.get("coordination_log", []):
        final_response += f"   • {log_entry}\n"
    
    state["final_response"] = final_response
    
    return state

def build_multi_agent_graph() -> StateGraph:
    """Build multi-agent coordination graph."""
    graph = StateGraph(MultiAgentState)
    
    # Add coordination and agent nodes
    graph.add_node("coordinator", task_coordination_node)
    graph.add_node("research_agent", research_agent_node)
    graph.add_node("planning_agent", planning_agent_node)
    graph.add_node("execution_agent", execution_agent_node)
    graph.add_node("synthesizer", result_synthesis_node)
    
    # Define workflow
    graph.set_entry_point("coordinator")
    
    # Parallel agent execution
    graph.add_edge("coordinator", "research_agent")
    graph.add_edge("coordinator", "planning_agent")
    graph.add_edge("coordinator", "execution_agent")
    
    # Synthesis after all agents complete
    graph.add_edge("research_agent", "synthesizer")
    graph.add_edge("planning_agent", "synthesizer")
    graph.add_edge("execution_agent", "synthesizer")
    
    graph.set_finish_point("synthesizer")
    
    return graph

def main():
    print("=== Multi-Agent Systems Demo ===")
    
    # Build the multi-agent graph
    graph = build_multi_agent_graph().compile()
    
    # Test scenarios
    test_requests = [
        "Research and plan a new product launch strategy",
        "Analyze market trends and create implementation roadmap",
        "Study competitor analysis and execute marketing campaign"
    ]
    
    for request in test_requests:
        print(f"\n{'='*60}")
        print(f"User Request: {request}")
        print('='*60)
        
        # Execute multi-agent workflow
        initial_state = {"user_request": request}
        final_state = graph.invoke(initial_state)
        
        # Display results
        print("\n" + final_state["final_response"])

if __name__ == "__main__":
    main()
```

## How to Run

1. Save as `12_multi_agent_systems.py`
2. Install: `pip install langgraph`
3. Run: `python 12_multi_agent_systems.py`

## Key Features

- **Agent Specialization**: Each agent has specific capabilities
- **Coordination Protocol**: Central coordinator manages task distribution
- **Parallel Execution**: Agents work simultaneously for efficiency
- **Context Sharing**: Agents can access each other's results
- **Result Synthesis**: Combined output from all agents

## Multi-Agent Patterns

### Coordinator-Worker Pattern
```python
# Central coordinator assigns tasks
coordinator → [agent1, agent2, agent3] → synthesizer
```

### Peer-to-Peer Communication
```python
# Agents communicate directly
agent1 ↔ agent2 ↔ agent3
```

### Hierarchical Organization
```python
# Layered agent structure
supervisor_agent → [team_lead1, team_lead2] → [worker_agents]
```

## Download Code

[Download 12_multi_agent_systems.py](12_multi_agent_systems.py){ .md-button .md-button--primary } 