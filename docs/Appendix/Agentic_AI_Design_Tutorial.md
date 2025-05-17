# Agentic AI Design with LangChain and LangGraph

## 1. Introduction to Agentic AI

Agentic AI systems are applications that can perceive their environment, make decisions, and take actions to achieve specific goals. Unlike traditional programs that follow a fixed set of instructions, agentic systems exhibit a degree of autonomy and can adapt their behavior based on interactions and new information.

Key characteristics of agentic AI systems include:
- **Goal-Oriented:** They are designed to achieve specific objectives.
- **Interactive:** They can communicate with users or other systems and respond to inputs.
- **Autonomous:** They can operate without constant human intervention, making decisions and taking actions independently.
- **Perceptive:** They can process information from their environment (e.g., user queries, tool outputs, data sources).
- **Adaptive:** They can learn from interactions and modify their behavior over time (though this tutorial focuses more on explicit state management for adaptability).

Building robust agentic AI requires a combination of powerful language models, tools to interact with the external world, and a framework to orchestrate complex workflows. This is where LangChain and LangGraph come into play.

- **LangChain** provides the foundational building blocks for creating applications powered by language models. It offers components for managing models, prompts, tools, memory, and creating chains of operations. We'll use LangChain to define the individual capabilities of our agent (e.g., what tools it can use, how it processes information).
- **LangGraph** is built on top of LangChain and allows you to construct sophisticated, stateful agentic systems as graphs. It excels at managing complex flows of control, enabling cycles, human-in-the-loop interactions, and persistent state. We'll use LangGraph to define the overall decision-making process and workflow of our agent.

This tutorial will guide you through designing agentic AI systems by leveraging the strengths of both LangChain and LangGraph.

## 2. LangChain: The Foundation for Agents

LangChain helps create the core components that an agent will use. Think of these as the agent's skills or tools.

### 2.1. Core Idea: Building with Components

LangChain is designed around modular components that can be combined to create powerful applications. For agentic systems, the key components are:

### 2.2. Models

Language models are the brain of an agent. LangChain provides interfaces for various types:
- **LLMs (Large Language Models):** Take text in, return text out.
- **Chat Models:** More structured, take a list of messages, return a message. These are commonly used for agents.
- **Text Embedding Models:** Convert text to numerical representations for semantic search.

```python
from langchain_openai import OpenAI, ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings

# Initialize a Chat Model (commonly used for agents)
chat_model = ChatOpenAI(model="gpt-4", temperature=0)

# Example of an LLM
llm = OpenAI(temperature=0.7)

# Example of an Embedding Model
embeddings = HuggingFaceEmbeddings()
```

### 2.3. Prompts

Prompts are how we instruct the model. For agents, prompts often define the agent's persona, its objectives, and how it should use tools.

```python
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

# Chat prompt template for an agent
agent_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. You have access to tools. Use them when necessary."),
    ("user", "{input}")
])

# Example of a simpler prompt
prompt_template = PromptTemplate.from_template("Tell me about {topic}.")
```

### 2.4. Tools: Enabling Agents to Act

Tools are interfaces that allow agents to interact with the outside world (e.g., search the web, run code, access databases). LangChain makes it easy to define and use tools.

The `@tool` decorator is a convenient way to create tools from functions:

```python
from langchain_core.tools import tool

@tool
def search_wikipedia(query: str) -> str:
    """Searches Wikipedia for the given query and returns the summary of the first result."""
    # In a real scenario, you would use the Wikipedia API
    # from wikipediaapi import Wikipedia
    # wiki_wiki = Wikipedia('MyAgent/1.0 (myemail@example.com)', 'en')
    # page = wiki_wiki.page(query)
    # if page.exists():
    #     return page.summary[0:500] # Return first 500 chars of summary
    # return f"Could not find information on Wikipedia for '{query}'."
    return f"Simulated Wikipedia search for '{query}': LangChain is a framework for developing applications powered by language models."

@tool
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {str(e)}"

# List of tools for an agent
agent_tools = [search_wikipedia, calculator]
```

### 2.5. Output Parsers

Output parsers convert the raw output from an LLM into a more structured format (e.g., JSON, a specific object). This is crucial for agents to reliably extract information or decide on actions.

```python
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

# Simple string output
string_parser = StrOutputParser()

# For structured output (e.g., an agent deciding which tool to call)
class AgentAction(BaseModel):
    tool_name: str = Field(description="The name of the tool to use.")
    tool_input: str = Field(description="The input for the tool.")

json_parser = JsonOutputParser(pydantic_object=AgentAction)
```
While `JsonOutputParser` can be used, agents created with functions like `create_openai_tools_agent` often handle tool invocation structures internally.

### 2.6. Memory (Brief Overview)

Memory allows agents to remember past interactions. While LangChain offers various memory modules, LangGraph's state management provides a more explicit and flexible way to handle memory and state for complex agents, as we'll see later.

LangChain memory types include:
- `ConversationBufferMemory`: Remembers all past messages.
- `ConversationBufferWindowMemory`: Remembers the last K messages.
- `ConversationSummaryMemory`: Creates a summary of the conversation.

We will primarily use LangGraph's state for managing memory in our agentic designs.

### 2.7. Basic Agent Construction with LangChain

LangChain provides functions to quickly create agents. `create_openai_tools_agent` (and similar functions for other model providers) are recommended for building agents that can use tools. These agents are designed to work with models that support tool calling (like newer OpenAI models).

```python
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Re-define tools if not in scope
# @tool
# def search_wikipedia(query: str) -> str: ...
# @tool
# def calculator(expression: str) -> str: ...
# agent_tools = [search_wikipedia, calculator]

# Initialize the Chat Model
llm = ChatOpenAI(model="gpt-4", temperature=0) # Using a specific model known for good tool use

# Define the prompt for the agent
# This prompt template expects 'input' and 'agent_scratchpad' (for intermediate steps)
# and also includes messages for chat history if needed.
# For tool calling agents, the prompt structure can be simpler as the model handles much of the reasoning.
AGENT_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. You have access to the following tools: search_wikipedia, calculator. Only use these tools when necessary to answer the user's question. Respond directly if you know the answer or the tools are not helpful."),
        ("user", "{input}"),
        # MessagesPlaceholder(variable_name="agent_scratchpad"), # create_openai_tools_agent handles this
    ]
)

# Create the agent
# This binds the LLM, tools, and prompt together.
# The agent runnable itself decides which tool to call, or to respond directly.
agent_runnable = create_openai_tools_agent(llm, agent_tools, AGENT_PROMPT)

# The AgentExecutor runs the agent, executes tools, and feeds results back to the agent
# until a final answer is produced.
agent_executor = AgentExecutor(agent=agent_runnable, tools=agent_tools, verbose=True)

# Example usage
# response = agent_executor.invoke({"input": "What is the capital of France and what is 2 + 2?"})
# print(response["output"])

# response_wikipedia = agent_executor.invoke({"input": "What is LangChain?"})
# print(response_wikipedia["output"])
```

While this `AgentExecutor` is powerful, managing more complex sequences of actions, conditional logic based on multi-step history, explicit state tracking beyond chat history, or incorporating human feedback loops can become challenging. This is where LangGraph provides a more robust framework for orchestration.

Next, we will explore LangGraph and how it allows us to build more sophisticated agentic workflows.

## 3. LangGraph: Orchestrating Complex Agentic Behavior

While LangChain provides the tools to build agents, LangGraph provides the framework to orchestrate them, especially when the agent's behavior involves multiple steps, conditional logic, loops, or requires explicit state management beyond simple chat history.

### 3.1. Why LangGraph?

Simple agent loops, like the `AgentExecutor` shown previously, are excellent for many tasks. However, as agentic systems become more complex, you might need:

- **Explicit State Management:** To track not just conversation history, but also intermediate results, confidence scores, available resources, or any custom data relevant to the agent's task.
- **Complex Control Flow:** To define workflows with branches (if-else logic), loops (for retries or iterative refinement), and the ability to jump between different stages of processing.
- **Human-in-the-Loop:** To pause the agent at critical junctures for human review, approval, or input.
- **Modularity at a Higher Level:** To define an agent's overall behavior as a graph of interconnected components, where each component (node) can itself be a LangChain chain or agent.
- **Cycles and Self-Correction:** To allow an agent to review its own work or a tool's output and decide to retry or refine its approach.
- **Multi-Agent Systems:** To coordinate multiple specialized agents working together on a larger task (though we'll only touch on this briefly).

LangGraph addresses these needs by allowing you to define agent workflows as **state machines** or **graphs**.

### 3.2. Core LangGraph Concepts

At its heart, LangGraph helps you build and run directed graphs where nodes represent computation steps and edges represent the flow of control and data.

**a) State (`StatefulGraph`)**

Every LangGraph workflow operates on a **state** object. This state is passed between nodes, and nodes can update it. You define the structure of this state, typically using Python's `TypedDict` or a Pydantic `BaseModel` for more complex states.

- The state holds all the information the agent needs to make decisions and carry out its task. This can include:
    - Conversation history (e.g., `messages`)
    - The current task or input (e.g., `input`)
    - Intermediate results from tools or chains (e.g., `search_results`, `draft_document`)
    - Control flags (e.g., `needs_revision`, `tool_to_call`)
    - Any other data relevant to your agent's logic.

**b) Nodes**

Nodes are the building blocks of your graph. Each node is a function or a LangChain Runnable (like a chain or an agent component) that takes the current state as input and returns a dictionary representing updates to the state.

- A node might:
    - Call an LLM to decide the next action.
    - Execute a tool.
    - Process data.
    - Prepare output for a user.

**c) Edges**

Edges define how the agent transitions from one node to another.

- **Standard Edges:** Unconditionally go from one node to the next.
- **Conditional Edges:** Route to different nodes based on the current state. This is how you implement branching logic (e.g., "if the agent decided to use a tool, go to the tool execution node; otherwise, go to the response node").
- **Entry Point:** You define a starting node for the graph.
- **`END`:** A special node name indicating the workflow should terminate.

### 3.3. Building a Basic Graph with LangGraph

Let's illustrate with a conceptual example. Imagine an agent that can either call a tool or respond directly.

First, define the state. The state will hold the input messages and what the next step should be.

```python
from typing import TypedDict, Sequence, Annotated
from langchain_core.messages import BaseMessage
import operator

class BasicAgentState(TypedDict):
    # messages will be appended to by each node
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # next_node will be set by a node to determine the next step
    next_node: str | None
```

Next, define the nodes. One node will represent the agent deciding what to do, another for calling a tool (if decided), and one for generating a final response.

```python
# (Conceptual: Full implementation of these nodes will integrate LangChain components)
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

# Dummy model and tool for illustration
class FakeChatModel:
    def invoke(self, messages):
        last_message_content = messages[-1].content.lower()
        if "tool" in last_message_content:
            # Simulate model deciding to use a tool
            return AIMessage(content="", tool_calls=[{"name": "my_tool", "args": {"query": "example"}, "id": "tool_abc123"}])
        return AIMessage(content=f"Responding to: {messages[-1].content}")

class FakeTool:
    def invoke(self, tool_input):
        return f"Tool executed with input: {tool_input}"

llm = FakeChatModel() # Replace with a real LangChain model
my_tool = FakeTool()  # Replace with a real LangChain tool

def agent_node(state: BasicAgentState) -> dict:
    print("--- Executing Agent Node ---")
    # Call our LangChain agent/model
    response_message = llm.invoke(state["messages"])
    
    if response_message.tool_calls:
        print(f"Agent decided to call tool: {response_message.tool_calls[0]['name']}")
        # Store the tool call and set next node to tool execution
        return {"messages": [response_message], "next_node": "tool_executor"}
    else:
        print("Agent decided to respond directly.")
        # No tool call, respond directly
        return {"messages": [response_message], "next_node": "responder"}

def tool_executor_node(state: BasicAgentState) -> dict:
    print("--- Executing Tool Executor Node ---")
    last_message = state["messages"][-1]
    tool_call = last_message.tool_calls[0]
    tool_output = my_tool.invoke(tool_call["args"])
    print(f"Tool output: {tool_output}")
    # Return a ToolMessage to feed back to the agent
    tool_message = ToolMessage(content=str(tool_output), tool_call_id=tool_call["id"])
    # After tool execution, typically you'd go back to the agent to process the tool's output
    return {"messages": [tool_message], "next_node": "agent"} 

def responder_node(state: BasicAgentState) -> dict:
    print("--- Executing Responder Node ---")
    # This node would typically take the last AIMessage and present it
    # For this basic example, we just signal the end.
    # In a more complex graph, it might format the final response.
    print(f"Final response would be: {state['messages'][-1].content}")
    return {"next_node": "__end__"} # Using __end__ to signify termination for conditional edges

```

Now, construct the graph:

```python
from langgraph.graph import StateGraph, END

# Create the graph instance
workflow = StateGraph(BasicAgentState)

# Add the nodes
workflow.add_node("agent", agent_node)
workflow.add_node("tool_executor", tool_executor_node)
workflow.add_node("responder", responder_node)

# Define the entry point
workflow.set_entry_point("agent")

# Add edges. We need conditional logic after the 'agent' node.
# LangGraph provides conditional edges for this.

def decide_next_node(state: BasicAgentState):
    # This function inspects the state and returns the name of the next node to execute.
    return state["next_node"]

# Conditional routing: after agent_node, go to tool_executor, responder, or end.
workflow.add_conditional_edges(
    "agent",
    decide_next_node, # The function that returns the key for the path to take
    {
        "tool_executor": "tool_executor",
        "responder": "responder",
        "__end__": END # If next_node is __end__, terminate.
    }
)

# After tool_executor, if it decided to go back to agent, it will set next_node="agent"
workflow.add_conditional_edges(
    "tool_executor",
    decide_next_node,
    {
        "agent": "agent",
        "__end__": END
    }
)

# After responder, end the graph
workflow.add_edge("responder", END) # Could also use conditional edge if responder could loop

# Compile the graph into a runnable LangChain object
app = workflow.compile()

# Run the graph
# initial_state_tool = {"messages": [HumanMessage(content="Tell me something that requires a tool.")]}
# for s in app.stream(initial_state_tool):
#     print(s)
# print("-----")
# initial_state_direct = {"messages": [HumanMessage(content="Hello!")]}
# for s in app.stream(initial_state_direct):
#     print(s)
```
This example demonstrates:
- Defining a state (`BasicAgentState`).
- Creating nodes that modify this state.
- Using `add_conditional_edges` to control the flow based on the state.
- Compiling the graph into a runnable application.

This graph structure is much more explicit and controllable than a single `AgentExecutor` loop, especially as logic becomes more intricate. We are using `next_node` in the state to explicitly control transitions, which is a common pattern.

In the next section, we'll combine LangChain's agent components with LangGraph to build a more concrete agentic system.

## 4. Designing an Agentic System: LangChain + LangGraph in Action

Now, let's build a more practical agent that combines the strengths of LangChain for component creation and LangGraph for orchestration. We'll create a "Research Assistant" agent that can:
1. Take a research question.
2. Use a search tool to find relevant information.
3. Summarize the findings.
4. Present the summary.

This example will use a more realistic setup with LangChain agents and tools integrated into LangGraph nodes.

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

We need:
- An LLM and tools.
- An agent runnable (built with `create_openai_tools_agent`) that decides what to do (search or summarize).
- A tool executor to run the chosen tools.

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

**a) `planner_node`**

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

**b) `tool_executor_node`**

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

    print(f"Starting research for: '{initial_input}'\n")
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
            print("--------------------------------------\n")
    
    final_state = research_app.invoke(initial_state, {"recursion_limit": 10})
    print("\n--- Final Research Result ---")
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

## 5. Advanced Agent Optimization with DSPy

While LangChain provides the building blocks and LangGraph orchestrates complex agentic flows, **DSPy** (Declarative Self-improving Language Programs, pronounced "dee-spy") offers a powerful paradigm for optimizing the LLM-driven components within your agents. DSPy shifts from manual prompt engineering to a more programmatic and systematic approach where you define *what* you want the LLM to do (via Signatures) and then use DSPy's optimizers (Teleprompters) to figure out *how* to best prompt the LLM to achieve that, often based on a few examples and defined metrics.

This section provides a technical guide on integrating DSPy into your LangChain/LangGraph agentic systems to enhance their performance, adaptability, and robustness.

## 5.1. The Need for Programmatic Prompt Engineering in Agents

Manually crafting and iterating on prompts for complex agents can be:
- **Time-consuming:** Finding the optimal wording, few-shot examples, or chain-of-thought structure requires extensive trial and error.
- **Brittle:** Prompts optimized for one LLM or a specific task variant may not generalize well.
- **Hard to maintain:** As agents evolve, managing and updating a large suite of hand-crafted prompts becomes cumbersome.

DSPy addresses these by allowing you to declare the task and let optimizers discover effective prompts. This is particularly beneficial in agentic systems where an LLM might be invoked for multiple distinct reasoning steps (e.g., understanding user intent, selecting a tool, formatting tool input, synthesizing information, reflecting on output).

## 5.2. Deep Dive into DSPy for Agentic Tasks

### 5.2.1. Core DSPy Concepts

- **Signatures:** These are declarative specifications of a task your LLM needs to perform. They define input fields (what information is provided) and output fields (what information is expected). Typed annotations are encouraged.
  ```python
  import dspy

  class ToolSelectionSignature(dspy.Signature):
      """Given the user query and a list of available tools, select the most appropriate tool and formulate its input."""
      user_query: str = dspy.InputField(desc="The user's original question or instruction.")
      tool_names: list[str] = dspy.InputField(desc="A list of names of available tools.")
      tool_descriptions: list[str] = dspy.InputField(desc="Corresponding descriptions for each tool.")
      selected_tool_name: str = dspy.OutputField(desc="The name of the chosen tool.")
      tool_input_query: str = dspy.OutputField(desc="The specific query or input to pass to the selected tool.")
  ```

- **Modules:** These are the building blocks of a DSPy program, analogous to layers in a neural network. They take one or more Signatures and an LLM, and implement a specific prompting strategy.
    - `dspy.Predict`: The simplest module. It takes a Signature and an LLM, and generates a basic prompt to instruct the LLM to fill the output fields given the input fields.
    - `dspy.ChainOfThought`: Takes a Signature and an LLM. It instructs the LLM to first generate a rationale (chain of thought) for how to arrive at the answer before producing the final output fields. This often improves reasoning for complex tasks.
    - `dspy.ReAct`: Implements the ReAct (Reason+Act) prompting strategy, suitable for building agents that can iteratively use tools. While powerful, we will focus on using simpler DSPy modules for specific agent sub-tasks and integrating them into LangGraph for overall orchestration.
    - `dspy.ProgramOfThought`: For tasks that require generating and executing code.

- **Teleprompters (Optimizers):** These are algorithms that tune the prompts used by your DSPy modules. They take your DSPy program (composed of modules), a metric to optimize for, and training data (often just a few examples).
    - `BootstrapFewShot`: Generates few-shot examples for your prompts from your training data.
    - `SignatureOptimizer` (formerly `BayesianSignatureOptimizer`): Systematically searches for better prompt instructions (e.g., for the `desc` fields in your Signature) to improve performance on your metric.
    - `MIPRO` (Multi-prompt Instruction Proposer): A more advanced optimizer that can generate complex instruction sets.

### 5.2.2. Technical Example: DSPy Module for Agent Tool Selection

Let's build a DSPy module using `dspy.ChainOfThought` for the `ToolSelectionSignature` defined above. This module will be responsible for the critical agentic step of deciding which tool to use and what input to provide to it.

```python
import dspy

# Assume lm is a configured dspy.LM (e.g., dspy.OpenAI, dspy.HFModel)
# For example:
# openai_llm = dspy.OpenAI(model='gpt-4-turbo', max_tokens=400)
# dspy.settings.configure(lm=openai_llm)

class EnhancedToolSelector(dspy.Module):
    def __init__(self):
        super().__init__()
        # Using ChainOfThought to encourage more robust reasoning for tool selection
        self.selector = dspy.ChainOfThought(ToolSelectionSignature)

    def forward(self, user_query: str, tool_names: list[str], tool_descriptions: list[str]):
        # Ensure tool_names and tool_descriptions are passed as separate lists
        prediction = self.selector(user_query=user_query, tool_names=tool_names, tool_descriptions=tool_descriptions)
        return dspy.Prediction(
            selected_tool_name=prediction.selected_tool_name,
            tool_input_query=prediction.tool_input_query
        )

# Example usage (assuming dspy.settings.configure(lm=...) has been called):
# tool_selector_module = EnhancedToolSelector()
# query = "What is the weather in London and what is 2+2?"
# available_tools = {
#     "weather_api": "Provides current weather information for a city.",
#     "calculator": "Evaluates mathematical expressions."
# }
# names = list(available_tools.keys())
# descriptions = list(available_tools.values())
# result = tool_selector_module(user_query=query, tool_names=names, tool_descriptions=descriptions)
# print(f"Selected Tool: {result.selected_tool_name}")
# print(f"Tool Input: {result.tool_input_query}")
```

This `EnhancedToolSelector` module can now be compiled (optimized) using a DSPy teleprompter. For instance, you could provide a few examples of user queries, available tools, and the desired tool selection/input, then use `BootstrapFewShot` to generate effective few-shot prompts for the underlying `ChainOfThought` module.

## 5.3. Integrating DSPy Modules into LangChain

To use your optimized DSPy module within a LangChain or LangGraph agent, you can wrap it as a LangChain `Tool`. This allows the agent to invoke the DSPy module just like any other tool.

### 5.3.1. Wrapping a DSPy Module as a LangChain `Tool`

```python
from langchain_core.tools import BaseTool, tool
from typing import Type, Any
from pydantic.v1 import BaseModel, Field # Use pydantic v1 for LangChain compatibility
import dspy

# Assume EnhancedToolSelector and its Signature are defined as above
# Assume 'compiled_tool_selector' is an instance of EnhancedToolSelector that has been
# potentially compiled/optimized using a DSPy teleprompter.
# If not compiled, it will use the basic prompts from dspy.ChainOfThought.

# compiled_tool_selector = EnhancedToolSelector() # Or a compiled version
# Example: define dummy compiled_tool_selector if dspy.settings.lm is not configured
# class DummyLM(dspy.LM):
#     def __init__(self):
#         super().__init__("dummy_model")
#     def __call__(self, prompt, **kwargs):
#         # Simulate a response for tool selection
#         if "weather" in prompt.lower() and "calculator" in prompt.lower():
#             return [dspy.Prediction(selected_tool_name="weather_api", tool_input_query="London", rationale="User asked for weather.")]
#         return [dspy.Prediction(selected_tool_name="unknown", tool_input_query="", rationale="Cannot determine tool.")]
#     def get_max_tokens(self):
#         return 1000
# if not dspy.settings.peek().lm:
#      dspy.settings.configure(lm=DummyLM())
# compiled_tool_selector = EnhancedToolSelector()

class DSPyToolSelectorSchema(BaseModel):
    user_query: str = Field(description="The user's original question or instruction.")
    # Tools are provided implicitly via the agent's toolset, not passed to this specific schema

class DSPyToolSelectorTool(BaseTool):
    name: str = "dspy_tool_selector"
    description: str = (
        "Invokes a DSPy-optimized module to select the best tool and formulate its input " 
        "based on the user query and available tools. Use this when unsure which specific tool to call."
    )
    args_schema: Type[BaseModel] = DSPyToolSelectorSchema
    dspy_module: Any # Stores the compiled DSPy module
    available_tools_dict: dict[str, str] # Tool name to description mapping

    def _run(self, user_query: str) -> dict:
        tool_names = list(self.available_tools_dict.keys())
        tool_descriptions = list(self.available_tools_dict.values())
        
        # Ensure the DSPy module is configured if it wasn't globally
        # if not dspy.settings.peek().lm and hasattr(self.dspy_module, 'selector') and hasattr(self.dspy_module.selector, 'lm'):
        #     current_lm = self.dspy_module.selector.lm
        #     if current_lm:
        #          with dspy.settings.context(lm=current_lm):
        #             prediction = self.dspy_module(user_query=user_query, tool_names=tool_names, tool_descriptions=tool_descriptions)
        #     else: # Fallback or raise error
        #         raise ValueError("DSPy LM not configured for tool selector.")
        # else: # Assumes global LM or LM within module is set
        #     prediction = self.dspy_module(user_query=user_query, tool_names=tool_names, tool_descriptions=tool_descriptions)
        
        # Simplified call assuming dspy.settings.lm is configured globally before this tool is used.
        # In a real system, you'd pass the LM or ensure it's set in the module upon instantiation.
        try:
            prediction = self.dspy_module(user_query=user_query, tool_names=tool_names, tool_descriptions=tool_descriptions)
            return {
                "selected_tool_name": prediction.selected_tool_name,
                "tool_input_query": prediction.tool_input_query
            }
        except Exception as e:
            # Log error e
            return {
                 "selected_tool_name": "error_handler_tool", 
                 "tool_input_query": f"Failed to select tool using DSPy: {str(e)}"
            }

    async def _arun(self, user_query: str) -> dict:
        # DSPy modules are typically synchronous. For async, you might need to wrap in run_in_executor.
        return self._run(user_query)

# Usage:
# Assuming `my_compiled_dspy_selector_module` is your (potentially) optimized DSPy module instance
# and `agent_tool_descriptions` is a dict like {"tool_name": "description"}
# dspy_powered_tool_selector = DSPyToolSelectorTool(
#     dspy_module=my_compiled_dspy_selector_module,
#     available_tools_dict=agent_tool_descriptions
# )
```

This `DSPyToolSelectorTool` can now be included in the list of tools provided to a LangChain agent or a LangGraph node.

## 5.4. Orchestrating DSPy-Powered Tools with LangGraph

Now, let's integrate our `DSPyToolSelectorTool` into a LangGraph agent. The core idea is to have a node in our graph that specifically calls this DSPy-powered tool to decide the next step or tool invocation.

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

# Assume other tools are defined, e.g., weather_tool, calculator_tool
# from langchain_community.tools.tavily_search import TavilySearchResults
# search_tool = TavilySearchResults(max_results=2)

# Define the state for our LangGraph agent
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_action_details: dict # To store output from DSPyToolSelectorTool
    # Potentially other state variables like intermediate_results, confidence_scores etc.

# Define node functions
def call_dspy_tool_selector_node(state: AgentState):
    # This node uses the DSPyToolSelectorTool
    # The actual tools (weather, calculator) are passed when instantiating the tool.
    # For simplicity, assume dspy_tool_selector_tool is already instantiated and available.
    
    # Simulate dspy.settings.configure if not done globally
    # This is crucial: DSPy modules need an LM in their context.
    # if not dspy.settings.peek().lm:
    #     # Replace with your actual LM configuration for DSPy
    #     # This LM should be the one your DSPy module was compiled/tested with.
    #     lm_for_dspy = dspy.OpenAI(model="gpt-4-turbo", api_key="YOUR_OPENAI_API_KEY") 
    #     dspy.settings.configure(lm=lm_for_dspy, trace=[]) # Add tracing if desired

    user_query = state["messages"][-1].content
    # In a real scenario, dspy_tool_selector_tool would be instantiated with the compiled module
    # and the available_tools_dict for the agent.
    # For this example, let's assume it's pre-configured and accessible.
    # action_details = dspy_tool_selector_tool.invoke({"user_query": user_query})
    
    # --- Placeholder for dspy_tool_selector_tool instantiation and invocation --- 
    # This part needs a fully configured DSPy environment with an LLM for the DSPy module
    # For now, we'll mock its output for the graph structure demonstration.
    print(f"--- Calling DSPy Tool Selector for query: {user_query} ---")
    if "weather" in user_query.lower():
        action_details = {"selected_tool_name": "weather_tool", "tool_input_query": "Paris"}
    elif "calculate" in user_query.lower():
        action_details = {"selected_tool_name": "calculator_tool", "tool_input_query": "3*5"}
    else:
        action_details = {"selected_tool_name": "final_answer", "tool_input_query": "I'm not sure how to handle that with my current tools."}
    # --- End Placeholder --- 
    
    return {"next_action_details": action_details}

def execute_selected_tool_node(state: AgentState):
    action_details = state["next_action_details"]
    tool_name = action_details.get("selected_tool_name")
    tool_input = action_details.get("tool_input_query")
    
    # Mock tool execution
    print(f"--- Executing Tool: {tool_name} with input: {tool_input} ---")
    if tool_name == "weather_tool":
        result = f"The weather in {tool_input} is sunny."
    elif tool_name == "calculator_tool":
        try: result = str(eval(tool_input))
        except: result = "Invalid expression"
    elif tool_name == "final_answer":
        result = tool_input # This is the direct answer
    else:
        result = "Unknown tool or error."
        
    return {"messages": [AIMessage(content=result)]}

# Define conditional edges
def should_continue_or_end(state: AgentState):
    if state["next_action_details"].get("selected_tool_name") == "final_answer":
        return "end"
    return "continue"

# Build the graph
workflow = StateGraph(AgentState)
workflow.add_node("dspy_selector", call_dspy_tool_selector_node)
workflow.add_node("tool_executor", execute_selected_tool_node)

workflow.set_entry_point("dspy_selector")
workflow.add_conditional_edges(
    "dspy_selector",
    should_continue_or_end,
    {
        "continue": "tool_executor",
        "end": END
    }
)
# If a tool is executed, we might want to loop back to the selector or another reasoning step.
# For this simplified example, tool execution leads to END if it's not 'final_answer' from selector.
# A more complete agent would often loop or go to a response generation node.
workflow.add_edge("tool_executor", END) # Simplified: in reality, may loop or go to synthesizer

# Compile the graph
# app = workflow.compile()

# Example run (mocking the initial message)
# initial_state = {"messages": [HumanMessage(content="What is the weather in Paris?")]}
# for event in app.stream(initial_state):
#     for k, v in event.items():
#         print(f"Node: {k}, Output: {v}")
#     print("----")
```
**Important Considerations for the LangGraph Example:**
1.  **DSPy LM Configuration:** The `call_dspy_tool_selector_node` *must* have access to a DSPy-configured LLM (via `dspy.settings.configure(lm=...)`) for the `dspy_module` to work. This LM should ideally be the one used during DSPy optimization. I've added comments to highlight this; a real implementation needs to handle this robustly (e.g., by passing the LM, or ensuring the DSPy module is instantiated with its required LM). The placeholder simulates this.
2.  **Full Agent Loop:** The example graph is simplified. A production agent would typically loop back after tool execution, potentially to the DSPy selector or to another LLM call to synthesize a final answer from the tool's output. The `tool_executor` currently just leads to `END` for brevity if a tool was selected.
3.  **Error Handling:** Robust error handling within nodes (e.g., if a DSPy module fails or a tool errors out) is crucial.

## 5.5. Advanced DSPy Strategies for Agentic Systems

- **Few-Shot Learning for Agent Behavior:** Use `dspy.BootstrapFewShot` with examples of complex query -> tool choice/input sequences to generate effective few-shot prompts for your DSPy tool selector. This can teach the selector nuanced tool usage patterns.
- **Optimizing Agent Personas and System Prompts:** While DSPy is often used for specific modules, its principles can be applied to optimize parts of an agent's overall system prompt if you can define a metric for "good persona adherence" or "effective instruction following."
- **Self-Correction Loops with DSPy:** You can design a DSPy signature like `CritiqueAndRefineSignature(previous_attempt: str, critique_instructions: str, refined_output: str)`. A LangGraph cycle could then use one DSPy module to generate an initial response/action, another to critique it, and a third (or the same one with different instructions) to refine it based on the critique. This is powerful for improving response quality or tool use accuracy.

## 5.6. Synergies and Best Practices

- **LangChain for Foundation:** Use LangChain for its vast collection of LLM wrappers, document loaders, text splitters, embedders, vector stores, and basic tool definitions.
- **DSPy for Optimized Reasoning Kernels:** Identify critical reasoning steps within your agent (e.g., tool selection, query transformation, information synthesis, output formatting) and implement these as DSPy modules. Optimize these modules using DSPy teleprompters with relevant few-shot examples and metrics.
- **LangGraph for Orchestration & State:** Use LangGraph to define the high-level control flow, manage explicit state, handle cycles, and integrate human-in-the-loop (HITL) steps. Your DSPy-powered LangChain tools become nodes within this graph.
- **Modularity:** Keep DSPy modules focused on specific, well-defined tasks. This makes them easier to optimize and reuse.
- **Iterative Optimization:** Start with basic DSPy modules (`dspy.Predict` or `dspy.ChainOfThought` with default prompts). As you gather data and identify weaknesses, introduce teleprompters to optimize them. Don't prematurely optimize.
- **Evaluation is Key:** Define clear metrics for your DSPy module's performance (e.g., accuracy of tool selection, quality of synthesized response). Use these metrics to guide optimization with teleprompters. LangSmith can be invaluable for tracing and evaluating the end-to-end behavior of your integrated agent.
- **LM Consistency:** When optimizing a DSPy module, use the same LLM (or a very similar one) that will be used by that module in the deployed agent. Prompt effectiveness can vary significantly between models.

By combining the strengths of LangChain, LangGraph, and DSPy, you can construct highly capable, adaptable, and performant agentic AI systems that move beyond simple prompt chaining towards more robust and optimized reasoning pipelines.

## 6. State Management and Persistence with Checkpointers

For many agentic systems, especially those that are long-running, involve human-in-the-loop, or need to recover from interruptions, it's crucial to save and restore the agent's state. LangGraph provides **checkpointers** for this purpose.

### 6.1. Why Persistence?

- **Long-Running Tasks:** If an agent takes hours or days to complete a task, you don't want to lose all progress if the system restarts.
- **Human-in-the-Loop (HITL):** When an agent pauses for human input, its current state must be saved so it can be resumed later, potentially on a different server or after a delay.
- **Resilience:** Recover from crashes or unexpected interruptions.
- **Debugging and Analysis ("Time Travel"):** Load a past state to understand why an agent behaved a certain way or to explore alternative execution paths from a specific point.

### 6.2. LangGraph Checkpointers

A checkpointer in LangGraph automatically saves the state of your graph at specified points (typically after each node execution or as configured). When you run a graph compiled with a checkpointer, you provide a `configurable` dictionary, often including a `thread_id`. This `thread_id` acts as a key to save and load the conversation or task state.

LangGraph offers several checkpointer backends:
- **`MemorySaver`:** Stores checkpoints in memory. Useful for testing and simple cases, but state is lost when the process ends.
- **`SqliteSaver`:** Stores checkpoints in a SQLite database file. Good for local persistence.
- **`RedisSaver`:** Stores checkpoints in a Redis instance. Suitable for distributed systems.
- Other backends can be implemented for different databases or storage systems.

### 6.3. Using a Checkpointer (Conceptual Example with `MemorySaver`)

Let's adapt our basic research assistant graph from Section 4 to use `MemorySaver`.

```python
from langgraph.checkpoint.memory import MemorySaver

# Assume ResearchAgentState, planner_node, tool_executor_node, 
# route_after_planner, route_after_tool_executor are defined as in Section 4.

# 1. Initialize a checkpointer
memory_saver = MemorySaver()

# 2. Create the graph (same structure as before)
workflow_with_checkpoint = StateGraph(ResearchAgentState)
workflow_with_checkpoint.add_node("planner", planner_node)
workflow_with_checkpoint.add_node("tool_executor", tool_executor_node)
workflow_with_checkpoint.set_entry_point("planner")
workflow_with_checkpoint.add_conditional_edges("planner", route_after_planner, {"tool_executor": "tool_executor", END: END})
workflow_with_checkpoint.add_conditional_edges("tool_executor", route_after_tool_executor, {"planner": "planner", END: END})

# 3. Compile the graph with the checkpointer
# The checkpointer will save the state after each step for a given thread_id.
research_app_persistent = workflow_with_checkpoint.compile(checkpointer=memory_saver)

# 4. Invoke the graph with a configurable thread_id
if __name__ == '__main__':
    thread_id_1 = "my_research_task_123" # Unique ID for this conversation/task
    initial_input_persistent = "What is LangGraph and how does it help with agent memory?"
    initial_state_persistent = {
        "input_question": initial_input_persistent,
        "messages": [HumanMessage(content=initial_input_persistent)]
    }

    print(f"Starting persistent research for: '{initial_input_persistent}' with Thread ID: {thread_id_1}\n")
    
    # First invocation - graph runs and state is saved under thread_id_1
    # for event in research_app_persistent.stream(initial_state_persistent, {"configurable": {"thread_id": thread_id_1}, "recursion_limit": 10}):
    #     # print(event) # Print events to see flow
    #     pass # Simplified for brevity
    # final_state_run1 = research_app_persistent.invoke(initial_state_persistent, {"configurable": {"thread_id": thread_id_1}, "recursion_limit": 10})
    # print(f"\n--- Final Result (Run 1, Thread ID: {thread_id_1}) ---")
    # print(f" Summary: {final_state_run1.get('summary', 'N/A')}")

    # Imagine some time passes, or another user interacts with the same thread.
    # The graph can be invoked again with the same thread_id. It will resume from the last saved state.
    # For MemorySaver, this only works if the Python process is still running.
    # For persistent savers (SQLite, Redis), it works across process restarts.

    # follow_up_input = "Can you elaborate on its checkpointer system?"
    # # Note: We don't pass the full initial_state again for subsequent calls on the same thread.
    # # We just pass the new input that should be added to the message history.
    # # The checkpointer handles loading the previous state for this thread_id.
    # current_state_before_follow_up = research_app_persistent.get_state({"configurable": {"thread_id": thread_id_1}})
    # follow_up_messages = current_state_before_follow_up.values["messages"] + [HumanMessage(content=follow_up_input)]
    
    # follow_up_state_input = {
    #     "input_question": follow_up_input, # Update input question if relevant for planner
    #     "messages": [HumanMessage(content=follow_up_input)] # Only the new message to be appended
    # }

    # print(f"\n--- Invoking with Follow-up (Thread ID: {thread_id_1}) ---")
    # # When invoking with a checkpointer and an existing thread_id,
    # # LangGraph appends the new messages to the history and continues.
    # for event in research_app_persistent.stream(follow_up_state_input, {"configurable": {"thread_id": thread_id_1}, "recursion_limit": 10}):
    #     # print(event)
    #     pass
    # final_state_run2 = research_app_persistent.invoke(follow_up_state_input, {"configurable": {"thread_id": thread_id_1}, "recursion_limit": 10})
    # print(f"\n--- Final Result (Run 2, Thread ID: {thread_id_1}) ---")
    # print(f" Summary: {final_state_run2.get('summary', 'N/A')}")
    # print(f" Full message history for thread {thread_id_1}:")
    # final_thread_state = research_app_persistent.get_state({"configurable": {"thread_id": thread_id_1}})
    # for msg in final_thread_state.values["messages"]:
    #     print(f"  {msg.type}: {msg.content[:100]}...")
```

**Key points for using checkpointers:**
- When compiling, pass the `checkpointer` instance.
- When invoking (`.invoke()`, `.stream()`), pass a `configurable` dictionary containing a `thread_id`. This ID groups all states for a single, continuous interaction or task.
- For follow-up interactions on the same `thread_id`, you usually just provide the new input (e.g., new messages). LangGraph, using the checkpointer, will load the prior state for that thread and continue.

### 6.4. Time Travel and State Inspection

Checkpointers also enable powerful debugging and analytical capabilities:

- **`get_state(config)`:** Retrieve the latest state for a given `thread_id`.
- **`list_states(config)` (or similar, e.g., `list_checkpoints` for some savers):** Get a history of all saved states (checkpoints) for a `thread_id`.
- **`update_state(config, values)`:** Manually update the state for a `thread_id`. Useful for correcting errors or injecting information.
- **Invoking from a past checkpoint:** Some checkpointers allow you to get a specific checkpoint and then invoke the graph *from that point in the past*, potentially with modified input, to explore different paths. This is invaluable for debugging complex agent behaviors or for A/B testing different responses from a certain state.

```python
# Conceptual: Time Travel / Inspection
# if __name__ == '__main__' and memory_saver: # Assuming research_app_persistent is compiled with memory_saver
#     thread_id_inspect = "my_research_task_123" # Use an existing thread_id
    
#     # Get the current state
#     current_state = research_app_persistent.get_state({"configurable": {"thread_id": thread_id_inspect}})
#     if current_state:
#         print(f"\n--- Current State for Thread ID: {thread_id_inspect} ---")
#         # print(current_state.values) # The actual state dictionary
#         print(f"  Current messages: {len(current_state.values['messages'])} total")
#         print(f"  Next node was to be: {current_state.values.get('next_node')}")

    # List all checkpoints (MemorySaver might require specific methods or may not fully support listing all historical checkpoints easily without a persistent backend like SQLite)
    # For SQLiteSaver, it would be like: checkpoints = memory_saver.list(configurable={"thread_id": thread_id_inspect})
    # And then you could pick a checkpoint from the list to resume from.
    # Refer to specific checkpointer documentation for exact methods.
```

Using a persistent checkpointer like `SqliteSaver` is highly recommended for any agent that needs to maintain state beyond a single in-memory session. You would replace `MemorySaver()` with `SqliteSaver.from_conn_string(":memory:")` (for in-memory SQLite) or `SqliteSaver.from_conn_string("my_agent_db.sqlite")` (for a file-based database).

## 7. Debugging and Tracing with LangSmith

Building complex agentic systems with LangChain and LangGraph involves many moving parts. LangSmith is a platform designed to help you debug, trace, monitor, and evaluate your language model applications, making it an invaluable tool for developing robust agents.

### 7.1. Why LangSmith?

- **Visibility:** Get a clear view of what your agent is doing at each step. See the inputs and outputs of LLM calls, tool executions, and graph node transitions.
- **Debugging:** Quickly identify errors, unexpected behavior, or inefficient paths in your agent's logic.
- **Collaboration:** Share traces with team members to troubleshoot issues.
- **Evaluation:** Log results, gather feedback, and run evaluations to measure and improve agent performance.
- **Monitoring:** Keep an eye on your agents in production (though this tutorial focuses on development).

### 7.2. Setting up LangSmith

To get started with LangSmith, you typically need to:
1.  Sign up at [smith.langchain.com](https://smith.langchain.com/).
2.  Create an API key.
3.  Set a few environment variables in your development environment:

```python
import os
import getpass # To securely get API key if not set as env var

# Best practice: Set these in your shell environment (e.g., .env file or export commands)
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = "YOUR_LANGSMITH_API_KEY"
# os.environ["LANGCHAIN_PROJECT"] = "My Agentic AI Project" # Optional: organize runs into projects

# Example of setting them programmatically if not already set (useful for notebooks)
def setup_langsmith_env():
    if "LANGCHAIN_TRACING_V2" not in os.environ:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        print("Set LANGCHAIN_TRACING_V2 to true")

    if "LANGCHAIN_API_KEY" not in os.environ:
        api_key = getpass.getpass("Enter your LangSmith API key: ")
        os.environ["LANGCHAIN_API_KEY"] = api_key
        print("LangSmith API key set from input.")
    else:
        print("LangSmith API key found in environment.")

    if "LANGCHAIN_PROJECT" not in os.environ:
        os.environ["LANGCHAIN_PROJECT"] = "Default Agentic Tutorial Project"
        print(f"Using LangSmith project: {os.environ['LANGCHAIN_PROJECT']}")

# Call this at the beginning of your script or notebook
# setup_langsmith_env()
```

Once these environment variables are set, LangChain and LangGraph will automatically start sending trace data to your LangSmith project.

### 7.3. Tracing LangChain Components and LangGraph Runs

When you execute your LangGraph application (e.g., `research_app.invoke(...)` or `research_app.stream(...)` from our example), LangSmith captures:

- **Overall Graph Execution:** The entry into the graph and its final output.
- **Node Executions:** Each time a node in your `StateGraph` is run, LangSmith records its inputs (the part of the state it received) and its outputs (the state updates it returned).
- **LangChain Component Calls:** If a node internally uses LangChain components (like an `AgentExecutor`, an LLM call, a specific chain, or a tool), these are also traced as nested operations.
    - You'll see the exact prompts sent to LLMs.
    - The arguments passed to tools and the data they returned.
    - The flow within `create_openai_tools_agent` or other agent runnables.

**Visualizing Graphs:**
LangSmith provides a visual representation of your LangGraph executions, making it much easier to understand the flow of control, especially with conditional edges and loops. You can see which path was taken through the graph for a given input.

### 7.4. Example: Inspecting the Research Assistant in LangSmith

If you run the Research Assistant agent (from Section 4) with LangSmith configured:

1.  Go to your LangSmith project.
2.  You will see a new trace for each invocation of `research_app.invoke()` or `research_app.stream()`.
3.  Clicking on a trace will show you:
    *   The initial input to the graph.
    *   A timeline of nodes executed (`planner`, `tool_executor`).
    *   For the `planner` node, you can expand it to see the internal call to your `planner_agent_runnable` (the `create_openai_tools_agent`). Further expanding this will show the LLM call, the prompt, and the model's response (including any tool calls it decided to make).
    *   For the `tool_executor` node, you'll see which tool was called (e.g., `web_search` or `summarize_text_tool`) and the arguments and output of that tool.
    *   If you used a checkpointer, the state at each step might also be visible or inferable from the inputs/outputs of the nodes.

This detailed, hierarchical view is crucial for understanding why your agent made certain decisions, how tools performed, and where potential improvements can be made.

### 7.5. Logging Feedback and Annotations

LangSmith also allows you to programmatically or manually add feedback to runs.

```python
from langsmith import Client

# client = Client() # Initialize if you need to interact with LangSmith API directly

# Example: After a run, you might log feedback (this usually requires the run_id)
# This is more for evaluation workflows, but shows the capability.

# run_id = "some_run_id_from_a_trace" # You'd get this from a trace or programmatically
# if client and run_id:
#     try:
#         client.create_feedback(
#             run_id=run_id,
#             key="user_satisfaction", # Arbitrary key for the feedback type
#             score=0.8, # Numerical score (e.g., 0.0 to 1.0)
#             comment="The summary was good but a bit too verbose."
#         )
#         print(f"Feedback added for run {run_id}")
#     except Exception as e:
#         print(f"Could not log feedback: {e}")
```
This feedback can be used to evaluate agent performance over time and identify areas for improvement.

By integrating LangSmith into your development workflow from the start, you gain powerful observability that significantly speeds up the development and refinement of complex agentic AI systems.

## 8. Conclusion

Throughout this tutorial, we've explored how to design and build agentic AI systems by leveraging the complementary strengths of LangChain and LangGraph.

**Key Takeaways:**

1.  **Agentic AI Principles:** We started by understanding that agentic AI systems are goal-oriented, interactive, autonomous, and perceptive. They require careful design to manage their decision-making processes and interactions with the external world.

2.  **LangChain for Core Components:** LangChain provides the essential building blocks for agents:
    *   **Models:** The underlying intelligence (LLMs, Chat Models).
    *   **Prompts:** How we instruct and guide the models.
    *   **Tools:** Enabling agents to interact with external systems and data sources (e.g., web search, calculators, custom functions).
    *   **Agent Runnables (`create_openai_tools_agent`):** Encapsulating the logic for an LLM to decide when and how to use tools, or respond directly.

3.  **LangGraph for Orchestration and State:** When agentic workflows become complex, LangGraph provides a robust framework for:
    *   **Explicit State Management:** Defining and tracking the agent's state (beyond simple chat history) using `TypedDict` or Pydantic models.
    *   **Complex Control Flow:** Implementing sophisticated logic with nodes (processing units) and edges (transitions), including conditional branching and cycles.
    *   **Modularity:** Structuring the agent's overall behavior as a graph, where each node can contain a LangChain component (like an agent or a chain).

4.  **Synergistic Design:** The true power comes from combining these two libraries:
    *   Use LangChain to create powerful, self-contained tools and agentic "skills."
    *   Use LangGraph to define the overarching state machine that orchestrates these skills, manages the flow of information, and implements higher-level logic like iteration, human intervention, and error handling.

5.  **Advanced Patterns:** LangGraph enables advanced agentic patterns such as:
    *   **Iterative Refinement:** Agents that can review and improve their own work through cycles.
    *   **Human-in-the-Loop:** Integrating human oversight and decision-making into the agent's workflow.
    *   **Multi-Agent Collaboration:** Designing systems where multiple specialized agents work together.

6.  **Persistence and Debugging:**
    *   **Checkpointers (`MemorySaver`, `SqliteSaver`, etc.):** Essential for saving and resuming agent state, enabling long-running tasks, HITL, and resilience.
    *   **LangSmith:** Provides invaluable tracing and visualization capabilities to understand, debug, and monitor the intricate workings of your agents.

Building effective agentic AI is an iterative process. By starting with clear definitions of your agent's goals, state, and available tools (using LangChain), and then orchestrating its behavior with a well-designed graph (using LangGraph), you can create highly capable and controllable AI systems.

The examples provided, from basic agent construction to a more complete research assistant and advanced patterns, serve as a starting point. The principles of modularity, explicit state management, and controlled execution flow are key to scaling the complexity and reliability of your agentic applications.

We encourage you to explore the official LangChain and LangGraph documentation further (see Section 9) and experiment with building your own agentic AI systems.

## 9. References and Further Reading

For more detailed information, please refer to the official documentation:

**LangChain:**
- [LangChain Python Documentation](https://python.langchain.com/docs/)
- [LangChain GitHub Repository](https://github.com/langchain-ai/langchain)

**LangGraph:**
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangGraph GitHub Repository](https://github.com/langchain-ai/langgraph)

**Debugging and Monitoring:**
- [LangSmith](https://smith.langchain.com/) 