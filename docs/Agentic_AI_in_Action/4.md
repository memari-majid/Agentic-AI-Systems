# Designing an Agentic System: LangChain + LangGraph in Action

⏱️ **Estimated reading time: 22 minutes**

Now, let's build a more practical agent that combines the strengths of LangChain for component creation and LangGraph for orchestration. We'll create a "Research Assistant" agent that can: 1. Take a research question. 2. Use a search tool to find relevant information. 3. Summarize the findings. 4. Present the summary.

This example will use a more realistic setup with LangChain agents and tools integrated into LangGraph nodes.

## System Development Methodology for Agentic AI

Before diving into the implementation, it's crucial to understand the systematic approach to developing agentic AI systems. This methodology ensures robust, maintainable, and scalable solutions that can evolve with changing requirements.

### Requirements Analysis for Agentic Systems

**Functional Requirements Identification**:
- **Agent Capabilities**: Define what the agent should be able to do (search, summarize, analyze, etc.)
- **Interaction Patterns**: Specify how users will interact with the agent (conversational, task-based, etc.)
- **Integration Needs**: Identify external systems, APIs, and data sources the agent must work with
- **Performance Expectations**: Set clear targets for response time, accuracy, and throughput

**Non-Functional Requirements**:
- **Scalability Requirements**: Expected user load, concurrent sessions, data volume
- **Reliability Requirements**: Uptime expectations, fault tolerance needs, recovery time objectives
- **Security Requirements**: Data privacy, access controls, audit trails, compliance needs
- **Usability Requirements**: User experience expectations, accessibility requirements

**Agent-Specific Considerations**:
```python
class AgentRequirements:
    def __init__(self):
        self.autonomy_level = "semi-autonomous"  # human-in-loop vs fully autonomous
        self.decision_boundaries = {
            "financial_threshold": 1000,  # max transaction without approval
            "confidence_threshold": 0.8,   # min confidence for autonomous action
            "escalation_triggers": ["legal_questions", "safety_concerns"]
        }
        self.knowledge_domains = ["general_web", "company_docs", "legal_compliance"]
        self.memory_requirements = {
            "session_memory": "full_conversation",
            "long_term_memory": "user_preferences_and_history",
            "shared_memory": "team_knowledge_base"
        }
```

### Iterative Development Approach

**Phase 1: Minimal Viable Agent (MVA)**:
- Start with basic functionality using simple prompts and limited tools
- Focus on core conversation flow and basic task completion
- Implement essential state management and error handling
- Get early user feedback on core functionality

**Phase 2: Enhanced Capabilities**:
- Add more sophisticated reasoning patterns
- Implement memory systems and context management
- Expand tool integration and error recovery
- Optimize for performance and reliability

**Phase 3: Production Readiness**:
- Implement comprehensive monitoring and logging
- Add security and compliance features
- Scale architecture for production loads
- Implement continuous learning and improvement

### Development Environment Setup

**Local Development Configuration**:
```python
# development_config.py
import os
from typing import Dict, Any

class DevelopmentConfig:
    def __init__(self):
        self.environment = "development"
        self.debug_mode = True
        self.logging_level = "DEBUG"
        
        # Model configurations for development
        self.models = {
            "primary": {
                "provider": "openai",
                "model": "gpt-4o-mini",  # cheaper for development
                "temperature": 0.1,
                "max_tokens": 500
            },
            "fallback": {
                "provider": "anthropic",
                "model": "claude-3-haiku",
                "temperature": 0.0
            }
        }
        
        # Development tool configurations
        self.tools = {
            "search": {
                "provider": "tavily",
                "max_results": 3,
                "timeout": 10
            },
            "memory": {
                "provider": "sqlite",  # local file for development
                "path": "./dev_memory.db"
            }
        }
        
        # Development-specific features
        self.features = {
            "enable_tracing": True,
            "mock_external_apis": True,
            "cache_responses": True,
            "detailed_logging": True
        }

def setup_development_environment():
    """Initialize development environment with proper configurations."""
    config = DevelopmentConfig()
    
    # Set up logging
    import logging
    logging.basicConfig(
        level=getattr(logging, config.logging_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('agent_development.log'),
            logging.StreamHandler()
        ]
    )
    
    # Initialize mock services for testing
    if config.features["mock_external_apis"]:
        setup_mock_services()
    
    return config
```

**Component Interface Specifications**:
- **Agent Interface**: Define clear contracts for agent inputs and outputs
- **Tool Interface**: Standardize tool registration, invocation, and error handling
- **State Interface**: Specify state schema and update patterns
- **Memory Interface**: Define storage and retrieval patterns for different memory types

### System Architecture Documentation

**Architecture Decision Records (ADRs)**:
```markdown
# ADR-001: State Management Approach

## Status
Accepted

## Context
Need to manage complex agent state across multiple interaction turns and potential system restarts.

## Decision
Use LangGraph's TypedDict state management with external persistence for long-term storage.

## Consequences
- Positive: Type safety, clear state schema, good debugging
- Negative: Requires careful schema evolution, potential serialization overhead
- Mitigation: Implement state migration strategies and efficient serialization
```

**Component Interaction Diagrams**:
- Define how different components (LLM, tools, memory, state) interact
- Specify data flow patterns and error propagation
- Document asynchronous operations and race condition handling

**Configuration Management**:
```python
class AgentSystemConfig:
    def __init__(self, environment: str = "development"):
        self.environment = environment
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration based on environment."""
        base_config = self._load_base_config()
        env_config = self._load_environment_config(self.environment)
        return {**base_config, **env_config}
    
    def get_model_config(self, model_type: str = "primary"):
        """Get model configuration with fallbacks."""
        return self.config["models"].get(model_type, self.config["models"]["fallback"])
    
    def get_tool_config(self, tool_name: str):
        """Get tool-specific configuration."""
        return self.config["tools"].get(tool_name, {})
```

### Development Best Practices

**Code Organization Patterns**:
```
agentic_system/
├── core/
│   ├── agent.py           # Main agent orchestration
│   ├── state.py           # State management
│   └── config.py          # Configuration management
├── tools/
│   ├── base.py            # Tool interface definitions
│   ├── search.py          # Search tool implementations
│   └── analysis.py        # Analysis tool implementations
├── memory/
│   ├── managers.py        # Memory management
│   ├── stores.py          # Storage backends
│   └── retrieval.py       # Retrieval strategies
├── utils/
│   ├── logging.py         # Logging utilities
│   ├── monitoring.py      # Performance monitoring
│   └── testing.py         # Testing utilities
└── tests/
    ├── unit/              # Unit tests
    ├── integration/       # Integration tests
    └── end_to_end/        # E2E tests
```

**Version Control Strategies**:
- **Configuration Versioning**: Track changes to agent configurations and prompts
- **Model Versioning**: Maintain compatibility across different model versions
- **State Schema Versioning**: Handle evolution of state structures
- **API Versioning**: Ensure backward compatibility for agent interfaces

**Documentation Standards**:
- **Agent Behavior Documentation**: Clear descriptions of what the agent does and doesn't do
- **Tool Documentation**: Comprehensive documentation for all tool integrations
- **State Schema Documentation**: Clear definitions of all state fields and their purposes
- **Error Handling Documentation**: Document all error conditions and recovery strategies

This systematic development approach ensures that agentic systems are built with clear requirements, proper architecture, and maintainable code from the start. Now let's see how these principles apply to our Research Assistant implementation.

### 4.1. Step 1: Define the Agent's State
Our agent needs to keep track of several pieces of information as it works through the research task. We'll define a state object using `TypedDict`.

```python
from typing import TypedDict, Annotated, Sequence, List, Optional
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
import operator

class ResearchAgentState(TypedDict):
    # Input question from the user
    input_question: str

    # Messages form the conversation history. operator.add appends to this list.
    messages: Annotated[Sequence[BaseMessage], operator.add]

    # The most recent search query generated by the agent
    search_query: Optional[str]

    # List of documents found by the search tool (simplified as strings for this example)
    search_results: Optional[List[str]]

    # The final summary of the research
    summary: Optional[str]

    # To control flow: which node to go to next?
    next_node: Optional[str]
```
### 4.2. Step 2: Define Agent Components (LangChain)
We need: - An LLM and tools. - An agent runnable (built with `create_openai_tools_agent`) that decides what to do (search or summarize). - A tool executor to run the chosen tools.

**a) Tools**

We'll use a real search tool (`TavilySearchResults`) and create a custom LangChain chain for summarization, which we'll wrap as a tool.

```python
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.output_parsers import StrOutputParser

# Ensure you have TAVILY_API_KEY set in your environment variables for TavilySearchResults
# os.environ["TAVILY_API_KEY"] = "your_tavily_api_key"
# os.environ["OPENAI_API_KEY"] = "your_openai_api_key"

# Initialize the LLM for the agent and summarizer
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 1. Search Tool
# Tavily Search is a good general-purpose search tool.
# Make sure to install: pip install langchain-community tavily-python
search_tool = TavilySearchResults(max_results=3) # Get top 3 results
search_tool.name = "web_search" # Give it a clear name for the agent
search_tool.description = "Searches the web for up-to-date information on a given query. Use this for recent events or general knowledge questions."

# 2. Summarization Tool (as a LangChain chain)
@tool
def summarize_text_tool(text_to_summarize: str, query: str) -> str:
    """Summarizes the provided text to answer the specific query. 
    Use this after performing a web search to extract relevant information from the search results based on the original query.
    Args:
        text_to_summarize: The text content retrieved from a web search (or part of it).
        query: The original user query to focus the summary on.
    """
    summarizer_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert summarizer. Your goal is to create a concise summary of the provided text, specifically focusing on answering the given query. Extract key information relevant to the query."),
        ("user", "Please summarize the following text:\n\n{text_to_summarize}\n\nBased on this query: {query}")
    ])
    summarization_chain = summarizer_prompt | llm | StrOutputParser()
    return summarization_chain.invoke({"text_to_summarize": text_to_summarize, "query": query})

research_assistant_tools = [search_tool, summarize_text_tool]
```
**b) Agent Runnable**

This LangChain agent will be the "brain" in one of our LangGraph nodes. It takes the current state (especially messages) and decides whether to call `web_search`, `summarize_text_tool`, or if it has enough information to respond.

```python
from langchain.agents import create_openai_tools_agent

# Prompt for the agent that decides the next step
# Note: The system message is crucial for guiding the agent's behavior with LangGraph.
# It needs to understand it's part of a larger process.
PLANNER_AGENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are a research assistant planner. Your goal is to answer the user's question by orchestrating a sequence of actions: searching the web and then summarizing the results.
"
     "Based on the current conversation and state, decide the next action. You have two tools available: 'web_search' and 'summarize_text_tool'.
"
     "1. If you need to find information, call 'web_search' with a relevant search query.
"
     "2. If you have search results and need to summarize them to answer the user's original question, call 'summarize_text_tool'. Provide the concatenated search results as 'text_to_summarize' and the original user question as 'query'.
"
     "3. If you have already summarized the information and have a final answer, or if the question can be answered directly without tools, respond to the user directly without calling any tools.
"
     "Consider the user's input question and the current messages to understand the context and what has been done so far."
    ),
    # MessagesPlaceholder(variable_name="messages"), # create_openai_tools_agent will add this
    ("user", "{input_question}") # The initial question is the main input
])

# Create the LangChain agent runnable
# This agent will output AIMessage objects, possibly with tool_calls
planner_agent_runnable = create_openai_tools_agent(llm, research_assistant_tools, PLANNER_AGENT_PROMPT)
```
### 4.3. Step 3: Define Graph Nodes (LangGraph)
Each node in our LangGraph will perform a specific part of the research task. Nodes take the current `ResearchAgentState` and return a dictionary of state updates.

**a) planner_node**

This node hosts our LangChain agent. It decides the next action (search, summarize, or finish).

```python
def planner_node(state: ResearchAgentState) -> dict:
    print("--- Planner Node ---")
    # Call the LangChain agent runnable
    # We pass the current messages and the input_question
    # The agent decides if it needs to call a tool or can respond directly
    agent_response: AIMessage = planner_agent_runnable.invoke(
        {"input_question": state["input_question"], "messages": state["messages"]}
    )

    updates = {"messages": [agent_response]} # Always update messages

    if agent_response.tool_calls:
        print(f"Planner agent decided to call tool(s): {agent_response.tool_calls}")
        # If the agent wants to call a tool, set next_node to tool_executor
        updates["next_node"] = "tool_executor"
    else:
        print("Planner agent decided to respond directly or has finished.")
        # If no tool call, it means the agent is ready to provide the final answer (or an intermediate one)
        # For this example, we'll assume it means the process is done or leads to a final response node.
        updates["next_node"] = "__end__" # Or route to a dedicated final response node
        updates["summary"] = agent_response.content # Assume direct response is the summary

    return updates
```
**b) tool_executor_node**

This node executes the tool chosen by the `planner_node`.

```python
from langchain_core.tools import BaseTool # For type hinting

# A simple tool executor that calls the LangChain tools
# In more complex scenarios, LangGraph offers a prebuilt ToolNode or ToolExecutor.

def tool_executor_node(state: ResearchAgentState) -> dict:
    print("--- Tool Executor Node ---")
    last_message = state["messages"][-1]
    if not isinstance(last_message, AIMessage) or not last_message.tool_calls:
        print(" Error: No tool call found in the last message.")
        return {"next_node": "planner", "messages": [AIMessage(content="Error: No tool call found")]}

    tool_call = last_message.tool_calls[0] # Assuming one tool call for simplicity
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    print(f" Executing tool: {tool_name} with args: {tool_args}")

    executed_tool: Optional[BaseTool] = None
    if tool_name == "web_search":
        executed_tool = search_tool
    elif tool_name == "summarize_text_tool":
        executed_tool = summarize_text_tool
    else:
        error_msg = f"Error: Unknown tool '{tool_name}' requested."
        print(error_msg)
        return {"messages": [ToolMessage(content=error_msg, tool_call_id=tool_call["id"])], "next_node": "planner"}

    try:
        # Invoke the tool
        if tool_name == "web_search":
            # Tavily tool expects a single string argument for the query
            tool_output = executed_tool.invoke(tool_args.get("query") or tool_args) 
        elif tool_name == "summarize_text_tool":
            # Our custom summarize tool takes specific arguments
            tool_output = executed_tool.invoke(tool_args)
        else: # Should not happen due to check above
            raise ValueError(f"Tool {tool_name} invocation not handled correctly.")

        print(f" Tool '{tool_name}' output received.")
        # Create a ToolMessage with the output
        tool_message = ToolMessage(content=str(tool_output), tool_call_id=tool_call["id"])

        updates = {"messages": [tool_message], "next_node": "planner"} # Go back to planner to process tool output

        # Update state based on tool executed
        if tool_name == "web_search":
            # The output of TavilySearchResults is a list of dicts, or a string on error.
            # For simplicity, let's assume it's a list of strings (page contents or snippets)
            if isinstance(tool_output, list):
                # Extract content from search results (Tavily returns dicts with 'content')
                contents = [res.get("content", "") for res in tool_output if isinstance(res, dict)]
                updates["search_results"] = contents
            else: # If it's a string (e.g. error message or single result)
                 updates["search_results"] = [str(tool_output)]
        elif tool_name == "summarize_text_tool":
            updates["summary"] = str(tool_output)
            updates["next_node"] = "__end__" # Summarization is the last step in this simple flow

        return updates

    except Exception as e:
        print(f" Error executing tool {tool_name}: {e}")
        error_message = ToolMessage(content=f"Error executing tool {tool_name}: {e}", tool_call_id=tool_call["id"])
        return {"messages": [error_message], "next_node": "planner"}
```
### 4.4. Step 4: Define Graph Edges (LangGraph)
Now we connect the nodes to define the workflow.

```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(ResearchAgentState)

# Add nodes
workflow.add_node("planner", planner_node)
workflow.add_node("tool_executor", tool_executor_node)

# Set entry point
workflow.set_entry_point("planner")

# Define conditional edges
def route_after_planner(state: ResearchAgentState):
    # Based on the 'next_node' field updated by planner_node or tool_executor_node
    if state.get("next_node") == "tool_executor":
        return "tool_executor"
    # If summary is present and no specific next node, or next_node is __end__
    if state.get("summary") or state.get("next_node") == "__end__":
        return END
    return "planner" # Default fallback or if planner needs to re-evaluate

def route_after_tool_executor(state: ResearchAgentState):
    # After tool execution, always go back to the planner to decide the next step
    # unless the tool executor itself (like summarize_text_tool) decided to end.
    if state.get("next_node") == "__end__":
         return END
    return "planner"

workflow.add_conditional_edges(
    "planner",
    route_after_planner,
    {
        "tool_executor": "tool_executor",
        END: END
        # Implicitly, if route_after_planner returns "planner", it stays or re-evaluates (not ideal, ensure explicit routing)
        # Better: ensure planner always sets a clear next_node or leads to END
    }
)

workflow.add_conditional_edges(
    "tool_executor",
    route_after_tool_executor,
    {
        "planner": "planner",
        END: END
    }
)

# Compile the graph
research_app = workflow.compile()
```
### 4.5. Step 5: Run the Agentic System
Let's test our research assistant!

```python
# Example Run
if __name__ == '__main__':
    initial_input = "What are the recent advancements in Large Language Models in 2024?"
    initial_state = {
        "input_question": initial_input,
        "messages": [HumanMessage(content=initial_input)]
        # Other fields (search_query, search_results, summary, next_node) will be populated by the graph
    }

    print(f"Starting research for: '{initial_input}'
")
    # Stream the execution to see the flow. research_app.invoke can also be used.
    for event in research_app.stream(initial_state, {"recursion_limit": 10}): # recursion_limit to prevent infinite loops
        for node_name, output_state in event.items():
            print(f"--- Output from Node: {node_name} ---")
            # Print relevant parts of the state updated by this node
            if output_state.get("messages"):
                print(f"  Messages: {output_state['messages'][-1]}") # Last message from this step
            if output_state.get("search_query"):
                print(f"  Search Query: {output_state['search_query']}")
            if output_state.get("search_results"):
                print(f"  Search Results (first one): {output_state['search_results'][0] if output_state['search_results'] else 'N/A'}")
            if output_state.get("summary"):
                print(f"  Summary: {output_state['summary']}")
            if output_state.get("next_node"):
                print(f"  Next Node: {output_state['next_node']}")
            print("--------------------------------------
")

    final_state = research_app.invoke(initial_state, {"recursion_limit": 10})
    print("
--- Final Research Result ---")
    if final_state.get("summary"):
        print(f"Summary: {final_state['summary']}")
    else:
        # If no summary, print the last AI message if available
        last_ai_message = next((m for m in reversed(final_state.get("messages", [])) if isinstance(m, AIMessage) and not m.tool_calls), None)
        if last_ai_message:
            print(f"Final Output: {last_ai_message.content}")
        else:
            print("No summary or direct answer found in the final state.")
```
This research assistant example demonstrates how LangChain components (agents, tools, chains) can be plugged into a LangGraph structure for more controlled, stateful, and observable agentic behavior. You can extend this by adding more tools, more complex routing logic, human-in-the-loop steps, or cycles for refinement. 