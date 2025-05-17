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