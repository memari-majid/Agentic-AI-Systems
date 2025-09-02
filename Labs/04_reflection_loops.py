#!/usr/bin/env python3
"""
Chapter 4 - Self-Critique Loop with LangGraph
--------------------------------------------
This example demonstrates how to implement a reflection and self-critique
loop using LangGraph. It shows a travel recommendation system that:
1. Proposes a destination based on user preferences
2. Reflects on how well the proposal matches the preferences
3. Revises if the match quality is below a threshold (up to 3 attempts)

Key concepts:
- Conditional branching with LangGraph
- Self-critique and revision cycles
- Explicit state management with TypedDict
- Using iteration limits to prevent endless loops
"""
import argparse
import json
import random
from typing import Dict, List, TypedDict, Optional
from langgraph.graph import StateGraph

# ---------------------------------------------------------------------------
# Destinations and preference matching --------------------------------------
# ---------------------------------------------------------------------------

# Sample destinations with attribute scores (0-1 scale)
DESTINATIONS = {
    "Paris": {"luxury": 0.9, "adventure": 0.2, "budget": 0.3},
    "Bangkok": {"luxury": 0.4, "adventure": 0.7, "budget": 0.9},
    "New York": {"luxury": 0.8, "adventure": 0.4, "budget": 0.5},
    "Reykjavik": {"luxury": 0.6, "adventure": 0.9, "budget": 0.2},
    "Bali": {"luxury": 0.7, "adventure": 0.8, "budget": 0.6},
    "Tokyo": {"luxury": 0.8, "adventure": 0.6, "budget": 0.4},
    "Morocco": {"luxury": 0.5, "adventure": 0.9, "budget": 0.7},
    "Swiss Alps": {"luxury": 0.9, "adventure": 0.8, "budget": 0.1}
}

def weighted_match(prefs: Dict[str, float], dest_weights: Dict[str, float]) -> float:
    """Calculate similarity between preferences and destination attributes."""
    # Calculate weighted score (sum of preference × attribute)
    score = 0.0
    total_weight = 0.0
    
    for k, pref_value in prefs.items():
        if k in dest_weights:
            score += pref_value * dest_weights[k]
            total_weight += pref_value
    
    # Normalize by total preference weight to get 0-1 score
    return score / max(1e-6, total_weight)

# ---------------------------------------------------------------------------
# State definition ----------------------------------------------------------
# ---------------------------------------------------------------------------
class ReflectState(TypedDict, total=False):
    user_preferences: Dict[str, float]  # {budget, luxury, adventure}
    proposal: str                       # destination proposed
    score: float                        # reflection score 0-1
    iteration: int                      # count of attempts
    history: List[str]                  # log of proposals and scores
    rejected: List[str]                 # previously rejected proposals

# ---------------------------------------------------------------------------
# Graph nodes ---------------------------------------------------------------
# ---------------------------------------------------------------------------

def propose_destination(state: ReflectState) -> ReflectState:
    """Propose a destination based on user preferences."""
    # Get user preferences from state
    prefs = state["user_preferences"]
    
    # Increment iteration counter
    if "iteration" not in state:
        state["iteration"] = 0  # type: ignore
    else:
        state["iteration"] += 1  # type: ignore
    
    # Get list of previously rejected destinations
    rejected = state.get("rejected", [])
    
    # Score all destinations by preference match
    candidates = {}
    for dest, attrs in DESTINATIONS.items():
        # Skip rejected destinations
        if dest in rejected:
            continue
        candidates[dest] = weighted_match(prefs, attrs)
    
    # Handle case where all destinations have been rejected
    if not candidates:
        print("All destinations have been rejected, resetting")
        candidates = {d: weighted_match(prefs, a) for d, a in DESTINATIONS.items()}
    
    # Choose destination with highest match score
    proposal = max(candidates, key=candidates.get)
    state["proposal"] = proposal  # type: ignore
    
    print(f"Iteration {state['iteration']}: Proposing {proposal}")
    return state


def reflect_on_proposal(state: ReflectState) -> ReflectState:
    """Evaluate how well the proposal matches user preferences."""
    # Get necessary values from state
    prefs = state["user_preferences"]
    proposal = state["proposal"]
    
    # Calculate match score
    score = weighted_match(prefs, DESTINATIONS[proposal])
    
    # Add small random factor to simulate human judgment variability
    noise = random.uniform(-0.05, 0.05)
    score = max(0, min(1, score + noise))
    
    # Update state with score
    state["score"] = score  # type: ignore
    
    # Record this proposal in history
    msg = f"Iter {state['iteration']}: proposed {proposal} (score={score:.2f})"
    
    if "history" not in state:
        state["history"] = []  # type: ignore
    state["history"].append(msg)  # type: ignore
    
    print(f"Reflection score: {score:.2f}")
    return state


def revise_proposal(state: ReflectState) -> ReflectState:
    """Mark current proposal as rejected and prepare for a new proposal."""
    # Get the proposal that didn't meet the threshold
    rejected = state["proposal"]
    
    # Initialize or update rejected list
    if "rejected" not in state:
        state["rejected"] = []  # type: ignore
    state["rejected"].append(rejected)  # type: ignore
    
    print(f"Rejecting {rejected} due to low match score")
    return state

# ---------------------------------------------------------------------------
# Conditional edge function ------------------------------------------------
# ---------------------------------------------------------------------------

def need_revision(state: ReflectState) -> str:
    """Determine whether to revise or finish based on score and iteration count."""
    # Get the quality threshold (can be adjusted as a parameter)
    quality_threshold = 0.7
    max_iterations = 3
    
    # Check if score is too low and we haven't exceeded iteration limit
    if state["score"] < quality_threshold and state["iteration"] < max_iterations:
        return "revise"
    return "finish"

# ---------------------------------------------------------------------------
# Graph construction --------------------------------------------------------
# ---------------------------------------------------------------------------

def build_reflection_graph(threshold: Optional[float] = None) -> StateGraph:
    """Build a graph with propose-reflect-revise loop."""
    g = StateGraph(ReflectState)
    
    # Add nodes for each step in the reflection loop
    g.add_node("propose", propose_destination)
    g.add_node("reflect", reflect_on_proposal)
    g.add_node("revise", revise_proposal)
    
    # Connect nodes: propose leads to reflect
    g.set_entry_point("propose")
    g.add_edge("propose", "reflect")
    
    # After reflection, conditionally go to revise or finish
    g.add_conditional_edges(
        "reflect", 
        need_revision, 
        {"revise": "propose", "finish": None}
    )
    
    # Connect revise back to propose to loop
    g.add_edge("revise", "propose")
    
    return g

# ---------------------------------------------------------------------------
# Main function -------------------------------------------------------------
# ---------------------------------------------------------------------------

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Travel Recommendation with Self-Reflection")
    parser.add_argument("--budget", type=float, default=0.3, help="Budget importance (0-1)")
    parser.add_argument("--luxury", type=float, default=0.6, help="Luxury importance (0-1)")
    parser.add_argument("--adventure", type=float, default=0.8, help="Adventure importance (0-1)")
    parser.add_argument("--threshold", type=float, default=0.7, help="Quality threshold (0-1)")
    args = parser.parse_args()

    # Print header
    print("\n=== Travel Recommendation with Self-Reflection ===\n")
    print("User Preferences:")
    print(f"  Budget importance: {args.budget:.1f}")
    print(f"  Luxury importance: {args.luxury:.1f}")
    print(f"  Adventure importance: {args.adventure:.1f}")
    print(f"  Quality threshold: {args.threshold:.1f}")
    
    # Build and compile the graph
    graph = build_reflection_graph(args.threshold).compile()
    
    # Create initial state with user preferences
    initial_state: ReflectState = {
        "user_preferences": {
            "budget": args.budget,
            "luxury": args.luxury,
            "adventure": args.adventure
        },
        "iteration": 0
    }
    
    # Run the graph
    print("\nStarting recommendation process...\n")
    final_state = graph.invoke(initial_state)
    
    # Display recommendation history
    print("\n--- Recommendation History ---")
    for entry in final_state.get("history", []):
        print(entry)
    
    # Show final recommendation
    print("\n--- Final Recommendation ---")
    print(f"Destination: {final_state['proposal']}")
    print(f"Match score: {final_state['score']:.2f}")
    print(f"Iterations needed: {final_state['iteration']}")
    
    # Show destination attributes
    dest = final_state['proposal']
    attrs = DESTINATIONS[dest]
    print(f"\nDestination attributes for {dest}:")
    for attr, value in attrs.items():
        print(f"  {attr.title()}: {value:.1f}")

if __name__ == "__main__":
    main() 