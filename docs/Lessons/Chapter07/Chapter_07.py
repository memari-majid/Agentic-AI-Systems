#!/usr/bin/env python3
# Chapter 7 – Effective Agentic System Design Techniques

# Required dependencies:
# pip install -U crewai langchain-openai

import os
from typing import Dict, List, Any

class AgenticDesignTechniques:
    """
    Demonstrates effective design techniques for agentic AI systems, including:
    - Goal setting and objective alignment
    - State management
    - Memory and context handling
    - Error handling and resilience
    - User-centered design principles
    """
    
    def __init__(self, api_key=None, model="gpt-4o-mini"):
        """Initialize the class for demonstrating agentic design techniques."""
        # Set up API key if provided
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
    
    def demonstrate_goal_setting(self):
        """
        Demonstrate the importance of proper goal setting in agent design.
        Shows different approaches to defining agent goals and their impacts.
        """
        print("EFFECTIVE GOAL SETTING IN AGENT DESIGN")
        print("-" * 50)
        
        print("1. Vague vs. Specific Goals")
        print("Vague Goal Example:")
        print("""
        flight_agent = Agent(
            role="Flight Specialist",
            goal="Find flights for the customer.",
            backstory="You have years of experience in the travel industry."
        )
        """)
        
        print("\nSpecific Goal Example:")
        print("""
        flight_agent = Agent(
            role="Flight Specialist",
            goal="Find the most cost-effective flights with convenient departure times that minimize layovers while considering the traveler's preferences for airlines and seat classes.",
            backstory="You have years of experience in the travel industry."
        )
        """)
        
        print("\n2. Conflicting Goals in Collaborative Settings")
        print("Problematic Setup:")
        print("""
        budget_agent = Agent(
            role="Budget Travel Specialist",
            goal="Find the absolute cheapest options for all aspects of the trip regardless of quality or convenience.",
            backstory="You are obsessed with saving money above all else."
        )

        experience_agent = Agent(
            role="Luxury Travel Consultant",
            goal="Create the most luxurious and memorable travel experience possible.",
            backstory="You believe travel should be extraordinary and unforgettable."
        )
        """)
        
        print("\nImproved Setup:")
        print("""
        budget_agent = Agent(
            role="Budget Travel Specialist",
            goal="Find cost-effective options that provide good value while respecting the traveler's overall budget of $2000. Collaborate with other specialists to balance cost with experience quality.",
            backstory="You are skilled at finding hidden gems that don't break the bank."
        )

        experience_agent = Agent(
            role="Experience Consultant",
            goal="Identify meaningful experiences that align with the traveler's interests while working within budget constraints. Prioritize authentic experiences over luxury when necessary.",
            backstory="You believe travel should be memorable and personally significant."
        )
        """)
        
        print("\nKey Principles for Effective Goal Setting:")
        print("1. Specificity Matters: The more specific the goal, the more directed and useful the agent's output will be.")
        print("2. Alignment is Critical: Goals should align with the user's actual needs rather than arbitrary metrics.")
        print("3. Collaborative Awareness: In multi-agent systems, goals should acknowledge the collaborative nature of the work.")
        print("4. Success Criteria: Effective goals implicitly or explicitly define what success looks like.")
        print("5. Balance: Goals should balance between being too prescriptive (limiting creativity) and too vague (lacking direction).")
    
    def demonstrate_state_management(self):
        """
        Demonstrate effective state management techniques for agentic systems.
        Covers persistent state, transitional state, and state versioning.
        """
        print("\nEFFECTIVE STATE MANAGEMENT TECHNIQUES")
        print("-" * 50)
        
        print("1. Persistent State")
        print("""
        class TravelAgent:
            def __init__(self):
                # Persistent state properties
                self.user_profile = {}  # Stores user preferences, budget, etc.
                self.travel_plan = {}   # Stores the evolving travel plan
                self.booking_history = []  # Stores history of bookings made
            
            def update_user_profile(self, new_info):
                # Update user profile while preserving existing information
                self.user_profile = {**self.user_profile, **new_info}
                
            def add_to_plan(self, component, details):
                # Add to travel plan while maintaining structure
                self.travel_plan[component] = details
                
            def record_booking(self, booking):
                # Record a new booking action
                self.booking_history.append({
                    "timestamp": self.get_timestamp(),
                    "action": booking
                })
        """)
        
        print("\n2. State Snapshots and Versioning")
        print("""
        class VersionedTravelAgent:
            def __init__(self):
                self.current_state = {
                    "user_profile": {},
                    "travel_plan": {},
                    "stage": "initial"
                }
                self.state_history = []  # List of state snapshots
                
            def update_state(self, updates):
                # Create a snapshot before updating
                self.state_history.append(self.current_state.copy())
                
                # Update the current state
                for key, value in updates.items():
                    if key in self.current_state:
                        if isinstance(self.current_state[key], dict) and isinstance(value, dict):
                            # Deep merge for nested dictionaries
                            self.current_state[key] = {**self.current_state[key], **value}
                        else:
                            # Regular update for non-dict values
                            self.current_state[key] = value
                
            def revert_to_previous_state(self):
                # Revert to the previous state
                if self.state_history:
                    self.current_state = self.state_history.pop()
                    return True
                return False
                
            def revert_to_state(self, index):
                # Revert to a specific state by index
                if 0 <= index < len(self.state_history):
                    self.current_state = self.state_history[index].copy()
                    # Truncate history up to this point
                    self.state_history = self.state_history[:index]
                    return True
                return False
        """)
        
        print("\n3. State Management Best Practices:")
        print("- Immutability: Use immutable state whenever possible to avoid side effects")
        print("- Version Control: Maintain a history of state changes to enable undoing actions")
        print("- Clear Structure: Design state with a clear structure that maps to user mental models")
        print("- Validation: Validate state updates to ensure consistency and correctness")
        print("- Error Handling: Build robust error handling around state transitions")
        print("- Documentation: Document the expected state structure and transitions")
    
    def demonstrate_memory_and_context(self):
        """
        Demonstrate memory and context handling techniques for agentic systems.
        Covers short-term, long-term memory, and context management.
        """
        print("\nMEMORY AND CONTEXT HANDLING TECHNIQUES")
        print("-" * 50)
        
        print("1. Short-term vs. Long-term Memory")
        print("""
        class AgentMemoryManager:
            def __init__(self, max_short_term_capacity=10):
                self.short_term_memory = []  # Recent interactions, limited capacity
                self.long_term_memory = {}   # Persistent storage of important information
                self.max_short_term_capacity = max_short_term_capacity
            
            def add_to_short_term(self, item):
                # Add item to short-term memory, maintaining capacity limit
                self.short_term_memory.append(item)
                if len(self.short_term_memory) > self.max_short_term_capacity:
                    # Remove oldest item when capacity is exceeded
                    self.short_term_memory.pop(0)
            
            def store_in_long_term(self, key, value):
                # Store or update information in long-term memory
                self.long_term_memory[key] = value
            
            def get_from_long_term(self, key, default=None):
                # Retrieve information from long-term memory
                return self.long_term_memory.get(key, default)
            
            def get_recent_context(self, n=5):
                # Get the n most recent items from short-term memory
                return self.short_term_memory[-n:] if n <= len(self.short_term_memory) else self.short_term_memory[:]
        """)
        
        print("\n2. Context Window Management")
        print("""
        class ContextManager:
            def __init__(self, max_tokens=4000):
                self.conversation_history = []
                self.max_tokens = max_tokens
                self.current_token_count = 0
            
            def add_message(self, role, content, token_count=None):
                # Estimate token count if not provided
                if token_count is None:
                    token_count = self._estimate_tokens(content)
                
                # Add message to history
                message = {"role": role, "content": content, "tokens": token_count}
                self.conversation_history.append(message)
                self.current_token_count += token_count
                
                # Prune history if needed
                self._prune_history()
            
            def _prune_history(self):
                # Remove oldest messages until we're under the token limit
                while self.current_token_count > self.max_tokens and len(self.conversation_history) > 1:
                    # Always keep at least the most recent message
                    removed = self.conversation_history.pop(0)
                    self.current_token_count -= removed["tokens"]
            
            def _estimate_tokens(self, text):
                # Simple token estimation (approx 4 chars per token)
                return len(text) // 4
            
            def get_context_for_model(self):
                # Return the conversation history in the format expected by the model
                return [{"role": msg["role"], "content": msg["content"]} 
                        for msg in self.conversation_history]
        """)
        
        print("\n3. Memory and Context Best Practices:")
        print("- Context Prioritization: Prioritize the most relevant information for the current task")
        print("- Summarization: Summarize historical information to keep context concise")
        print("- Tokenization Awareness: Be mindful of token limits in LLM context windows")
        print("- Hierarchical Context: Organize memory hierarchically (recent, relevant, background)")
        print("- Memory Types: Distinguish between episodic (event-based) and semantic (knowledge) memory")
        print("- Retrieval Augmentation: Use vector databases for efficient memory retrieval")
    
    def demonstrate_error_handling(self):
        """
        Demonstrate error handling and resilience techniques for agentic systems.
        Covers graceful degradation, fallbacks, and monitoring.
        """
        print("\nERROR HANDLING AND RESILIENCE TECHNIQUES")
        print("-" * 50)
        
        print("1. Robust Function Calling")
        print("""
        def call_external_api(endpoint, params, retries=3, backoff_factor=2):
            \"\"\"Call external API with automatic retries and exponential backoff\"\"\"
            import requests
            import time
            
            for attempt in range(retries):
                try:
                    response = requests.get(endpoint, params=params, timeout=10)
                    response.raise_for_status()  # Raise exception for HTTP errors
                    return response.json()  # Success case
                except (requests.exceptions.RequestException, ValueError) as e:
                    wait_time = backoff_factor ** attempt
                    print(f"API call failed: {e}. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
            
            # If we've exhausted all retries
            return {"error": "API call failed after multiple attempts", "endpoint": endpoint}
        """)
        
        print("\n2. Graceful Degradation")
        print("""
        class ResilientTravelAgent:
            def __init__(self):
                self.flight_service = FlightService()
                self.hotel_service = HotelService()
                self.local_cache = {}
            
            def search_flights(self, origin, destination, date):
                try:
                    # Primary approach: Get real-time flight information
                    results = self.flight_service.search(origin, destination, date)
                    # Cache the results for future fallback
                    self.local_cache[f"flights_{origin}_{destination}_{date}"] = results
                    return results
                except ServiceUnavailableError:
                    # First fallback: Check local cache
                    cached = self.local_cache.get(f"flights_{origin}_{destination}_{date}")
                    if cached:
                        return {
                            "results": cached,
                            "warning": "Using cached flight information that may be outdated"
                        }
                    
                    # Second fallback: Use approximate information
                    return {
                        "results": self._generate_approximate_flights(origin, destination),
                        "warning": "Flight service unavailable. Showing estimated options only."
                    }
                    
            def _generate_approximate_flights(self, origin, destination):
                # Generate approximate flight information based on historical data or rules
                return [{"airline": "Various Airlines", 
                         "price_range": "Typically $300-600",
                         "note": "This is an estimate. Please check airline websites for current prices."}]
        """)
        
        print("\n3. Monitoring and Observability")
        print("""
        class ObservableAgent:
            def __init__(self):
                self.metrics = {
                    "api_calls": 0,
                    "api_errors": 0,
                    "response_times": [],
                    "user_satisfaction": []
                }
                self.activity_log = []
            
            def log_activity(self, action, details, user_id=None):
                \"\"\"Log an agent activity with timestamp\"\"\"
                import time
                
                entry = {
                    "timestamp": time.time(),
                    "action": action,
                    "details": details,
                    "user_id": user_id
                }
                self.activity_log.append(entry)
                
                # Also increment relevant metrics
                if action == "api_call":
                    self.metrics["api_calls"] += 1
                elif action == "api_error":
                    self.metrics["api_errors"] += 1
                elif action == "response_time":
                    self.metrics["response_times"].append(details["time_ms"])
                
            def record_user_feedback(self, satisfaction_score):
                \"\"\"Record a user satisfaction score (1-5)\"\"\"
                if 1 <= satisfaction_score <= 5:
                    self.metrics["user_satisfaction"].append(satisfaction_score)
            
            def get_error_rate(self):
                \"\"\"Calculate the API error rate\"\"\"
                if self.metrics["api_calls"] == 0:
                    return 0
                return self.metrics["api_errors"] / self.metrics["api_calls"]
            
            def get_average_response_time(self):
                \"\"\"Calculate the average response time\"\"\"
                if not self.metrics["response_times"]:
                    return 0
                return sum(self.metrics["response_times"]) / len(self.metrics["response_times"])
            
            def get_user_satisfaction(self):
                \"\"\"Calculate the average user satisfaction\"\"\"
                if not self.metrics["user_satisfaction"]:
                    return 0
                return sum(self.metrics["user_satisfaction"]) / len(self.metrics["user_satisfaction"])
        """)
        
        print("\n4. Error Handling Best Practices:")
        print("- Expect Failure: Design assuming external services will sometimes fail")
        print("- Fallback Mechanisms: Create multiple levels of fallback for critical functions")
        print("- Transparent Errors: Communicate failures and limitations clearly to users")
        print("- User Recovery: Provide actionable paths for users to recover from errors")
        print("- Monitoring: Implement robust monitoring to detect and address recurring issues")
        print("- Logging: Maintain detailed logs of agent actions and error states for diagnosis")
    
    def demonstrate_user_centered_design(self):
        """
        Demonstrate user-centered design principles for agentic systems.
        Covers personalization, transparency, and feedback mechanisms.
        """
        print("\nUSER-CENTERED DESIGN PRINCIPLES")
        print("-" * 50)
        
        print("1. Personalization and Adaptation")
        print("""
        class AdaptiveTravelAgent:
            def __init__(self):
                self.user_preferences = {}
                self.interaction_history = []
                
            def learn_from_interaction(self, interaction):
                \"\"\"Update user model based on interaction\"\"\"
                self.interaction_history.append(interaction)
                
                # Extract and update preferences
                if interaction["type"] == "hotel_selection":
                    self._update_accommodation_preferences(interaction["selection"])
                elif interaction["type"] == "activity_interest":
                    self._update_activity_preferences(interaction["interest_level"], interaction["activity_type"])
                
            def _update_accommodation_preferences(self, selection):
                # Extract features from selection
                features = selection.get("features", {})
                
                # Initialize preferences if not present
                if "accommodation" not in self.user_preferences:
                    self.user_preferences["accommodation"] = {}
                    
                # Update preference weights
                for feature, value in features.items():
                    if feature not in self.user_preferences["accommodation"]:
                        # New feature
                        self.user_preferences["accommodation"][feature] = value
                    else:
                        # Existing feature - update with weighted average
                        current = self.user_preferences["accommodation"][feature]
                        # 70% weight to new selection, 30% to historical preference
                        self.user_preferences["accommodation"][feature] = 0.7 * value + 0.3 * current
            
            def personalize_recommendations(self, options, option_type):
                \"\"\"Rank options based on learned user preferences\"\"\"
                if option_type not in self.user_preferences:
                    # No learned preferences yet, return default order
                    return options
                    
                preferences = self.user_preferences[option_type]
                
                # Calculate preference score for each option
                scored_options = []
                for option in options:
                    score = 0
                    option_features = option.get("features", {})
                    
                    for feature, value in option_features.items():
                        if feature in preferences:
                            # Weight the feature by learned preference
                            score += value * preferences[feature]
                            
                    scored_options.append((option, score))
                
                # Sort by score (highest first) and return just the options
                return [option for option, score in sorted(scored_options, key=lambda x: x[1], reverse=True)]
        """)
        
        print("\n2. Transparency and Explainability")
        print("""
        class ExplainableTravelAgent:
            def __init__(self):
                self.recommendation_factors = {}
                
            def recommend_hotel(self, options, user_preferences):
                scored_options = []
                
                for hotel in options:
                    # Calculate score based on different factors
                    score = 0
                    factor_breakdown = {}
                    
                    # Location score (0-10)
                    location_score = self._score_location(hotel, user_preferences)
                    factor_breakdown["location"] = location_score
                    score += location_score * 0.4  # 40% weight to location
                    
                    # Amenities score (0-10)
                    amenities_score = self._score_amenities(hotel, user_preferences)
                    factor_breakdown["amenities"] = amenities_score
                    score += amenities_score * 0.3  # 30% weight to amenities
                    
                    # Price score (0-10, higher = better value)
                    price_score = self._score_price(hotel, user_preferences)
                    factor_breakdown["price"] = price_score
                    score += price_score * 0.3  # 30% weight to price
                    
                    # Store the factor breakdown for explanation
                    self.recommendation_factors[hotel["id"]] = factor_breakdown
                    
                    scored_options.append((hotel, score))
                
                # Sort by score
                sorted_options = [hotel for hotel, score in sorted(scored_options, key=lambda x: x[1], reverse=True)]
                
                return sorted_options
                
            def explain_recommendation(self, hotel_id):
                \"\"\"Generate human-readable explanation for why a hotel was recommended\"\"\"
                if hotel_id not in self.recommendation_factors:
                    return "No explanation available for this recommendation."
                    
                factors = self.recommendation_factors[hotel_id]
                
                # Create explanation based on factor scores
                explanation = "This hotel was recommended because of:\n"
                
                if factors["location"] >= 8:
                    explanation += "- Its excellent location matching your preferences\n"
                elif factors["location"] >= 6:
                    explanation += "- Its good location that reasonably matches your preferences\n"
                
                if factors["amenities"] >= 8:
                    explanation += "- The impressive amenities that align with your needs\n"
                elif factors["amenities"] >= 6:
                    explanation += "- The decent amenities that cover most of your needs\n"
                
                if factors["price"] >= 8:
                    explanation += "- The excellent value for money\n"
                elif factors["price"] >= 6:
                    explanation += "- The reasonable price point given its features\n"
                
                return explanation
        """)
        
        print("\n3. User-Centered Best Practices:")
        print("- User Modeling: Build and refine user models through interactions")
        print("- Preference Learning: Learn from user choices and apply to future recommendations")
        print("- Progressive Disclosure: Present information in layers of increasing complexity")
        print("- Clear Explanations: Provide transparent explanations for agent decisions")
        print("- Feedback Loops: Create mechanisms for users to provide feedback and corrections")
        print("- User Control: Allow users to override agent decisions and adjust parameters")
        print("- Graceful Onboarding: Minimize the initial information required from users")


# Example usage
if __name__ == "__main__":
    print("Chapter 7 - Effective Agentic System Design Techniques\n")
    
    techniques = AgenticDesignTechniques()
    
    # Uncomment sections below to demonstrate different techniques
    
    # techniques.demonstrate_goal_setting()
    # techniques.demonstrate_state_management()
    # techniques.demonstrate_memory_and_context()
    # techniques.demonstrate_error_handling()
    # techniques.demonstrate_user_centered_design()
    
    print("\nThis module demonstrates key design techniques for building effective agentic AI systems, including:")
    print("1. Goal setting and objective alignment")
    print("2. State management")
    print("3. Memory and context handling")
    print("4. Error handling and resilience")
    print("5. User-centered design principles")
    
    print("\nTo explore these techniques, uncomment the relevant demonstration sections in the script.")
    print("Each technique includes code examples and best practices for implementation.") 