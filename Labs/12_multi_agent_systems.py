#!/usr/bin/env python3
"""
Chapter 12 Extension - Multi-Agent Systems
-----------------------------------------
This example demonstrates collaborative multi-agent architectures:

1. Agent specialization and division of labor
2. Communication protocols between agents
3. Debate and consensus mechanisms
4. Hierarchical agent organizations
5. Evaluation of collaborative outcomes

Key concepts:
- Agent roles and specialization
- Structured communication
- Emerging consensus
- Coordination patterns
"""
import argparse
import json
import time
import random
from enum import Enum
from typing import Dict, List, TypedDict, Optional, Any, Tuple, Set

from langgraph.graph import StateGraph

# ---------------------------------------------------------------------------
# Agent Types and Data Structures ------------------------------------------
# ---------------------------------------------------------------------------

class AgentRole(str, Enum):
    COORDINATOR = "coordinator"
    RESEARCHER = "researcher"
    CRITIC = "critic"
    EXECUTOR = "executor"
    EVALUATOR = "evaluator"

class AgentMessage(TypedDict):
    from_agent: AgentRole
    to_agent: Optional[AgentRole]  # None means broadcast to all
    content: str
    timestamp: float
    msg_type: str  # e.g., "request", "response", "critique", "plan", etc.
    iteration: int

class MultiAgentState(TypedDict, total=False):
    task: str
    messages: List[AgentMessage]
    artifacts: Dict[str, Any]
    current_agent: AgentRole
    convergence_score: float
    solution: Optional[str]
    evaluation: Optional[Dict[str, float]]
    max_iterations: int
    current_iteration: int

# ---------------------------------------------------------------------------
# Agent Implementations ----------------------------------------------------
# ---------------------------------------------------------------------------

def coordinator_agent(state: MultiAgentState) -> MultiAgentState:
    """
    Coordinator agent that manages the collaboration process.
    - Assigns tasks to specialized agents
    - Tracks progress and ensures convergence
    - Makes final decisions when needed
    """
    current_iteration = state.get("current_iteration", 0)
    max_iterations = state.get("max_iterations", 5)
    messages = state.get("messages", [])
    artifacts = state.get("artifacts", {})
    
    # First iteration: initialize the task
    if current_iteration == 0:
        task = state.get("task", "")
        print(f"\n🧠 Coordinator: Initializing task '{task}'")
        
        # Create initial plan
        initial_plan = "1. Research phase: Gather information\n2. Analysis phase: Evaluate options\n3. Planning phase: Develop solution\n4. Execution phase: Implement solution"
        artifacts["plan"] = initial_plan
        
        # Send initial message to researcher
        messages.append({
            "from_agent": AgentRole.COORDINATOR,
            "to_agent": AgentRole.RESEARCHER,
            "content": f"Please research the following task: {task}",
            "timestamp": time.time(),
            "msg_type": "request",
            "iteration": current_iteration
        })
        
        # Update state
        state["messages"] = messages
        state["artifacts"] = artifacts
        state["current_iteration"] = current_iteration + 1
        state["current_agent"] = AgentRole.RESEARCHER
        
    # Middle iterations: manage the process
    elif current_iteration < max_iterations - 1:
        print(f"\n🧠 Coordinator: Managing iteration {current_iteration}")
        
        # Analyze recent messages
        recent_messages = [m for m in messages if m["iteration"] == current_iteration - 1]
        
        # Check if we have all needed responses
        needed_responses = set()
        for msg in recent_messages:
            if msg["from_agent"] == AgentRole.COORDINATOR and msg["msg_type"] == "request":
                needed_responses.add(msg["to_agent"])
        
        received_responses = {msg["from_agent"] for msg in recent_messages 
                             if msg["msg_type"] == "response" and msg["to_agent"] == AgentRole.COORDINATOR}
        
        # If we're missing responses, request them again
        if needed_responses and not needed_responses.issubset(received_responses):
            missing = needed_responses - received_responses
            print(f"  Missing responses from: {missing}")
            
            for agent in missing:
                messages.append({
                    "from_agent": AgentRole.COORDINATOR,
                    "to_agent": agent,
                    "content": f"Following up on my previous request. Please respond.",
                    "timestamp": time.time(),
                    "msg_type": "request",
                    "iteration": current_iteration
                })
            
            # Keep the current agent as the first missing one
            state["current_agent"] = list(missing)[0]
        else:
            # Determine next phase based on iteration
            phase = current_iteration % 3
            
            if phase == 0:  # Research phase
                messages.append({
                    "from_agent": AgentRole.COORDINATOR,
                    "to_agent": AgentRole.RESEARCHER,
                    "content": "Please continue researching and provide additional information.",
                    "timestamp": time.time(),
                    "msg_type": "request",
                    "iteration": current_iteration
                })
                state["current_agent"] = AgentRole.RESEARCHER
            
            elif phase == 1:  # Critique phase
                # Get the latest research
                research = next((m["content"] for m in reversed(messages) 
                               if m["from_agent"] == AgentRole.RESEARCHER 
                               and m["msg_type"] == "response"), "")
                
                messages.append({
                    "from_agent": AgentRole.COORDINATOR,
                    "to_agent": AgentRole.CRITIC,
                    "content": f"Please critique this research and suggest improvements:\n\n{research}",
                    "timestamp": time.time(),
                    "msg_type": "request",
                    "iteration": current_iteration
                })
                state["current_agent"] = AgentRole.CRITIC
            
            else:  # Execution phase
                # Get the latest critique
                critique = next((m["content"] for m in reversed(messages) 
                               if m["from_agent"] == AgentRole.CRITIC 
                               and m["msg_type"] == "response"), "")
                
                messages.append({
                    "from_agent": AgentRole.COORDINATOR,
                    "to_agent": AgentRole.EXECUTOR,
                    "content": f"Based on our research and critique, please develop a solution:\n\n{critique}",
                    "timestamp": time.time(),
                    "msg_type": "request",
                    "iteration": current_iteration
                })
                state["current_agent"] = AgentRole.EXECUTOR
        
        # Update state
        state["messages"] = messages
        state["current_iteration"] = current_iteration + 1
        
    # Final iteration: conclude the task
    else:
        print(f"\n🧠 Coordinator: Finalizing task at iteration {current_iteration}")
        
        # Collect all execution results
        execution_results = [m["content"] for m in messages 
                            if m["from_agent"] == AgentRole.EXECUTOR 
                            and m["msg_type"] == "response"]
        
        # Create final solution
        solution = "FINAL SOLUTION:\n\n"
        solution += "\n".join(execution_results[-2:]) if execution_results else "No solution developed."
        
        # Request evaluation
        messages.append({
            "from_agent": AgentRole.COORDINATOR,
            "to_agent": AgentRole.EVALUATOR,
            "content": f"Please evaluate this solution:\n\n{solution}",
            "timestamp": time.time(),
            "msg_type": "request",
            "iteration": current_iteration
        })
        
        # Store the solution
        state["solution"] = solution
        state["messages"] = messages
        state["current_iteration"] = current_iteration + 1
        state["current_agent"] = AgentRole.EVALUATOR
    
    return state

def researcher_agent(state: MultiAgentState) -> MultiAgentState:
    """
    Researcher agent that gathers and synthesizes information.
    - Collects relevant data
    - Organizes information
    - Identifies knowledge gaps
    """
    # Get current state
    task = state.get("task", "")
    messages = state.get("messages", [])
    current_iteration = state.get("current_iteration", 0)
    
    # Get the latest request from the coordinator
    request = next((msg["content"] for msg in reversed(messages) 
                   if msg["to_agent"] == AgentRole.RESEARCHER 
                   and msg["msg_type"] == "request"), "")
    
    print(f"\n📚 Researcher: Working on iteration {current_iteration}")
    print(f"  Received request: {request[:50]}..." if len(request) > 50 else f"  Received request: {request}")
    
    # Simulate research with a time delay
    time.sleep(0.5)
    
    # Generate research findings based on the task and iteration
    if "research" in request.lower() or "information" in request.lower():
        # First iteration provides basic information
        if current_iteration <= 1:
            research = f"Initial research on '{task}':\n\n"
            research += "1. Key aspects of the problem:\n"
            research += "   - The problem involves multiple stakeholders\n"
            research += "   - There are technical and non-technical components\n"
            research += "   - Time constraints will affect the solution\n\n"
            research += "2. Potential approaches:\n"
            research += "   - Approach A: Quick implementation, moderate results\n"
            research += "   - Approach B: Longer timeline, more comprehensive\n"
            research += "   - Approach C: Hybrid solution with phased delivery"
        else:
            # Later iterations add more detailed information
            research = f"Additional research on '{task}':\n\n"
            research += "3. Detailed analysis of approaches:\n"
            research += "   - Approach A strengths: faster implementation, lower cost\n"
            research += "   - Approach B strengths: more complete solution, better long-term results\n"
            research += "   - Approach C strengths: balances time constraints with solution quality\n\n"
            research += "4. Related case studies:\n"
            research += "   - Case Study X demonstrated a 40% improvement using a hybrid approach\n"
            research += "   - Case Study Y showed technical challenges with rapid implementation\n\n"
            research += "5. Recommended approach based on research: Approach C (Hybrid solution)"
    else:
        # Generic response for unclear requests
        research = f"Research findings for task '{task}':\n\n"
        research += "The task requires balancing multiple factors including time, quality, and resources.\n"
        research += "Based on analysis, a flexible approach with regular evaluation points is recommended."
    
    # Send response back to coordinator
    messages.append({
        "from_agent": AgentRole.RESEARCHER,
        "to_agent": AgentRole.COORDINATOR,
        "content": research,
        "timestamp": time.time(),
        "msg_type": "response",
        "iteration": current_iteration - 1
    })
    
    # Update state
    state["messages"] = messages
    state["current_agent"] = AgentRole.COORDINATOR
    
    return state

def critic_agent(state: MultiAgentState) -> MultiAgentState:
    """
    Critic agent that identifies weaknesses and suggests improvements.
    - Analyzes proposals for flaws
    - Suggests alternative approaches
    - Provides constructive feedback
    """
    # Get current state
    messages = state.get("messages", [])
    current_iteration = state.get("current_iteration", 0)
    
    # Get the latest request from the coordinator
    request = next((msg["content"] for msg in reversed(messages) 
                   if msg["to_agent"] == AgentRole.CRITIC 
                   and msg["msg_type"] == "request"), "")
    
    print(f"\n🔍 Critic: Working on iteration {current_iteration}")
    print(f"  Received request: {request[:50]}..." if len(request) > 50 else f"  Received request: {request}")
    
    # Simulate critical analysis with a time delay
    time.sleep(0.5)
    
    # Generate critique
    critique = "Critique of the research:\n\n"
    critique += "Strengths:\n"
    critique += "- Good identification of multiple approaches\n"
    critique += "- Consideration of stakeholder needs\n"
    critique += "- Evidence-based recommendations\n\n"
    
    critique += "Weaknesses:\n"
    critique += "- Insufficient detail on implementation steps\n"
    critique += "- Limited consideration of resource constraints\n"
    critique += "- Missing risk assessment for each approach\n\n"
    
    critique += "Suggestions for improvement:\n"
    critique += "1. Develop a more detailed implementation plan for the hybrid approach\n"
    critique += "2. Add a section on required resources and potential constraints\n"
    critique += "3. Include a risk assessment and mitigation strategies\n"
    critique += "4. Consider a phased implementation with clear milestones\n\n"
    
    critique += "Recommended focus: Develop a phased implementation plan with risk mitigation strategies."
    
    # Send response back to coordinator
    messages.append({
        "from_agent": AgentRole.CRITIC,
        "to_agent": AgentRole.COORDINATOR,
        "content": critique,
        "timestamp": time.time(),
        "msg_type": "response",
        "iteration": current_iteration - 1
    })
    
    # Update state
    state["messages"] = messages
    state["current_agent"] = AgentRole.COORDINATOR
    
    return state

def executor_agent(state: MultiAgentState) -> MultiAgentState:
    """
    Executor agent that implements solutions.
    - Turns plans into actionable steps
    - Identifies implementation details
    - Provides concrete solutions
    """
    # Get current state
    messages = state.get("messages", [])
    current_iteration = state.get("current_iteration", 0)
    task = state.get("task", "")
    
    # Get the latest request from the coordinator
    request = next((msg["content"] for msg in reversed(messages) 
                   if msg["to_agent"] == AgentRole.EXECUTOR 
                   and msg["msg_type"] == "request"), "")
    
    print(f"\n⚙️ Executor: Working on iteration {current_iteration}")
    print(f"  Received request: {request[:50]}..." if len(request) > 50 else f"  Received request: {request}")
    
    # Simulate execution with a time delay
    time.sleep(0.5)
    
    # Generate execution plan
    solution = f"Implementation plan for task '{task}':\n\n"
    
    solution += "Phase 1: Setup and Initial Implementation (Weeks 1-2)\n"
    solution += "- Action 1.1: Establish project team and roles\n"
    solution += "- Action 1.2: Define success metrics and KPIs\n"
    solution += "- Action 1.3: Set up basic infrastructure\n"
    solution += "- Milestone: Basic framework operational\n\n"
    
    solution += "Phase 2: Core Development (Weeks 3-6)\n"
    solution += "- Action 2.1: Implement primary functionality\n"
    solution += "- Action 2.2: Develop integration points\n"
    solution += "- Action 2.3: Create monitoring system\n"
    solution += "- Milestone: Core system operational\n\n"
    
    solution += "Phase 3: Refinement and Expansion (Weeks 7-10)\n"
    solution += "- Action 3.1: Add advanced features\n"
    solution += "- Action 3.2: Optimize performance\n"
    solution += "- Action 3.3: Implement feedback from early phases\n"
    solution += "- Milestone: Complete solution deployed\n\n"
    
    solution += "Risk Mitigation:\n"
    solution += "- Risk 1: Resource constraints → Prioritization framework established\n"
    solution += "- Risk 2: Technical challenges → Expert advisors identified\n"
    solution += "- Risk 3: Timeline pressure → Buffer periods built into schedule\n\n"
    
    solution += "Required Resources:\n"
    solution += "- Team: 1 project manager, 2 senior developers, 1 QA specialist\n"
    solution += "- Infrastructure: Cloud hosting, CI/CD pipeline\n"
    solution += "- Budget: Estimated at $X for initial 3 months"
    
    # Send response back to coordinator
    messages.append({
        "from_agent": AgentRole.EXECUTOR,
        "to_agent": AgentRole.COORDINATOR,
        "content": solution,
        "timestamp": time.time(),
        "msg_type": "response",
        "iteration": current_iteration - 1
    })
    
    # Update state
    state["messages"] = messages
    state["current_agent"] = AgentRole.COORDINATOR
    
    return state

def evaluator_agent(state: MultiAgentState) -> MultiAgentState:
    """
    Evaluator agent that assesses the quality of solutions.
    - Measures solutions against requirements
    - Identifies strengths and weaknesses
    - Provides an objective assessment
    """
    # Get current state
    messages = state.get("messages", [])
    current_iteration = state.get("current_iteration", 0)
    
    # Get the latest request from the coordinator
    request = next((msg["content"] for msg in reversed(messages) 
                   if msg["to_agent"] == AgentRole.EVALUATOR 
                   and msg["msg_type"] == "request"), "")
    
    # Get the solution to evaluate
    solution = state.get("solution", "")
    
    print(f"\n⭐ Evaluator: Working on iteration {current_iteration}")
    
    # Simulate evaluation with a time delay
    time.sleep(0.5)
    
    # Generate evaluation metrics
    evaluation = {
        "comprehensiveness": 0.85,
        "feasibility": 0.78,
        "clarity": 0.91,
        "risk_management": 0.72,
        "resource_allocation": 0.80,
        "overall_quality": 0.82
    }
    
    # Generate evaluation text
    evaluation_text = "Solution Evaluation:\n\n"
    
    evaluation_text += "Strengths:\n"
    evaluation_text += "- Well-structured phased approach\n"
    evaluation_text += "- Clear milestones and deliverables\n"
    evaluation_text += "- Good consideration of risks\n"
    evaluation_text += "- Realistic timeline\n\n"
    
    evaluation_text += "Areas for improvement:\n"
    evaluation_text += "- More detail needed on specific technologies\n"
    evaluation_text += "- Budget estimates could be more precise\n"
    evaluation_text += "- Additional contingency planning recommended\n\n"
    
    evaluation_text += "Metrics:\n"
    for metric, score in evaluation.items():
        evaluation_text += f"- {metric.replace('_', ' ').title()}: {score:.2f}/1.00\n"
    
    evaluation_text += f"\nOverall assessment: {evaluation['overall_quality'] * 100:.1f}% optimal solution"
    
    # Send response back to coordinator
    messages.append({
        "from_agent": AgentRole.EVALUATOR,
        "to_agent": AgentRole.COORDINATOR,
        "content": evaluation_text,
        "timestamp": time.time(),
        "msg_type": "response",
        "iteration": current_iteration - 1
    })
    
    # Update state
    state["messages"] = messages
    state["evaluation"] = evaluation
    state["convergence_score"] = 1.0  # Mark as complete
    
    return state

# ---------------------------------------------------------------------------
# Router Function ----------------------------------------------------------
# ---------------------------------------------------------------------------

def router(state: MultiAgentState) -> str:
    """Route to the next agent based on the current_agent field."""
    return state.get("current_agent", AgentRole.COORDINATOR)

# ---------------------------------------------------------------------------
# Process Function ---------------------------------------------------------
# ---------------------------------------------------------------------------

def decide_if_finished(state: MultiAgentState) -> bool:
    """Determine if the multi-agent process has finished."""
    # Check if we've reached a convergence score threshold
    if state.get("convergence_score", 0) >= 0.9:
        return True
    
    # Check if we've done a complete final iteration
    current_iteration = state.get("current_iteration", 0)
    max_iterations = state.get("max_iterations", 5)
    
    if current_iteration > max_iterations:
        # Check if we have an evaluation
        if state.get("evaluation") is not None:
            return True
    
    return False

# ---------------------------------------------------------------------------
# Graph Construction -------------------------------------------------------
# ---------------------------------------------------------------------------

def build_multi_agent_graph() -> StateGraph:
    """Build the graph for a multi-agent system."""
    # Create the graph with our state
    graph = StateGraph(MultiAgentState)
    
    # Add agent nodes
    graph.add_node(AgentRole.COORDINATOR, coordinator_agent)
    graph.add_node(AgentRole.RESEARCHER, researcher_agent)
    graph.add_node(AgentRole.CRITIC, critic_agent)
    graph.add_node(AgentRole.EXECUTOR, executor_agent)
    graph.add_node(AgentRole.EVALUATOR, evaluator_agent)
    
    # Set the coordinator as entry point
    graph.set_entry_point(AgentRole.COORDINATOR)
    
    # Add conditional routing based on the current_agent field
    graph.add_conditional_edges(
        AgentRole.COORDINATOR,
        router,
        {
            AgentRole.RESEARCHER: AgentRole.RESEARCHER,
            AgentRole.CRITIC: AgentRole.CRITIC,
            AgentRole.EXECUTOR: AgentRole.EXECUTOR,
            AgentRole.EVALUATOR: AgentRole.EVALUATOR,
        }
    )
    
    # Connect all agents back to the coordinator
    graph.add_edge(AgentRole.RESEARCHER, AgentRole.COORDINATOR)
    graph.add_edge(AgentRole.CRITIC, AgentRole.COORDINATOR)
    graph.add_edge(AgentRole.EXECUTOR, AgentRole.COORDINATOR)
    graph.add_edge(AgentRole.EVALUATOR, AgentRole.COORDINATOR)
    
    # Add finishing condition
    graph.add_finished_state(decide_if_finished)
    
    return graph

# ---------------------------------------------------------------------------
# Visualization and Reporting ----------------------------------------------
# ---------------------------------------------------------------------------

def print_agent_communication(messages: List[AgentMessage]) -> None:
    """Print the communication between agents in a readable format."""
    print("\n=== Agent Communication Log ===")
    
    for i, msg in enumerate(messages):
        from_agent = msg["from_agent"]
        to_agent = msg["to_agent"] or "ALL"
        content_preview = msg["content"][:50] + "..." if len(msg["content"]) > 50 else msg["content"]
        
        # Format each message
        print(f"{i+1}. {from_agent} → {to_agent} [{msg['msg_type']}]: {content_preview}")

def print_solution_summary(state: MultiAgentState) -> None:
    """Print a summary of the final solution."""
    solution = state.get("solution", "No solution found.")
    evaluation = state.get("evaluation", {})
    
    print("\n=== Solution Summary ===")
    
    # Print a condensed version of the solution
    print("\nSolution Overview:")
    lines = solution.split('\n')
    in_phase = False
    for line in lines:
        if line.startswith("Phase ") or line.startswith("Risk ") or line.startswith("Required "):
            in_phase = True
            print(line)
        elif in_phase and line.startswith("- "):
            # Only print the first part of each bullet point
            print(line.split('→')[0] if '→' in line else line)
        elif line.strip() == "":
            in_phase = False
            print()
    
    # Print evaluation metrics if available
    if evaluation:
        print("\nEvaluation Metrics:")
        for metric, score in evaluation.items():
            print(f"- {metric.replace('_', ' ').title()}: {score:.2f}/1.00")
    
    # Print overall assessment
    overall = evaluation.get("overall_quality", 0) * 100
    print(f"\nOverall Quality Score: {overall:.1f}%")

# ---------------------------------------------------------------------------
# Alternative Multi-Agent Patterns -----------------------------------------
# ---------------------------------------------------------------------------

def describe_alternative_patterns() -> None:
    """Describe other multi-agent collaboration patterns."""
    print("\n=== Alternative Multi-Agent Patterns ===")
    
    print("""
1. Debate Pattern
----------------
Agents with different perspectives debate a topic to reach consensus:

- Proposer Agent: Suggests initial solutions
- Supporter Agent: Identifies strengths and adds supporting evidence
- Challenger Agent: Identifies weaknesses and potential issues
- Mediator Agent: Summarizes arguments and drives toward consensus
- Decider Agent: Makes final judgment after debate concludes

Implementation Example:
```python
def build_debate_graph() -> StateGraph:
    graph = StateGraph(DebateState)
    
    # Add agent nodes
    graph.add_node("proposer", proposer_agent)
    graph.add_node("supporter", supporter_agent)
    graph.add_node("challenger", challenger_agent)
    graph.add_node("mediator", mediator_agent)
    graph.add_node("decider", decider_agent)
    
    # Define debate flow
    graph.set_entry_point("proposer")
    graph.add_edge("proposer", "supporter")
    graph.add_edge("supporter", "challenger")
    graph.add_edge("challenger", "mediator")
    
    # Conditional edge: either continue debate or reach decision
    graph.add_conditional_edges(
        "mediator",
        debate_continues,
        {
            "continue": "proposer",  # Loop back for another round
            "conclude": "decider"     # Move to final decision
        }
    )
    
    graph.set_finish_point("decider")
    return graph
```
    """)
    
    print("""
2. Market Pattern
----------------
Agents bid on and trade tasks based on their capabilities:

- Manager Agent: Defines tasks and evaluates results
- Worker Agents: Bid on tasks they're optimized to handle
- Broker Agent: Matches tasks to workers based on bids
- QA Agent: Evaluates work quality and provides feedback

Implementation Example:
```python
def worker_selection(state: MarketState) -> str:
    # Select worker based on bids
    task = state["current_task"]
    bids = state["bids"].get(task.id, {})
    
    if not bids:
        return "broker"  # No bids, go back to broker
    
    # Select highest rated worker within budget
    qualified_workers = [w for w in bids.keys() 
                         if bids[w]["rating"] > 0.7 and bids[w]["cost"] <= task.budget]
    
    if not qualified_workers:
        return "broker"  # No qualified workers
        
    # Return worker ID with highest rating
    best_worker = max(qualified_workers, key=lambda w: bids[w]["rating"])
    return best_worker
```
    """)
    
    print("""
3. Hierarchical Organization
---------------------------
Agents organized in management layers with different responsibilities:

- Executive Agent: Sets high-level goals and evaluates outcomes
- Manager Agents: Break goals into tasks and coordinate specialists
- Specialist Agents: Handle specific domains (research, writing, coding)
- Assistant Agents: Handle routine subtasks under specialist direction

Implementation:
```python
# Define a hierarchical team for a complex task
executive = ExecutiveAgent(name="executive")
managers = [
    ManagerAgent(name="research_manager"),
    ManagerAgent(name="development_manager"),
    ManagerAgent(name="quality_manager")
]

specialists = {
    "research": [
        SpecialistAgent(name="market_researcher"),
        SpecialistAgent(name="technical_researcher")
    ],
    "development": [
        SpecialistAgent(name="frontend_dev"),
        SpecialistAgent(name="backend_dev"),
        SpecialistAgent(name="data_engineer")
    ],
    "quality": [
        SpecialistAgent(name="tester"),
        SpecialistAgent(name="documentation")
    ]
}

# Connect the hierarchy
for manager in managers:
    executive.add_subordinate(manager)
    
for domain, specs in specialists.items():
    manager = next(m for m in managers if domain in m.name)
    for specialist in specs:
        manager.add_subordinate(specialist)
```
    """)

# ---------------------------------------------------------------------------
# Main Function ------------------------------------------------------------
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Multi-Agent System Demo")
    parser.add_argument("--task", type=str, default="Develop a new customer onboarding process",
                      help="Task for the agents to collaborate on")
    parser.add_argument("--iterations", type=int, default=5,
                      help="Maximum number of iterations")
    parser.add_argument("--patterns", action="store_true",
                      help="Show alternative multi-agent patterns")
    
    args = parser.parse_args()
    
    # Show alternative patterns if requested
    if args.patterns:
        describe_alternative_patterns()
        return
    
    print("\n=== Multi-Agent Collaboration System ===")
    print(f"Task: {args.task}")
    print(f"Maximum iterations: {args.iterations}")
    
    # Build the multi-agent graph
    graph = build_multi_agent_graph().compile()
    
    # Initialize the state
    initial_state: MultiAgentState = {
        "task": args.task,
        "messages": [],
        "artifacts": {},
        "current_agent": AgentRole.COORDINATOR,
        "convergence_score": 0.0,
        "max_iterations": args.iterations,
        "current_iteration": 0
    }
    
    # Execute the graph
    print("\nStarting agent collaboration...")
    final_state = graph.invoke(initial_state)
    
    # Display results
    print_agent_communication(final_state.get("messages", []))
    print_solution_summary(final_state)
    
    print("\n=== Multi-Agent System Benefits ===")
    print("""
1. Specialized Expertise:
   Each agent contributes unique capabilities to the solution

2. Improved Quality:
   The critic agent identifies weaknesses that might be missed 
   by a single agent approach

3. Balanced Solutions:
   Multiple perspectives lead to more balanced and thorough outcomes

4. Scalability:
   The system can be extended with additional specialized agents 
   as needed for more complex problems
    """)

if __name__ == "__main__":
    main() 