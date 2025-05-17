#!/usr/bin/env python3
"""
Chapter 5 – Parallel Tool-Use Planner (LangGraph)
================================================
Demonstrates:
• Parallel branches calling independent tools (flights, hotels, activities)
• Merge node to compile a complete itinerary
• Typed state, built-in retries

Run:
    python planner_langgraph.py --origin JFK --dest CDG --checkin 2025-05-07 --checkout 2025-05-14

Dependencies:
    pip install -U langgraph typing_extensions tenacity
"""
from __future__ import annotations

import argparse
import json
from typing import Dict, List, TypedDict

from langgraph.graph import StateGraph
from tenacity import retry, stop_after_attempt, wait_fixed

# ---------------------------------------------------------------------------
# Mock tool implementations --------------------------------------------------
# ---------------------------------------------------------------------------

def _demo_flights(origin: str, destination: str, date: str):
    return [
        {"airline": "BudgetAir", "price": 300, "route": f"{origin}-{destination}"},
        {"airline": "ComfortJet", "price": 450, "route": f"{origin}-{destination}"},
    ]

def _demo_hotels(location: str, check_in: str, check_out: str):
    return [
        {"name": "Central Hotel", "price": 180, "rating": 4.2},
        {"name": "Luxury Suites", "price": 420, "rating": 4.8},
    ]

def _demo_activities(location: str, date_range: str):
    return [
        {"name": "City Walking Tour", "price": 45},
        {"name": "Wine Tasting", "price": 80},
    ]

# Retry wrappers -------------------------------------------------------------
@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def search_flights(origin: str, destination: str, date: str):
    return _demo_flights(origin, destination, date)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def find_hotels(location: str, check_in: str, check_out: str):
    return _demo_hotels(location, check_in, check_out)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def find_activities(location: str, date_range: str):
    return _demo_activities(location, date_range)

# ---------------------------------------------------------------------------
# State typing ---------------------------------------------------------------
# ---------------------------------------------------------------------------
class PlannerState(TypedDict, total=False):
    origin: str
    destination: str
    date: str
    check_in: str
    check_out: str
    flights: List[Dict]
    hotels: List[Dict]
    activities: List[Dict]
    itinerary: Dict

# ---------------------------------------------------------------------------
# Nodes ----------------------------------------------------------------------
# ---------------------------------------------------------------------------

def flight_node(state: PlannerState) -> PlannerState:
    state["flights"] = search_flights(state["origin"], state["destination"], state["date"])  # type: ignore
    return state

def hotel_node(state: PlannerState) -> PlannerState:
    state["hotels"] = find_hotels(state["destination"], state["check_in"], state["check_out"])  # type: ignore
    return state

def activity_node(state: PlannerState) -> PlannerState:
    date_range = f"{state['check_in']} – {state['check_out']}"
    state["activities"] = find_activities(state["destination"], date_range)  # type: ignore
    return state

def merge_itinerary(state: PlannerState) -> PlannerState:
    state["itinerary"] = {
        "flights": state.get("flights", []),
        "hotel": min(state.get("hotels", []), key=lambda h: h["price"], default={}),
        "activities": state.get("activities", []),
    }
    return state

# ---------------------------------------------------------------------------
# Build graph ----------------------------------------------------------------
# ---------------------------------------------------------------------------

def build_planner_graph() -> StateGraph:
    g = StateGraph(PlannerState)

    # Parallel branch entry
    g.add_node("start", lambda s: s)
    g.set_entry_point("start")

    # Branch nodes
    g.add_node("flights", flight_node)
    g.add_node("hotels", hotel_node)
    g.add_node("activities", activity_node)

    # Fan-out edges from start
    for branch in ("flights", "hotels", "activities"):
        g.add_edge("start", branch)

    # Merge
    g.add_node("merge", merge_itinerary)
    for branch in ("flights", "hotels", "activities"):
        g.add_edge(branch, "merge")

    g.set_finish_point("merge")
    return g

# ---------------------------------------------------------------------------
# CLI ------------------------------------------------------------------------
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Parallel Travel Planner (LangGraph)")
    parser.add_argument("--origin", required=True)
    parser.add_argument("--dest", required=True)
    parser.add_argument("--date", default="2025-05-07")
    parser.add_argument("--checkin", required=True)
    parser.add_argument("--checkout", required=True)
    args = parser.parse_args()

    graph = build_planner_graph().compile()

    init: PlannerState = {
        "origin": args.origin,
        "destination": args.dest,
        "date": args.date,
        "check_in": args.checkin,
        "check_out": args.checkout,
    }
    result = graph.invoke(init)

    print("\n--- Generated Itinerary ---")
    print(json.dumps(result["itinerary"], indent=2))


if __name__ == "__main__":
    main() 