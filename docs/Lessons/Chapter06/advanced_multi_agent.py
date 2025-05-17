#!/usr/bin/env python3
"""
Advanced Multi-Agent Collaboration Patterns (Chapter 6.5)
--------------------------------------------------------

This implementation demonstrates advanced multi-agent collaboration patterns that 
extend the basic Coordinator-Worker-Delegator approach with:

1. Structured communication protocols
2. Feedback loops and critic roles
3. Multi-dimensional specialization
4. Convergence and consensus mechanisms
5. Dynamic routing based on state

Usage:
    python advanced_multi_agent.py --task "Design a new employee onboarding system"
"""

import argparse
import time
import json
from enum import Enum
from typing import Dict, List, TypedDict, Optional, Any, Tuple, Set

try:
    from langgraph.graph import StateGraph
except ImportError:
    print("LangGraph not installed. Install with: pip install langgraph")
    StateGraph = object  # Placeholder to avoid syntax errors


# ---------------------------------------------------------------------------
# Agent Types and Data Structures ------------------------------------------
# ---------------------------------------------------------------------------

class AgentRole(str, Enum):
    """Roles for the advanced multi-agent system."""
    COORDINATOR = "coordinator"
    RESEARCHER = "researcher"
    CRITIC = "critic"
    EXECUTOR = "executor"
    EVALUATOR = "evaluator"


class AgentMessage(TypedDict):
    """Structured message format for agent communication."""
    from_agent: AgentRole
    to_agent: Optional[AgentRole]  # None means broadcast to all
    content: str
    timestamp: float
    msg_type: str  # e.g., "request", "response", "critique", "plan", etc.
    iteration: int


class MultiAgentState(TypedDict, total=False):
    """State representation for advanced multi-agent system."""
    task: str
    messages: List[AgentMessage]
    artifacts: Dict[str, Any]
    current_agent: AgentRole
    current_phase: str
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
        state["current_phase"] = "research"
        
    # Middle iterations: manage the process
    elif current_iteration < max_iterations - 1:
        print(f"\n🧠 Coordinator: Managing iteration {current_iteration}")
        
        # Analyze recent messages
        recent_messages = [m for m in messages if m["iteration"] == current_iteration - 1]
        
        # Determine next phase based on iteration and task progress
        phase = current_iteration % 4
        
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
            state["current_phase"] = "research"
        
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
            state["current_phase"] = "critique"
        
        elif phase == 2:  # Execution planning phase
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
            state["current_phase"] = "execution"
            
        else:  # Evaluation phase
            # Early evaluation to gauge progress
            execution_results = [m["content"] for m in messages 
                               if m["from_agent"] == AgentRole.EXECUTOR 
                               and m["msg_type"] == "response"]
            
            if execution_results:
                latest_execution = execution_results[-1]
                messages.append({
                    "from_agent": AgentRole.COORDINATOR,
                    "to_agent": AgentRole.EVALUATOR,
                    "content": f"Please evaluate this solution draft:\n\n{latest_execution}",
                    "timestamp": time.time(),
                    "msg_type": "request",
                    "iteration": current_iteration
                })
                state["current_agent"] = AgentRole.EVALUATOR
                state["current_phase"] = "evaluation"
            else:
                # Fallback if we don't have execution results yet
                messages.append({
                    "from_agent": AgentRole.COORDINATOR,
                    "to_agent": AgentRole.RESEARCHER,
                    "content": "Let's explore the problem space further. Please provide more detailed research.",
                    "timestamp": time.time(),
                    "msg_type": "request",
                    "iteration": current_iteration
                })
                state["current_agent"] = AgentRole.RESEARCHER
                state["current_phase"] = "research"
    
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
            "content": f"Please evaluate this final solution:\n\n{solution}",
            "timestamp": time.time(),
            "msg_type": "request",
            "iteration": current_iteration
        })
        
        # Store the solution
        state["solution"] = solution
        state["messages"] = messages
        state["current_iteration"] = current_iteration + 1
        state["current_agent"] = AgentRole.EVALUATOR
        state["current_phase"] = "final_evaluation"
    
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
    print(f"  Request: {request[:50]}..." if len(request) > 50 else f"  Request: {request}")
    
    # In a real implementation, would use an LLM here to generate research
    # For demonstration, we'll use templates based on the task
    if "onboarding" in task.lower():
        if current_iteration <= 1:
            research = f"Initial research on '{task}':\n\n"
            research += "1. Key aspects of employee onboarding:\n"
            research += "   - Administrative processes (paperwork, IT setup, etc.)\n"
            research += "   - Cultural integration and company values communication\n"
            research += "   - Role-specific training and knowledge transfer\n\n"
            research += "2. Potential approaches:\n"
            research += "   - Approach A: Digital-first onboarding with minimal in-person components\n"
            research += "   - Approach B: High-touch mentorship model with extensive shadowing\n"
            research += "   - Approach C: Hybrid approach with digital tools and structured in-person activities"
        else:
            research = f"Additional research on '{task}':\n\n"
            research += "3. Detailed analysis of approaches:\n"
            research += "   - Digital-first strengths: Scalability, consistency, self-paced learning\n"
            research += "   - Mentorship strengths: Better cultural integration, personalized experience\n"
            research += "   - Hybrid strengths: Balance of efficiency and personalization\n\n"
            research += "4. Industry benchmarks:\n"
            research += "   - Companies with similar hybrid systems report 65% faster time-to-productivity\n"
            research += "   - Retention rates improve 40% with structured mentorship components\n\n"
            research += "5. Recommended approach: Hybrid system with digital core and structured mentorship"
    else:
        # Generic research for other tasks
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
            research = f"Additional research on '{task}':\n\n"
            research += "3. Detailed analysis of approaches:\n"
            research += "   - Approach A strengths: faster implementation, lower cost\n"
            research += "   - Approach B strengths: more complete solution, better long-term results\n"
            research += "   - Approach C strengths: balances time constraints with solution quality\n\n"
            research += "4. Related case studies:\n"
            research += "   - Case Study X demonstrated a 40% improvement using a hybrid approach\n"
            research += "   - Case Study Y showed technical challenges with rapid implementation\n\n"
            research += "5. Recommended approach based on research: Approach C (Hybrid solution)"
    
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
    task = state.get("task", "")
    
    # Get the latest request from the coordinator
    request = next((msg["content"] for msg in reversed(messages) 
                   if msg["to_agent"] == AgentRole.CRITIC 
                   and msg["msg_type"] == "request"), "")
    
    print(f"\n🔍 Critic: Working on iteration {current_iteration}")
    print(f"  Request: {request[:50]}..." if len(request) > 50 else f"  Request: {request}")
    
    # In a real implementation, would use an LLM here to generate critique
    # For demonstration, we'll use templates based on the task
    if "onboarding" in task.lower():
        critique = "Critique of the onboarding research:\n\n"
        critique += "Strengths:\n"
        critique += "- Comprehensive consideration of multiple onboarding dimensions\n"
        critique += "- Evidence-based comparison of different approaches\n"
        critique += "- Clear recommendations with supporting data\n\n"
        
        critique += "Weaknesses:\n"
        critique += "- Insufficient attention to department-specific needs\n"
        critique += "- Limited discussion of cost implications and ROI\n"
        critique += "- No consideration of remote vs. in-office employee differences\n\n"
        
        critique += "Suggestions for improvement:\n"
        critique += "1. Develop department-specific onboarding modules within the hybrid framework\n"
        critique += "2. Add cost analysis for each approach with expected ROI calculations\n"
        critique += "3. Include specific adaptations for remote employees\n"
        critique += "4. Consider phased implementation timeline with clear milestones\n\n"
        
        critique += "Recommended focus: Develop a customizable hybrid system with clear ROI metrics and remote employee considerations."
    else:
        # Generic critique for other tasks
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
    print(f"  Request: {request[:50]}..." if len(request) > 50 else f"  Request: {request}")
    
    # In a real implementation, would use an LLM here to generate solution
    # For demonstration, we'll use templates based on the task
    if "onboarding" in task.lower():
        solution = f"Implementation plan for employee onboarding system:\n\n"
        
        solution += "Phase 1: Digital Foundation (Weeks 1-4)\n"
        solution += "- Action 1.1: Select and customize digital onboarding platform\n"
        solution += "- Action 1.2: Develop core modules (company overview, policies, benefits)\n"
        solution += "- Action 1.3: Create department-specific content templates\n"
        solution += "- Action 1.4: Set up automated workflows for paperwork and IT provisioning\n"
        solution += "- Milestone: Digital platform ready for initial testing\n\n"
        
        solution += "Phase 2: Mentorship Structure (Weeks 5-8)\n"
        solution += "- Action 2.1: Develop mentor selection criteria and training\n"
        solution += "- Action 2.2: Create structured shadowing schedules by department\n"
        solution += "- Action 2.3: Build check-in templates and milestone tracking\n"
        solution += "- Action 2.4: Implement feedback mechanisms for continuous improvement\n"
        solution += "- Milestone: Mentorship program documented and ready for launch\n\n"
        
        solution += "Phase 3: Integration and Rollout (Weeks 9-12)\n"
        solution += "- Action 3.1: Integrate digital platform with mentorship program\n"
        solution += "- Action 3.2: Pilot with 5 new hires across departments\n"
        solution += "- Action 3.3: Refine based on feedback\n"
        solution += "- Action 3.4: Full deployment with ongoing monitoring\n"
        solution += "- Milestone: Complete system deployed company-wide\n\n"
        
        solution += "Special Adaptations for Remote Employees:\n"
        solution += "- Virtual office tours and team introductions\n"
        solution += "- Scheduled video check-ins to replace in-person shadowing\n"
        solution += "- Digital collaboration tools training\n\n"
        
        solution += "Cost and ROI:\n"
        solution += "- Implementation cost: $X for platform, $Y for staff time\n"
        solution += "- Expected ROI: 35% reduction in time-to-productivity, 25% improvement in 90-day retention"
    else:
        # Generic solution for other tasks
        solution = f"Implementation plan for '{task}':\n\n"
        
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
        solution += "- Risk 3: Timeline pressure → Buffer periods built into schedule"
    
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
    task = state.get("task", "")
    
    # Get the solution to evaluate
    solution = state.get("solution", "")
    if not solution:
        # If we don't have a final solution, look for the latest execution result
        solution = next((msg["content"] for msg in reversed(messages) 
                       if msg["from_agent"] == AgentRole.EXECUTOR 
                       and msg["msg_type"] == "response"), "")
    
    print(f"\n⭐ Evaluator: Working on iteration {current_iteration}")
    
    # In a real implementation, would use an LLM here to generate evaluation
    # For demonstration, we'll use templates based on the task
    
    # Generate evaluation metrics
    if "onboarding" in task.lower():
        evaluation = {
            "comprehensiveness": 0.88,
            "feasibility": 0.82,
            "clarity": 0.90,
            "cost_effectiveness": 0.75,
            "adaptability": 0.85,
            "overall_quality": 0.84
        }
    else:
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
    
    if "onboarding" in task.lower():
        evaluation_text += "Strengths:\n"
        evaluation_text += "- Comprehensive phased approach with clear milestones\n"
        evaluation_text += "- Good balance of digital and human elements\n"
        evaluation_text += "- Specific adaptations for remote employees\n"
        evaluation_text += "- Clear ROI metrics identified\n\n"
        
        evaluation_text += "Areas for improvement:\n"
        evaluation_text += "- Consider adding cross-departmental collaboration opportunities\n"
        evaluation_text += "- More detail needed on mentor selection and training\n"
        evaluation_text += "- Consider long-term maintenance of the system\n\n"
    else:
        evaluation_text += "Strengths:\n"
        evaluation_text += "- Well-structured phased approach\n"
        evaluation_text += "- Clear milestones and deliverables\n"
        evaluation_text += "- Good consideration of risks\n\n"
        
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
    
    # Set convergence score based on current phase
    # If we're in the final evaluation, mark as complete
    convergence_score = 1.0 if state.get("current_phase") == "final_evaluation" else 0.5
    
    # Update state
    state["messages"] = messages
    state["evaluation"] = evaluation
    state["convergence_score"] = convergence_score
    state["current_agent"] = AgentRole.COORDINATOR
    
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
    if state.get("current_iteration", 0) >= state.get("max_iterations", 5):
        return True
        
    return False


# ---------------------------------------------------------------------------
# Graph Building -----------------------------------------------------------
# ---------------------------------------------------------------------------

def build_multi_agent_graph() -> StateGraph:
    """Build the multi-agent collaboration graph using LangGraph."""
    g = StateGraph(MultiAgentState)
    
    # Add all agent nodes
    g.add_node(AgentRole.COORDINATOR, coordinator_agent)
    g.add_node(AgentRole.RESEARCHER, researcher_agent)
    g.add_node(AgentRole.CRITIC, critic_agent)
    g.add_node(AgentRole.EXECUTOR, executor_agent)
    g.add_node(AgentRole.EVALUATOR, evaluator_agent)
    
    # Connect via dynamic routing
    g.add_conditional_edges(
        AgentRole.COORDINATOR,
        router,
        {
            AgentRole.RESEARCHER: AgentRole.RESEARCHER,
            AgentRole.CRITIC: AgentRole.CRITIC,
            AgentRole.EXECUTOR: AgentRole.EXECUTOR,
            AgentRole.EVALUATOR: AgentRole.EVALUATOR,
        }
    )
    
    # All other agents return to coordinator
    for role in [AgentRole.RESEARCHER, AgentRole.CRITIC, 
                AgentRole.EXECUTOR, AgentRole.EVALUATOR]:
        g.add_edge(role, AgentRole.COORDINATOR)
    
    # Set entry and terminal state
    g.set_entry_point(AgentRole.COORDINATOR)
    g.add_edge(AgentRole.COORDINATOR, "end", decide_if_finished)
    
    return g


# ---------------------------------------------------------------------------
# Util Functions -----------------------------------------------------------
# ---------------------------------------------------------------------------

def print_message_thread(messages: List[AgentMessage]) -> None:
    """Print the message thread in a readable format."""
    print("\n" + "="*80)
    print("MESSAGE THREAD")
    print("="*80)
    
    for i, msg in enumerate(messages):
        from_agent = msg["from_agent"]
        to_agent = msg["to_agent"] if msg["to_agent"] else "ALL"
        iteration = msg["iteration"]
        
        print(f"\n[{i+1}] Iteration {iteration}: {from_agent} → {to_agent}")
        print(f"Type: {msg['msg_type']}")
        if len(msg["content"]) > 200:
            print(f"Content: {msg['content'][:200]}...(truncated)")
        else:
            print(f"Content: {msg['content']}")
    
    print("\n" + "="*80)


def print_solution_summary(state: MultiAgentState) -> None:
    """Print a summary of the solution and evaluation."""
    solution = state.get("solution", "No solution generated.")
    evaluation = state.get("evaluation", {})
    
    print("\n" + "="*80)
    print("SOLUTION SUMMARY")
    print("="*80)
    
    print("\nSOLUTION:")
    print("-"*40)
    print(solution)
    
    if evaluation:
        print("\nEVALUATION:")
        print("-"*40)
        for metric, score in evaluation.items():
            print(f"- {metric.replace('_', ' ').title()}: {score:.2f}/1.00")
        
        overall = evaluation.get("overall_quality", 0)
        print(f"\nOverall Quality: {overall * 100:.1f}%")
    
    print("\n" + "="*80)


def run_multi_agent_system(task: str, max_iterations: int = 5, verbose: bool = False) -> MultiAgentState:
    """Run the multi-agent system on a given task."""
    # Initialize state
    state = MultiAgentState(
        task=task,
        messages=[],
        artifacts={},
        current_agent=AgentRole.COORDINATOR,
        current_iteration=0,
        max_iterations=max_iterations
    )
    
    # Build graph
    graph = build_multi_agent_graph()
    
    # In a real implementation with LangGraph, we would run:
    # final_state = graph.invoke(state)
    
    # For this demonstration, we'll manually step through the graph
    current_state = state
    
    while not decide_if_finished(current_state):
        current_agent = router(current_state)
        
        if current_agent == AgentRole.COORDINATOR:
            current_state = coordinator_agent(current_state)
        elif current_agent == AgentRole.RESEARCHER:
            current_state = researcher_agent(current_state)
        elif current_agent == AgentRole.CRITIC:
            current_state = critic_agent(current_state)
        elif current_agent == AgentRole.EXECUTOR:
            current_state = executor_agent(current_state)
        elif current_agent == AgentRole.EVALUATOR:
            current_state = evaluator_agent(current_state)
    
    # Print results
    if verbose:
        print_message_thread(current_state.get("messages", []))
    
    print_solution_summary(current_state)
    
    return current_state


# ---------------------------------------------------------------------------
# Main Function ------------------------------------------------------------
# ---------------------------------------------------------------------------

def main():
    """Main function to run the multi-agent system."""
    parser = argparse.ArgumentParser(description="Advanced Multi-Agent Collaboration System")
    parser.add_argument("--task", type=str, default="Design a new employee onboarding system",
                        help="The task to solve")
    parser.add_argument("--iterations", type=int, default=5,
                        help="Maximum number of iterations")
    parser.add_argument("--verbose", action="store_true",
                        help="Print detailed message thread")
    
    args = parser.parse_args()
    
    print("\n" + "="*80)
    print("ADVANCED MULTI-AGENT COLLABORATION SYSTEM")
    print("="*80)
    print(f"\nTask: {args.task}")
    print(f"Max Iterations: {args.iterations}")
    print("\nSystem includes:")
    print("- Coordinator Agent: Manages the collaboration process")
    print("- Researcher Agent: Gathers and synthesizes information")
    print("- Critic Agent: Identifies weaknesses and suggests improvements")
    print("- Executor Agent: Implements solutions with concrete steps")
    print("- Evaluator Agent: Assesses solution quality objectively")
    
    # Run the system
    final_state = run_multi_agent_system(args.task, args.iterations, args.verbose)
    
    print("\nCollaboration complete!")


if __name__ == "__main__":
    main() 