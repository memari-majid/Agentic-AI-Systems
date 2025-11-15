# Lab 2: Travel Booking Agent

⏱️ **Estimated completion time: 25 minutes**

## Overview

This lab demonstrates an agentic travel booking system using LangGraph's state graph approach. It showcases more advanced concepts including:

- Explicit state typing with TypedDict
- Pure functional nodes for better testing and reliability
- Built-in retry logic for external service calls
- Clear separation of concerns

## Learning Objectives

By the end of this lab, you will understand:
- How to use TypedDict for structured state management
- Implementing retry logic for external API calls
- Building sequential workflows with LangGraph
- Error handling and graceful failure management

## Prerequisites

- Python 3.8+
- LangGraph installed (`pip install langgraph`)
- Tenacity for retry logic (`pip install tenacity`)

## Lab Code

```python
#!/usr/bin/env python3
"""
Chapter 2 - Travel Booking with LangGraph
-----------------------------------------
This example demonstrates an agentic travel booking system using LangGraph's
state graph approach. It showcases:
  • Explicit state typing with TypedDict
  • Pure functional nodes for better testing/reliability
  • Built-in retry logic for external service calls
  • Clear separation of concerns
"""
import argparse
import json
from typing import Dict, List, TypedDict

from tenacity import retry, stop_after_attempt, wait_exponential
from langgraph.graph import StateGraph

# ---------------------------------------------------------------------------
# Mock travel provider API ---------------------------------------------------
# ---------------------------------------------------------------------------
class TravelProvider:
    @staticmethod
    def flight_lookup(departure, destination):
        """Simulate an external API call to find flights."""
        print(f"Looking up flights from {departure} to {destination}")
        return {
            "status_code": 200,
            "flight_options": [
                {"airline": "BudgetAir", "price": 300, "departure_time": "08:00"},
                {"airline": "ComfortJet", "price": 450, "departure_time": "11:30"},
                {"airline": "LuxAir", "price": 800, "departure_time": "14:45"},
            ],
        }

# Use our mock provider
travel_provider = TravelProvider()

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
    return travel_provider.flight_lookup(origin, destination)

# ---------------------------------------------------------------------------
# Graph nodes ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def store_flight_options(state: AgentState) -> AgentState:
    """Call the flight search API and store scored flight options."""
    origin = state["origin"]
    dest = state["destination"]
    response = _flight_lookup(origin, dest)
    
    if response["status_code"] != 200:
        raise RuntimeError("Flight search failed")

    # Apply scoring logic - here we score based on inverse price
    scored = [
        {**f, "score": 1000 / f["price"]} for f in response["flight_options"]
    ]
    
    # Store in state
    state["flight_options"] = scored  # type: ignore
    return state


def autonomous_decision(state: AgentState) -> AgentState:
    """Select the best flight based on highest score."""
    options = state.get("flight_options", [])
    
    if not options:
        raise ValueError("No flight options to choose from")
    
    # Pick the option with highest score
    best = max(options, key=lambda x: x["score"])
    state["selected_flight"] = best  # type: ignore
    return state


def execute_booking(state: AgentState) -> AgentState:
    """Simulate booking the selected flight and return confirmation."""
    flight = state.get("selected_flight")
    
    if not flight:
        raise ValueError("No selected flight to book")
    
    # Generate a confirmation code
    confirmation = f"BOOK-{flight['airline']}-{state['origin']}-{state['destination']}"
    state["booking_confirmation"] = confirmation  # type: ignore
    return state

# ---------------------------------------------------------------------------
# Build LangGraph ------------------------------------------------------------
# ---------------------------------------------------------------------------
def build_travel_graph() -> StateGraph:
    """Construct the travel booking graph with three sequential steps."""
    # Create graph with our state type
    g = StateGraph(AgentState)

    # Add nodes
    g.add_node("search", store_flight_options)
    g.add_node("decide", autonomous_decision)
    g.add_node("book", execute_booking)

    # Connect nodes in sequence
    g.add_edge("search", "decide")
    g.add_edge("decide", "book")

    # Define entry and exit points
    g.set_entry_point("search")
    g.set_finish_point("book")

    return g

# ---------------------------------------------------------------------------
# Main function --------------------------------------------------------------
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="LangGraph Travel Booking Demo")
    parser.add_argument("--origin", default="SFO", help="Departure airport code")
    parser.add_argument("--destination", default="JFK", help="Destination airport code")
    args = parser.parse_args()

    # Build and compile the graph
    graph = build_travel_graph().compile()

    # Create initial state with user inputs
    initial_state: AgentState = {
        "origin": args.origin, 
        "destination": args.destination
    }
    
    print(f"\nBooking a flight from {args.origin} to {args.destination}...\n")
    
    # Execute the graph
    final_state = graph.invoke(initial_state)

    # Display results
    print("\n--- Flight Search Results ---")
    for option in final_state.get("flight_options", []):
        print(f"{option['airline']}: ${option['price']} (Score: {option['score']:.2f})")
    
    print("\n--- Selected Flight ---")
    selected = final_state.get("selected_flight", {})
    print(f"{selected.get('airline')}: ${selected.get('price')} at {selected.get('departure_time')}")
    
    print("\n--- Booking Confirmation ---")
    print(f"Confirmation code: {final_state.get('booking_confirmation')}")

if __name__ == "__main__":
    main()
```

## How to Run

1. Save the code above as `02_travel_booking_graph.py`
2. Install dependencies: `pip install langgraph tenacity`
3. Run the script: `python 02_travel_booking_graph.py`
4. Try with custom airports: `python 02_travel_booking_graph.py --origin LAX --destination LHR`

## Expected Output

```
Booking a flight from SFO to JFK...

Looking up flights from SFO to JFK

--- Flight Search Results ---
BudgetAir: $300 (Score: 3.33)
ComfortJet: $450 (Score: 2.22)
LuxAir: $800 (Score: 1.25)

--- Selected Flight ---
BudgetAir: $300 at 08:00

--- Booking Confirmation ---
Confirmation code: BOOK-BudgetAir-SFO-JFK
```

## Key Concepts Explained

### TypedDict State Management
- Provides structure and type safety for your graph state
- Makes code more maintainable and self-documenting
- Enables better IDE support and error detection

### Retry Logic with Tenacity
- Automatically retries failed API calls
- Exponential backoff prevents overwhelming external services
- Graceful handling of temporary network issues

### Sequential Graph Flow
- Simple linear progression through search → decide → book
- Each node performs a specific, testable function
- Clear separation of concerns

### Autonomous Decision Making
- Agent automatically selects the best option based on scoring criteria
- Demonstrates how agents can make decisions without human intervention
- Scoring algorithm can be customized for different criteria

## Exercises

1. **Modify the scoring algorithm**: Try different criteria like departure time preferences or airline preferences
2. **Add error handling**: What happens if no flights are found?
3. **Add more decision factors**: Include duration, number of stops, or user preferences
4. **Implement user confirmation**: Add a step for user approval before booking

## Download Code

[Download 02_travel_booking_graph.py](02_travel_booking_graph.py){ .md-button .md-button--primary } 