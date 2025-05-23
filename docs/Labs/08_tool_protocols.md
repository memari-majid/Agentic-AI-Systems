# Lab 8: Tool Protocol Comparison

⏱️ **Estimated completion time: 35 minutes**

## Overview

This lab demonstrates different approaches to tool integration in agent frameworks, comparing OpenAI function calling, LangChain tools, and LangGraph tool nodes.

## Learning Objectives

- Understanding different tool integration schemas
- Converting between tool formats
- Implementing tools in various frameworks

## Key Concepts

### Tool Definition Approaches
1. **OpenAI Function Calling**: JSON schema-based definitions
2. **LangChain Tools**: Python decorator and class-based approaches  
3. **LangGraph Tool Nodes**: Graph-integrated tool execution

## Lab Code

```python
#!/usr/bin/env python3
"""
Tool Protocol Comparison Demo
Compare OpenAI, LangChain, and LangGraph tool integration approaches.
"""
import json
from typing import Dict, List, Optional

# Mock tool functions
def get_weather(location: str, date: Optional[str] = None) -> Dict:
    return {"location": location, "temperature": 22, "condition": "Sunny"}

def search_hotels(location: str, check_in: str, check_out: str) -> List[Dict]:
    return [{"name": "Grand Hotel", "price": 250, "rating": 4.5}]

# OpenAI Function Calling Format
openai_functions = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather information",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"},
                    "date": {"type": "string", "description": "Date (YYYY-MM-DD)"}
                },
                "required": ["location"]
            }
        }
    }
]

# LangChain Tool Definition (using decorator)
from langchain.tools import tool

@tool
def weather_tool(location: str, date: Optional[str] = None) -> Dict:
    """Get weather information for a location."""
    return get_weather(location, date)

# LangGraph Tool Node Integration
from langgraph.graph import StateGraph
from typing import TypedDict

class ToolState(TypedDict, total=False):
    query: str
    tool_requests: List[Dict]
    tool_results: List[Dict]
    response: str

def tool_execution_node(state: ToolState) -> ToolState:
    """Execute tools based on requests in state."""
    results = []
    for request in state.get("tool_requests", []):
        if request["tool"] == "weather":
            result = get_weather(**request["args"])
            results.append({"tool": "weather", "result": result})
    
    state["tool_results"] = results
    return state

def main():
    print("=== Tool Protocol Comparison ===")
    
    # Demonstrate OpenAI format
    print("\n1. OpenAI Function Calling:")
    print(json.dumps(openai_functions[0], indent=2))
    
    # Demonstrate LangChain tool
    print("\n2. LangChain Tool:")
    print(f"Name: {weather_tool.name}")
    print(f"Description: {weather_tool.description}")
    
    # Demonstrate LangGraph integration
    print("\n3. LangGraph Tool Node:")
    graph = StateGraph(ToolState)
    graph.add_node("tools", tool_execution_node)
    graph.set_entry_point("tools")
    graph.set_finish_point("tools")
    
    # Test the tool node
    state = {
        "tool_requests": [
            {"tool": "weather", "args": {"location": "London"}}
        ]
    }
    result = graph.compile().invoke(state)
    print(f"Tool result: {result['tool_results']}")

if __name__ == "__main__":
    main()
```

## How to Run

1. Save as `08_tool_protocols.py`
2. Install: `pip install langgraph langchain`
3. Run: `python 08_tool_protocols.py`

## Key Takeaways

- **OpenAI**: JSON schema for structured function definitions
- **LangChain**: Python-native tool definitions with decorators
- **LangGraph**: Tools as graph nodes for complex workflows

## Download Code

[Download 08_tool_protocols.py](08_tool_protocols.py){ .md-button .md-button--primary } 