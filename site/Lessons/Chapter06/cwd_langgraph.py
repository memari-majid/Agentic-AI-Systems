#!/usr/bin/env python3
"""
Chapter 6 – Coordinator / Worker / Delegator with LangGraph
==========================================================
Pattern
  • Coordinator   – parses user request and drafts a high-level plan
  • Delegator     – assigns subtasks to specialist workers
  • Workers       – flights / hotels / activities (parallel)

Run:
    python cwd_langgraph.py --request_file sample_request.txt

Dependencies:
    pip install -U langgraph typing_extensions tenacity
"""
from __future__ import annotations

import argparse
import json
import textwrap
from pathlib import Path
from typing import Dict, List, TypedDict

from langgraph.graph import StateGraph
from tenacity import retry, stop_after_attempt, wait_fixed

# ---------------------------------------------------------------------------
# Mock tool implementations (same as Chapter 5) ------------------------------
# ---------------------------------------------------------------------------

def _demo_flights(origin: str, destination: str):
    return [
        {"airline": "BudgetAir", "price": 320},
        {"airline": "ComfortJet", "price": 480},
    ]

def _demo_hotels(location: str, max_price: int):
    return [
        {"name": "City Hotel", "price": 150},
        {"name": "Luxury Palace", "price": 380},
    ]

def _demo_activities(location: str, preference: str):
    return [
        {"name": "Museum Tour", "price": 60},
        {"name": "Food Crawl", "price": 90},
    ]

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def search_flights(origin: str, destination: str):
    return _demo_flights(origin, destination)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def find_hotels(location: str, max_price: int):
    return _demo_hotels(location, max_price)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def find_activities(location: str, preference: str):
    return _demo_activities(location, preference)

# ---------------------------------------------------------------------------
# State ---------------------------------------------------------------------
# ---------------------------------------------------------------------------
class CWDState(TypedDict, total=False):
    request_text: str
    coordinator_plan: Dict
    flights: List[Dict]
    hotels: List[Dict]
    activities: List[Dict]
    complete_itinerary: Dict

# ---------------------------------------------------------------------------
# Coordinator node ----------------------------------------------------------
# ---------------------------------------------------------------------------

def coordinator_node(state: CWDState) -> CWDState:
    """Parse free-form request into a simple JSON plan."""
    req = state["request_text"].lower()
    plan: Dict = {}
    # Very naive extraction for demo purposes
    if "paris" in req:
        plan["destination"] = "Paris"
    if "new york" in req and "paris" in req:
        plan["origin"] = "New York"
    plan["max_price_hotel"] = 400 if "hotel" in req else 0
    plan["preference"] = "culture" if "museum" in req else "mixed"
    state["coordinator_plan"] = plan  # type: ignore
    return state

# ---------------------------------------------------------------------------
# Delegator node ------------------------------------------------------------
# ---------------------------------------------------------------------------

def delegator_prepare(state: CWDState) -> CWDState:
    """Just pass state; in real life could split into sub-tasks"""
    return state

# ---------------------------------------------------------------------------
# Worker nodes --------------------------------------------------------------
# ---------------------------------------------------------------------------

def flights_worker(state: CWDState) -> CWDState:
    plan = state["coordinator_plan"]
    state["flights"] = search_flights(plan["origin"], plan["destination"])  # type: ignore
    return state


def hotels_worker(state: CWDState) -> CWDState:
    plan = state["coordinator_plan"]
    state["hotels"] = find_hotels(plan["destination"], plan["max_price_hotel"])  # type: ignore
    return state


def activities_worker(state: CWDState) -> CWDState:
    plan = state["coordinator_plan"]
    state["activities"] = find_activities(plan["destination"], plan["preference"])  # type: ignore
    return state

# ---------------------------------------------------------------------------
# Merge / assemble ----------------------------------------------------------
# ---------------------------------------------------------------------------

def assemble_itinerary(state: CWDState) -> CWDState:
    plan = state["coordinator_plan"]
    state["complete_itinerary"] = {
        "destination": plan.get("destination"),
        "flights": state.get("flights", []),
        "hotel": min(state.get("hotels", []), key=lambda h: h["price"], default={}),
        "activities": state.get("activities", []),
    }
    return state

# ---------------------------------------------------------------------------
# Build LangGraph -----------------------------------------------------------
# ---------------------------------------------------------------------------

def build_cwd_graph() -> StateGraph:
    g = StateGraph(CWDState)

    g.add_node("coordinator", coordinator_node)
    g.set_entry_point("coordinator")

    g.add_node("delegator", delegator_prepare)
    g.add_edge("coordinator", "delegator")

    # Workers in parallel
    g.add_node("flights", flights_worker)
    g.add_node("hotels", hotels_worker)
    g.add_node("activities", activities_worker)

    for w in ("flights", "hotels", "activities"):
        g.add_edge("delegator", w)

    # Merge
    g.add_node("assemble", assemble_itinerary)
    for w in ("flights", "hotels", "activities"):
        g.add_edge(w, "assemble")

    g.set_finish_point("assemble")
    return g

# ---------------------------------------------------------------------------
# CLI -----------------------------------------------------------------------
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="CWD Travel Planner (LangGraph)")
    parser.add_argument("--request_file", required=True, help="Path to text file with user request")
    args = parser.parse_args()

    request_text = Path(args.request_file).read_text().strip()
    initial: CWDState = {"request_text": request_text}

    graph = build_cwd_graph().compile()
    result = graph.invoke(initial)

    print("\n--- Final Travel Package ---")
    print(json.dumps(result["complete_itinerary"], indent=2))


if __name__ == "__main__":
    main() 