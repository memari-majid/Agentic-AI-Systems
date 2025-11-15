# Lab 1: Hello Graph - LangGraph Basics

⏱️ **Estimated completion time: 15 minutes**

## Overview

This lab provides a minimalist introduction to LangGraph, showing how to create a simple stateful graph with just a few lines of code. You'll learn the fundamental concepts of:

- Creating a state graph
- Defining node functions
- Adding conditional edges
- Running graph execution

## Learning Objectives

By the end of this lab, you will understand:
- How to create a basic LangGraph with state management
- The concept of nodes and edges in graph-based agents
- How to implement conditional logic in graph flows
- How to execute and monitor graph execution

## Prerequisites

- Python 3.8+
- LangGraph installed (`pip install langgraph`)

## Lab Code

```python
#!/usr/bin/env python3
"""
Hello LangGraph - Simple State Graph Example
--------------------------------------------
This file provides a minimalist introduction to LangGraph, showing 
how to create a simple stateful graph with just a few lines of code.
"""
from langgraph.graph import StateGraph

def main():
    # 1. Create a graph that works with a simple dictionary state
    graph = StateGraph(dict)

    # 2. Define a node function that increments a counter
    def increment(state):
        state["count"] = state.get("count", 0) + 1
        state["message"] = f"Hello Graph! Count: {state['count']}"
        return state

    # 3. Add the node to the graph
    graph.add_node("increment", increment)

    # 4. Add a self-loop to run the increment node multiple times
    graph.add_conditional_edges(
        "increment",
        lambda state: "increment" if state.get("count", 0) < 3 else "end",
        {"increment": "increment", "end": None}
    )

    # 5. Set the entry point
    graph.set_entry_point("increment")

    # 6. Compile and run
    runnable = graph.compile()
    
    print("\n--- Running the graph ---")
    result = runnable.invoke({})
    print(f"Final state: {result}")
    
    print("\n--- Step-by-step execution ---")
    steps = []
    for step in runnable.stream({}):
        steps.append(step)
        print(f"Step {len(steps)}: {step}")
    
    print("\n--- Understanding the Example ---")
    print("This simple example demonstrates core LangGraph concepts:")
    print("1. State: A simple dictionary that holds our counter value")
    print("2. Nodes: Functions that transform the state (our increment function)")
    print("3. Edges: Define flow between nodes (our self-loop)")
    print("4. Conditional Logic: Decisions about which path to take (continue or stop)")
    
if __name__ == "__main__":
    main()
```

## How to Run

1. Save the code above as `01_hello_graph.py`
2. Install dependencies: `pip install langgraph`
3. Run the script: `python 01_hello_graph.py`

## Expected Output

```
--- Running the graph ---
Final state: {'count': 3, 'message': 'Hello Graph! Count: 3'}

--- Step-by-step execution ---
Step 1: {'increment': {'count': 1, 'message': 'Hello Graph! Count: 1'}}
Step 2: {'increment': {'count': 2, 'message': 'Hello Graph! Count: 2'}}
Step 3: {'increment': {'count': 3, 'message': 'Hello Graph! Count: 3'}}

--- Understanding the Example ---
This simple example demonstrates core LangGraph concepts:
1. State: A simple dictionary that holds our counter value
2. Nodes: Functions that transform the state (our increment function)
3. Edges: Define flow between nodes (our self-loop)
4. Conditional Logic: Decisions about which path to take (continue or stop)
```

## Key Concepts Explained

### State Management
- LangGraph uses a state object that flows through the graph
- Each node can read and modify the state
- State persists across node executions

### Nodes
- Nodes are functions that transform the state
- They receive the current state and return the updated state
- Nodes represent discrete steps in your agent's logic

### Conditional Edges
- Allow dynamic routing based on state conditions
- Enable loops, branching, and complex control flow
- Make agents adaptive and responsive to changing conditions

## Next Steps

- Try modifying the increment function to do different operations
- Experiment with different conditional logic
- Add more nodes to create a more complex graph

## Download Code

[Download 01_hello_graph.py](01_hello_graph.py){ .md-button .md-button--primary } 