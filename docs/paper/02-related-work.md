---
version: 2025.11.15
last_updated: 2025-11-15
last_updated_display: November 15, 2025
---

# 2. Related Work

This section surveys foundational and contemporary research that informs our framework for agentic AI systems.

---

## 2.1 Foundations of Intelligent Agents

The concept of intelligent agents has deep roots in artificial intelligence research. Wooldridge and Jennings established foundational definitions of agency, distinguishing:

- **Weak agency**: Autonomy, social ability, reactivity, pro-activeness
- **Strong agency**: Mental states, emotions, beliefs

Russell and Norvig formalized agent architectures including:

- Simple reflex agents
- Model-based agents
- Goal-based agents
- Utility-based agents

Recent work has extended these classical frameworks to the era of large language models. Xi et al. surveyed LLM-based autonomous agents, identifying **perception, memory, reasoning, and action** as core components. Wang et al. provided a comprehensive survey of LLM-based agents with focus on planning and tool use capabilities.

---

## 2.2 Large Language Models as Foundation

The development of large-scale transformer models has enabled unprecedented natural language capabilities:

- **GPT-3** [Brown et al., 2020]: Few-shot learning
- **GPT-4** [OpenAI, 2023]: Complex reasoning, multimodal
- **LLaMA** [Touvron et al., 2023]: Open foundation models
- **Claude** [Anthropic, 2023]: Long context, safety-focused

### Reasoning Frameworks

**Chain-of-Thought (CoT)** prompting shows that LLMs can perform multi-step reasoning when appropriately prompted.

**ReAct** framework interleaves reasoning and acting in an iterative cycle.

**Tree-of-Thoughts** extends this to explore multiple reasoning paths in parallel.

These techniques form the basis for reasoning in modern agentic systems.

---

## 2.3 Tool Use and Function Calling

Integration of LLMs with external tools has been explored extensively:

- **Toolformer** [Schick et al., 2023]: Self-supervised tool learning
- **ToolLLM** [Qin et al., 2023]: Complex tool learning with 16,000+ APIs
- **Model Context Protocol (MCP)** [Anthropic, 2024]: Standardized tool interface

These approaches enable seamless communication between LLMs and external systems.

---

## 2.4 Multi-Agent Systems

Classical multi-agent systems research established coordination mechanisms and communication protocols. Recent work has adapted these concepts for LLM-based agents:

### Key Frameworks

**Generative Agents** [Park et al., 2023]  
Capable of believable social behavior in simulated environments

**MetaGPT** [Hong et al., 2023]  
Multi-agent software development using role-based collaboration

**AutoGen** [Wu et al., 2023]  
Framework for building conversational multi-agent systems

---

## 2.5 Retrieval-Augmented Generation

RAG was introduced to enhance language models with external knowledge retrieval:

- **RAG** [Lewis et al., 2020]: Original framework
- **Dense Passage Retrieval (DPR)** [Karpukhin et al., 2020]: Dense retrieval
- **Contriever** [Izacard et al., 2021]: Unsupervised retrieval
- **Hybrid approaches** [Lin et al., 2021]: Combining sparse and dense

**Practical frameworks**: LlamaIndex and LangChain provide implementation support.

---

## 2.6 Fine-Tuning and Adaptation

Parameter-efficient fine-tuning methods enable efficient model adaptation:

- **LoRA** [Hu et al., 2021]: Low-rank adaptation
- **Prefix-Tuning** [Li & Liang, 2021]: Learnable prefix vectors
- **Adapter layers** [Houlsby et al., 2019]: Bottleneck layers

**Instruction tuning** and **RLHF** (Reinforcement Learning from Human Feedback) have proven effective for aligning models with human preferences.

---

## 2.7 Agent Frameworks and Platforms

Several frameworks have emerged for building agentic systems:

### Major Frameworks

Several frameworks have emerged for building agentic systems, each addressing different aspects of agent development and deployment. LangChain provides a modular framework for LLM applications, offering comprehensive support for chains, agents, and memory components that can be composed to create complex agent behaviors. Building upon this foundation, LangGraph introduces a graph-based state machine framework specifically designed for managing complex workflows with explicit state transitions and checkpoint capabilities. For developers prioritizing type safety and structured outputs, Pydantic AI offers a production-ready approach to agent development with built-in validation and error handling. DSPy takes a different approach by providing a programming model that optimizes LM prompts and weights through systematic compilation and evaluation. AutoGPT explores fully autonomous agent capabilities with self-directed task execution, while CrewAI focuses on role-based multi-agent collaboration with specialized agent teams working together to accomplish complex objectives.

---

## 2.8 Safety and Alignment

Ensuring safe and aligned agent behavior is critical:

- **Constitutional AI** [Bai et al., 2022]: Training for helpful, harmless, honest behavior
- **Red-teaming** [Perez et al., 2022]: Adversarial testing to identify failure modes
- **Guardrails** [Rebedea et al., 2023]: Runtime safety constraints

---

!!! summary "Key Takeaways"
    - Agentic AI builds on foundations from classical AI, cognitive science, and modern LLMs
    - Multiple frameworks address different aspects (modularity, state management, type safety, optimization)
    - Safety and alignment are critical research areas
    - Both RAG and fine-tuning have roles in knowledge integration

---

[⬅️ Introduction](01-introduction.md) | [Foundations & Architecture ➡️](03-foundations.md)

