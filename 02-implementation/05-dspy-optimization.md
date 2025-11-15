## 5. Advanced Agent Optimization with DSPy
While LangChain provides the building blocks and LangGraph orchestrates complex agentic flows, DSPy (Declarative Self-improving Language Programs, pronounced "dee-spy") offers a powerful paradigm for optimizing the LLM-driven components within your agents. DSPy shifts from manual prompt engineering to a more programmatic and systematic approach where you define what you want the LLM to do (via Signatures) and then use DSPy's optimizers (Teleprompters) to figure out how to best prompt the LLM to achieve that, often based on a few examples and defined metrics.

This section provides a technical guide on integrating DSPy into your LangChain/LangGraph agentic systems to enhance their performance, adaptability, and robustness.

### 5.1. The Need for Programmatic Prompt Engineering in Agents
Manually crafting and iterating on prompts for complex agents can be: - Time-consuming: Finding the optimal wording, few-shot examples, or chain-of-thought structure requires extensive trial and error. - Brittle: Prompts optimized for one LLM or a specific task variant may not generalize well. - Hard to maintain: As agents evolve, managing and updating a large suite of hand-crafted prompts becomes cumbersome.

DSPy addresses these by allowing you to declare the task and let optimizers discover effective prompts. This is particularly beneficial in agentic systems where an LLM might be invoked for multiple distinct reasoning steps (e.g., understanding user intent, selecting a tool, formatting tool input, synthesizing information, reflecting on output).

### 5.2. Deep Dive into DSPy for Agentic Tasks
#### 5.2.1. Core DSPy Concepts
**Signatures**: These are declarative specifications of a task your LLM needs to perform. They define input fields (what information is provided) and output fields (what information is expected). Typed annotations are encouraged.

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
**Modules**: These are the building blocks of a DSPy program, analogous to layers in a neural network. They take one or more Signatures and an LLM, and implement a specific prompting strategy.

- `dspy.Predict`: The simplest module. It takes a Signature and an LLM, and generates a basic prompt to instruct the LLM to fill the output fields given the input fields.
- `dspy.ChainOfThought`: Takes a Signature and an LLM. It instructs the LLM to first generate a rationale (chain of thought) for how to arrive at the answer before producing the final output fields. This often improves reasoning for complex tasks.
- `dspy.ReAct`: Implements the ReAct (Reason+Act) prompting strategy, suitable for building agents that can iteratively use tools. While powerful, we will focus on using simpler DSPy modules for specific agent sub-tasks and integrating them into LangGraph for overall orchestration.
- `dspy.ProgramOfThought`: For tasks that require generating and executing code.

**Teleprompters (Optimizers)**: These are algorithms that tune the prompts used by your DSPy modules. They take your DSPy program (composed of modules), a metric to optimize for, and training data (often just a few examples).

- `BootstrapFewShot`: Generates few-shot examples for your prompts from your training data.
- `SignatureOptimizer` (formerly `BayesianSignatureOptimizer`): Systematically searches for better prompt instructions (e.g., for the `desc` fields in your Signature) to improve performance on your metric.
- `MIPRO` (Multi-prompt Instruction Proposer): A more advanced optimizer that can generate complex instruction sets.

#### 5.2.2. Technical Example: DSPy Module for Agent Tool Selection
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

### 5.3. Integrating DSPy Modules into LangChain
To use your optimized DSPy module within a LangChain or LangGraph agent, you can wrap it as a LangChain Tool. This allows the agent to invoke the DSPy module just like any other tool.

#### 5.3.1. Wrapping a DSPy Module as a LangChain Tool
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

### 5.4. Orchestrating DSPy-Powered Tools with LangGraph
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
1. **DSPy LM Configuration:** The `call_dspy_tool_selector_node` must have access to a DSPy-configured LLM (via `dspy.settings.configure(lm=...)`) for the `dspy_module` to work. This LM should ideally be the one used during DSPy optimization. I've added comments to highlight this; a real implementation needs to handle this robustly (e.g., by passing the LM, or ensuring the DSPy module is instantiated with its required LM). The placeholder simulates this. 
2. **Full Agent Loop:** The example graph is simplified. A production agent would typically loop back after tool execution, potentially to the DSPy selector or to another LLM call to synthesize a final answer from the tool's output. The `tool_executor` currently just leads to `END` for brevity if a tool was selected. 
3. **Error Handling:** Robust error handling within nodes (e.g., if a DSPy module fails or a tool errors out) is crucial.

### 5.5. Advanced DSPy Strategies for Agentic Systems
- **Few-Shot Learning for Agent Behavior:** Use `dspy.BootstrapFewShot` with examples of complex query -> tool choice/input sequences to generate effective few-shot prompts for your DSPy tool selector. This can teach the selector nuanced tool usage patterns.
- **Optimizing Agent Personas and System Prompts:** While DSPy is often used for specific modules, its principles can be applied to optimize parts of an agent's overall system prompt if you can define a metric for "good persona adherence" or "effective instruction following."
- **Self-Correction Loops with DSPy:** You can design a DSPy signature like `CritiqueAndRefineSignature(previous_attempt: str, critique_instructions: str, refined_output: str)`. A LangGraph cycle could then use one DSPy module to generate an initial response/action, another to critique it, and a third (or the same one with different instructions) to refine it based on the critique. This is powerful for improving response quality or tool use accuracy.

### 5.6. Synergies and Best Practices
- **LangChain for Foundation:** Use LangChain for its vast collection of LLM wrappers, document loaders, text splitters, embedders, vector stores, and basic tool definitions.
- **DSPy for Optimized Reasoning Kernels:** Identify critical reasoning steps within your agent (e.g., tool selection, query transformation, information synthesis, output formatting) and implement these as DSPy modules. Optimize these modules using DSPy teleprompters with relevant few-shot examples and metrics.
- **LangGraph for Orchestration & State:** Use LangGraph to define the high-level control flow, manage explicit state, handle cycles, and integrate human-in-the-loop (HITL) steps. Your DSPy-powered LangChain tools become nodes within this graph.
- **Modularity:** Keep DSPy modules focused on specific, well-defined tasks. This makes them easier to optimize and reuse.
- **Iterative Optimization:** Start with basic DSPy modules (`dspy.Predict` or `dspy.ChainOfThought` with default prompts). As you gather data and identify weaknesses, introduce teleprompters to optimize them. Don't prematurely optimize.
- **Evaluation is Key:** Define clear metrics for your DSPy module's performance (e.g., accuracy of tool selection, quality of synthesized response). Use these metrics to guide optimization with teleprompters. LangSmith can be invaluable for tracing and evaluating the end-to-end behavior of your integrated agent.
- **LM Consistency:** When optimizing a DSPy module, use the same LLM (or a very similar one) that will be used by that module in the deployed agent. Prompt effectiveness can vary significantly between models.

By combining the strengths of LangChain, LangGraph, and DSPy, you can construct highly capable, adaptable, and performant agentic AI systems that move beyond simple prompt chaining towards more robust and optimized reasoning pipelines.

## Performance Engineering for Agentic Systems

While DSPy provides optimization for individual reasoning components, production agentic systems require comprehensive performance engineering that spans infrastructure, model selection, caching strategies, and resource management. This section covers systematic approaches to building high-performance, cost-effective agentic systems that scale efficiently.

### Performance Optimization Strategies

**Model Selection and Routing Optimization**:
Intelligent model selection can dramatically improve both performance and cost-effectiveness by matching task complexity to model capabilities.

```python
from typing import Dict, List, Optional, Tuple
import time
import asyncio
from dataclasses import dataclass
from enum import Enum

class TaskComplexity(Enum):
    SIMPLE = "simple"          # Basic Q&A, simple tool selection
    MODERATE = "moderate"      # Multi-step reasoning, context synthesis
    COMPLEX = "complex"        # Advanced planning, complex analysis
    CRITICAL = "critical"      # High-stakes decisions, safety-critical

@dataclass
class ModelConfig:
    name: str
    provider: str
    cost_per_token: float
    max_tokens: int
    avg_latency_ms: float
    reliability_score: float
    capabilities: List[str]

class IntelligentModelRouter:
    def __init__(self):
        self.model_configs = {
            "gpt-4o": ModelConfig(
                name="gpt-4o",
                provider="openai",
                cost_per_token=0.00001,
                max_tokens=128000,
                avg_latency_ms=2500,
                reliability_score=0.98,
                capabilities=["reasoning", "coding", "analysis", "planning"]
            ),
            "gpt-4o-mini": ModelConfig(
                name="gpt-4o-mini",
                provider="openai", 
                cost_per_token=0.0000005,
                max_tokens=128000,
                avg_latency_ms=800,
                reliability_score=0.95,
                capabilities=["reasoning", "simple_analysis"]
            ),
            "claude-3-haiku": ModelConfig(
                name="claude-3-haiku",
                provider="anthropic",
                cost_per_token=0.00000025,
                max_tokens=200000,
                avg_latency_ms=600,
                reliability_score=0.94,
                capabilities=["reasoning", "fast_response"]
            )
        }
        
        # Performance history for adaptive routing
        self.performance_history = {}
        
    def select_model(self, 
                    task_complexity: TaskComplexity,
                    context_length: int,
                    latency_requirement: Optional[float] = None,
                    cost_priority: bool = False) -> str:
        """Select optimal model based on task requirements."""
        
        suitable_models = self._filter_suitable_models(
            task_complexity, context_length
        )
        
        if not suitable_models:
            return "gpt-4o"  # Fallback to most capable
        
        # Score models based on requirements
        scores = {}
        for model_name in suitable_models:
            config = self.model_configs[model_name]
            
            # Base score from reliability
            score = config.reliability_score
            
            # Adjust for latency requirements
            if latency_requirement:
                if config.avg_latency_ms <= latency_requirement:
                    score += 0.3
                else:
                    score -= 0.5
            
            # Adjust for cost priority
            if cost_priority:
                # Lower cost = higher score
                cost_factor = 1 / (config.cost_per_token * 1000000)
                score += cost_factor * 0.2
            
            # Historical performance adjustment
            historical_score = self._get_historical_performance(model_name)
            score += historical_score * 0.1
            
            scores[model_name] = score
        
        return max(scores.items(), key=lambda x: x[1])[0]
    
    def _filter_suitable_models(self, complexity: TaskComplexity, 
                               context_length: int) -> List[str]:
        """Filter models that can handle the task complexity and context."""
        suitable = []
        
        for name, config in self.model_configs.items():
            # Check context length capacity
            if config.max_tokens < context_length * 1.2:  # 20% buffer
                continue
                
            # Check capability match
            required_capabilities = self._get_required_capabilities(complexity)
            if not all(cap in config.capabilities for cap in required_capabilities):
                continue
                
            suitable.append(name)
        
        return suitable
    
    def _get_required_capabilities(self, complexity: TaskComplexity) -> List[str]:
        """Map task complexity to required model capabilities."""
        capability_map = {
            TaskComplexity.SIMPLE: ["reasoning"],
            TaskComplexity.MODERATE: ["reasoning", "analysis"],
            TaskComplexity.COMPLEX: ["reasoning", "analysis", "planning"],
            TaskComplexity.CRITICAL: ["reasoning", "analysis", "planning", "coding"]
        }
        return capability_map.get(complexity, ["reasoning"])
    
    def record_performance(self, model_name: str, 
                          latency: float, success: bool, quality_score: float):
        """Record model performance for adaptive routing."""
        if model_name not in self.performance_history:
            self.performance_history[model_name] = []
            
        self.performance_history[model_name].append({
            "latency": latency,
            "success": success,
            "quality_score": quality_score,
            "timestamp": time.time()
        })
        
        # Keep only recent history (last 100 requests)
        self.performance_history[model_name] = \
            self.performance_history[model_name][-100:]
```

**Advanced Caching and Memoization**:
Implement multi-level caching to reduce redundant computations and API calls.

```python
import hashlib
import json
import redis
from typing import Any, Optional, Union
from functools import wraps
import pickle

class AgentCacheManager:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_client = redis.from_url(redis_url)
        self.local_cache = {}
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
            "total_requests": 0
        }
    
    def _generate_cache_key(self, prefix: str, **kwargs) -> str:
        """Generate consistent cache key from parameters."""
        # Sort parameters for consistent key generation
        sorted_params = json.dumps(kwargs, sort_keys=True, default=str)
        hash_digest = hashlib.md5(sorted_params.encode()).hexdigest()
        return f"{prefix}:{hash_digest}"
    
    def cache_llm_response(self, ttl: int = 3600):
        """Decorator for caching LLM responses."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key from function arguments
                cache_key = self._generate_cache_key(
                    f"llm_response:{func.__name__}", 
                    args=args, 
                    kwargs=kwargs
                )
                
                self.cache_stats["total_requests"] += 1
                
                # Try local cache first
                if cache_key in self.local_cache:
                    self.cache_stats["hits"] += 1
                    return self.local_cache[cache_key]
                
                # Try Redis cache
                try:
                    cached_result = self.redis_client.get(cache_key)
                    if cached_result:
                        result = pickle.loads(cached_result)
                        self.local_cache[cache_key] = result  # Store in local cache
                        self.cache_stats["hits"] += 1
                        return result
                except Exception as e:
                    print(f"Redis cache error: {e}")
                
                # Cache miss - execute function
                self.cache_stats["misses"] += 1
                result = func(*args, **kwargs)
                
                # Store in both caches
                try:
                    self.redis_client.setex(
                        cache_key, 
                        ttl, 
                        pickle.dumps(result)
                    )
                    self.local_cache[cache_key] = result
                except Exception as e:
                    print(f"Cache storage error: {e}")
                
                return result
            return wrapper
        return decorator
    
    def cache_tool_result(self, tool_name: str, ttl: int = 1800):
        """Cache tool execution results."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = self._generate_cache_key(
                    f"tool_result:{tool_name}",
                    args=args,
                    kwargs=kwargs
                )
                
                # Check cache
                try:
                    cached_result = self.redis_client.get(cache_key)
                    if cached_result:
                        return pickle.loads(cached_result)
                except Exception:
                    pass
                
                # Execute and cache
                result = func(*args, **kwargs)
                try:
                    self.redis_client.setex(
                        cache_key,
                        ttl,
                        pickle.dumps(result)
                    )
                except Exception as e:
                    print(f"Tool cache error: {e}")
                
                return result
            return wrapper
        return decorator
    
    def invalidate_pattern(self, pattern: str):
        """Invalidate cache entries matching a pattern."""
        try:
            for key in self.redis_client.scan_iter(match=pattern):
                self.redis_client.delete(key)
        except Exception as e:
            print(f"Cache invalidation error: {e}")
    
    def get_cache_statistics(self) -> Dict[str, Any]:
        """Get cache performance statistics."""
        total = self.cache_stats["total_requests"]
        if total > 0:
            hit_rate = self.cache_stats["hits"] / total
        else:
            hit_rate = 0.0
            
        return {
            "hit_rate": hit_rate,
            "total_requests": total,
            "cache_hits": self.cache_stats["hits"],
            "cache_misses": self.cache_stats["misses"],
            "local_cache_size": len(self.local_cache)
        }
```

**Parallel Processing and Async Optimization**:
Optimize agent performance through intelligent parallelization of independent operations.

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Callable, Any, Dict
import logging

class AgentParallelProcessor:
    def __init__(self, max_workers: int = 10, max_concurrent_llm: int = 5):
        self.max_workers = max_workers
        self.max_concurrent_llm = max_concurrent_llm
        self.llm_semaphore = asyncio.Semaphore(max_concurrent_llm)
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        
    async def parallel_tool_execution(self, 
                                    tool_calls: List[Dict[str, Any]]) -> List[Any]:
        """Execute multiple tool calls in parallel."""
        
        async def execute_single_tool(tool_call):
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_func = tool_call["function"]
            
            try:
                # Run tool in thread pool to avoid blocking
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    self.executor, 
                    tool_func, 
                    **tool_args
                )
                return {"success": True, "result": result, "tool": tool_name}
            except Exception as e:
                logging.error(f"Tool {tool_name} failed: {e}")
                return {"success": False, "error": str(e), "tool": tool_name}
        
        # Execute all tools concurrently
        tasks = [execute_single_tool(call) for call in tool_calls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return results
    
    async def parallel_llm_calls(self, 
                                llm_requests: List[Dict[str, Any]]) -> List[Any]:
        """Execute multiple LLM calls with concurrency control."""
        
        async def execute_llm_call(request):
            async with self.llm_semaphore:  # Rate limiting
                llm_func = request["function"]
                args = request["args"]
                
                try:
                    if asyncio.iscoroutinefunction(llm_func):
                        result = await llm_func(**args)
                    else:
                        loop = asyncio.get_event_loop()
                        result = await loop.run_in_executor(
                            self.executor, 
                            llm_func, 
                            **args
                        )
                    return {"success": True, "result": result}
                except Exception as e:
                    return {"success": False, "error": str(e)}
        
        tasks = [execute_llm_call(req) for req in llm_requests]
        results = await asyncio.gather(*tasks)
        
        return results
    
    async def pipeline_optimization(self, 
                                  pipeline_stages: List[Callable]) -> Any:
        """Execute pipeline stages with optimal overlapping."""
        
        results = []
        tasks = []
        
        # Start first stage
        first_stage = pipeline_stages[0]
        current_task = asyncio.create_task(self._execute_stage(first_stage, None))
        
        # Pipeline subsequent stages
        for i, stage in enumerate(pipeline_stages[1:], 1):
            # Wait for previous stage to complete
            previous_result = await current_task
            results.append(previous_result)
            
            # Start next stage with previous result
            current_task = asyncio.create_task(
                self._execute_stage(stage, previous_result)
            )
        
        # Wait for final stage
        final_result = await current_task
        results.append(final_result)
        
        return results
    
    async def _execute_stage(self, stage_func: Callable, input_data: Any) -> Any:
        """Execute a single pipeline stage."""
        try:
            if asyncio.iscoroutinefunction(stage_func):
                return await stage_func(input_data)
            else:
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(
                    self.executor, 
                    stage_func, 
                    input_data
                )
        except Exception as e:
            logging.error(f"Pipeline stage failed: {e}")
            raise
```

### Resource Management and Cost Optimization

**Token Usage Optimization**:
Implement intelligent token management to minimize costs while maintaining quality.

```python
import tiktoken
from typing import Dict, List, Optional, Tuple
import re

class TokenOptimizer:
    def __init__(self, model_name: str = "gpt-4"):
        self.encoding = tiktoken.encoding_for_model(model_name)
        self.max_context = self._get_max_context(model_name)
        
    def _get_max_context(self, model_name: str) -> int:
        """Get maximum context window for model."""
        context_limits = {
            "gpt-4": 8192,
            "gpt-4-32k": 32768,
            "gpt-4-turbo": 128000,
            "gpt-4o": 128000,
            "gpt-4o-mini": 128000,
            "gpt-3.5-turbo": 16385
        }
        return context_limits.get(model_name, 8192)
    
    def optimize_prompt(self, 
                       system_prompt: str,
                       conversation_history: List[str],
                       current_query: str,
                       max_tokens_for_response: int = 1000) -> Tuple[str, List[str]]:
        """Optimize prompt to fit within token limits."""
        
        # Reserve tokens for response
        available_tokens = self.max_context - max_tokens_for_response
        
        # Count tokens for essential components
        system_tokens = len(self.encoding.encode(system_prompt))
        query_tokens = len(self.encoding.encode(current_query))
        
        # Reserve tokens for system prompt and current query
        available_for_history = available_tokens - system_tokens - query_tokens
        
        # Optimize conversation history
        optimized_history = self._optimize_conversation_history(
            conversation_history, 
            available_for_history
        )
        
        return system_prompt, optimized_history
    
    def _optimize_conversation_history(self, 
                                     history: List[str], 
                                     token_budget: int) -> List[str]:
        """Optimize conversation history to fit token budget."""
        
        if not history:
            return []
        
        # Strategy 1: Recent messages first (sliding window)
        recent_history = []
        current_tokens = 0
        
        for message in reversed(history):
            message_tokens = len(self.encoding.encode(message))
            if current_tokens + message_tokens <= token_budget:
                recent_history.insert(0, message)
                current_tokens += message_tokens
            else:
                break
        
        # Strategy 2: If still over budget, compress messages
        if current_tokens > token_budget:
            recent_history = self._compress_messages(recent_history, token_budget)
        
        return recent_history
    
    def _compress_messages(self, messages: List[str], token_budget: int) -> List[str]:
        """Compress messages using text summarization techniques."""
        compressed_messages = []
        
        for message in messages:
            message_tokens = len(self.encoding.encode(message))
            
            if message_tokens <= token_budget // len(messages):
                compressed_messages.append(message)
            else:
                # Simple compression: keep first and last parts
                compressed = self._compress_single_message(message, token_budget // len(messages))
                compressed_messages.append(compressed)
        
        return compressed_messages
    
    def _compress_single_message(self, message: str, target_tokens: int) -> str:
        """Compress a single message to target token count."""
        current_tokens = len(self.encoding.encode(message))
        
        if current_tokens <= target_tokens:
            return message
        
        # Simple strategy: keep beginning and end, truncate middle
        target_chars = int(len(message) * (target_tokens / current_tokens))
        
        if target_chars < 100:  # Minimum meaningful length
            return message[:target_chars] + "..."
        
        # Keep first 60% and last 40% of target
        first_part = int(target_chars * 0.6)
        last_part = int(target_chars * 0.4)
        
        return message[:first_part] + "...[truncated]..." + message[-last_part:]
    
    def estimate_cost(self, 
                     input_tokens: int, 
                     output_tokens: int, 
                     model_name: str) -> float:
        """Estimate cost for token usage."""
        
        pricing = {
            "gpt-4": {"input": 0.00003, "output": 0.00006},
            "gpt-4-turbo": {"input": 0.00001, "output": 0.00003},
            "gpt-4o": {"input": 0.000005, "output": 0.000015},
            "gpt-4o-mini": {"input": 0.00000015, "output": 0.0000006},
            "gpt-3.5-turbo": {"input": 0.0000005, "output": 0.0000015}
        }
        
        model_pricing = pricing.get(model_name, pricing["gpt-4"])
        
        input_cost = input_tokens * model_pricing["input"]
        output_cost = output_tokens * model_pricing["output"]
        
        return input_cost + output_cost
```

**Resource Pool Management**:
```python
import asyncio
from typing import Dict, Any, Optional
import time
from dataclasses import dataclass

@dataclass
class ResourceMetrics:
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    average_latency: float = 0.0
    total_cost: float = 0.0
    tokens_used: int = 0

class ResourcePoolManager:
    def __init__(self):
        self.resource_pools = {}
        self.metrics = {}
        self.rate_limiters = {}
        
    def create_resource_pool(self, 
                           pool_name: str,
                           max_concurrent: int,
                           rate_limit_per_minute: int):
        """Create a managed resource pool with rate limiting."""
        
        self.resource_pools[pool_name] = {
            "semaphore": asyncio.Semaphore(max_concurrent),
            "rate_limiter": asyncio.Semaphore(rate_limit_per_minute),
            "last_reset": time.time(),
            "requests_this_minute": 0
        }
        
        self.metrics[pool_name] = ResourceMetrics()
    
    async def execute_with_pool(self, 
                               pool_name: str,
                               func: callable,
                               *args, **kwargs) -> Any:
        """Execute function using managed resource pool."""
        
        if pool_name not in self.resource_pools:
            raise ValueError(f"Resource pool {pool_name} not found")
        
        pool = self.resource_pools[pool_name]
        metrics = self.metrics[pool_name]
        
        # Rate limiting check
        await self._check_rate_limit(pool_name)
        
        async with pool["semaphore"]:
            start_time = time.time()
            metrics.total_requests += 1
            
            try:
                result = await func(*args, **kwargs)
                metrics.successful_requests += 1
                
                # Update metrics
                latency = time.time() - start_time
                metrics.average_latency = (
                    (metrics.average_latency * (metrics.successful_requests - 1) + latency)
                    / metrics.successful_requests
                )
                
                return result
                
            except Exception as e:
                metrics.failed_requests += 1
                raise e
    
    async def _check_rate_limit(self, pool_name: str):
        """Check and enforce rate limiting."""
        pool = self.resource_pools[pool_name]
        current_time = time.time()
        
        # Reset counter if minute has passed
        if current_time - pool["last_reset"] >= 60:
            pool["requests_this_minute"] = 0
            pool["last_reset"] = current_time
            # Release all rate limiter permits
            while pool["rate_limiter"]._value < pool["rate_limiter"]._initial_value:
                pool["rate_limiter"].release()
        
        # Acquire rate limit permit
        await pool["rate_limiter"].acquire()
        pool["requests_this_minute"] += 1
    
    def get_pool_metrics(self, pool_name: str) -> ResourceMetrics:
        """Get metrics for a specific resource pool."""
        return self.metrics.get(pool_name, ResourceMetrics())
    
    def get_all_metrics(self) -> Dict[str, ResourceMetrics]:
        """Get metrics for all resource pools."""
        return self.metrics.copy()
```

This performance engineering framework provides the foundation for building high-performance, cost-effective agentic systems that can scale efficiently while maintaining quality and reliability. The combination of intelligent model routing, advanced caching, parallel processing, and resource management ensures optimal performance across different workloads and usage patterns.

⏱️ **Estimated reading time: 22 minutes** 