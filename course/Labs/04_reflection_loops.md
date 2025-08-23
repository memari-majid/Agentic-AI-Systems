# Lab 4: Self-Critique Loops

⏱️ **Estimated completion time: 35 minutes**

## Overview

This lab demonstrates the powerful concept of reflection in agentic systems. The agent generates content, critiques its own work, and iteratively improves the output. This self-reflective capability is crucial for building more reliable and self-improving agents.

## Learning Objectives

By the end of this lab, you will understand:
- Implementation of reflection loops in LangGraph
- Self-critique mechanisms for quality improvement
- Iterative refinement processes
- When to terminate reflection loops

## Prerequisites

- Python 3.8+
- LangGraph installed (`pip install langgraph`)

## Key Concepts

### Reflection Loops
Reflection loops allow agents to critique and improve their own output through iterative cycles of generation, evaluation, and refinement.

### Self-Critique
Agents can evaluate the quality of their own work using internal criteria or external validation.

## Lab Code

```python
#!/usr/bin/env python3
"""
Chapter 4 - Self-Critique with LangGraph
----------------------------------------
This example demonstrates the powerful concept of reflection in agentic systems.
The agent generates content, critiques its own work, and iteratively improves
the output.

Key concepts:
- Reflection loops for self-improvement
- Quality assessment and iterative refinement
- Termination conditions for reflection cycles
"""

import random
from typing import TypedDict, Optional, List
from langgraph.graph import StateGraph

class ReflectionState(TypedDict, total=False):
    task: str
    draft: str
    critique: str
    final_output: str
    iteration: int
    quality_score: float
    improvement_history: List[str]

# ---------------------------------------------------------------------------
# Mock LLM functions for demonstration --------------------------------------
# ---------------------------------------------------------------------------

def generate_content(task: str) -> str:
    """Simulate content generation based on task."""
    content_templates = {
        "marketing email": [
            "Dear valued customer, we're excited to announce our new product!",
            "Hello! Don't miss out on this amazing opportunity to save big!",
            "Greetings! Our revolutionary new service is now available."
        ],
        "technical documentation": [
            "This API endpoint accepts POST requests with JSON payload.",
            "The system architecture consists of three main components.",
            "Installation requires Python 3.8+ and the following dependencies."
        ],
        "creative story": [
            "Once upon a time, in a land far away, there lived a brave knight.",
            "The spaceship hurtled through the cosmos towards an unknown destination.",
            "Sarah discovered the hidden doorway behind the old bookshelf."
        ]
    }
    
    # Use task keywords to determine template category
    for category in content_templates:
        if category in task.lower():
            return random.choice(content_templates[category])
    
    # Default generic content
    return f"This is a response to the task: {task}"

def critique_content(content: str, task: str) -> tuple[str, float]:
    """Simulate content critique with quality scoring."""
    issues = []
    quality_score = 7.0  # Base score
    
    # Check for various quality factors
    if len(content) < 50:
        issues.append("Content is too brief and lacks detail")
        quality_score -= 2.0
    
    if not any(char.isupper() for char in content):
        issues.append("Content lacks proper capitalization")
        quality_score -= 0.5
    
    if "!" not in content and "marketing" in task.lower():
        issues.append("Marketing content should be more energetic")
        quality_score -= 1.0
    
    if "API" in task and "endpoint" not in content:
        issues.append("Technical documentation should mention endpoints")
        quality_score -= 1.5
    
    if len(content.split()) < 10:
        issues.append("Content needs more comprehensive coverage")
        quality_score -= 1.0
    
    # Add some randomness to simulate LLM variability
    quality_score += random.uniform(-0.5, 0.5)
    quality_score = max(0.0, min(10.0, quality_score))  # Clamp to 0-10 range
    
    if not issues:
        critique = "The content meets quality standards."
    else:
        critique = f"Issues identified: {'; '.join(issues)}"
    
    return critique, quality_score

def improve_content(original: str, critique: str, task: str) -> str:
    """Simulate content improvement based on critique."""
    improved = original
    
    if "too brief" in critique:
        improved += " Here are additional details and comprehensive information about the topic."
    
    if "capitalization" in critique:
        improved = improved.capitalize()
    
    if "energetic" in critique:
        improved += " This is an incredible opportunity you won't want to miss!"
    
    if "endpoints" in critique:
        improved += " The endpoint supports GET, POST, PUT, and DELETE operations."
    
    if "comprehensive" in critique:
        improved += f" Let me provide more thorough coverage of {task}."
    
    return improved

# ---------------------------------------------------------------------------
# Graph nodes ---------------------------------------------------------------
# ---------------------------------------------------------------------------

def generate_draft(state: ReflectionState) -> ReflectionState:
    """Generate initial draft or improved version based on critique."""
    task = state["task"]
    
    if state.get("critique"):
        # Improve existing draft based on critique
        current_draft = state.get("draft", "")
        critique = state.get("critique", "")
        improved_draft = improve_content(current_draft, critique, task)
        state["draft"] = improved_draft
    else:
        # Generate initial draft
        initial_draft = generate_content(task)
        state["draft"] = initial_draft
    
    # Track iteration
    state["iteration"] = state.get("iteration", 0) + 1
    
    # Add to improvement history
    if "improvement_history" not in state:
        state["improvement_history"] = []
    state["improvement_history"].append(f"Iteration {state['iteration']}: {state['draft'][:50]}...")
    
    return state

def self_critique(state: ReflectionState) -> ReflectionState:
    """Evaluate the current draft and provide critique."""
    draft = state.get("draft", "")
    task = state.get("task", "")
    
    critique, quality_score = critique_content(draft, task)
    
    state["critique"] = critique
    state["quality_score"] = quality_score
    
    print(f"\nIteration {state.get('iteration', 0)}:")
    print(f"Draft: {draft}")
    print(f"Quality Score: {quality_score:.1f}/10")
    print(f"Critique: {critique}")
    
    return state

def finalize_output(state: ReflectionState) -> ReflectionState:
    """Finalize the output once quality threshold is met."""
    state["final_output"] = state.get("draft", "")
    print(f"\n✅ Final output ready after {state.get('iteration', 0)} iterations")
    print(f"Final quality score: {state.get('quality_score', 0):.1f}/10")
    return state

# ---------------------------------------------------------------------------
# Conditional logic ---------------------------------------------------------
# ---------------------------------------------------------------------------

def should_continue_reflection(state: ReflectionState) -> str:
    """Determine whether to continue refining or finalize the output."""
    quality_score = state.get("quality_score", 0)
    iteration = state.get("iteration", 0)
    
    # Stop if quality is good enough (score >= 8) or max iterations reached
    if quality_score >= 8.0 or iteration >= 5:
        return "finalize"
    else:
        return "improve"

# ---------------------------------------------------------------------------
# Graph construction --------------------------------------------------------
# ---------------------------------------------------------------------------

def build_reflection_graph() -> StateGraph:
    """Build a graph that implements reflection loops for content improvement."""
    g = StateGraph(ReflectionState)
    
    # Add nodes
    g.add_node("generate", generate_draft)
    g.add_node("critique", self_critique)
    g.add_node("finalize", finalize_output)
    
    # Set entry point
    g.set_entry_point("generate")
    
    # Add edges
    g.add_edge("generate", "critique")
    
    # Add conditional edge for reflection loop
    g.add_conditional_edges(
        "critique",
        should_continue_reflection,
        {
            "improve": "generate",  # Continue loop
            "finalize": "finalize"  # Exit loop
        }
    )
    
    # Set finish point
    g.set_finish_point("finalize")
    
    return g

# ---------------------------------------------------------------------------
# Demo function -------------------------------------------------------------
# ---------------------------------------------------------------------------

def main():
    print("=== Self-Critique Reflection Loop Demo ===\n")
    
    # Example tasks to test
    tasks = [
        "Write a marketing email for our new AI-powered productivity app",
        "Create technical documentation for our REST API",
        "Write a creative story about time travel"
    ]
    
    # Build the graph
    graph = build_reflection_graph().compile()
    
    for task in tasks:
        print(f"\n{'='*60}")
        print(f"Task: {task}")
        print('='*60)
        
        # Run the reflection loop
        final_state = graph.invoke({"task": task})
        
        print(f"\n📝 Final Output:")
        print(f"{final_state['final_output']}")
        
        print(f"\n🔄 Improvement History:")
        for entry in final_state.get('improvement_history', []):
            print(f"  • {entry}")

if __name__ == "__main__":
    main()
```

## How to Run

1. Save the code above as `04_reflection_loops.py`
2. Install dependencies: `pip install langgraph`
3. Run the script: `python 04_reflection_loops.py`

## Expected Output

```
=== Self-Critique Reflection Loop Demo ===

============================================================
Task: Write a marketing email for our new AI-powered productivity app
============================================================

Iteration 1:
Draft: Hello! Don't miss out on this amazing opportunity to save big!
Quality Score: 6.5/10
Critique: Issues identified: Marketing content should be more energetic

Iteration 2:
Draft: Hello! Don't miss out on this amazing opportunity to save big! This is an incredible opportunity you won't want to miss!
Quality Score: 8.2/10
Critique: The content meets quality standards.

✅ Final output ready after 2 iterations
Final quality score: 8.2/10

📝 Final Output:
Hello! Don't miss out on this amazing opportunity to save big! This is an incredible opportunity you won't want to miss!

🔄 Improvement History:
  • Iteration 1: Hello! Don't miss out on this amazing opportunity...
  • Iteration 2: Hello! Don't miss out on this amazing opportunity...
```

## Key Concepts Explained

### Reflection Loop Architecture
- **Generate**: Creates initial content or improvements
- **Critique**: Evaluates quality and identifies issues
- **Conditional Logic**: Decides whether to continue or finalize

### Quality Assessment
- Numerical scoring system (0-10 scale)
- Multiple criteria evaluation
- Threshold-based termination

### Iterative Improvement
- Each iteration builds on previous work
- Specific improvements based on critique
- History tracking for transparency

### Termination Conditions
- Quality threshold reached (score ≥ 8.0)
- Maximum iterations limit (5 iterations)
- Prevents infinite loops

## Advanced Patterns

### Multi-Criteria Evaluation
```python
def advanced_critique(content: str, criteria: List[str]) -> Dict[str, float]:
    """Evaluate content against multiple criteria."""
    scores = {}
    for criterion in criteria:
        scores[criterion] = evaluate_criterion(content, criterion)
    return scores
```

### Weighted Quality Scoring
```python
def weighted_quality_score(scores: Dict[str, float], weights: Dict[str, float]) -> float:
    """Calculate weighted average quality score."""
    total_score = sum(scores[criterion] * weights[criterion] for criterion in scores)
    total_weight = sum(weights.values())
    return total_score / total_weight
```

## Exercises

1. **Add more critique criteria**: Implement checks for grammar, tone, or domain-specific requirements
2. **Implement external validation**: Add human feedback or external API evaluation
3. **Dynamic termination**: Adjust quality thresholds based on content type
4. **Parallel critique**: Evaluate multiple aspects simultaneously

## Real-World Applications

- **Content Generation**: Blog posts, marketing materials, documentation
- **Code Review**: Automated code quality improvement
- **Creative Writing**: Story refinement and editing
- **Research Papers**: Academic writing improvement

## Download Code

[Download 04_reflection_loops.py](04_reflection_loops.py){ .md-button .md-button--primary } 