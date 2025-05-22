#!/usr/bin/env python3
"""
Chapter 2 – Advanced Example: Travel-Booking LangGraph
-----------------------------------------------------
This script refactors the simple `TravelAgent` into a LangGraph
state-graph that shows:
  • explicit state typing (TypedDict)
  • deterministic tool-calling (flight lookup)
  • autonomous decision & booking node
  • built-in retry/back-off for robustness

Run with:
    python travel_booking_langgraph.py --origin SAN --destination SEA

Dependencies:
    pip install -U langgraph typing_extensions tenacity
"""
from __future__ import annotations

import argparse
import json
from typing import Dict, List, TypedDict

from tenacity import retry, stop_after_attempt, wait_exponential
from langgraph.graph import StateGraph, ToolNode
from langgraph.prebuilt import SimpleTool

# ---------------------------------------------------------------------------
# Mock travel provider (reuse same stub the book used) -----------------------
# ---------------------------------------------------------------------------
try:
    from travel_provider import travel_provider  # type: ignore
except ImportError:
    # Fallback stub so that the graph can run standalone
    class _Stub:
        @staticmethod
        def flight_lookup(departure, destination):
            return {
                "status_code": 200,
                "flight_options": [
                    {"airline": "BudgetAir", "price": 300},
                    {"airline": "ComfortJet", "price": 450},
                    {"airline": "LuxAir", "price": 800},
                ],
            }

    travel_provider = _Stub()  # type: ignore

# ---------------------------------------------------------------------------
# State definition -----------------------------------------------------------
# ---------------------------------------------------------------------------
class AgentState(TypedDict, total=False):
    origin: str
    destination: str
    flight_options: List[Dict]
    selected_flight: Dict
    booking_confirmation: str

# ---------------------------------------------------------------------------
# Tool wrappers --------------------------------------------------------------
# ---------------------------------------------------------------------------
@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=4))
def _flight_lookup(origin: str, destination: str) -> Dict:
    """Wrap the external provider with retry logic."""
    return travel_provider.flight_lookup(origin, destination)  # type: ignore

flight_search_tool = SimpleTool(
    name="search_flights",
    description="Search flight options given origin & destination",
    fn=_flight_lookup,
)

# ---------------------------------------------------------------------------
# Graph nodes ----------------------------------------------------------------
# ---------------------------------------------------------------------------

def store_flight_options(state: AgentState) -> AgentState:
    """Call the tool node output and store scored flight options."""
    origin = state["origin"]
    dest = state["destination"]
    response = _flight_lookup(origin, dest)
    if response["status_code"] != 200:
        raise RuntimeError("Flight search failed")

    scored = [
        {**f, "score": 1000 / f["price"]} for f in response["flight_options"]
    ]
    state["flight_options"] = scored  # type: ignore
    return state


def autonomous_decision(state: AgentState) -> AgentState:
    """Select best flight based on highest score."""
    options = state.get("flight_options", [])
    if not options:
        raise ValueError("No flight options to choose from")
    best = max(options, key=lambda x: x["score"])
    state["selected_flight"] = best  # type: ignore
    return state


def execute_booking(state: AgentState) -> AgentState:
    """Simulate booking and add confirmation code."""
    flight = state.get("selected_flight")
    if not flight:
        raise ValueError("No selected flight to book")
    conf = f"BOOK-{flight['airline']}-{state['origin']}-{state['destination']}"
    state["booking_confirmation"] = conf  # type: ignore
    return state

# ---------------------------------------------------------------------------
# Build LangGraph ------------------------------------------------------------
# ---------------------------------------------------------------------------

def build_travel_graph() -> StateGraph:
    g = StateGraph(AgentState)

    # Add sequential nodes
    g.add_node("search", store_flight_options)
    g.add_node("decide", autonomous_decision)
    g.add_node("book", execute_booking)

    # Edges
    g.add_edge("search", "decide")
    g.add_edge("decide", "book")

    # Entry point & return
    g.set_entry_point("search")
    g.set_finish_point("book")

    return g

# ---------------------------------------------------------------------------
# CLI ------------------------------------------------------------------------
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="LangGraph Travel Booking Demo")
    parser.add_argument("--origin", required=True, help="Departure airport code")
    parser.add_argument("--destination", required=True, help="Destination airport code")
    args = parser.parse_args()

    graph = build_travel_graph().compile()

    initial_state: AgentState = {"origin": args.origin, "destination": args.destination}
    final_state = graph.invoke(initial_state)

    print("\n--- FINAL STATE ---")
    print(json.dumps(final_state, indent=2))

    if "booking_confirmation" in final_state:
        print(f"\nBooking confirmed: {final_state['booking_confirmation']}")


if __name__ == "__main__":
    main() 