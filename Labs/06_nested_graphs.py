#!/usr/bin/env python3
"""
Chapter 6 - Coordinator/Worker/Delegator with Nested Graphs
----------------------------------------------------------
This example demonstrates how to implement the Coordinator/Worker/Delegator (CWD)
pattern using LangGraph. It models an organizational hierarchy where:

1. A coordinator creates a high-level plan from a user request
2. A delegator distributes work to specialized workers
3. Workers handle specific tasks in parallel
4. Results are assembled into a final output

Key concepts:
- Hierarchical organization in a graph
- Parallel execution of worker nodes
- State management across organization layers
- Nested subgraphs
"""
import argparse
import json
from typing import Dict, List, TypedDict

from tenacity import retry, stop_after_attempt, wait_fixed
from langgraph.graph import StateGraph

# ---------------------------------------------------------------------------
# Mock external APIs --------------------------------------------------------
# ---------------------------------------------------------------------------

def _mock_flights_api(origin: str, destination: str):
    """Mock flight search API."""
    print(f"Worker: Searching flights from {origin} to {destination}")
    return [
        {"airline": "EconoFly", "price": 350, "duration": "2h 15m"},
        {"airline": "LuxAir", "price": 720, "duration": "1h 55m"},
    ]

def _mock_hotels_api(location: str, max_price: int):
    """Mock hotel search API."""
    print(f"Worker: Finding hotels in {location} under ${max_price}")
    return [
        {"name": "Downtown Inn", "price": 175, "rating": 3.8},
        {"name": "Grand Hotel", "price": 340, "rating": 4.5},
    ]

def _mock_activities_api(location: str, preference: str):
    """Mock activities search API."""
    print(f"Worker: Finding {preference} activities in {location}")
    return [
        {"name": "Guided City Tour", "price": 35, "duration": "3 hours"},
        {"name": "Local Food Experience", "price": 75, "duration": "4 hours"},
    ]

# ---------------------------------------------------------------------------
# API wrappers with retry logic ---------------------------------------------
# ---------------------------------------------------------------------------

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def search_flights(origin: str, destination: str):
    """Wrap flight search with retry logic."""
    return _mock_flights_api(origin, destination)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def find_hotels(location: str, max_price: int):
    """Wrap hotel search with retry logic."""
    return _mock_hotels_api(location, max_price)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def find_activities(location: str, preference: str):
    """Wrap activities search with retry logic."""
    return _mock_activities_api(location, preference)

# ---------------------------------------------------------------------------
# State definition ----------------------------------------------------------
# ---------------------------------------------------------------------------
class CWDState(TypedDict, total=False):
    request_text: str              # User's request
    coordinator_plan: Dict         # Plan created by coordinator
    flights: List[Dict]            # Flight options found by worker
    hotels: List[Dict]             # Hotel options found by worker
    activities: List[Dict]         # Activity options found by worker
    complete_itinerary: Dict       # Final assembled result

# ---------------------------------------------------------------------------
# Coordinator node ----------------------------------------------------------
# ---------------------------------------------------------------------------

def coordinator_node(state: CWDState) -> CWDState:
    """
    The coordinator analyzes the user request and creates a high-level plan.
    
    In a real system, this would use an LLM to extract information from natural
    language. For simplicity in this example, we'll use basic text matching.
    """
    request = state["request_text"].lower()
    print("\nCoordinator: Analyzing request and creating plan")
    
    # Extract destination
    destination = None
    if "paris" in request:
        destination = "Paris"
    elif "tokyo" in request:
        destination = "Tokyo"
    elif "new york" in request:
        destination = "New York"
    
    # Extract origin
    origin = None
    if "from london" in request:
        origin = "London"
    elif "from berlin" in request:
        origin = "Berlin"
    elif "from san francisco" in request:
        origin = "San Francisco"
    
    # Set defaults if not found
    if not destination:
        destination = "Paris"  # Default destination
    if not origin:
        origin = "London"  # Default origin
    
    # Determine budget preferences
    max_price_hotel = 400  # Default
    if "luxury" in request:
        max_price_hotel = 800
    elif "budget" in request:
        max_price_hotel = 200
    
    # Determine activity preferences
    preference = "general"  # Default
    if "museum" in request or "culture" in request or "art" in request:
        preference = "cultural"
    elif "food" in request or "cuisine" in request:
        preference = "culinary"
    elif "outdoor" in request or "adventure" in request:
        preference = "outdoor"
    
    # Create the plan
    plan = {
        "origin": origin,
        "destination": destination,
        "max_price_hotel": max_price_hotel,
        "preference": preference
    }
    
    print(f"Coordinator Plan: {json.dumps(plan, indent=2)}")
    
    # Store plan in state
    state["coordinator_plan"] = plan  # type: ignore
    return state

# ---------------------------------------------------------------------------
# Delegator node ------------------------------------------------------------
# ---------------------------------------------------------------------------

def delegator_prepare(state: CWDState) -> CWDState:
    """
    The delegator takes the coordinator's plan and prepares it for workers.
    
    In more complex systems, this would involve breaking down tasks, assigning
    priorities, and managing worker selection.
    """
    plan = state["coordinator_plan"]
    print("\nDelegator: Distributing tasks to specialized workers")
    
    # In this simple example, we just pass through the state
    # A more complex delegator might transform the plan into worker-specific tasks
    
    print(f"  • Assigned flight search: {plan['origin']} → {plan['destination']}")
    print(f"  • Assigned hotel search: {plan['destination']} (max ${plan['max_price_hotel']})")
    print(f"  • Assigned activity search: {plan['preference']} in {plan['destination']}")
    
    return state

# ---------------------------------------------------------------------------
# Worker nodes --------------------------------------------------------------
# ---------------------------------------------------------------------------

def flights_worker(state: CWDState) -> CWDState:
    """Worker responsible for finding flights."""
    plan = state["coordinator_plan"]
    
    # Call the flight search API with parameters from the plan
    flights = search_flights(plan["origin"], plan["destination"])
    
    # Store results in state
    state["flights"] = flights  # type: ignore
    return state


def hotels_worker(state: CWDState) -> CWDState:
    """Worker responsible for finding hotels."""
    plan = state["coordinator_plan"]
    
    # Call the hotel search API with parameters from the plan
    hotels = find_hotels(plan["destination"], plan["max_price_hotel"])
    
    # Store results in state
    state["hotels"] = hotels  # type: ignore
    return state


def activities_worker(state: CWDState) -> CWDState:
    """Worker responsible for finding activities."""
    plan = state["coordinator_plan"]
    
    # Call the activities search API with parameters from the plan
    activities = find_activities(plan["destination"], plan["preference"])
    
    # Store results in state
    state["activities"] = activities  # type: ignore
    return state

# ---------------------------------------------------------------------------
# Result assembly -----------------------------------------------------------
# ---------------------------------------------------------------------------

def assemble_itinerary(state: CWDState) -> CWDState:
    """
    Combine all worker results into a complete itinerary.
    
    This represents the final integration of all parallel work streams.
    """
    plan = state["coordinator_plan"]
    print("\nAssembling final itinerary from worker results")
    
    # For this demo, we'll choose the cheapest flight, highest rated hotel,
    # and include all activities
    
    # Select cheapest flight
    flights = state.get("flights", [])
    selected_flight = min(flights, key=lambda f: f["price"]) if flights else None
    
    # Select highest rated hotel
    hotels = state.get("hotels", [])
    selected_hotel = max(hotels, key=lambda h: h["rating"]) if hotels else None
    
    # Include all activities found
    activities = state.get("activities", [])
    
    # Create the complete itinerary
    state["complete_itinerary"] = {
        "destination": plan.get("destination"),
        "origin": plan.get("origin"),
        "flight": selected_flight,
        "hotel": selected_hotel,
        "activities": activities,
    }
    
    return state

# ---------------------------------------------------------------------------
# Graph construction --------------------------------------------------------
# ---------------------------------------------------------------------------

def build_cwd_graph() -> StateGraph:
    """Build the graph representing CWD organizational structure."""
    g = StateGraph(CWDState)
    
    # Add the coordinator node as entry point
    g.add_node("coordinator", coordinator_node)
    g.set_entry_point("coordinator")
    
    # Add delegator node
    g.add_node("delegator", delegator_prepare)
    g.add_edge("coordinator", "delegator")
    
    # Add worker nodes
    g.add_node("flights", flights_worker)
    g.add_node("hotels", hotels_worker)
    g.add_node("activities", activities_worker)
    
    # Connect delegator to all workers
    for worker in ("flights", "hotels", "activities"):
        g.add_edge("delegator", worker)
    
    # Connect all workers to assembly
    g.add_node("assemble", assemble_itinerary)
    for worker in ("flights", "hotels", "activities"):
        g.add_edge(worker, "assemble")
    
    # Set assembly as finish point
    g.set_finish_point("assemble")
    
    return g

# ---------------------------------------------------------------------------
# Advanced nested subgraphs example -----------------------------------------
# ---------------------------------------------------------------------------

def create_nested_subgraph_example():
    """
    Example of using nested subgraphs for even more complex organization.
    
    This function is not called in the main demo but illustrates how
    subgraphs can be nested for complex hierarchies.
    """
    # This is a conceptual example showing how nested graphs would work
    # but not executed in the main flow
    
    # Main graph representing the entire organization
    main_graph = StateGraph(Dict)
    
    # Create strategy team subgraph
    strategy_team = StateGraph(Dict)
    strategy_team.add_node("analyze", lambda s: s)
    strategy_team.add_node("plan", lambda s: s)
    strategy_team.add_edge("analyze", "plan")
    strategy_team.set_entry_point("analyze")
    strategy_team.set_finish_point("plan")
    
    # Create operations team subgraph
    operations_team = StateGraph(Dict)
    operations_team.add_node("logistics", lambda s: s)
    operations_team.add_node("execution", lambda s: s)
    operations_team.add_edge("logistics", "execution")
    operations_team.set_entry_point("logistics")
    operations_team.set_finish_point("execution")
    
    # Add team subgraphs to main graph
    main_graph.add_node("strategy", strategy_team.compile())
    main_graph.add_node("operations", operations_team.compile())
    main_graph.add_edge("strategy", "operations")
    
    # This pattern mirrors real organizational charts
    return main_graph

# ---------------------------------------------------------------------------
# Main function -------------------------------------------------------------
# ---------------------------------------------------------------------------

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Coordinator-Worker-Delegator Demo")
    parser.add_argument("--request", type=str, 
                      default="I want to travel from London to Paris, stay in a nice hotel, and enjoy some cultural activities.",
                      help="User request text")
    args = parser.parse_args()

    # Print header
    print("\n=== Coordinator-Worker-Delegator Pattern Demo ===\n")
    print(f"User Request: \"{args.request}\"")
    
    # Build the CWD graph
    graph = build_cwd_graph().compile()
    
    # Create initial state with user request
    initial_state: CWDState = {"request_text": args.request}
    
    # Execute the graph with organizational workflow
    final_state = graph.invoke(initial_state)
    
    # Display the results
    print("\n=== Final Travel Package ===\n")
    itinerary = final_state["complete_itinerary"]
    
    print(f"Trip from {itinerary['origin']} to {itinerary['destination']}")
    
    # Flight information
    flight = itinerary.get("flight", {})
    if flight:
        print(f"\nFlight: {flight['airline']}")
        print(f"  Price: ${flight['price']}")
        print(f"  Duration: {flight['duration']}")
    
    # Hotel information
    hotel = itinerary.get("hotel", {})
    if hotel:
        print(f"\nHotel: {hotel['name']}")
        print(f"  Price: ${hotel['price']} per night")
        print(f"  Rating: {hotel['rating']}/5.0")
    
    # Activities
    print("\nRecommended Activities:")
    for idx, activity in enumerate(itinerary.get("activities", [])):
        print(f"  {idx+1}. {activity['name']}")
        print(f"     ${activity['price']} - {activity['duration']}")

if __name__ == "__main__":
    main() 