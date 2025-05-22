#!/usr/bin/env python3
# Chapter 4 – Reflection and Introspection in Agents

# Required dependencies:
# pip install -U openai crewai pysqlite3-binary

import random
import os

# 1. Meta Reasoning - example
# Let's take a look at a simple meta-reasoning approach without AI.

# Simulated travel agent with meta-reasoning capabilities
class ReflectiveTravelAgent:
    def __init__(self):
        # Initialize preference weights that determine how user preferences influence recommendations
        self.preferences_weights = {
            "budget": 0.5,    # Weight for budget-related preferences
            "luxury": 0.3,    # Weight for luxury-related preferences
            "adventure": 0.2  # Weight for adventure-related preferences
        }
        self.user_feedback = []  # List to store user feedback for meta-reasoning

    def recommend_destination(self, user_preferences):
        """
        Recommend a destination based on user preferences and internal weightings.

        Args:
            user_preferences (dict): User's preferences with keys like 'budget', 'luxury', 'adventure'

        Returns:
            str: Recommended destination
        """
        # Calculate scores for each destination based on weighted user preferences
        score = {
            "Paris": (self.preferences_weights["luxury"] * user_preferences["luxury"] + 
                      self.preferences_weights["adventure"] * user_preferences["adventure"]),
            "Bangkok": (self.preferences_weights["budget"] * user_preferences["budget"] +
                        self.preferences_weights["adventure"] * user_preferences["adventure"]),
            "New York": (self.preferences_weights["luxury"] * user_preferences["luxury"] +
                         self.preferences_weights["budget"] * user_preferences["budget"])
        }
        # Select the destination with the highest calculated score
        recommendation = max(score, key=score.get)
        return recommendation

    def get_user_feedback(self, actual_experience):
        """
        Simulate receiving user feedback and trigger meta-reasoning to adjust recommendations.

        Args:
            actual_experience (str): The destination the user experienced
        """
        # Simulate user feedback: 1 for positive, -1 for negative
        feedback = random.choice([1, -1])
        print(f"Feedback for {actual_experience}: {'Positive' if feedback == 1 else 'Negative'}")
        
        # Store the feedback for later analysis
        self.user_feedback.append((actual_experience, feedback))
        
        # Trigger meta-reasoning to adjust the agent's reasoning process based on feedback
        self.meta_reasoning()

    def meta_reasoning(self):
        """
        Analyze collected feedback and adjust preference weights to improve future recommendations.
        This simulates the agent reflecting on its reasoning process and making adjustments.
        """
        for destination, feedback in self.user_feedback:
            if feedback == -1:  # Negative feedback indicates dissatisfaction
                # Reduce the weight of the main attribute associated with the destination
                if destination == "Paris":
                    self.preferences_weights["luxury"] *= 0.9  # Decrease luxury preference
                elif destination == "Bangkok":
                    self.preferences_weights["budget"] *= 0.9  # Decrease budget preference
                elif destination == "New York":
                    self.preferences_weights["budget"] *= 0.9  # Decrease budget preference
            elif feedback == 1:  # Positive feedback indicates satisfaction
                # Increase the weight of the main attribute associated with the destination
                if destination == "Paris":
                    self.preferences_weights["luxury"] *= 1.1  # Increase luxury preference
                elif destination == "Bangkok":
                    self.preferences_weights["budget"] *= 1.1  # Increase budget preference
                elif destination == "New York":
                    self.preferences_weights["budget"] *= 1.1  # Increase budget preference

        # Normalize weights to ensure they sum up to 1 for consistency
        total_weight = sum(self.preferences_weights.values())
        for key in self.preferences_weights:
            self.preferences_weights[key] /= total_weight

        # Display updated weights after meta-reasoning adjustments
        print(f"Updated weights: {self.preferences_weights}\n")


def simulate_reflective_agent():
    """Simulate the reflective agent's behavior and meta-reasoning"""
    agent = ReflectiveTravelAgent()

    # User's initial preferences
    user_preferences = {
        "budget": 0.8,      # High preference for budget-friendly options
        "luxury": 0.2,      # Low preference for luxury
        "adventure": 0.5    # Moderate preference for adventure activities
    }

    # First recommendation based on initial preferences and weights
    recommended = agent.recommend_destination(user_preferences)
    print(f"Recommended destination: {recommended}")

    # Simulate user experience and provide feedback
    agent.get_user_feedback(recommended)

    # Second recommendation after adjusting weights based on feedback
    recommended = agent.recommend_destination(user_preferences)
    print(f"Updated recommendation: {recommended}")


# 2. Self Explanation - example with OpenAI

def demonstrate_self_explanation(api_key=None):
    """
    Demonstrate how an agent can explain its reasoning when making decisions.
    This provides transparency into the decision-making process.
    
    Args:
        api_key: Optional OpenAI API key. If not provided, will prompt for it.
    """
    try:
        import openai
        
        # Set up API key
        if api_key is None:
            import getpass
            api_key = getpass.getpass(prompt="Enter OpenAI API Key: ")
        os.environ["OPENAI_API_KEY"] = api_key
            
        # Mock data for the travel recommendation
        user_preferences = {
            "location": "Paris",
            "budget": 200,
            "preferences": ["proximity to attractions", "user ratings"],
        }

        # Input reasoning factors for the GPT model
        reasoning_prompt = f"""
        You are an AI-powered travel assistant. Explain your reasoning behind a hotel recommendation for a user traveling to {user_preferences['location']}.
        Consider:
        1. Proximity to popular attractions.
        2. High ratings from similar travelers.
        3. Competitive pricing within ${user_preferences['budget']} budget.
        4. Preferences: {user_preferences['preferences']}.
        Provide a clear, transparent self-explanation.
        """

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a reflective travel assistant."},
                {"role": "user", "content": reasoning_prompt},
            ]
        )

        # Print self-explanation
        print("Agent Self-Explanation:")
        print(response.choices[0].message.content)
        
    except ImportError:
        print("OpenAI package not installed. Run 'pip install openai' to use this function.")
    except Exception as e:
        print(f"Error demonstrating self-explanation: {e}")


# 3. CrewAI Implementation Examples
# This is a simplified version without running the full crew implementation
# since it requires additional setup and API keys

def explain_crewai_implementation():
    """Explain how CrewAI can be used for reflection and introspection"""
    print("""
CrewAI Implementation for Reflection and Introspection

CrewAI allows creating a team of specialized agents that work together:

1. Tool-based agents can:
   - Recommend destinations based on user preferences
   - Emulate user feedback on recommendations
   - Update internal weights based on feedback for future recommendations

2. Agent roles typically include:
   - Recommendation Agent: Makes initial recommendations based on preferences
   - Feedback Agent: Simulates or processes user feedback
   - Meta-Reasoning Agent: Adjusts internal weights based on feedback

3. The workflow connects these agents together:
   - First agent recommends destinations based on preferences
   - Second agent provides/processes feedback on recommendations
   - Third agent reasons about the feedback and updates weights

This approach allows for:
- Continuous learning from user feedback
- Transparent reasoning about decisions
- Progressive improvement of recommendations over time

To implement this with CrewAI, you would:
1. Define tools for each function
2. Create agents with specific roles
3. Define tasks that connect outputs between agents
4. Create a crew to orchestrate the workflow
""")


if __name__ == "__main__":
    print("Chapter 4 - Reflection and Introspection in Agents\n")
    
    print("Example 1: Meta-reasoning with a simulated travel agent")
    print("-" * 60)
    simulate_reflective_agent()
    
    print("\nExample 2: Self-explanation with GPT")
    print("-" * 60)
    print("Requires OpenAI API key. To run this example, uncomment the line below:")
    print("# demonstrate_self_explanation()")
    
    print("\nExample 3: CrewAI for reflection and introspection")
    print("-" * 60)
    explain_crewai_implementation() 