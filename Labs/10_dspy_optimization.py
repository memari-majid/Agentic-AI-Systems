#!/usr/bin/env python3
"""
Chapter 10 Extension - DSPy Prompt Optimization
----------------------------------------------
This example demonstrates how to use DSPy to programmatically optimize prompts
for agentic systems:

1. Basic DSPy concepts and modules
2. Teleprompters for optimizing prompts
3. Trainable reasoning modules
4. Comparison of optimized vs. unoptimized agents
5. Integration with other agent architectures

Key concepts:
- Prompt optimization beyond manual engineering
- Data-driven prompt improvement
- Composable reasoning modules
- Systematic agent evaluation
"""
import argparse
import json
import time
from typing import Dict, List, TypedDict, Optional, Any, Tuple
from enum import Enum

# Mock imports for demonstration purposes
try:
    import dspy
    from dspy.teleprompt import Teleprompter, BootstrapFewShot
    DSPY_AVAILABLE = True
except ImportError:
    DSPY_AVAILABLE = False
    # Create mock classes to demonstrate concepts
    class MockDSPy:
        class Module:
            def __init__(self, **kwargs):
                pass
        
        class Predict:
            def __init__(self, **kwargs):
                pass
                
        class ChainOfThought:
            def __init__(self, **kwargs):
                pass
        
        class Example:
            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    setattr(self, k, v)
    
    # Create mock teleprompter
    class MockTeleprompter:
        def __init__(self, **kwargs):
            pass
            
        def optimize(self, *args, **kwargs):
            pass
    
    # Create mock bootstrapper
    class MockBootstrapFewShot:
        def __init__(self, **kwargs):
            pass
    
    # Set up mock module
    dspy = MockDSPy()
    dspy.teleprompt = type('obj', (object,), {
        'Teleprompter': MockTeleprompter,
        'BootstrapFewShot': MockBootstrapFewShot
    })

# ---------------------------------------------------------------------------
# Basic DSPy structures and types ------------------------------------------
# ---------------------------------------------------------------------------

class TaskType(str, Enum):
    TRAVEL_PLANNING = "travel_planning"
    RESEARCH = "research"
    DECISION_MAKING = "decision_making"

class AgentEvaluation(TypedDict):
    accuracy: float
    reasoning_quality: float
    hallucination_count: int
    execution_time: float

class AgentState(TypedDict, total=False):
    task: str
    task_type: TaskType
    context: List[str]
    question: str
    reasoning: str
    answer: str
    optimized: bool
    performance: Optional[AgentEvaluation]

# ---------------------------------------------------------------------------
# Sample data for training and evaluation ----------------------------------
# ---------------------------------------------------------------------------

def get_travel_planning_examples() -> List[Any]:
    """Define examples for travel planning tasks."""
    if DSPY_AVAILABLE:
        return [
            dspy.Example(
                task="Plan a 3-day trip to Paris for a family of four.",
                task_type=TaskType.TRAVEL_PLANNING,
                context=[
                    "Paris is known for attractions like the Eiffel Tower, Louvre, and Notre Dame.",
                    "Family-friendly activities include Luxembourg Gardens and boat tours on the Seine.",
                    "The Paris Museum Pass provides access to over 50 museums and monuments.",
                    "Paris has a reliable metro system for transportation."
                ],
                question="What should the itinerary include for a family with two children (ages 8 and 10)?",
                reasoning="When planning for a family with young children, I need to balance cultural attractions with engaging activities for kids. The itinerary should include major landmarks but also allow for breaks and family-friendly activities. Transportation between sites should be considered to minimize walking for children. Each day should have a mix of indoor and outdoor activities in case of weather changes.",
                answer="Day 1: Morning at the Eiffel Tower (book tickets in advance), lunch near Trocadéro, afternoon at Luxembourg Gardens with puppet shows and boat rentals. Day 2: Louvre Museum in the morning (focus on the highlights tour for kids), lunch in the Tuileries Garden, afternoon Seine River boat tour. Day 3: Morning at the Natural History Museum, picnic lunch, afternoon at Cité des Sciences et de l'Industrie (Science Museum) which is highly interactive for children. Use the metro for transportation between sites and consider the Paris Museum Pass for savings."
            ),
            dspy.Example(
                task="Plan a weekend getaway to New York City for a couple.",
                task_type=TaskType.TRAVEL_PLANNING,
                context=[
                    "NYC is known for Broadway shows, Central Park, and museums like the Met.",
                    "Popular neighborhoods include SoHo, Greenwich Village, and Times Square.",
                    "NYC has extensive subway and taxi transportation options.",
                    "Restaurant reservations are recommended for popular dining spots."
                ],
                question="What are the best activities for a romantic weekend in NYC?",
                reasoning="For a romantic weekend, I should focus on atmospheric experiences and intimate settings rather than just tourist attractions. Evening activities are important for couples. I should also consider locations that provide good views or ambiance, and opportunities for memorable experiences. Transportation between sites should be efficient to maximize time together.",
                answer="Day 1: Morning walk through Central Park, visit to the Met Museum, late afternoon drinks at a rooftop bar like 230 Fifth for skyline views, evening Broadway show (book tickets in advance). Day 2: Brunch in Greenwich Village at a café like Buvette, walk the High Line in the afternoon, sunset cruise around Manhattan with Champagne, dinner in the West Village at a romantic spot like One if by Land, Two if by Sea (make reservations well in advance). Use the subway for longer distances and enjoy walks through charming neighborhoods when possible."
            )
        ]
    else:
        # Return mock examples if DSPy isn't available
        return [{"task": "Example task 1"}, {"task": "Example task 2"}]

def get_research_examples() -> List[Any]:
    """Define examples for research tasks."""
    if DSPY_AVAILABLE:
        return [
            dspy.Example(
                task="Research the impact of artificial intelligence on healthcare.",
                task_type=TaskType.RESEARCH,
                context=[
                    "AI is being used for medical image analysis, drug discovery, and personalized medicine.",
                    "Machine learning algorithms can detect patterns in patient data to predict disease risk.",
                    "There are concerns about privacy, bias, and the need for human oversight in medical AI.",
                    "The FDA has begun approving AI-based medical devices and software."
                ],
                question="What are the main benefits and challenges of AI adoption in healthcare?",
                reasoning="I need to analyze both the positive and negative aspects of AI in healthcare. For benefits, I should consider diagnostic capabilities, efficiency improvements, and new treatment possibilities. For challenges, I should examine technical limitations, ethical concerns, implementation difficulties, and regulatory issues. I should provide a balanced perspective with concrete examples.",
                answer="Benefits of AI in healthcare include: 1) Improved diagnostic accuracy, particularly in radiology and pathology where AI can detect subtle patterns; 2) Accelerated drug discovery through simulation and prediction models; 3) Personalized treatment recommendations based on individual patient data; 4) Operational efficiencies like optimized scheduling and resource allocation. Challenges include: 1) Ensuring algorithm transparency and explainability for clinical decisions; 2) Addressing bias in training data that could lead to healthcare disparities; 3) Integration difficulties with existing healthcare IT systems; 4) Data privacy concerns with sensitive medical information; 5) Liability questions when AI contributes to medical decisions. The field requires careful balance between innovation and appropriate oversight."
            )
        ]
    else:
        # Return mock examples if DSPy isn't available
        return [{"task": "Example research task"}]

def get_decision_making_examples() -> List[Any]:
    """Define examples for decision making tasks."""
    if DSPY_AVAILABLE:
        return [
            dspy.Example(
                task="Decide which project management software to implement for a marketing team of 15 people.",
                task_type=TaskType.DECISION_MAKING,
                context=[
                    "The team currently uses a mix of email, spreadsheets, and ad-hoc tools.",
                    "Budget is $50 per user per month maximum.",
                    "Key requirements include task assignment, timeline visualization, file sharing, and client approval workflows.",
                    "Top contenders are Asana, Monday.com, ClickUp, and Trello."
                ],
                question="Which software should they choose and why?",
                reasoning="I need to evaluate each option against the requirements, budget constraints, and team context. I'll consider features, pricing, ease of implementation, and specific use cases for a marketing team. The decision needs to balance immediate needs with room for growth. Integration with existing tools should also be considered.",
                answer="The marketing team should implement Monday.com for these reasons: 1) Its visual interface with customizable boards aligns well with marketing workflows and campaign planning; 2) At $39/user/month for the Pro plan, it meets budget requirements while providing all necessary features; 3) It offers superior timeline visualization with Gantt charts that help manage campaign schedules; 4) Its client-facing features allow for better approval workflows and feedback collection; 5) It includes strong collaboration features for a 15-person team with tagging, commenting, and file sharing; 6) It offers templates specifically designed for marketing use cases like campaign planning and content calendars. While Asana and ClickUp are strong alternatives, Monday.com's balance of visual appeal, marketing-specific features, and collaborative capabilities make it the best choice for this specific team size and use case."
            )
        ]
    else:
        # Return mock examples if DSPy isn't available
        return [{"task": "Example decision task"}]

# ---------------------------------------------------------------------------
# DSPy Modules -------------------------------------------------------------
# ---------------------------------------------------------------------------

class SimpleAgent(dspy.Module):
    """A basic agent that uses a simple predict module."""
    
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(
            task="task",
            task_type="task_type",
            context="context",
            question="question",
            answer="answer"
        )
    
    def forward(self, task: str, task_type: TaskType, context: List[str], question: str) -> Dict:
        """Generate an answer directly."""
        prediction = self.predict(
            task=task,
            task_type=task_type,
            context=context,
            question=question
        )
        return {"answer": prediction.answer}

class ReasoningAgent(dspy.Module):
    """An agent that employs chain-of-thought reasoning."""
    
    def __init__(self):
        super().__init__()
        self.predict = dspy.ChainOfThought(
            task="task",
            task_type="task_type",
            context="context",
            question="question",
            reasoning="reasoning",
            answer="answer"
        )
    
    def forward(self, task: str, task_type: TaskType, context: List[str], question: str) -> Dict:
        """Generate reasoning and an answer."""
        prediction = self.predict(
            task=task,
            task_type=task_type,
            context=context,
            question=question
        )
        return {
            "reasoning": prediction.reasoning,
            "answer": prediction.answer
        }

# ---------------------------------------------------------------------------
# Optimization functions ---------------------------------------------------
# ---------------------------------------------------------------------------

def optimize_agent(agent_module, task_type: TaskType) -> dspy.Module:
    """
    Optimize an agent module using DSPy's teleprompter.
    
    In a real application, this would use actual optimization metrics
    and more sophisticated techniques.
    """
    if not DSPY_AVAILABLE:
        # Mock optimization if DSPy isn't available
        print("DSPy not available. Showing mock optimization.")
        time.sleep(1)
        return agent_module
    
    print(f"Beginning optimization for task type: {task_type}...")
    
    # Get appropriate examples for task type
    if task_type == TaskType.TRAVEL_PLANNING:
        examples = get_travel_planning_examples()
    elif task_type == TaskType.RESEARCH:
        examples = get_research_examples()
    elif task_type == TaskType.DECISION_MAKING:
        examples = get_decision_making_examples()
    else:
        examples = get_travel_planning_examples()
    
    # Split examples into train and test sets
    # In real applications, you'd have more examples and better splitting
    train_examples = examples
    
    # Create a teleprompter with a bootstrapping optimizer
    teleprompter = dspy.teleprompt.Teleprompter(
        optimizer=dspy.teleprompt.BootstrapFewShot(
            metric=lambda example, prediction: 1.0,  # Mock metric for demonstration
            max_bootstrapped_demos=3,
            num_threads=1
        )
    )
    
    # Optimize the agent
    print("Applying bootstrap optimization...")
    optimized_agent = teleprompter.optimize(
        agent_module,
        trainset=train_examples,
        metric=lambda example, prediction: 1.0,  # Mock metric
    )
    
    print("Optimization complete.")
    return optimized_agent

# ---------------------------------------------------------------------------
# Evaluation functions -----------------------------------------------------
# ---------------------------------------------------------------------------

def evaluate_agent(agent, examples: List[Any]) -> AgentEvaluation:
    """
    Evaluate an agent's performance on a set of examples.
    
    In a real implementation, this would use actual metrics like
    answer correctness, reasoning quality, etc.
    """
    # Mock evaluation metrics
    accuracy = 0.85
    reasoning_quality = 0.7
    hallucination_count = 2
    
    # Time execution (even in mock mode)
    start_time = time.time()
    
    # Run the agent on a couple of examples for demonstration
    if DSPY_AVAILABLE and examples:
        for i, example in enumerate(examples[:2]):
            if i == 0:  # Just run one example to demonstrate
                print(f"\nRunning evaluation on example: {example.task}")
                result = agent(
                    task=example.task,
                    task_type=example.task_type,
                    context=example.context,
                    question=example.question
                )
                print(f"Generated answer: {result.get('answer', 'No answer')[:100]}...")
                if 'reasoning' in result:
                    print(f"Reasoning: {result['reasoning'][:100]}...")
    
    execution_time = time.time() - start_time
    
    # Return mock evaluation results
    return {
        "accuracy": accuracy,
        "reasoning_quality": reasoning_quality,
        "hallucination_count": hallucination_count,
        "execution_time": execution_time
    }

def compare_agents(base_agent: dspy.Module, optimized_agent: dspy.Module, 
                  task_type: TaskType) -> Tuple[AgentEvaluation, AgentEvaluation]:
    """Compare performance between base and optimized agents."""
    # Get test examples
    if task_type == TaskType.TRAVEL_PLANNING:
        examples = get_travel_planning_examples()
    elif task_type == TaskType.RESEARCH:
        examples = get_research_examples()
    else:
        examples = get_decision_making_examples()
    
    print("\n=== Comparing Base vs Optimized Agent ===")
    
    print("\nEvaluating base agent...")
    base_results = evaluate_agent(base_agent, examples)
    
    print("\nEvaluating optimized agent...")
    optimized_results = evaluate_agent(optimized_agent, examples)
    
    return base_results, optimized_results

# ---------------------------------------------------------------------------
# Demo run functions -------------------------------------------------------
# ---------------------------------------------------------------------------

def run_simple_agent_demo() -> None:
    """Run a demonstration of the simple agent."""
    print("\n=== Simple Agent Demo ===")
    
    # Create the base agent
    print("Creating base agent...")
    agent = SimpleAgent()
    
    # Get task data
    task_type = TaskType.TRAVEL_PLANNING
    examples = get_travel_planning_examples()
    
    if DSPY_AVAILABLE and examples:
        example = examples[0]
        
        # Run the base agent
        print(f"\nRunning base agent on task: {example.task}")
        result = agent(
            task=example.task,
            task_type=example.task_type,
            context=example.context,
            question=example.question
        )
        
        print(f"\nBase agent answer: {result['answer'][:150]}...")
        
        # Optimize the agent
        optimized_agent = optimize_agent(agent, task_type)
        
        # Run the optimized agent
        print(f"\nRunning optimized agent on the same task...")
        optimized_result = optimized_agent(
            task=example.task,
            task_type=example.task_type,
            context=example.context,
            question=example.question
        )
        
        print(f"\nOptimized agent answer: {optimized_result['answer'][:150]}...")
    else:
        print("\nMock execution (DSPy not available)")
        print("Base agent would generate a simple answer.")
        print("Optimized agent would generate an improved answer.")
    
    # Compare performance
    base_eval, opt_eval = compare_agents(agent, 
                                         optimize_agent(agent, task_type) if DSPY_AVAILABLE else agent, 
                                         task_type)
    
    print("\n=== Performance Comparison ===")
    print(f"Base Agent - Accuracy: {base_eval['accuracy']:.2f}, Time: {base_eval['execution_time']:.2f}s")
    print(f"Optimized Agent - Accuracy: {opt_eval['accuracy']:.2f}, Time: {opt_eval['execution_time']:.2f}s")
    
    # Calculate improvements
    acc_improvement = ((opt_eval['accuracy'] - base_eval['accuracy']) / base_eval['accuracy']) * 100
    print(f"\nAccuracy improvement: {acc_improvement:.1f}%")

def run_reasoning_agent_demo() -> None:
    """Run a demonstration of the reasoning agent."""
    print("\n=== Reasoning Agent Demo ===")
    
    # Create the base agent
    print("Creating reasoning agent...")
    agent = ReasoningAgent()
    
    # Get task data
    task_type = TaskType.DECISION_MAKING
    examples = get_decision_making_examples()
    
    if DSPY_AVAILABLE and examples:
        example = examples[0]
        
        # Run the base agent
        print(f"\nRunning reasoning agent on task: {example.task}")
        result = agent(
            task=example.task,
            task_type=example.task_type,
            context=example.context,
            question=example.question
        )
        
        print(f"\nBase agent reasoning: {result['reasoning'][:150]}...")
        print(f"Base agent answer: {result['answer'][:150]}...")
        
        # Optimize the agent
        optimized_agent = optimize_agent(agent, task_type)
        
        # Run the optimized agent
        print(f"\nRunning optimized reasoning agent on the same task...")
        optimized_result = optimized_agent(
            task=example.task,
            task_type=example.task_type,
            context=example.context,
            question=example.question
        )
        
        print(f"\nOptimized agent reasoning: {optimized_result['reasoning'][:150]}...")
        print(f"Optimized agent answer: {optimized_result['answer'][:150]}...")
    else:
        print("\nMock execution (DSPy not available)")
        print("Base agent would generate reasoning and an answer.")
        print("Optimized agent would generate improved reasoning and answer.")
    
    # Compare performance
    base_eval, opt_eval = compare_agents(agent, 
                                         optimize_agent(agent, task_type) if DSPY_AVAILABLE else agent, 
                                         task_type)
    
    print("\n=== Performance Comparison ===")
    print(f"Base Agent - Reasoning Quality: {base_eval['reasoning_quality']:.2f}, " 
          f"Hallucinations: {base_eval['hallucination_count']}")
    print(f"Optimized Agent - Reasoning Quality: {opt_eval['reasoning_quality']:.2f}, "
          f"Hallucinations: {opt_eval['hallucination_count']}")
    
    # Calculate improvements
    quality_improvement = ((opt_eval['reasoning_quality'] - base_eval['reasoning_quality']) / 
                           base_eval['reasoning_quality']) * 100
    hallucination_reduction = ((base_eval['hallucination_count'] - opt_eval['hallucination_count']) / 
                              base_eval['hallucination_count']) * 100 if base_eval['hallucination_count'] > 0 else 0
    
    print(f"\nReasoning quality improvement: {quality_improvement:.1f}%")
    print(f"Hallucination reduction: {hallucination_reduction:.1f}%")

# ---------------------------------------------------------------------------
# Integration patterns with LangGraph ---------------------------------------
# ---------------------------------------------------------------------------

def show_integration_examples() -> None:
    """Show examples of integrating DSPy with LangGraph."""
    print("\n=== DSPy Integration with LangGraph ===")
    print("""
Integration Pattern 1: DSPy for optimized prompts, LangGraph for orchestration
--------------------------------------------------------------------------------
```python
# Define a DSPy module for optimized prompting
class OptimizedAnswerer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.ChainOfThought(
            context="context", 
            question="question",
            reasoning="reasoning",
            answer="answer"
        )
    
    def forward(self, context, question):
        prediction = self.predict(context=context, question=question)
        return {
            "reasoning": prediction.reasoning,
            "answer": prediction.answer
        }

# Optimize it with DSPy
optimized_answerer = dspy.teleprompt.Teleprompter(...).optimize(
    OptimizedAnswerer(),
    trainset=train_examples
)

# Use within LangGraph
def answer_node(state: AgentState) -> AgentState:
    # Extract context and question from state
    context = state.get("context", [])
    question = state.get("question", "")
    
    # Use optimized DSPy module
    result = optimized_answerer(context=context, question=question)
    
    # Update state with results
    state["reasoning"] = result["reasoning"]
    state["answer"] = result["answer"]
    return state

# Add to LangGraph
graph = StateGraph(AgentState)
graph.add_node("answer", answer_node)
```
""")

    print("""
Integration Pattern 2: DSPy for state transformation modules
-----------------------------------------------------------
```python
# Define a DSPy module for each state transformation
class ContextBuilder(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(
            query="query",
            relevant_information="relevant_information" 
        )
    
    def forward(self, query):
        return self.predict(query=query)

class PlanGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.ChainOfThought(
            context="context",
            query="query",
            reasoning="reasoning",
            plan="plan"
        )
    
    def forward(self, context, query):
        return self.predict(context=context, query=query)

# Optimize each module separately
optimized_context_builder = dspy.teleprompt.Teleprompter(...).optimize(
    ContextBuilder(),
    trainset=context_examples
)

optimized_planner = dspy.teleprompt.Teleprompter(...).optimize(
    PlanGenerator(),
    trainset=planning_examples
)

# Use them in LangGraph nodes
def build_context_node(state: AgentState) -> AgentState:
    result = optimized_context_builder(query=state["question"])
    state["context"] = result["relevant_information"]
    return state

def create_plan_node(state: AgentState) -> AgentState:
    result = optimized_planner(
        context=state["context"],
        query=state["question"]
    )
    state["reasoning"] = result["reasoning"]
    state["plan"] = result["plan"]
    return state

# Add to LangGraph
graph = StateGraph(AgentState)
graph.add_node("build_context", build_context_node)
graph.add_node("create_plan", create_plan_node)
graph.add_edge("build_context", "create_plan")
```
""")

# ---------------------------------------------------------------------------
# Main function -------------------------------------------------------------
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="DSPy Prompt Optimization Demo")
    parser.add_argument("--demo", choices=["simple", "reasoning", "integration", "all"], 
                      default="all", help="Which demo to run")
    args = parser.parse_args()
    
    # Check if DSPy is available
    if not DSPY_AVAILABLE:
        print("""
Note: DSPy is not installed. Running in mock mode.
To install DSPy, run: pip install dspy-ai
        """)
    
    print("\n=== DSPy Prompt Optimization Demo ===")
    print("This example shows how to optimize prompts and reasoning modules.")
    
    # Run the appropriate demo
    if args.demo in ["simple", "all"]:
        run_simple_agent_demo()
    
    if args.demo in ["reasoning", "all"]:
        run_reasoning_agent_demo()
    
    if args.demo in ["integration", "all"]:
        show_integration_examples()
    
    # Conclusion and takeaways
    print("\n=== Key Takeaways ===")
    print("""
1. DSPy provides a programmatic approach to prompt optimization, moving beyond
   manual prompt engineering.

2. Optimized prompts can improve:
   - Task accuracy
   - Reasoning quality
   - Reduction in hallucinations
   - Runtime efficiency

3. Integration patterns with LangGraph:
   - Use DSPy for optimized module prompts, LangGraph for orchestration
   - Create optimized modules for specific state transformations
   - Combine the strengths of both frameworks

4. The optimization process is data-driven, allowing for systematic improvement
   based on examples and metrics.
""")

if __name__ == "__main__":
    main() 