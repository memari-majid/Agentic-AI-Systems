#!/usr/bin/env python3
# Chapter 2: Principles of Agentic Systems
# Implementing Algorithm 1: Travel Booking Assistant Algorithm with Agency and Autonomy
# This is a simple Python implementation of Algorithm 1 in Chapter 2.

from travel_provider import travel_provider
from typing import List, Dict, Any

class TravelAgent:
    def __init__(self, name: str):
        self.name = name
        self.goals: List[str] = []
        self.knowledge_base: Dict[str, Any] = {}

    def set_goal(self, goal: str):
        """Agency: Defining objectives"""
        self.goals.append(goal)
        print(f"Goal set: {goal}")

    def update_knowledge(self, departure: str, destination: str):
        """Agency: Acquiring information from an API, and scoring"""
        # Simulating API call to get flight options
        response = travel_provider.flight_lookup(departure, destination)
        if response['status_code'] == 200:
            flight_options = response['flight_options']
            # Simple scoring based on price (lower is better)
            scored_options = [
                {**flight, 'score': 1000 / flight['price']} 
                for flight in flight_options
            ]
            self.knowledge_base['flight_options'] = scored_options
            print(f"Knowledge updated with {len(scored_options)} flight options")
        else:
            print("Failed to fetch flight information")

    def make_decision(self) -> Dict[str, Any]:
        """Autonomy: Independent decision-making"""
        if 'flight_options' not in self.knowledge_base:
            raise ValueError("No flight options available for decision-making")
        best_option = max(self.knowledge_base['flight_options'], key=lambda x: x['score'])
        print(f"Decision made: Selected flight {best_option['airline']}")
        return best_option

    def book_travel(self, departure: str, destination: str):
        """Agency: Execute action on behalf of user"""
        print(f"Agent {self.name} is booking travel from {departure} to {destination}")
        
        self.set_goal(f"Book flight from {departure} to {destination}")
        self.update_knowledge(departure, destination)
        
        try:
            best_flight = self.make_decision()
            # Simulating booking process
            booking_confirmation = f"BOOK-{best_flight['airline']}-{self.name.upper()}"
            self.knowledge_base['booking_confirmation'] = booking_confirmation
            print(f"Booking confirmed: {booking_confirmation}")
        except Exception as e:
            print(f"Booking failed: {str(e)}")

        return self

# Usage example
if __name__ == "__main__":
    agent = TravelAgent("TripPlanner")
    agent.book_travel("SAN", "SEA")
    print("\n----------- Final Agent State: -----------")
    print(f"Name: {agent.name}")
    print(f"Goals: {agent.goals}")
    print(f"Knowledge Base: {agent.knowledge_base}")
    if 'booking_confirmation' in agent.knowledge_base:
        print(f"Booking Confirmation: {agent.knowledge_base['booking_confirmation']}") 