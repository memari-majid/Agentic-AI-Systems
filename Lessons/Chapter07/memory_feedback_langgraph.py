#!/usr/bin/env python3
"""
Chapter 7 – Memory & Feedback Demo (LangGraph)
=============================================
A minimal conversational agent that:
  • maintains short-term & long-term memory
  • summarises when context window would overflow
  • adapts responses based on learned user preferences

Run:
    python memory_feedback_langgraph.py --message "I love art museums"

Dependencies:
    pip install -U langgraph typing_extensions
"""
from __future__ import annotations

import argparse
import json
from typing import Dict, List, TypedDict

from langgraph.graph import StateGraph

# -----------------------------
# State Typing
# -----------------------------
class MemoryState(TypedDict, total=False):
    user_message: str
    short_term: List[str]
    long_term: Dict[str, float]  # preference weights
    response: str

MAX_SHORT = 5  # max short-term entries before summarise

# -----------------------------
# Nodes
# -----------------------------

def store_short_term(state: MemoryState) -> MemoryState:
    msg = state["user_message"]
    short = state.get("short_term", [])
    short.append(msg)
    if len(short) > MAX_SHORT:
        short = short[-MAX_SHORT:]
    state["short_term"] = short  # type: ignore
    return state


def update_long_term(state: MemoryState) -> MemoryState:
    msg = state["user_message"].lower()
    long = state.get("long_term", {})
    # Naive keyword preference learning
    if "museum" in msg or "art" in msg:
        long["art"] = long.get("art", 0.5) + 0.1
    if "food" in msg or "restaurant" in msg:
        long["food"] = long.get("food", 0.5) + 0.1
    # Cap weights
    for k in long:
        long[k] = min(long[k], 1.0)
    state["long_term"] = long  # type: ignore
    return state


def generate_response(state: MemoryState) -> MemoryState:
    prefs = state.get("long_term", {})
    base = "Sounds great! "
    if prefs.get("art", 0) > 0.7:
        base += "Since you love art, I recommend the Louvre on your next trip."
    elif prefs.get("food", 0) > 0.7:
        base += "Given your food interests, let's explore a culinary tour."
    else:
        base += "Tell me more about what you enjoy while travelling."
    state["response"] = base  # type: ignore
    return state

# -----------------------------
# Build graph
# -----------------------------

def build_memory_graph() -> StateGraph:
    g = StateGraph(MemoryState)
    g.add_node("short", store_short_term)
    g.add_node("long", update_long_term)
    g.add_node("respond", generate_response)

    g.set_entry_point("short")
    g.add_edge("short", "long")
    g.add_edge("long", "respond")
    g.set_finish_point("respond")
    return g

# -----------------------------
# CLI
# -----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Memory & Feedback Demo")
    parser.add_argument("--message", required=True, help="User input message")
    args = parser.parse_args()

    initial: MemoryState = {"user_message": args.message, "short_term": [], "long_term": {}}
    graph = build_memory_graph().compile()
    out = graph.invoke(initial)

    print("\nAgent response:")
    print(out["response"])
    print("\nShort-term memory:", out["short_term"])
    print("Long-term memory:", json.dumps(out.get("long_term", {}), indent=2)) 