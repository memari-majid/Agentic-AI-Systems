# LangGraph: Orchestrating Complex Agentic Behavior

⏱️ **Estimated reading time: 13 minutes**

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