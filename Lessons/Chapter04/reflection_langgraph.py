#!/usr/bin/env python3
"""
Chapter 4 – Reflection & Introspection with LangGraph
----------------------------------------------------
This example builds a two-pass reasoning loop:
    1. Propose a destination recommendation.
    2. Reflect on the proposal and produce a quality score.
    3. If the score is low, revise and re-evaluate (max 3 iterations).

It demonstrates:
• dynamic self-critique
• conditional looping in LangGraph
• explicit state typing

Run:
    python reflection_langgraph.py
Requires:
    pip install -U langgraph typing_extensions
"""
from __future__ import annotations

import json
import random
from typing import Dict, TypedDict, List
from langgraph.graph import StateGraph

# ------------------------------
# State definition
# ------------------------------
class ReflectState(TypedDict, total=False):
    user_preferences: Dict[str, float]  # {budget, luxury, adventure}
    proposal: str                       # destination proposed
    score: float                        # reflection score 0-1
    iteration: int
    history: List[str]

# ------------------------------
# Data / helpers
# ------------------------------
DESTINATIONS = {
    "Paris": {"luxury": 0.9, "adventure": 0.2, "budget": 0.3},
    "Bangkok": {"luxury": 0.4, "adventure": 0.7, "budget": 0.9},
    "New York": {"luxury": 0.8, "adventure": 0.4, "budget": 0.5},
    "Reykjavik": {"luxury": 0.6, "adventure": 0.9, "budget": 0.2},
}

def weighted_match(prefs: Dict[str, float], dest_weights: Dict[str, float]) -> float:
    """Cosine-like similarity (simplified)."""
    score = 0.0
    for k in prefs:
        score += prefs[k] * dest_weights[k]
    return score / max(1e-6, sum(prefs.values()))

# ------------------------------
# Graph nodes
# ------------------------------

def propose_destination(state: ReflectState) -> ReflectState:
    prefs = state["user_preferences"]
    scored = {d: weighted_match(prefs, w) for d, w in DESTINATIONS.items()}
    proposal = max(scored, key=scored.get)
    state["proposal"] = proposal  # type: ignore
    return state


def reflect_on_proposal(state: ReflectState) -> ReflectState:
    # Simulate reflection: high score if proposal aligns, else random lower
    prefs = state["user_preferences"]
    proposal = state["proposal"]
    base = weighted_match(prefs, DESTINATIONS[proposal])
    noise = random.uniform(-0.1, 0.1)
    score = max(0, min(1, base + noise))
    state["score"] = score  # type: ignore
    msg = f"Iter {state['iteration']}: proposed {proposal} (score={score:.2f})"
    state.setdefault("history", []).append(msg)  # type: ignore
    return state


def revise_proposal(state: ReflectState) -> ReflectState:
    """Very naive revision: remove current proposal and choose next best."""
    rejected = state["proposal"]
    prefs = state["user_preferences"]
    remaining = {d: w for d, w in DESTINATIONS.items() if d != rejected}
    new_prop = max(remaining, key=lambda d: weighted_match(prefs, remaining[d]))
    state["proposal"] = new_prop  # type: ignore
    return state

# ------------------------------
# Conditional edge function
# ------------------------------

def need_revision(state: ReflectState) -> str:
    if state["score"] < 0.7 and state["iteration"] < 3:
        return "revise"
    return "finish"

# ------------------------------
# Build graph
# ------------------------------

def build_reflection_graph() -> StateGraph:
    g = StateGraph(ReflectState)

    # Nodes
    g.add_node("propose", propose_destination)
    g.add_node("reflect", reflect_on_proposal)
    g.add_node("revise", revise_proposal)

    # Edges
    g.set_entry_point("propose")
    g.add_edge("propose", "reflect")
    g.add_conditional_edges("reflect", need_revision, {"revise": "propose", "finish": None})

    return g

# ------------------------------
# Demo
# ------------------------------

if __name__ == "__main__":
    prefs = {"budget": 0.3, "luxury": 0.6, "adventure": 0.8}
    state: ReflectState = {"user_preferences": prefs, "iteration": 0}

    graph = build_reflection_graph().compile()
    final_state = graph.invoke(state)

    print("\n--- Reflection History ---")
    for line in final_state.get("history", []):
        print(line)

    print("\nFinal recommendation:")
    print(json.dumps({"destination": final_state["proposal"], "score": final_state["score"]}, indent=2)) 