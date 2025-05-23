# Lab 9: Safety Guardrails

⏱️ **Estimated completion time: 40 minutes**

## Overview

This lab demonstrates implementing safety guardrails and content filtering in agentic systems, including input validation, output filtering, and safety checkpoints.

## Learning Objectives

- Implementing input/output safety filters
- Creating safety checkpoints in workflows
- Handling policy violations gracefully

## Key Concepts

### Safety Guardrails
1. **Input Validation**: Screen user inputs for harmful content
2. **Output Filtering**: Ensure agent responses meet safety standards
3. **Workflow Checkpoints**: Safety gates at critical decision points

## Lab Code

```python
#!/usr/bin/env python3
"""
Safety Guardrails Demo
Implement content filtering and safety checkpoints in agent workflows.
"""
import re
from typing import Dict, List, TypedDict
from langgraph.graph import StateGraph

class SafetyState(TypedDict, total=False):
    user_input: str
    input_safe: bool
    agent_response: str
    output_safe: bool
    safety_violations: List[str]
    final_response: str

# Safety filters
BLOCKED_PATTERNS = [
    r'\b(hack|exploit|attack)\b',
    r'\b(illegal|harmful|dangerous)\b',
    r'\b(personal|private|confidential)\s+information\b'
]

SENSITIVE_TOPICS = ['violence', 'illegal activities', 'personal data']

def input_safety_filter(state: SafetyState) -> SafetyState:
    """Check if user input contains harmful content."""
    user_input = state["user_input"].lower()
    violations = []
    
    # Check against blocked patterns
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, user_input):
            violations.append(f"Blocked pattern detected: {pattern}")
    
    # Check for sensitive topics
    for topic in SENSITIVE_TOPICS:
        if topic in user_input:
            violations.append(f"Sensitive topic: {topic}")
    
    state["input_safe"] = len(violations) == 0
    state["safety_violations"] = violations
    
    print(f"Input safety check: {'PASS' if state['input_safe'] else 'FAIL'}")
    if violations:
        print(f"Violations: {violations}")
    
    return state

def process_request(state: SafetyState) -> SafetyState:
    """Process the user request if input is safe."""
    if not state["input_safe"]:
        state["agent_response"] = "I cannot process this request due to safety concerns."
        return state
    
    # Mock agent processing
    query = state["user_input"]
    if "weather" in query.lower():
        response = "The weather is sunny with a temperature of 22°C."
    elif "help" in query.lower():
        response = "I'm here to help! What would you like to know?"
    else:
        response = f"I understand you're asking about: {query}"
    
    state["agent_response"] = response
    return state

def output_safety_filter(state: SafetyState) -> SafetyState:
    """Check if agent response is safe to return."""
    response = state["agent_response"].lower()
    violations = []
    
    # Check for inappropriate content in response
    inappropriate_terms = ['inappropriate', 'harmful', 'dangerous']
    for term in inappropriate_terms:
        if term in response:
            violations.append(f"Inappropriate content: {term}")
    
    state["output_safe"] = len(violations) == 0
    
    print(f"Output safety check: {'PASS' if state['output_safe'] else 'FAIL'}")
    if violations:
        print(f"Output violations: {violations}")
    
    return state

def finalize_response(state: SafetyState) -> SafetyState:
    """Finalize the response based on safety checks."""
    if state["input_safe"] and state["output_safe"]:
        state["final_response"] = state["agent_response"]
    else:
        state["final_response"] = "I apologize, but I cannot provide a response to this request due to safety guidelines."
    
    return state

def build_safety_graph() -> StateGraph:
    """Build graph with safety checkpoints."""
    graph = StateGraph(SafetyState)
    
    # Add safety nodes
    graph.add_node("input_filter", input_safety_filter)
    graph.add_node("process", process_request)
    graph.add_node("output_filter", output_safety_filter)
    graph.add_node("finalize", finalize_response)
    
    # Connect nodes
    graph.set_entry_point("input_filter")
    graph.add_edge("input_filter", "process")
    graph.add_edge("process", "output_filter")
    graph.add_edge("output_filter", "finalize")
    graph.set_finish_point("finalize")
    
    return graph

def main():
    print("=== Safety Guardrails Demo ===")
    
    graph = build_safety_graph().compile()
    
    # Test cases
    test_inputs = [
        "What's the weather like today?",
        "How can I hack into a system?",
        "Tell me about illegal activities",
        "Can you help me with my homework?"
    ]
    
    for user_input in test_inputs:
        print(f"\n--- Testing: '{user_input}' ---")
        
        state = {"user_input": user_input}
        result = graph.invoke(state)
        
        print(f"Final response: {result['final_response']}")

if __name__ == "__main__":
    main()
```

## How to Run

1. Save as `09_guardrails.py`
2. Install: `pip install langgraph`
3. Run: `python 09_guardrails.py`

## Key Features

- **Multi-layered filtering**: Input and output safety checks
- **Pattern matching**: Regex-based content detection
- **Graceful degradation**: Safe fallback responses
- **Audit trail**: Tracking of safety violations

## Download Code

[Download 09_guardrails.py](09_guardrails.py){ .md-button .md-button--primary } 