#!/usr/bin/env python3
"""
Chapter 3 – Advanced Example: Utility-Driven Decision with LangGraph
-------------------------------------------------------------------
Highlights
• Branch scoring using the utility function
• Parallel evaluation of travel options
• Aggregation node picks highest-utility outcome

Run:
    python decision_langgraph.py
Requires:
    pip install -U langgraph typing_extensions
"""
from __future__ import annotations

import json
from typing import Dict, List, TypedDict
from langgraph.graph import StateGraph

# ---------------------------------------------------------------------------
# Re-use utility from original example --------------------------------------
# ---------------------------------------------------------------------------

def travel_utility_function(travel_option):
    price_utility = (1000 - travel_option["price"]) * 0.05
    comfort_utility = travel_option["comfort_rating"] * 10
    convenience_utility = travel_option["convenience_score"] * 15
    return price_utility + comfort_utility + convenience_utility

TRAVEL_OPTIONS = [
    {"name": "Budget Airline", "price": 300, "comfort_rating": 3, "convenience_score": 2},
    {"name": "Premium Airline", "price": 800, "comfort_rating": 8, "convenience_score": 7},
    {"name": "Train", "price": 200, "comfort_rating": 6, "convenience_score": 5},
    {"name": "Road Trip", "price": 150, "comfort_rating": 4, "convenience_score": 3},
]

# ---------------------------------------------------------------------------
# State definition -----------------------------------------------------------
# ---------------------------------------------------------------------------
class OptionState(TypedDict, total=False):
    option: Dict
    score: float

class DecisionState(TypedDict, total=False):
    evaluated: List[OptionState]
    best_option: Dict

# ---------------------------------------------------------------------------
# Graph nodes ----------------------------------------------------------------
# ---------------------------------------------------------------------------

def evaluate_option(state: DecisionState, option: Dict) -> DecisionState:
    score = travel_utility_function(option)
    if "evaluated" not in state:
        state["evaluated"] = []  # type: ignore
    state["evaluated"].append({"option": option, "score": score})  # type: ignore
    return state


def aggregate(state: DecisionState) -> DecisionState:
    best = max(state["evaluated"], key=lambda x: x["score"])["option"]  # type: ignore
    state["best_option"] = best  # type: ignore
    return state

# ---------------------------------------------------------------------------
# Build graph ----------------------------------------------------------------
# ---------------------------------------------------------------------------

def build_decision_graph() -> StateGraph:
    g = StateGraph(DecisionState)

    # One node per option (could be executed in parallel by executor) ----
    previous = "start"
    g.set_entry_point(previous)
    g.add_node(previous, lambda s: s)  # no-op seed

    for idx, opt in enumerate(TRAVEL_OPTIONS):
        node_name = f"eval_{idx}"
        g.add_node(node_name, lambda s, o=opt: evaluate_option(s, o))
        g.add_edge(previous, node_name)
        previous = node_name

    # Aggregation -----------------------------------------------------------
    g.add_node("aggregate", aggregate)
    g.add_edge(previous, "aggregate")
    g.set_finish_point("aggregate")
    return g

# ---------------------------------------------------------------------------
# CLI ------------------------------------------------------------------------
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    graph = build_decision_graph().compile()
    final_state = graph.invoke({})
    print("\n--- Decision Result ---")
    print(json.dumps(final_state, indent=2)) 