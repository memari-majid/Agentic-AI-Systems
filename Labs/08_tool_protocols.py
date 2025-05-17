#!/usr/bin/env python3
"""
Chapter 8 - Tool Protocol Comparison
-----------------------------------
This example demonstrates different approaches to tool integration in agent frameworks:
1. OpenAI function calling schema
2. LangChain tool definitions
3. LangGraph tool node integration

Key concepts:
- Schema formats for tool definitions
- Docstring vs JSON schema approaches
- Integration patterns in different frameworks
- Conversion between tool formats
"""
import argparse
import json
import os
import time
from enum import Enum
from typing import Dict, List, Optional, TypedDict, Union
from datetime import datetime

try:
    # For OpenAI tool definition example
    from openai import OpenAI
except ImportError:
    # Mock class for when OpenAI package isn't available
    class OpenAI:
        def __init__(self, *args, **kwargs):
            pass

# LangChain tools import for examples
try:
    from langchain.tools import BaseTool, StructuredTool, tool
except ImportError:
    # Mock class hierarchy for when LangChain isn't available
    class BaseTool:
        def __init__(self, name=None, description=None, func=None):
            self.name = name
            self.description = description
            self.func = func

    class StructuredTool(BaseTool):
        pass

    # Simple tool decorator for examples
    def tool(func=None, name=None, description=None):
        def decorator(f):
            f._tool_name = name or f.__name__
            f._tool_description = description or f.__doc__
            return f
        return decorator if func is None else decorator(func)

# LangGraph imports for examples
try:
    from langgraph.graph import StateGraph
except ImportError:
    pass  # We'll skip LangGraph examples if not available

# ---------------------------------------------------------------------------
# Common tool functionality -------------------------------------------------
# ---------------------------------------------------------------------------

def get_weather(location: str, date: Optional[str] = None) -> Dict:
    """
    Get weather information for a location and date.
    
    Args:
        location: City or location name
        date: Date in YYYY-MM-DD format (defaults to today)
    
    Returns:
        Dict containing weather information
    """
    # Simulate API call latency
    time.sleep(0.1)
    
    # For demo purposes, generate mock weather data
    today = datetime.now().strftime("%Y-%m-%d")
    date = date or today
    
    # Return mock weather data
    return {
        "location": location,
        "date": date,
        "temperature": 22 if "London" in location else 28,
        "condition": "Partly Cloudy" if date == today else "Sunny",
        "humidity": 65,
        "wind_speed": 12,
    }

def search_hotels(location: str, check_in: str, check_out: str, max_price: Optional[int] = None) -> List[Dict]:
    """
    Search for hotels in a given location.
    
    Args:
        location: City or location name
        check_in: Check-in date (YYYY-MM-DD)
        check_out: Check-out date (YYYY-MM-DD)
        max_price: Maximum price per night (optional)
    
    Returns:
        List of hotel options
    """
    # Simulate API call latency
    time.sleep(0.2)
    
    # Mock hotel data
    hotels = [
        {
            "name": "Grand Hotel",
            "location": location,
            "price": 250,
            "rating": 4.5,
            "amenities": ["Pool", "Spa", "Restaurant"]
        },
        {
            "name": "Budget Inn",
            "location": location,
            "price": 120,
            "rating": 3.8,
            "amenities": ["Free WiFi", "Breakfast"]
        },
        {
            "name": "Luxury Suites",
            "location": location,
            "price": 380,
            "rating": 4.7,
            "amenities": ["Pool", "Spa", "Restaurant", "Gym", "Concierge"]
        }
    ]
    
    # Apply max price filter if provided
    if max_price:
        hotels = [h for h in hotels if h["price"] <= max_price]
    
    return hotels

def search_flights(origin: str, destination: str, date: str) -> List[Dict]:
    """
    Search for flights between locations.
    
    Args:
        origin: Departure city or airport code
        destination: Arrival city or airport code
        date: Departure date (YYYY-MM-DD)
    
    Returns:
        List of flight options
    """
    # Simulate API call latency
    time.sleep(0.3)
    
    # Mock flight data
    return [
        {
            "airline": "SkyLine Airways",
            "flight_number": "SL356",
            "origin": origin,
            "destination": destination,
            "departure_time": "08:30",
            "arrival_time": "10:45",
            "price": 320,
            "available_seats": 23
        },
        {
            "airline": "Global Air",
            "flight_number": "GA189",
            "origin": origin,
            "destination": destination,
            "departure_time": "12:20",
            "arrival_time": "14:30",
            "price": 475,
            "available_seats": 8
        },
        {
            "airline": "Swift Jet",
            "flight_number": "SJ901",
            "origin": origin,
            "destination": destination,
            "departure_time": "16:40",
            "arrival_time": "18:55",
            "price": 280,
            "available_seats": 5
        }
    ]

# ---------------------------------------------------------------------------
# OpenAI Function Calling Format --------------------------------------------
# ---------------------------------------------------------------------------

def define_openai_functions():
    """Define tools using OpenAI's function calling schema."""
    functions = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather information for a location and date",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City or location name"
                        },
                        "date": {
                            "type": "string",
                            "description": "Date in YYYY-MM-DD format (defaults to today)",
                            "format": "date"
                        }
                    },
                    "required": ["location"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_hotels",
                "description": "Search for hotels in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City or location name"
                        },
                        "check_in": {
                            "type": "string",
                            "description": "Check-in date (YYYY-MM-DD)",
                            "format": "date"
                        },
                        "check_out": {
                            "type": "string",
                            "description": "Check-out date (YYYY-MM-DD)",
                            "format": "date"
                        },
                        "max_price": {
                            "type": "integer",
                            "description": "Maximum price per night (optional)"
                        }
                    },
                    "required": ["location", "check_in", "check_out"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_flights",
                "description": "Search for flights between locations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "origin": {
                            "type": "string",
                            "description": "Departure city or airport code"
                        },
                        "destination": {
                            "type": "string",
                            "description": "Arrival city or airport code"
                        },
                        "date": {
                            "type": "string",
                            "description": "Departure date (YYYY-MM-DD)",
                            "format": "date"
                        }
                    },
                    "required": ["origin", "destination", "date"]
                }
            }
        }
    ]
    
    return functions

def demonstrate_openai_function_calling():
    """Demonstrate how to use OpenAI function calling."""
    # This example only shows the setup - not the actual API call
    functions = define_openai_functions()
    
    # Example of how you would use these functions with OpenAI
    print("\n=== OpenAI Function Calling Setup ===")
    print("Function definitions:")
    for func in functions:
        print(f"  - {func['function']['name']} : {func['function']['description']}")
    
    # In a real implementation, you would:
    if os.environ.get("OPENAI_API_KEY"):
        print("\nExample calling pattern (not executed):")
        print("""
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a travel assistant."},
        {"role": "user", "content": "What's the weather like in London?"}
    ],
    tools=functions,
    tool_choice="auto"
)

# Process the response
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)
    
    if function_name == "get_weather":
        weather_data = get_weather(**function_args)
        # Use the weather data in the assistant's response
        """)
    else:
        print("\nSet OPENAI_API_KEY environment variable to run actual OpenAI examples")

# ---------------------------------------------------------------------------
# LangChain Tool Format ----------------------------------------------------
# ---------------------------------------------------------------------------

# Method 1: Using the @tool decorator
@tool
def get_weather_tool(location: str, date: Optional[str] = None) -> Dict:
    """Get weather information for a location and date.
    
    Args:
        location: City or location name
        date: Date in YYYY-MM-DD format (defaults to today)
    """
    return get_weather(location, date)

# Method 2: Creating a structured tool
def search_hotels_tool():
    """Create a LangChain structured tool for hotel search."""
    return StructuredTool.from_function(
        func=search_hotels,
        name="search_hotels",
        description="Search for hotels in a given location",
    )

# Method 3: Creating a tool class
class FlightSearchTool(BaseTool):
    name = "search_flights"
    description = "Search for flights between locations"
    
    def _run(self, origin: str, destination: str, date: str):
        return search_flights(origin, destination, date)
    
    def _arun(self, origin: str, destination: str, date: str):
        # In a real implementation, this would be an async version
        raise NotImplementedError("Async version not implemented")

def demonstrate_langchain_tools():
    """Demonstrate different ways to define LangChain tools."""
    print("\n=== LangChain Tool Definitions ===")
    
    # Method 1: Using the @tool decorator
    print("\n1. Using @tool decorator:")
    print(f"   Name: {get_weather_tool.name}")
    print(f"   Description: {get_weather_tool.description}")
    
    # Method 2: Creating a structured tool
    hotel_tool = search_hotels_tool()
    print("\n2. Using StructuredTool.from_function:")
    print(f"   Name: {hotel_tool.name}")
    print(f"   Description: {hotel_tool.description}")
    
    # Method 3: Creating a tool class
    flight_tool = FlightSearchTool()
    print("\n3. Using BaseTool subclass:")
    print(f"   Name: {flight_tool.name}")
    print(f"   Description: {flight_tool.description}")
    
    # LangChain usage example
    print("\nExample usage in LangChain agent:")
    print("""
from langchain.agents import AgentExecutor, create_react_agent
from langchain.llms import OpenAI

tools = [get_weather_tool, search_hotels_tool(), FlightSearchTool()]
llm = OpenAI(temperature=0)

# Define the agent prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful travel assistant."),
    ("human", "{input}"),
    ("system", "Use the tools available to you to assist the user.")
])

# Create the agent
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Run the agent
agent_executor.invoke({"input": "What's the weather in Paris today?"})
""")

# ---------------------------------------------------------------------------
# LangGraph Tool Node Integration -------------------------------------------
# ---------------------------------------------------------------------------

class ToolState(TypedDict, total=False):
    query: str
    weather_request: Optional[Dict]
    weather_result: Optional[Dict]
    hotel_request: Optional[Dict]
    hotel_result: Optional[List[Dict]]
    flight_request: Optional[Dict]
    flight_result: Optional[List[Dict]]
    response: str

def demonstrate_langgraph_tools():
    """Demonstrate how tools are integrated in LangGraph."""
    print("\n=== LangGraph Tool Integration ===")
    print("In LangGraph, tools are typically implemented as nodes in the graph.")
    
    # Example of tool nodes in LangGraph
    print("\nExample node definitions:")
    print("""
def weather_tool_node(state: ToolState) -> ToolState:
    if state.get("weather_request"):
        request = state["weather_request"]
        result = get_weather(**request)
        state["weather_result"] = result
    return state

def hotel_tool_node(state: ToolState) -> ToolState:
    if state.get("hotel_request"):
        request = state["hotel_request"]
        result = search_hotels(**request)
        state["hotel_result"] = result
    return state

def flight_tool_node(state: ToolState) -> ToolState:
    if state.get("flight_request"):
        request = state["flight_request"]
        result = search_flights(**request)
        state["flight_result"] = result
    return state
""")
    
    # Example of graph construction
    print("\nExample graph construction:")
    print("""
def build_tool_graph() -> StateGraph:
    graph = StateGraph(ToolState)
    
    # Add tool nodes
    graph.add_node("weather_tool", weather_tool_node)
    graph.add_node("hotel_tool", hotel_tool_node)
    graph.add_node("flight_tool", flight_tool_node)
    
    # Decision node to determine which tool to use
    graph.add_node("router", router_node)
    
    # Set entry point
    graph.set_entry_point("router")
    
    # Add conditional edges from router to appropriate tool
    graph.add_conditional_edges(
        "router",
        route_to_tool,
        {
            "weather": "weather_tool",
            "hotel": "hotel_tool",
            "flight": "flight_tool",
            "response": None  # End of graph
        }
    )
    
    # Connect tools back to router
    graph.add_edge("weather_tool", "router")
    graph.add_edge("hotel_tool", "router")
    graph.add_edge("flight_tool", "router")
    
    return graph
""")
    
    # Using tool node with prebuilt tooling
    print("\nLangGraph also provides prebuilt ToolNode:")
    print("""
from langgraph.prebuilt import ToolNode

# Create a ToolNode that can execute multiple tools
tool_node = ToolNode([get_weather_tool, search_hotels_tool(), FlightSearchTool()])

# Add to graph
graph.add_node("tools", tool_node)
""")

# ---------------------------------------------------------------------------
# Protocol Conversion Functions ---------------------------------------------
# ---------------------------------------------------------------------------

def convert_openai_to_langchain(openai_function):
    """Convert an OpenAI function definition to a LangChain tool."""
    print("\n=== Converting OpenAI Function to LangChain Tool ===")
    
    function_def = openai_function["function"]
    name = function_def["name"]
    description = function_def["description"]
    
    print(f"Converting: {name}")
    print("""
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

# Define the input schema based on OpenAI function parameters
class {name}Input(BaseModel):
    {param_fields}
    
# Create the structured tool
{name}_tool = StructuredTool.from_function(
    func={original_func},
    name="{name}",
    description="{description}",
    args_schema={name}Input
)
""".format(
        name=name,
        description=description,
        param_fields="\n    ".join([
            f"{param}: {get_pydantic_type(props)} = Field(description=\"{props.get('description', '')}\")" 
            for param, props in function_def["parameters"]["properties"].items()
        ]),
        original_func=name
    ))

def get_pydantic_type(property_def):
    """Convert JSON Schema type to Python/Pydantic type."""
    type_map = {
        "string": "str",
        "integer": "int",
        "number": "float",
        "boolean": "bool",
        "array": "list",
        "object": "dict"
    }
    
    if property_def.get("type") in type_map:
        if property_def.get("type") == "string" and property_def.get("format") == "date":
            return "str  # date format"
        return type_map[property_def["type"]]
    return "Any"

# ---------------------------------------------------------------------------
# Main function -------------------------------------------------------------
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Tool Protocol Comparison")
    parser.add_argument("--protocol", choices=["openai", "langchain", "langgraph", "convert", "all"], 
                      default="all", help="Which tool protocol to demonstrate")
    args = parser.parse_args()
    
    print("\n=== Tool Protocol Comparison ===")
    print("This example shows how tools are defined in different frameworks.\n")
    
    if args.protocol in ["openai", "all"]:
        demonstrate_openai_function_calling()
    
    if args.protocol in ["langchain", "all"]:
        demonstrate_langchain_tools()
    
    if args.protocol in ["langgraph", "all"]:
        demonstrate_langgraph_tools()
    
    if args.protocol in ["convert", "all"]:
        # Demonstrate conversion between formats
        openai_funcs = define_openai_functions()
        convert_openai_to_langchain(openai_funcs[0])
    
    print("\n=== Protocol Comparison Summary ===")
    print("""
Approach          | Schema Format     | Typing Support    | Integration Pattern
------------------|-------------------|-------------------|-------------------
OpenAI Functions  | JSON Schema       | Limited           | Structured output parsing
LangChain Tools   | Python docstrings | Pydantic/Python   | Agent framework integration  
LangGraph Tools   | Graph nodes       | TypedDict/Python  | State transformation nodes

Each approach has strengths:
- OpenAI: Clean JSON schema, native integration with OpenAI models
- LangChain: Multiple definition styles, rich ecosystem integration
- LangGraph: Tool calls as explicit graph nodes with type safety
""")

if __name__ == "__main__":
    main() 