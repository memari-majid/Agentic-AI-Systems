#!/usr/bin/env python3
# Chapter 3 – Essential Components of Intelligent Agents
# ---

# Utility Functions
# The code sample below demonstrates a simple utility function for our travel booking example.

import random

def travel_utility_function(travel_option):
    """
    A utility function that evaluates travel options based on price,
    comfort, and convenience.
    """
    price_utility = (1000 - travel_option['price']) * 0.05  # Lower price is better
    comfort_utility = travel_option['comfort_rating'] * 10
    convenience_utility = travel_option['convenience_score'] * 15
    
    total_utility = price_utility + comfort_utility + convenience_utility
    
    return total_utility

# Define some example travel options
travel_options = [
    {
        'name': 'Budget Airline',
        'price': 300,
        'comfort_rating': 3,
        'convenience_score': 2
    },
    {
        'name': 'Premium Airline',
        'price': 800,
        'comfort_rating': 8,
        'convenience_score': 7
    },
    {
        'name': 'Train',
        'price': 200,
        'comfort_rating': 6,
        'convenience_score': 5
    },
    {
        'name': 'Road Trip',
        'price': 150,
        'comfort_rating': 4,
        'convenience_score': 3
    }
]

# Calculate and print the utility for each travel option
def print_travel_options():
    for option in travel_options:
        utility = travel_utility_function(option)
        print(f"Option: {option['name']}")
        print(f"Price: ${option['price']}, Comfort: {option['comfort_rating']}/10, Convenience: {option['convenience_score']}/10")
        print(f"Utility: {utility:.2f}\n")

    # Find the best option based on utility
    best_option = max(travel_options, key=travel_utility_function)
    print(f"The best travel option according to our utility function is: {best_option['name']}")
    print(f"Its utility value is: {travel_utility_function(best_option):.2f}")


# Enhancing Agent Capabilities with Generative AI
# ---

# Start building Agentic AI
# In order to be able to use the code below, you must sign-up with OpenAI to create a developer account
# to get access to the GPT model(s). Head over to the website https://platform.openai.com/ and sign-up.
# Once you are signed up, you must add a credit-card and create a new project to get a project key.
# Refer to Open AI documentation for more details.

# Install dependencies:
# pip install -U openai ipywidgets

def book_flight(passenger_name: str, 
               from_city: str, 
               to_city: str, 
               travel_date: str) -> str:
    # simply returns a string
    return {"response": f"A {travel_date} flight has been booked from {from_city} to {to_city} for {passenger_name}"}

# We define a tool with the function above and let the LLM know that it has this tool
# to make the flight booking. The LLM will only use this function if all the function 
# parameters are available, otherwise it will ask followup questions.

from openai import OpenAI
import json

# You need to provide your own API key
# api_key = "your-api-key-here"  # Replace with your actual API key
# openai = OpenAI(api_key=api_key)

tools = [{
        "type": "function",
        "function":{
            "name": "book_flight",
            "description": "Book a flight for the customer. Call this whenever you need to book a flight, for example when a customer asks 'I want to book a flight from Los Angeles to New York'",
            "parameters": {
                "type": "object",
                "properties": {
                    "from_city": {
                        "type": "string",
                        "description": "The departure city.",
                    },
                    "to_city": {
                        "type": "string",
                        "description": "The arrival city.",
                    },
                    "travel_date": {
                        "type": "string",
                        "description": "The date of travel.",
                    },
                    "passenger_name": {
                        "type": "string",
                        "description": "The passenger's legal name.",
                    },
                },
                "required": ["passenger_name","from_city", "to_city", "travel_date"],
                "additionalProperties": False,
            }
    }
}]

# This is the main function that calls the LLM
def travel_agent(user_message: str, messages: list, openai_client=None) -> str:
    if openai_client is None:
        raise ValueError("OpenAI client is required. Please provide your API key.")
        
    messages.append({"role": "user", "content": user_message})
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            tools=tools
        )        
        if response.choices[0].message.content:
            return response.choices[0].message.content
        elif response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            arguments = json.loads(tool_call.function.arguments)
            from_city = arguments.get('from_city')
            to_city = arguments.get('to_city')
            travel_date = arguments.get('travel_date')
            passenger_name = arguments.get('passenger_name')
            
            # Call our travel booking function that we defined earlier
            booking_confirmation = book_flight(passenger_name=passenger_name, from_city=from_city, to_city=to_city, travel_date=travel_date)

            function_call_result_message = {
                "role": "tool",
                "content": json.dumps({
                    "confirmation_message": booking_confirmation,
                }),
                "tool_call_id": response.choices[0].message.tool_calls[0].id
            }
            messages.append(response.choices[0].message)
            messages.append(function_call_result_message)
            response = openai_client.chat.completions.create(
                            model="gpt-4-turbo",
                            messages=messages,                            
                        )
            return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Example usage:
if __name__ == "__main__":
    # First demonstrate the travel utility function
    print("UTILITY FUNCTION DEMONSTRATION:")
    print("-" * 40)
    print_travel_options()
    
    print("\n\nOPENAI AGENT DEMONSTRATION:")
    print("-" * 40)
    print("To use the OpenAI agent, you need to:")
    print("1. Install required packages: pip install -U openai ipywidgets")
    print("2. Set your OpenAI API key")
    print("3. Initialize the OpenAI client")
    print("4. Run the agent with a sample conversation")
    print("\nSample code:")
    print("""
    import getpass
    api_key = getpass.getpass(prompt="Enter OpenAI API Key: ")
    openai_client = OpenAI(api_key=api_key)
    
    messages = [
        {"role": "system", "content": \"\"\"You are a helpful travel agent assistant. 
         Use the supplied tools to assist the customer. 
         If you don't have enough information to book, just ask. 
         When you have the travel cities, dates and name, you can use the tool to book the ticket.\"\"\"},
    ]
    
    response = travel_agent("I want to book a flight", messages, openai_client)
    print(f"Agent: {response}")
    """) 