# LangGraph Tutorial: Orchestrating AI Agents

## Introduction

LangGraph is a framework built on top of LangChain that enables developers to build powerful, stateful, and controllable AI agents. It provides a graph-based approach to orchestrating complex agent behaviors with first-class support for streaming, human-in-the-loop workflows, and persistent state management.

## Table of Contents

1. [Installation](#installation)
2. [Key Concepts](#key-concepts)
3. [Building a Basic Chatbot](#building-a-basic-chatbot)
4. [Adding Tools](#adding-tools)
5. [Adding Memory](#adding-memory)
6. [Human-in-the-Loop Controls](#human-in-the-loop-controls)
7. [Customizing State](#customizing-state)
8. [Time Travel](#time-travel)
9. [Multi-Agent Systems](#multi-agent-systems)
10. [Advanced Techniques](#advanced-techniques)

## Installation

Install LangGraph using pip:

```bash
pip install langgraph
```

For specific integrations with LangChain:

```bash
pip install "langgraph[langchain]"
```

## Key Concepts

### State Machines and Graph Construction

LangGraph uses a state-based approach where agent workflows are defined as directed graphs:

```python
from langgraph.graph import StateGraph
from typing import TypedDict, Annotated, Sequence
import operator

# Define the state type
class AgentState(TypedDict):
    messages: Sequence[dict]
    next: str

# Create a graph
graph = StateGraph(AgentState)

# Add nodes
graph.add_node("assistant", assistant_node)
graph.add_node("tools", tools_node)

# Add edges
graph.add_edge("assistant", "tools")
graph.add_conditional_edges(
    "tools",
    condition_function,
    {
        "continue": "assistant",
        "end": END
    }
)

# Compile the graph
chain = graph.compile()
```

### Nodes and Edges

Nodes represent processing units (agents, tools, or human reviewers), while edges define the flow between nodes.

### State Management

LangGraph maintains state across agent steps, enabling complex, multi-turn interactions:

```python
# State is passed from node to node
def assistant_node(state):
    messages = state["messages"]
    response = chat_model.invoke(messages)
    return {"messages": messages + [response]}
```

## Building a Basic Chatbot

Let's build a simple, conversational agent:

```python
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from typing import TypedDict, Sequence
from langchain_core.messages import AIMessage, HumanMessage

# Define the state
class ChatState(TypedDict):
    messages: Sequence[HumanMessage | AIMessage]

# Initialize the model
model = ChatOpenAI(temperature=0.7)

# Define nodes
def chat_node(state):
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": state["messages"] + [response]}

# Create the graph
workflow = StateGraph(ChatState)
workflow.add_node("chat", chat_node)

# Add edges - in this simple case, the chat node just returns to itself
workflow.set_entry_point("chat")
workflow.add_edge("chat", END)

# Compile the graph
chain = workflow.compile()

# Use the chain
result = chain.invoke({"messages": [HumanMessage(content="Tell me a joke")]})
print(result["messages"][-1].content)
```

## Adding Tools

Let's enhance our agent by adding tool capabilities:

```python
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate

# Define a simple calculator tool
@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {str(e)}"

# Define a search tool
@tool
def search(query: str) -> str:
    """Search for information on the internet."""
    # Simplified implementation
    return f"Found results for: {query}"

tools = [calculator, search]

# Create an agent with tools
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an assistant with access to tools. Use them when necessary."),
    ("user", "{input}")
])

agent = create_openai_tools_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# Define state
class AgentState(TypedDict):
    messages: Sequence
    input: str

# Define nodes
def agent_node(state):
    input_msg = state["input"] if "input" in state else state["messages"][-1].content
    response = agent_executor.invoke({"input": input_msg})
    return {"messages": state["messages"] + [AIMessage(content=response["output"])]}

# Create graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)

# Compile
chain = workflow.compile()

# Use
result = chain.invoke({"messages": [HumanMessage(content="What is 25 * 16?")]})
print(result["messages"][-1].content)
```

## Adding Memory

Now let's add memory to our agent:

```python
from langgraph.checkpoint.memory import MemorySaver

# Define state with memory
class AgentStateWithMemory(TypedDict):
    messages: Sequence
    memory: dict

# Define memory operations
def add_to_memory(state, key, value):
    state["memory"][key] = value
    return state

def get_from_memory(state, key):
    return state["memory"].get(key, None)

# Create a memory-aware node
def memory_aware_node(state):
    messages = state["messages"]
    memory = state["memory"]
    
    # Add context from memory if available
    context = f"Previous info: {memory.get('previous_info', 'None')}"
    
    # Process with model
    augmented_prompt = messages[-1].content + "\n" + context
    response = model.invoke([HumanMessage(content=augmented_prompt)])
    
    # Update memory
    memory["last_response"] = response.content
    
    return {"messages": messages + [response], "memory": memory}

# Create graph with persistence
memory_saver = MemorySaver()
workflow = StateGraph(AgentStateWithMemory, checkpointer=memory_saver)
workflow.add_node("process", memory_aware_node)
workflow.set_entry_point("process")
workflow.add_edge("process", END)

# Compile
chain = workflow.compile()

# Use with persistent state
result = chain.invoke({
    "messages": [HumanMessage(content="My name is Alice")],
    "memory": {}
})

# In a later interaction, memory persists
second_result = chain.invoke({
    "messages": [HumanMessage(content="What's my name?")],
    "memory": result["memory"]
})

print(second_result["messages"][-1].content)
```

## Human-in-the-Loop Controls

Adding human oversight to agent actions:

```python
from IPython.display import display
import ipywidgets as widgets

# Define human review state
class ReviewState(TypedDict):
    messages: Sequence
    needs_review: bool
    approved: bool

# Define AI node
def ai_node(state):
    messages = state["messages"]
    response = model.invoke(messages)
    
    # Determine if this needs review
    sensitive_topics = ["financial", "medical", "legal"]
    needs_review = any(topic in response.content.lower() for topic in sensitive_topics)
    
    return {
        "messages": messages + [response],
        "needs_review": needs_review,
        "approved": False
    }

# Define human review node (simplified for notebook)
def human_review_node(state):
    latest_message = state["messages"][-1].content
    print(f"Please review this response:\n{latest_message}")
    
    # In real application, you'd get human input here
    # For this example, we'll simulate approval
    approval = input("Approve? (y/n): ").lower() == 'y'
    
    return {
        "messages": state["messages"],
        "needs_review": False,
        "approved": approval
    }

# Define router function
def review_router(state):
    if state["needs_review"]:
        return "human_review"
    return "end"

# Create graph
workflow = StateGraph(ReviewState)
workflow.add_node("ai", ai_node)
workflow.add_node("human_review", human_review_node)

# Add conditional edges
workflow.add_conditional_edges(
    "ai",
    review_router,
    {
        "human_review": "human_review",
        "end": END
    }
)
workflow.add_edge("human_review", END)
workflow.set_entry_point("ai")

# Compile
chain = workflow.compile()
```

## Customizing State

Creating complex state objects for specific applications:

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal

# Define a rich state model
class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str

class AgentAction(BaseModel):
    tool: str
    input: Dict
    timestamp: str

class RichAgentState(BaseModel):
    messages: List[Message] = Field(default_factory=list)
    actions: List[AgentAction] = Field(default_factory=list)
    context: Dict = Field(default_factory=dict)
    current_step: int = 0
    error_count: int = 0
    max_steps: int = 10

# Use with LangGraph
def process_with_custom_state(state: RichAgentState):
    # Access structured state elements
    current_messages = state.messages
    context_data = state.context
    
    # Business logic using structured state
    if state.current_step >= state.max_steps:
        return state.model_copy(update={"messages": current_messages + [Message(role="assistant", content="Maximum steps reached")]})
    
    # Process with model
    response = model.invoke([{"role": m.role, "content": m.content} for m in current_messages])
    
    # Update state
    return state.model_copy(
        update={
            "messages": current_messages + [Message(role="assistant", content=response.content)],
            "current_step": state.current_step + 1
        }
    )

# With LangGraph
from langgraph.graph import StateGraph, END

graph = StateGraph(RichAgentState)
graph.add_node("process", process_with_custom_state)
graph.set_entry_point("process")
graph.add_edge("process", END)

agent = graph.compile()
```

## Time Travel

LangGraph supports "time travel" for exploring alternative paths and debugging:

```python
from langgraph.checkpoint import MemorySaver

# Create a graph with checkpoints
memory_checkpointer = MemorySaver()
graph = StateGraph(AgentState, checkpointer=memory_checkpointer)

# Add nodes and edges
graph.add_node("assistant", assistant_node)
graph.add_node("tools", tools_node)
graph.set_entry_point("assistant")
graph.add_edge("assistant", "tools")
graph.add_conditional_edges(
    "tools",
    tools_router,
    {
        "continue": "assistant",
        "end": END
    }
)

# Compile with thread manager
chain = graph.compile()

# Run the chain and save the thread ID
result = chain.invoke({"messages": [HumanMessage(content="Tell me about LangGraph")]})
thread_id = chain.get_thread_id(result)

# Later, we can rewind to a specific step
checkpoints = memory_checkpointer.list_checkpoints(thread_id)
third_checkpoint = checkpoints[2]  # Rewind to third step

# Create a new branch from that checkpoint
new_result = chain.invoke(
    {"messages": [HumanMessage(content="Tell me about LangGraph differently")]},
    thread_id=thread_id,
    checkpoint_id=third_checkpoint
)
```

## Multi-Agent Systems

Creating systems with multiple collaborating agents:

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

# Define different specialist agents
researcher_model = ChatOpenAI(model="gpt-4")
writer_model = ChatOpenAI(model="gpt-4")
reviewer_model = ChatOpenAI(model="gpt-4")

# Define state
class TeamState(TypedDict):
    task: str
    research: str
    draft: str
    feedback: str
    final_document: str

# Define nodes
def researcher_node(state):
    task = state["task"]
    research_prompt = f"Research this topic thoroughly: {task}"
    response = researcher_model.invoke([HumanMessage(content=research_prompt)])
    return {"research": response.content}

def writer_node(state):
    task = state["task"]
    research = state["research"]
    writing_prompt = f"Write content about {task} based on this research: {research}"
    response = writer_model.invoke([HumanMessage(content=writing_prompt)])
    return {"draft": response.content}

def reviewer_node(state):
    draft = state["draft"]
    review_prompt = f"Review this draft critically: {draft}"
    response = reviewer_model.invoke([HumanMessage(content=review_prompt)])
    return {"feedback": response.content}

def finalizer_node(state):
    draft = state["draft"]
    feedback = state["feedback"]
    finalize_prompt = f"Improve this draft based on feedback.\nDraft: {draft}\nFeedback: {feedback}"
    response = writer_model.invoke([HumanMessage(content=finalize_prompt)])
    return {"final_document": response.content}

# Create graph
workflow = StateGraph(TeamState)

# Add nodes
workflow.add_node("researcher", researcher_node)
workflow.add_node("writer", writer_node)
workflow.add_node("reviewer", reviewer_node)
workflow.add_node("finalizer", finalizer_node)

# Add edges
workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", "reviewer")
workflow.add_edge("reviewer", "finalizer")
workflow.add_edge("finalizer", END)

# Compile
team = workflow.compile()

# Use
result = team.invoke({"task": "Explain how LangGraph enables multi-agent collaboration"})
print(result["final_document"])
```

## Advanced Techniques

### Cyclic Graphs and Self-Improvement

```python
from langgraph.graph import StateGraph, END
from typing import Annotated, TypedDict, Sequence
import operator

# Define state for self-improving agent
class ImprovingAgentState(TypedDict):
    messages: Sequence
    iterations: int
    max_iterations: int
    current_solution: str

# Define nodes
def solve_node(state):
    messages = state["messages"]
    iterations = state["iterations"]
    current = state["current_solution"]
    
    context = f"Previous solution (iteration {iterations}): {current}" if current else "First attempt"
    prompt = messages[-1].content + "\n" + context
    
    response = model.invoke([HumanMessage(content=prompt)])
    
    return {
        "messages": messages,
        "iterations": iterations + 1,
        "max_iterations": state["max_iterations"],
        "current_solution": response.content
    }

def evaluate_node(state):
    solution = state["current_solution"]
    eval_prompt = f"Critically evaluate this solution and suggest improvements: {solution}"
    response = model.invoke([HumanMessage(content=eval_prompt)])
    
    return {
        "messages": state["messages"] + [AIMessage(content=response.content)],
        "iterations": state["iterations"],
        "max_iterations": state["max_iterations"],
        "current_solution": state["current_solution"]
    }

# Define router
def iteration_router(state):
    if state["iterations"] < state["max_iterations"]:
        return "continue"
    return "complete"

# Create graph with cycle
workflow = StateGraph(ImprovingAgentState)
workflow.add_node("solve", solve_node)
workflow.add_node("evaluate", evaluate_node)

workflow.set_entry_point("solve")
workflow.add_edge("solve", "evaluate")

# Add conditional edge that creates a cycle
workflow.add_conditional_edges(
    "evaluate",
    iteration_router,
    {
        "continue": "solve",  # Loop back
        "complete": END
    }
)

# Compile
improving_agent = workflow.compile()

# Use
result = improving_agent.invoke({
    "messages": [HumanMessage(content="Design an algorithm for efficient document retrieval")],
    "iterations": 0,
    "max_iterations": 3,
    "current_solution": ""
})

print(f"Final solution after {result['iterations']} iterations:")
print(result["current_solution"])
```

## Conclusion

LangGraph provides a powerful framework for building complex, stateful AI systems with controllable workflows. Its key strengths include:

- **Reliability and controllability** through explicit state management and graph-based workflows
- **Extensibility** through its low-level primitives that avoid rigid abstractions
- **First-class streaming support** for transparency into agent reasoning
- **Checkpoint management** enabling time travel and exploration of alternative paths

For more information and detailed documentation, visit:
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [GitHub Repository](https://github.com/langchain-ai/langgraph)
- [LangSmith](https://smith.langchain.com/) for debugging and monitoring

---

*This tutorial serves as an introduction to LangGraph. For production applications, always refer to the latest documentation and best practices.* 