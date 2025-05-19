# Enabling Tool Use and Planning in Agents

## Overview
This chapter explores how intelligent agents use tools and planning algorithms to accomplish complex tasks. By combining robust planning strategies with the ability to access and utilize external tools, AI agents can extend their capabilities beyond their inherent knowledge limitations, allowing them to solve a wider range of problems more effectively. We will delve into the mechanisms of tool integration, various planning paradigms suitable for Large Language Model (LLM)-based agents, and practical implementations using LangChain and LangGraph.

## Key Concepts

### Understanding Tool Use in Agents
- **Definition**: Tool usage refers to an agent's ability to identify the need for, select, and leverage external resources, software functions, or APIs to augment its functionality, gather information, or interact with the environment.
- **Tool Calling vs. Function Calling**:
  - **Function Calling**: Typically refers to an LLM generating a structured request (e.g., JSON) that specifies a function to be executed *within the same application or runtime environment* as the agent. The agent\'s internal code directly handles this call. For example, an LLM might output a JSON object like `{"function": "calculator", "parameters": {"expression": "2+2"}}`, which the agent\'s code then parses and executes locally.
  - **Tool Calling**: A broader term that encompasses function calling but often implies interaction with *external* APIs, services, systems, or even physical hardware. The LLM still generates a structured request, but the agent controller might need to make network requests, interact with operating system utilities, or interface with other processes. For example, calling a weather API, a database, or a custom enterprise API.
  - **Nuance**: The line can be blurry. A "function" could be a wrapper around an external API call. The key distinction often lies in whether the execution stays within the agent\'s immediate process or involves external communication/systems. LangChain and other frameworks often use "tool" as the general term.
- **LLM Tool Calling Process**:
  1.  **Intent Recognition & Tool Selection**: The LLM, based on the user query and its current context, determines that a task requires an external tool. It selects the most appropriate tool from a predefined set.
  2.  **Parameter Generation**: The LLM generates the necessary parameters for the selected tool in a structured format (often JSON).
  3.  **Agent Controller Execution**: The agent\'s control logic (e.g., a LangGraph node) receives this structured request. It parses the tool name and parameters.
  4.  **Tool Execution**: The controller invokes the actual tool/function with the provided parameters. This might involve making an API call, querying a database, or running a local script.
  5.  **Result Handling**: The tool returns a result (data, success/failure status, error message).
  6.  **Error Management**: If the tool call fails, the agent might have retry logic, attempt a different tool, or inform the LLM/user of the failure.
  7.  **Response Formulation**: The result from the tool is passed back to the LLM.
  8.  **Continuation**: The LLM uses the tool\'s output to continue the conversation, generate a final answer, or decide on the next step (which might involve another tool call).
  *(Conceptual Diagram: User Request -> LLM (Selects Tool & Params) -> Agent Controller (Parses & Executes) -> External Tool -> Result -> Agent Controller -> LLM (Processes Result) -> User Response)*
- **Security Considerations for Tool Use**:
    - **Input Sanitization**: Never trust LLM-generated parameters directly, especially if they are used in shell commands, database queries, or API calls that can have side effects. Sanitize and validate all inputs.
    - **Least Privilege**: Tools should operate with the minimum permissions necessary. If a tool reads from a database, it shouldn\'t have write access unless explicitly required.
    - **API Key Management**: Securely store and manage API keys and other credentials. Use environment variables or dedicated secret management services.
    - **Rate Limiting & Cost Control**: Be mindful of API rate limits and potential costs associated with tool use. Implement safeguards.
    - **Sandboxing**: For tools that execute code (e.g., a Python interpreter tool), run them in a sandboxed environment to prevent malicious actions.
    - **User Confirmation**: For tools that perform critical actions (e.g., sending an email, modifying a file, making a purchase), consider adding a user confirmation step.

### Defining Tools for Agents
- **Framework Approach (e.g., LangChain, LlamaIndex)**:
  - Often involves defining a Python class or using decorators.
  - Docstrings are crucial: They are often used by the LLM to understand the tool\'s purpose, when to use it, its required inputs (name, type, description), and expected outputs.
  - Example (Conceptual LangChain Tool):
    ```python
    from langchain_core.tools import tool

    @tool
    def get_weather(location: str, unit: str = "celsius") -> str:
        \"\"\"Returns the current weather for a specified location.
        Args:
            location: The city and state, e.g., "San Francisco, CA".
            unit: Temperature unit, either "celsius" or "fahrenheit". Defaults to "celsius".
        \"\"\"
        # ... implementation to call a weather API ...
        return f"The weather in {location} is..." 
    ```
- **Direct LLM Integration (e.g., OpenAI API)**:
  - Tools are defined using a JSON schema that describes the function name, description, and parameters (including their types and descriptions).
  - This schema is provided to the LLM as part of the API call.
- **Tool Types & Examples**:
  - **API tools**:
    - *Example*: A tool to search for academic papers on arXiv.
    - *Pseudo-code*: `arxiv_search(query: str) -> List[PaperSummary]`
  - **Database tools**:
    - *Example*: A tool to query a SQL database for customer orders.
    - *Pseudo-code*: `query_customer_database(sql_query: str) -> List[Row]`
  - **Utility functions**:
    - *Example*: A tool to perform complex mathematical calculations.
    - *Pseudo-code*: `advanced_calculator(expression: str) -> float`
    - *Example*: A tool to summarize long text.
    - *Pseudo-code*: `summarize_text(text: str, length: int) -> str`
  - **Integration tools**:
    - *Example*: A tool to create a new issue in a GitHub repository.
    - *Pseudo-code*: `create_github_issue(repo: str, title: str, body: str) -> IssueLink`
  - **Hardware interface tools**:
    - *Example*: A tool to control a smart home device (e.g., turn on lights).
    - *Pseudo-code*: `set_light_status(light_id: str, status: bool) -> Confirmation`

#### Key Design Considerations for Tool Integration:
- **Clear Tool Abstraction and Interface**: Define tools with a consistent interface (e.g., common method signatures for execution, standardized input/output formats). This makes it easier for the agent (and developers) to work with diverse tools.
- **Robust Error Handling and Reporting**: Tools must have robust internal error handling and report errors back to the agent in a structured way. The agent needs to understand if a tool call failed, why it failed (if possible), and what to do next (e.g., retry, try an alternative tool, inform the user).
- **Tool Discovery and Selection Logic**: If the agent has many tools, design an efficient and accurate mechanism for it to select the appropriate tool(s) for a given task. This might involve LLM-based selection based on tool descriptions, or more structured decision trees or classifiers.
- **Parameter Validation and Sanitization**: As mentioned in Security Considerations, rigorously validate and sanitize any parameters generated by the LLM before passing them to a tool, especially for tools with side effects or those executing commands.
- **Configuration and Management**: For agents with many tools, consider a tool management system that allows for easy addition, removal, and updating of tools, including their configurations (e.g., API keys, endpoints).
- **Performance Monitoring of Tools**: Track the performance (latency, success/failure rates) of individual tools. This helps identify slow or unreliable tools that might need optimization or replacement.
- **User Feedback on Tool Actions**: For actions taken by tools that directly impact the user or environment, provide clear feedback to the user about what action was taken and by which tool.
- **Idempotency of Tools**: Where feasible, design tools to be idempotent so that retrying a failed tool call doesn't lead to unintended multiple executions.
- **Contextual Tool Behavior**: Some tools might need to behave differently based on the agent's current context or state. Design how this context is passed to and utilized by the tools.

### Planning Algorithms for Agents
Planning is the process by which an agent decides on a sequence of actions to achieve a goal.

#### Key Design Considerations for Agent Planning Systems:
- **Plan Representation**: Choose a suitable representation for plans (e.g., linear sequences of actions, hierarchical task networks, state graphs). The representation should be expressive enough for the complexity of tasks and easy for the agent to generate, execute, and modify.
- **Planning Horizon and Granularity**: Decide on the appropriate level of detail for plans. Should the agent plan far into the future with fine-grained steps, or create high-level plans that are refined dynamically? This depends on the task and the predictability of the environment.
- **Plan Generation Strategy**: Select a planning algorithm or strategy (e.g., LLM-based generation like ReAct, classical planners, HTN) that fits the agent's capabilities and the nature of the problems it solves. Consider the trade-off between plan optimality and planning time.
- **Execution Monitoring**: Implement a robust mechanism to monitor the execution of the plan. This includes tracking which steps have been completed, detecting failures, and identifying deviations from the expected outcomes.
- **Replanning and Adaptation**: Design the system to handle plan failures or unexpected changes in the environment. This requires the ability to re-plan dynamically, either by modifying the existing plan or generating a new one. LLMs can be very effective at replanning given new context.
- **Resource Management in Planning**: If actions in a plan consume resources (e.g., time, budget, API call quotas), the planner should ideally consider these constraints.
- **Integration with Tool Use**: Planning often involves sequencing tool calls. Ensure the planner can correctly identify when tools are needed, which tools to use, and how to incorporate their outputs into the ongoing plan.
- **Learning from Planning Experience**: Consider how the agent might learn from successful or failed plans to improve its planning capabilities over time (e.g., by storing and reusing effective plan skeletons, or by learning better heuristics for plan generation).
- **User Collaboration in Planning**: For some applications, allow users to inspect, modify, or approve plans generated by the agent, fostering a collaborative planning process.
- **Explainability of Plans**: Especially for complex plans, the agent should be able to explain (at some level) why it chose a particular sequence of actions.

- **Less Practical Algorithms for LLM Agents**:
  - **STRIPS (Stanford Research Institute Problem Solver)**: Represents states as sets of logical propositions and actions by pre-conditions and post-conditions. *Why less practical for LLMs*: Too rigid and formal for the nuances of natural language; LLM interactions are not easily reducible to binary state propositions.
  - **A\* Planning**: A graph traversal and path search algorithm, which finds the shortest path between a start node and a goal node. *Why less practical for LLMs*: Defining a meaningful "distance" or heuristic cost function (`h(n)`) in the vast, high-dimensional space of language and LLM-generated states is extremely challenging.
  - **GraphPlan**: Builds a planning graph and searches for a valid plan. *Why less practical for LLMs*: Assumes discrete states and actions, struggles with the open-ended and often unpredictable nature of LLM outputs and interactions.
  - **Monte Carlo Tree Search (MCTS)**: A heuristic search algorithm for some kinds of decision processes, most notably game playing. *Why less practical for LLMs*: Simulating numerous possible future states and LLM interactions is computationally very expensive and slow, making it impractical for real-time agent responses.
- **Moderately Practical**:
  - **Fast Forward (FF)**: A heuristic search planner that uses a relaxed planning graph to guide its search. It\'s goal-oriented. *How it can be adapted*: The concept of identifying helpful actions towards a goal can be mimicked by prompting an LLM to break down a task and identify next steps. *Limitations*: Still relies on a more structured state/action representation than what LLMs naturally provide; defining heuristics can be tricky.
- **Most Practical Algorithms for LLM Agents**:
  - **LLM-based Planning**: Leverages the LLM itself to generate plans.
    - **Strategies**:
        - **ReAct (Reason and Act)**: The LLM generates both a reasoning trace (thought) and an action for each step. The action can be a tool call or a final response. The observation from the action is fed back to the LLM for the next thought/action cycle.
        - **Self-Ask**: The LLM iteratively asks itself questions to break down a problem, answers them (often using tools), and then uses these intermediate answers to solve the main problem.
        - **Plan-and-Execute**: The LLM first generates a multi-step plan. Then, an agent controller executes each step of the plan, potentially calling tools and feeding results back to the LLM if the plan needs adjustment.
    - *Conceptual Example (ReAct-like)*:
        User: "What\'s the weather in Paris and can you book me a flight there for next week?"
        LLM Thought 1: "I need to find the weather in Paris and then search for flights. I\'ll start with the weather."
        LLM Action 1: `get_weather(location="Paris, FR")`
        Tool Result: "The weather in Paris is 15°C and sunny."
        LLM Thought 2: "Okay, weather is good. Now I need to find flights. I need the current date to determine 'next week'."
        LLM Action 2: `get_current_date()`
        Tool Result: "Today is 2023-10-26."
        LLM Thought 3: "Next week starts around 2023-11-02. I need a destination (Paris) and origin. I should ask the user for the origin."
        LLM Action 3: `ask_user(question="What is your departure city for the flight to Paris?")`
        ...and so on.
  - **Hierarchical Task Network (HTN)**: Decomposes complex tasks into smaller, manageable subtasks (methods) in a hierarchical manner until primitive actions (operators) are reached.
    - *How it works with LLMs*: An LLM can be prompted to perform the task decomposition. For example, "Plan a vacation to Italy" might be decomposed into "Plan Travel," "Plan Accommodation," "Plan Activities." Each of_these can be further decomposed.
    - *Benefits*: Excellent for complex, multi-step tasks requiring structured organization. Allows for reuse of methods for common sub-problems.
    - *Illustrative Task Breakdown*:
        Task: `Organize a Birthday Party`
        Methods:
            1. `GuestListAndInvitations`
                - `CompileGuestList` (primitive)
                - `DesignInvitation` (primitive, maybe using an image generation tool)
                - `SendInvitations` (primitive, maybe using an email tool)
            2. `VenueAndDecorations`
                - `BookVenue` (primitive, tool call to a booking system)
                - `PlanDecorations` (primitive)
                - `BuyDecorations` (primitive, tool call to an e-commerce API)
            3. `FoodAndCake`
                - `OrderCatering` (primitive)
                - `OrderCake` (primitive)
- **Other Relevant Planning Concepts**:
    - **Reconfigurable/Adaptive Planning**: The ability of an agent to modify its plan during execution if unexpected events occur or if a step fails. LLMs can be prompted to re-plan based on new information.
    - **Role of Memory in Planning**: Short-term memory (scratchpad) is crucial for LLM-based planners like ReAct to maintain context across steps. Long-term memory can store successful (or failed) plans for future reuse or learning.

### RouterChain in LangChain

One of the simplest planning approaches is to use a router pattern that selects the right tool or specialized chain for a given task. LangChain\'s LCEL (LangChain Expression Language) provides a `RouterChain` implementation.

```python
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI # Assuming use of OpenAI LLM
# Define placeholder chains for illustration
from langchain.chains.llm import LLMChain

# Define the different specialized chains (placeholders)
# In a real scenario, these would be more complex chains, possibly involving tools
llm = OpenAI() # Initialize your LLM
prompt_travel = PromptTemplate.from_template("Handle travel query: {input}")
travel_chain = LLMChain(llm=llm, prompt=prompt_travel)

prompt_dining = PromptTemplate.from_template("Handle dining query: {input}")
dining_chain = LLMChain(llm=llm, prompt=prompt_dining)

prompt_activities = PromptTemplate.from_template("Handle activities query: {input}")
activities_chain = LLMChain(llm=llm, prompt=prompt_activities)

error_chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template("Cannot route: {input}"))


# Define the routing logic
# A more nuanced template could include examples or more specific instructions
router_template = \"\"\"Given a user request, classify it into one of the following categories: Travel, Dining, or Activities.
If the request is about booking flights, hotels, or transportation, classify as Travel.
If the request is about restaurant recommendations, reviews, or reservations, classify as Dining.
If the request is about finding things to do, local attractions, or events, classify as Activities.
If unsure, classify as Error.

Request: {input}
Classification:\"\"\"

router_prompt = PromptTemplate(
    template=router_template,
    input_variables=[\"input\"],
    output_parser=RouterOutputParser(next_chains=["Travel", "Dining", "Activities"]), # Inform parser of valid next chains
)

# Create the router chain
router_chain = LLMRouterChain.from_llm(
    llm=OpenAI(), # Or your chosen LLM
    prompt=router_prompt,
    # output_parser is implicitly handled by from_llm when prompt has an output_parser
)

# Create the multi-route chain
chain = MultiPromptChain(
    router_chain=router_chain,
    destination_chains={
        "Travel": travel_chain,
        "Dining": dining_chain,
        "Activities": activities_chain,
    },
    default_chain=error_chain, # Chain to use if routing fails or LLM outputs an unknown destination
    verbose=True
)

# Use the chain
# response = chain.invoke({"input": "I need a hotel in Paris for next week"})
# print(response)
# response = chain.invoke({"input": "Suggest some good Italian restaurants nearby."})
# print(response)
```

The `RouterChain` directs requests to specialized sub-chains.
- **`RouterOutputParser`**: This parser is crucial. It takes the raw output from the LLM (which is supposed to be the name of the destination chain, e.g., "Travel") and structures it into a dictionary that `MultiPromptChain` can use. This dictionary typically includes the `destination` (the name of the next chain) and `next_inputs` (the original input to be passed to that destination chain). It ensures the LLM's routing decision is correctly interpreted.
- **Limitations**:
    - **Simple Logic**: Primarily designed for selecting one path out of many based on a single classification.
    - **No Sequential Dependencies**: Not inherently designed for tasks where Step B depends on the output of Step A, unless the destination chains themselves handle such logic internally.
    - **Limited Conditional Logic**: Struggles with complex conditional branching beyond the initial route.

### Parallel Planner in LangGraph

For more complex planning that involves multiple concurrent actions, LangGraph provides a parallel execution pattern that enables fan-out/fan-in workflows. This is particularly useful for travel planning where you might want to search for flights, hotels, and activities simultaneously. This pattern is exemplified in the `travel_booking_parallel_planner.py` lab.

```python
from typing import TypedDict, List, Dict, Optional

# State typing for clarity and safety
class PlannerState(TypedDict, total=False):
    # total=False means not all keys need to be present in every state update.
    # This is useful as different nodes might populate different parts of the state.
    origin: Optional[str]
    destination: str
    date: Optional[str] # For flights
    check_in: Optional[str] # For hotels
    check_out: Optional[str] # For hotels
    flights: Optional[List[Dict]]  
    hotels: Optional[List[Dict]]
    activities: Optional[List[Dict]]
    itinerary: Optional[Dict]
    error: Optional[str] # To capture errors from tool calls

# Placeholder tool functions (in a real app, these would call APIs)
def search_flights(origin: str, destination: str, date: str) -> List[Dict]:
    print(f"Searching flights from {origin} to {destination} on {date}")
    if not origin or not date: return [{"error": "Missing origin or date for flight search"}]
    return [{"flight_id": "FL123", "price": 300, "duration": "6h"}] 

def find_hotels(destination: str, check_in: str, check_out: str) -> List[Dict]:
    print(f"Finding hotels in {destination} from {check_in} to {check_out}")
    if not check_in or not check_out: return [{"error": "Missing check-in or check-out date for hotel search"}]
    return [{"hotel_id": "H456", "name": "Grand Hotel", "price": 150}]

def find_activities(destination: str, date_range: str) -> List[Dict]:
    print(f"Finding activities in {destination} for {date_range}")
    return [{"activity_id": "A789", "name": "Museum Visit", "type": "Cultural"}]

# Separate nodes for different search operations
def flight_node(state: PlannerState) -> Partial[PlannerState]:
    try:
        flights = search_flights(
            state.get("origin"), state["destination"], state.get("date")
        )
        return {"flights": flights}
    except Exception as e:
        return {"error": f"Flight search failed: {e}", "flights": []}


def hotel_node(state: PlannerState) -> Partial[PlannerState]:
    try:
        hotels = find_hotels(
            state["destination"], state.get("check_in"), state.get("check_out")
        )
        return {"hotels": hotels}
    except Exception as e:
        return {"error": f"Hotel search failed: {e}", "hotels": []}

def activity_node(state: PlannerState) -> Partial[PlannerState]:
    try:
        date_range = f"{state.get('check_in', 'N/A')} – {state.get('check_out', 'N/A')}"
        activities = find_activities(state["destination"], date_range)
        return {"activities": activities}
    except Exception as e:
        return {"error": f"Activity search failed: {e}", "activities": []}


# A merge node that compiles results into a final itinerary
# This node acts as the "fan-in" point after parallel execution.
def merge_itinerary(state: PlannerState) -> Partial[PlannerState]:
    itinerary = {
        "flights": state.get("flights", []),
        "hotel": min(state.get("hotels", []), key=lambda h: h.get("price", float('inf')), default={"error": "No hotels found or hotel data incomplete"}),
        "activities": state.get("activities", []),
    }
    # Consolidate errors
    errors = []
    if state.get("error"): errors.append(state["error"]) # General error
    for flight_list in state.get("flights", []):
        if isinstance(flight_list, list): # Check if it's a list of flights
             for flight in flight_list:
                if isinstance(flight, dict) and flight.get("error"): errors.append(f"Flight Error: {flight['error']}")
        elif isinstance(flight_list, dict) and flight_list.get("error"): # if search_flights itself returned a single error dict
            errors.append(f"Flight Error: {flight_list['error']}")

    # Similar error checking for hotels and activities if their tool functions can return error dicts
    # For simplicity, we assume hotels and activities lists don't contain error dicts themselves here,
    # but a robust implementation would check.

    final_state_update = {"itinerary": itinerary}
    if errors:
        final_state_update["error"] = "; ".join(errors) # Combine all errors
    return final_state_update
```

The graph structure enables parallel execution:
```python
from langgraph.graph import StateGraph, END
from typing import Partial # Required for LangGraph node return types

def build_planner_graph() -> StateGraph:
    g = StateGraph(PlannerState)

    # Entry point: "start" node. It doesn't do much, just passes the initial state.
    # It acts as the initial "fan-out" point.
    g.add_node("start", lambda s: s) 
    g.set_entry_point("start")
    
    # Add parallel branch nodes
    g.add_node("flights", flight_node)
    g.add_node("hotels", hotel_node)
    g.add_node("activities", activity_node)

    # All parallel branches lead from "start"
    g.add_edge("start", "flights")
    g.add_edge("start", "hotels")
    g.add_edge("start", "activities")

    # Add the merge node
    g.add_node("merge", merge_itinerary)

    # After each parallel branch completes, it goes to the "merge" node.
    # This creates the "fan-in" point.
    # LangGraph handles waiting for all incoming edges to "merge" before executing it,
    # if "merge" is configured as a barrier or if it's the natural convergence point.
    # For simple fan-out/fan-in, we define conditional edges or a collector node.
    # A more robust way to handle this join is by using a conditional edge from each
    # parallel node that checks if all data is ready, or by having a dedicated collector node.

    # For simplicity in this example, we'll route all to merge.
    # In a real LangGraph setup for joining parallel branches, you'd typically have:
    # 1. The parallel nodes (flights, hotels, activities).
    # 2. A "join" node (our 'merge' node) that is only run after all parallel nodes complete.
    # LangGraph implicitly handles this if 'merge' is the single successor to all parallel nodes
    # and there are no other paths.
    # To make the join explicit and robust, especially with conditional routing,
    # one might use a counter or check for the presence of all required data in the state
    # before proceeding to the merge node, often using conditional edges.

    g.add_edge("flights", "merge")
    g.add_edge("hotels", "merge")
    g.add_edge("activities", "merge")
    
    # End after merging
    g.add_edge("merge", END)
    
    return g.compile()

# Example Usage:
# planner = build_planner_graph()
# initial_state = {"origin": "NYC", "destination": "Paris", "date": "2024-12-01", "check_in": "2024-12-01", "check_out": "2024-12-08"}
# for event in planner.stream(initial_state):
#     print(event)
#     print("---")
```
- **`PlannerState` TypedDict**: `total=False` is used because not all pieces of information (like `flights`, `hotels`) will be available at every step of the graph. Nodes update only parts of the state. Defining the state structure upfront helps with type checking and understanding data flow.
- **Fan-out/Fan-in**:
    - **Fan-out**: From the `start` node, the graph branches out to `flights`, `hotels`, and `activities` nodes. These can (conceptually and often practically, depending on the LangGraph executor) run in parallel if they don't have direct dependencies on each other's immediate output for *initiation*.
    - **Fan-in**: The `merge_itinerary` node acts as the convergence point. LangGraph ensures that this node runs only after all its prerequisite parallel branches (`flights`, `hotels`, `activities` in this setup) have completed and updated the state.
- **Error Handling in Parallel Branches**:
    - Each node (`flight_node`, `hotel_node`, `activity_node`) should ideally have its own try-except block.
    - If a tool call fails, the node can update the `PlannerState` with an error message (e.g., `state["error"] = "Flight API unavailable"` or add to a list of errors `state["errors"].append(...)`).
    - The `merge_itinerary` node (or a subsequent error handling node) can then inspect these error fields. It could decide to:
        - Proceed with partial results if some branches succeeded.
        - Halt and report the errors.
        - Trigger a retry mechanism for the failed branches (more advanced, might involve looping back in the graph).
- **Conditional Edges & Complex Merging**:
    - Instead of directly connecting all parallel nodes to `merge_itinerary`, you could have conditional edges. For example, after `flight_node`, an edge could check `if state.get("flights")`.
    - A more complex merge node might:
        - Prioritize certain results (e.g., if flights are essential but activities are optional).
        - Attempt to find alternatives if a primary option failed (e.g., search for trains if flights failed).
        - Aggregate data in more sophisticated ways (e.g., calculate total cost).

### Advanced Planning and Tool Orchestration with LangGraph

LangGraph's flexibility allows for more sophisticated planning beyond simple parallel execution.

- **Conditional Tool Execution**:
  - Use conditional edges to decide whether to run a tool based on the current state. For example, only call a `book_hotel` tool if `find_hotels` returned valid options and the user confirmed.
  ```python
  # def should_book_hotel(state: PlannerState) -> str:
  #     if state.get("hotels") and not state.get("hotels")[0].get("error") and state.get("user_confirmation_for_hotel"):
  #         return "book_hotel_node"
  #     return "skip_hotel_booking_node" # or END
  # g.add_conditional_edges("confirm_hotel_node", should_book_hotel, {"book_hotel_node": "book_hotel_node", "skip_hotel_booking_node": "some_other_node_or_END"})
  ```
- **Dynamic Tool Selection**:
  - An LLM node can act as a planner that, at each step, decides the *next* tool to use based on the overall goal and the current state. This is closer to the ReAct or Self-Ask paradigm implemented within a graph.
  - The LLM's output would be parsed to determine the next node (tool) to route to.
- **Integrating Reflection/Self-Critique (from Chapter 4)**:
  - After a planning step or a tool execution, a "reflection node" can be added.
  - This node (powered by an LLM) would:
    1.  Review the last action and its outcome.
    2.  Assess if the outcome aligns with the goal.
    3.  If not, suggest modifications:
        - Re-try a tool with different parameters.
        - Choose an alternative tool.
        - Revise the plan.
  - This creates a loop: Plan -> Act -> Observe -> Reflect -> Re-plan/Act.
  - The `reflection_langgraph.py` lab from Chapter 4 provides a template for such a self-critique loop, which can be adapted for planning. For instance, if a `search_flights` tool returns no results, a reflection node could analyze why (e.g., "Maybe the date is too far in the future, or the origin/destination pair is uncommon") and suggest trying with adjusted dates or nearby airports.
- **Conceptual Link to `travel_booking_parallel_planner.py`**:
  - While the lab focuses on parallel execution, it can be extended. Imagine after the `merge_itinerary` node, if the itinerary is incomplete or unsatisfactory (e.g., no flights found, or hotel price too high), a conditional edge could route the state to a "refine_plan_node". This node, using an LLM, would look at the `PlannerState` (including any errors) and decide what to do next:
    - Re-run `flight_node` with different dates.
    - Add a new node, e.g., `alternative_transport_node` (search for trains).
    - Ask the user for more flexible parameters.
  - This makes the planner adaptive.

### Integrating DSPy for Tool Definition, Planning, and Parameter Generation

DSPy offers a programmatic way to define and optimize prompts, which can be highly beneficial for tool use and planning in agentic systems.

- **DSPy for Tool Selection & Parameter Generation**:
  - **Signatures for Tool Use**: You can define a DSPy `Signature` where the input is the user query and current context, and the output fields are `tool_name: str` and `tool_parameters: Dict`.
    ```python
    # import dspy
    # class SelectTool(dspy.Signature):
    #     \"\"\"Given the user query and conversation history, select the best tool and generate its parameters.\"\"\"
    #     user_query = dspy.InputField(desc="The user's latest request.")
    #     available_tools = dspy.InputField(desc="List of available tools with their descriptions.")
    #     # conversation_history = dspy.InputField(desc="The recent conversation history.") # Optional
        
    #     tool_name = dspy.OutputField(desc="The name of the selected tool (e.g., 'get_weather', 'search_flights').")
    #     tool_parameters = dspy.OutputField(desc="A dictionary of parameters for the selected tool.")

    # # This signature can be used in a DSPy module.
    # class ToolSelectorModule(dspy.Module):
    #     def __init__(self, tools_json_schema):
    #         super().__init__()
    #         self.tools_json_schema = tools_json_schema # Stringified JSON schema of tools
    #         self.select_tool = dspy.Predict(SelectTool)

    #     def forward(self, user_query):
    #         prediction = self.select_tool(user_query=user_query, available_tools=self.tools_json_schema)
    #         return prediction.tool_name, prediction.tool_parameters
    ```
  - The `available_tools` input field in the signature would be a description of your tools (similar to what you'd pass to OpenAI's function calling API, or derived from LangChain tool docstrings).
  - A DSPy teleprompter (optimizer like `BootstrapFewShot`) could then be used with examples of queries and desired tool/parameter outputs to generate and refine a few-shot prompt for the `SelectTool` predictor, making the LLM more reliable at choosing the correct tool and forming its parameters.
- **DSPy for LLM-based Planning**:
  - Similarly, a signature can be defined for generating a plan:
    ```python
    # class GeneratePlan(dspy.Signature):
    #     \"\"\"Generate a step-by-step plan to achieve the user's goal.\"\"\"
    #     user_goal = dspy.InputField(desc="The user's overall objective.")
    #     # available_tools = dspy.InputField(desc="List of available tools.") # Can be included
    #     plan = dspy.OutputField(desc="A list of strings, where each string is a step in the plan.")
    ```
  - The optimized DSPy module can then be a node in your LangGraph agent. The output `plan` (a list of steps) can be iterated over by subsequent LangGraph nodes, which might involve executing tools or further LLM calls for each step.
- **Integration into a LangGraph Workflow**:
  1.  **Initial Request**: User query comes in.
  2.  **DSPy Planning Node**: A LangGraph node containing a DSPy module (e.g., using `GeneratePlan` signature) generates an initial plan.
  3.  **DSPy Tool Selection/Parameter Node**: For each step in the plan that requires a tool, another LangGraph node with a DSPy module (e.g., `ToolSelectorModule`) determines the specific tool and its parameters.
  4.  **Tool Execution Node**: The selected tool is executed.
  5.  **Reflection/Update Node**: Results are fed back. If the plan needs adjustment or a tool failed, a reflection node (potentially also using DSPy for optimized reflective prompts) can update the plan or re-trigger tool selection.
- **Benefits**:
    - **Systematic Prompt Engineering**: DSPy provides a structured way to create and manage prompts for complex tasks like planning and tool use.
    - **Optimization**: Teleprompters can automatically find better prompts than manually crafted ones, leading to more robust and accurate agent behavior.
    - **Modularity**: DSPy modules can be developed and tested independently before being integrated into a larger LangGraph agent.

This chapter provides the foundational knowledge for building agents that can intelligently plan and utilize tools, significantly expanding their problem-solving capabilities. The combination of LangGraph's state management and execution flow with the LLM's reasoning, augmented by DSPy's optimization, offers a powerful toolkit for developing sophisticated agentic systems. The `travel_booking_parallel_planner.py` lab provides a practical starting point for implementing some of these concepts.