#!/usr/bin/env python3
"""
Chapter 3 - Parallel Utility Scoring with LangGraph
--------------------------------------------------
This example demonstrates how to implement parallel utility-based decision making
using LangGraph. It evaluates multiple travel options in parallel and picks the
one with the highest utility score.

Key concepts:
- Parallel branch evaluation for multiple options
- Utility function implementation
- Aggregation of results with max utility selection
- Comparison with LCEL implementation
"""
import json
from typing import Dict, List, TypedDict
from langgraph.graph import StateGraph

# ---------------------------------------------------------------------------
# Travel options and utility function ---------------------------------------
# ---------------------------------------------------------------------------

def travel_utility_function(travel_option):
    """Calculate utility based on price, comfort, and convenience."""
    price_utility = (1000 - travel_option["price"]) * 0.05  # Lower price = higher utility
    comfort_utility = travel_option["comfort_rating"] * 10   # Higher comfort = higher utility
    convenience_utility = travel_option["convenience_score"] * 15  # Higher convenience = higher utility
    
    # Total utility is the sum of all factors
    total_utility = price_utility + comfort_utility + convenience_utility
    
    print(f"Option: {travel_option['name']}")
    print(f"  Price utility: {price_utility:.2f}")
    print(f"  Comfort utility: {comfort_utility:.2f}")
    print(f"  Convenience utility: {convenience_utility:.2f}")
    print(f"  Total utility: {total_utility:.2f}")
    
    return total_utility

# Sample travel options for evaluation
TRAVEL_OPTIONS = [
    {"name": "Budget Airline", "price": 300, "comfort_rating": 3, "convenience_score": 2},
    {"name": "Premium Airline", "price": 800, "comfort_rating": 8, "convenience_score": 7},
    {"name": "Train", "price": 200, "comfort_rating": 6, "convenience_score": 5},
    {"name": "Road Trip", "price": 150, "comfort_rating": 4, "convenience_score": 3},
]

# ---------------------------------------------------------------------------
# State definitions ---------------------------------------------------------
# ---------------------------------------------------------------------------
class OptionState(TypedDict, total=False):
    option: Dict
    score: float

class DecisionState(TypedDict, total=False):
    evaluated: List[OptionState]
    best_option: Dict

# ---------------------------------------------------------------------------
# Graph nodes ---------------------------------------------------------------
# ---------------------------------------------------------------------------

def evaluate_option(state: DecisionState, option: Dict) -> DecisionState:
    """Calculate utility score for a single option and store in state."""
    score = travel_utility_function(option)
    
    # Initialize evaluated list if it doesn't exist
    if "evaluated" not in state:
        state["evaluated"] = []  # type: ignore
    
    # Add this option and its score to evaluated options
    state["evaluated"].append({"option": option, "score": score})  # type: ignore
    return state

def aggregate(state: DecisionState) -> DecisionState:
    """Find the option with the highest utility score."""
    if not state.get("evaluated"):
        raise ValueError("No options have been evaluated")
    
    # Find option with maximum score
    best = max(state["evaluated"], key=lambda x: x["score"])["option"]  # type: ignore
    state["best_option"] = best  # type: ignore
    return state

# ---------------------------------------------------------------------------
# Graph construction --------------------------------------------------------
# ---------------------------------------------------------------------------

def build_decision_graph() -> StateGraph:
    """Build a graph that evaluates options in parallel and selects the best."""
    # Create the graph with our state type
    g = StateGraph(DecisionState)

    # Add a starting node
    g.add_node("start", lambda s: s)  # no-op seed node
    g.set_entry_point("start")
    
    # Track the last node we added for chaining
    previous = "start"
    
    # Add an evaluation node for each travel option
    # In a real parallel executor, these would run concurrently
    for idx, opt in enumerate(TRAVEL_OPTIONS):
        node_name = f"eval_{idx}"
        
        # Create a node that evaluates this specific option
        # We use a default argument to capture the current option value
        g.add_node(node_name, lambda s, o=opt: evaluate_option(s, o))
        
        # Connect the previous node to this one
        g.add_edge(previous, node_name)
        
        # Update previous to continue the chain
        previous = node_name

    # Add the aggregation node to pick the best option
    g.add_node("aggregate", aggregate)
    g.add_edge(previous, "aggregate")
    
    # Set the finish point
    g.set_finish_point("aggregate")
    
    return g

# ---------------------------------------------------------------------------
# Run the demo --------------------------------------------------------------
# ---------------------------------------------------------------------------

def main():
    print("\n=== Utility-Based Decision Making with LangGraph ===\n")
    
    # Build and compile the graph
    graph = build_decision_graph().compile()
    
    # Run the graph with empty initial state
    print("\nEvaluating travel options...\n")
    final_state = graph.invoke({})
    
    # Display results
    print("\n--- Decision Results ---")
    print(f"Best option: {final_state['best_option']['name']}")
    print(f"Price: ${final_state['best_option']['price']}")
    print(f"Comfort rating: {final_state['best_option']['comfort_rating']}/10")
    print(f"Convenience score: {final_state['best_option']['convenience_score']}/10")
    
    # Show all evaluated options sorted by score
    print("\nAll options by score:")
    sorted_options = sorted(
        final_state["evaluated"], 
        key=lambda x: x["score"], 
        reverse=True
    )
    
    for idx, item in enumerate(sorted_options):
        option = item["option"]
        score = item["score"]
        print(f"{idx+1}. {option['name']} - Utility: {score:.2f}")

if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------
# LCEL Alternative (not executed) -------------------------------------------
# ---------------------------------------------------------------------------
"""
# This is how you would implement the same logic using LangChain Expression Language

from langchain.schema.runnable import RunnablePassthrough, RunnableMap

# Create a scoring chain
score_option = (
    RunnablePassthrough.assign(
        score=lambda x: travel_utility_function(x["option"])
    )
)

# Create parallel scoring with map
parallel_scoring = (
    RunnableMap({
        "options": lambda _: TRAVEL_OPTIONS
    })
    .assign(
        scored_options=lambda x: [
            score_option.invoke({"option": opt}) 
            for opt in x["options"]
        ]
    )
    .assign(
        best_option=lambda x: max(x["scored_options"], key=lambda o: o["score"])["option"]
    )
)

# Use the chain
result = parallel_scoring.invoke({})
print(f"Best option: {result['best_option']['name']}")
""" 