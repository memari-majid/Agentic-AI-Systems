# Building Agentic AI Systems - Practical Labs

This directory contains hands-on exercises and example implementations that demonstrate key concepts from the course. These labs provide practical experience with agentic AI systems, focusing on implementation patterns using frameworks like LangGraph and LangChain.

## Setup

To run these examples, make sure you have installed the required dependencies:

```bash
pip install -r ../requirements.txt
```

## Lab Descriptions

The labs are designed to progressively build your understanding of agentic systems:

1. **LangGraph Basics** (`01_hello_graph.py`)  
   A simple introduction to graph-based agent orchestration with minimal code.

2. **Travel Booking** (`02_travel_booking_graph.py`)  
   Demonstrates state management and retry logic in a practical booking scenario.

3. **Parallel Scoring** (`03_parallel_scoring.py`)  
   Implements utility-based decision making with parallel evaluation of options.

4. **Reflection Loops** (`04_reflection_loops.py`)  
   Explores self-critique and improvement mechanisms for more robust agents.

5. **Parallel Planning** (`05_parallel_planning.py`)  
   Shows fan-out/fan-in architecture for efficient parallel tool use.

6. **Nested Graphs** (`06_nested_graphs.py`)  
   Implements the Coordinator/Worker/Delegator pattern using nested graph structures.

7. **Memory Feedback** (`07_memory_feedback.py`)  
   Creates hybrid short-term/long-term memory systems with feedback loops.

8. **Tool Protocols** (`08_tool_protocols.py`)  
   Compares OpenAI function calling and LangChain tool integration approaches.

9. **Guardrails** (`09_guardrails.py`)  
   Demonstrates safety measures and constraints in agentic systems.

10. **DSPy Optimization** (`10_dspy_optimization.py`)  
    Explores systematic prompt optimization techniques for improved agent performance.

11. **Agent Fine-tuning** (`11_agent_finetuning.py`)  
    Shows approaches for specialized LLM training for agent capabilities.

12. **Multi-Agent Systems** (`12_multi_agent_systems.py`)  
    Demonstrates collaborative agent architectures for complex problem-solving.

## Running the Labs

Each lab can be run directly from the command line:

```bash
python 01_hello_graph.py
```

Most labs include optional command-line arguments that allow you to experiment with different configurations:

```bash
# Example for multi-agent systems lab
python 12_multi_agent_systems.py --task "Design a marketing campaign"
```

## Learning Path

For the best learning experience, it's recommended to work through the labs in order, as they build upon concepts introduced in previous exercises. Each lab corresponds to topics covered in the main course chapters:

- Labs 1-3: Foundation concepts (Chapters 1-3)
- Labs 4-7: Agent design and implementation (Chapters 4-7)
- Labs 8-12: Advanced topics and applications (Chapters 8-11)

## Notes

- Most examples include detailed comments explaining key concepts and design choices
- The labs are designed to run with minimal external dependencies when possible
- If using OpenAI or Anthropic APIs, you'll need to set up your API keys as environment variables 