# Labs & Code Examples

> Hands-on coding exercises for building agentic AI systems with complete implementations.

## Overview

This section contains practical, hands-on laboratories that teach you to build agentic AI systems through code. Each lab includes detailed markdown explanations and complete Python implementations.

## Lab Structure

Each lab consists of:
- **📄 `.md` file** - Detailed explanation, concepts, and instructions
- **🐍 `.py` file** - Complete, runnable Python implementation
- **📝 Comments** - Inline code documentation
- **🎯 Learning objectives** - Clear goals for each lab

---

## Beginner Labs

Perfect for getting started with agentic AI development.

### [Lab 01: Hello Graph](01-hello-graph.md) | [Code](01-hello-graph.py)
**Your first agentic AI system**

Build a simple graph-based agent using LangGraph to understand core concepts.

**You'll Learn:**
- Basic graph construction
- Node and edge definitions
- State management basics
- Simple agent flows

**Prerequisites:** Python basics, LLM API access  
**Time:** 30-45 minutes

---

### [Lab 02: Travel Booking Graph](02-travel-booking-graph.md) | [Code](02-travel-booking-graph.py)
**Multi-step workflow agent**

Create a travel booking agent that handles flight search, hotel booking, and itinerary creation.

**You'll Learn:**
- Multi-step workflows
- Conditional branching
- Tool integration
- State transitions

**Prerequisites:** Lab 01  
**Time:** 45-60 minutes

---

### [Lab 03: Parallel Scoring](03-parallel-scoring.md) | [Code](03-parallel-scoring.py)
**Concurrent agent execution**

Build an agent that scores multiple options in parallel for efficient decision-making.

**You'll Learn:**
- Parallel execution
- Result aggregation
- Performance optimization
- Concurrent workflows

**Prerequisites:** Labs 01-02  
**Time:** 40-50 minutes

---

## Intermediate Labs

Advance your skills with more complex patterns.

### [Lab 04: Reflection Loops](04-reflection-loops.md) | [Code](04-reflection-loops.py)
**Self-improving agents**

Implement agents that critique and improve their own outputs through reflection.

**You'll Learn:**
- Self-critique mechanisms
- Iterative improvement
- Quality assessment
- Reflection patterns

**Prerequisites:** Labs 01-03  
**Time:** 50-60 minutes

---

### [Lab 05: Parallel Planning](05-parallel-planning.md) | [Code](05-parallel-planning.py)
**Advanced planning systems**

Build agents that create and execute complex plans with parallel sub-tasks.

**You'll Learn:**
- Plan generation
- Task decomposition
- Parallel execution
- Result synthesis

**Prerequisites:** Labs 01-04  
**Time:** 55-70 minutes

---

### [Lab 06: Nested Graphs](06-nested-graphs.md) | [Code](06-nested-graphs.py)
**Hierarchical agent systems**

Create nested graph structures for complex, hierarchical workflows.

**You'll Learn:**
- Graph composition
- Hierarchical workflows
- Nested state management
- Modular design

**Prerequisites:** Labs 01-05  
**Time:** 60-75 minutes

---

### [Lab 07: Memory & Feedback](07-memory-feedback.md) | [Code](07-memory-feedback.py)
**Agents with persistent memory**

Implement memory systems that allow agents to learn from past interactions.

**You'll Learn:**
- Memory architectures
- Persistent state
- Feedback loops
- Learning mechanisms

**Prerequisites:** Labs 01-06  
**Time:** 55-70 minutes

---

## Advanced Labs

Master advanced techniques and production patterns.

### [Lab 08: Tool Protocols](08-tool-protocols.md) | [Code](08-tool-protocols.py)
**Standardized tool integration**

Implement agents that use tools following modern protocols like MCP.

**You'll Learn:**
- Tool protocol design
- Standardized interfaces
- Error handling
- Production patterns

**Prerequisites:** Labs 01-07  
**Time:** 65-80 minutes

---

### [Lab 09: Guardrails](09-guardrails.md) | [Code](09-guardrails.py)
**Safety and constraint systems**

Build safety mechanisms and guardrails for production agents.

**You'll Learn:**
- Safety constraints
- Input/output filtering
- Policy enforcement
- Risk mitigation

**Prerequisites:** Labs 01-08  
**Time:** 60-75 minutes

---

### [Lab 10: DSPy Optimization](10-dspy-optimization.md) | [Code](10-dspy-optimization.py)
**Automatic prompt optimization**

Use DSPy to automatically optimize agent prompts and performance.

**You'll Learn:**
- Prompt optimization
- DSPy framework
- Automated tuning
- Performance metrics

**Prerequisites:** Labs 01-09  
**Time:** 70-90 minutes

---

### [Lab 11: Agent Fine-Tuning](11-agent-finetuning.md) | [Code](11-agent-finetuning.py)
**Model customization**

Fine-tune models specifically for agentic tasks.

**You'll Learn:**
- Fine-tuning strategies
- Dataset preparation
- Training workflows
- Model evaluation

**Prerequisites:** Labs 01-10, ML experience  
**Time:** 90-120 minutes

---

### [Lab 12: Multi-Agent Systems](12-multi-agent-systems.md) | [Code](12-multi-agent-systems.py)
**Coordinated agent teams**

Build systems where multiple specialized agents collaborate.

**You'll Learn:**
- Multi-agent coordination
- Role specialization
- Communication protocols
- Team orchestration

**Prerequisites:** Labs 01-11  
**Time:** 80-100 minutes

---

### [Lab 13: Document RAG Agents](13-document-rag-agents.md)
**RAG-powered agents**

Build agents that leverage document retrieval for knowledge-intensive tasks.

**You'll Learn:**
- RAG architecture
- Vector databases
- Retrieval strategies
- Document processing

**Prerequisites:** Labs 01-12  
**Time:** 75-90 minutes

---

### [Lab 13: Document RAG Pipeline](13-document-rag-pipeline.md)
**Production RAG systems**

Implement complete RAG pipelines for production use.

**You'll Learn:**
- End-to-end pipelines
- Production patterns
- Scalability
- Monitoring

**Prerequisites:** Labs 01-12, RAG agents lab  
**Time:** 80-100 minutes

---

## Learning Paths

### Path 1: Complete Sequential
```
Lab 01 → Lab 02 → Lab 03 → ... → Lab 13
```
Best for systematic learning of all concepts.

### Path 2: Quick Start
```
Lab 01 → Lab 02 → Lab 04 → Lab 10 → Lab 13
```
Fast track to essential patterns.

### Path 3: Multi-Agent Focus
```
Lab 01 → Lab 03 → Lab 05 → Lab 06 → Lab 12
```
Specialized path for multi-agent systems.

### Path 4: Production Ready
```
Lab 01 → Lab 07 → Lab 08 → Lab 09 → Lab 10 → Lab 13
```
Focus on production-ready patterns.

## Prerequisites

### General Requirements
- **Python 3.9+**
- **LLM API access** (OpenAI, Anthropic, or similar)
- **Basic Python knowledge**
- **Terminal/command line familiarity**

### Recommended Setup
```bash
pip install langchain langgraph langsmith openai python-dotenv
```

### Environment Variables
```bash
export OPENAI_API_KEY="your-key-here"
export LANGSMITH_API_KEY="your-key-here"  # Optional, for tracking
```

## How to Use These Labs

1. **Read the `.md` file first** - Understand concepts and approach
2. **Examine the `.py` file** - Study the implementation
3. **Run the code** - Execute and observe behavior
4. **Modify and experiment** - Change parameters and logic
5. **Build on it** - Extend for your use cases

## Tips for Success

✅ **Start simple** - Begin with Lab 01 even if experienced  
✅ **Read comments** - Code is heavily documented  
✅ **Experiment** - Modify examples to test understanding  
✅ **Debug actively** - Use print statements and debuggers  
✅ **Track costs** - Monitor API usage and costs  
✅ **Take notes** - Document learnings and insights  

## Troubleshooting

**Common Issues:**
- API key not set → Check environment variables
- Module not found → Install required packages
- Rate limits → Add delays or use rate limiting
- Out of credits → Check API account balance

## Integration with Other Sections

- **[Foundations](../01-foundations/)** - Theory behind the labs
- **[Implementation](../02-implementation/)** - Framework documentation
- **[Modern Frameworks](../03-modern-frameworks/)** - Alternative tools
- **[Research](../05-research/)** - Advanced concepts

---

**Total Labs:** 14 (13 numbered + 1 variant)  
**Difficulty:** Beginner → Advanced  
**Est. Total Time:** 15-25 hours for all labs  
**Language:** Python  
**Frameworks:** LangChain, LangGraph, DSPy

[← Back to Main](../README.md)