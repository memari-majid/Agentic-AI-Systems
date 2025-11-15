---
version: 2025.11.15
last_updated: 2025-11-15
last_updated_display: November 15, 2025
---

# 3. Foundations and Architecture of Agentic Systems

This section establishes the theoretical foundations and core architectural components that enable agentic behavior.

---

## 3.1 Defining Agency in AI Systems

We adopt a pragmatic definition of agency that synthesizes classical AI concepts with modern capabilities. An AI system exhibits agency when it possesses four fundamental characteristics that work together to enable autonomous and goal-directed behavior. First, the system must demonstrate autonomy, which encompasses the ability to operate without continuous human intervention while making independent decisions within defined boundaries. Second, the system must exhibit goal-orientation, possessing the capacity to pursue explicit or implicit objectives across multiple interactions and adapting its strategies dynamically to achieve desired outcomes. Third, the system must engage in environmental interaction, which includes the ability to perceive environmental state accurately, execute actions that modify the environment in meaningful ways, and respond appropriately to feedback received from the environment. Fourth, the system must display adaptivity, demonstrating the capacity to adjust its behavior based on accumulated experience, received feedback, and changing circumstances in its operational context. Together, these four characteristics distinguish truly agentic systems from reactive or purely generative AI systems.

---

## 3.2 The Autonomy Spectrum

Rather than treating autonomy as binary, we propose a **five-level spectrum**:

| Level | Name | Description | Example |
|-------|------|-------------|---------|
| **0** | Reactive Generation | Responds to inputs without persistent state or goals | Basic Q&A chatbot |
| **1** | Stateful Interaction | Maintains conversational context, references previous exchanges | ChatGPT-like assistants |
| **2** | Goal-Oriented Behavior | Pursues explicit objectives across multiple steps | Task completion agents |
| **3** | Adaptive Planning | Modifies approach based on results, handles unexpected situations | Research assistants |
| **4** | Strategic Autonomy | Identifies sub-goals autonomously, meta-cognitive self-correction | Advanced autonomous systems |

!!! example "Level Progression"
    Most current systems operate at **Levels 1-2**. Research is pushing toward **Levels 3-4** with improved planning and reflection capabilities.

---

## 3.3 Core Architectural Principles

Drawing from cognitive architectures and modern AI systems, we identify **seven core principles** for agentic design:

### 3.3.1 Explicit State Management

Large language models are fundamentally stateless, with each inference being independent. Agentic systems must therefore implement explicit state management encompassing environmental state, which represents the current understanding of the world; goal state, which captures objectives, constraints, and success criteria; progress state, which tracks completed actions and remaining steps; and memory state, which maintains relevant historical information. State management can be implemented through various mechanisms including key-value stores, graph databases, or structured conversation history.

### 3.3.2 Perception-Action Loops

Effective agents implement tight perception-action loops:

```
Observe → Reason → Act → Observe Results → Repeat
```

This mirrors the sense-plan-act cycle from robotics, adapted to language-based agents.

### 3.3.3 Memory Hierarchies

Cognitive science distinguishes between working memory, short-term memory, and long-term memory. Agentic systems benefit from implementing analogous memory structures that mirror these human cognitive capabilities. Working memory maintains the current conversation context and immediate observations, providing the agent with awareness of its present situation. Episodic memory stores specific past experiences and interactions, enabling the agent to recall and learn from previous encounters. Semantic memory encodes general knowledge and learned patterns that can be applied across different contexts. Finally, procedural memory captures encoded skills and action strategies that the agent has developed through experience, allowing it to execute complex behaviors efficiently without explicit reasoning about each step.

### 3.3.4 Tool Integration

Effective agents leverage external tools to overcome inherent LLM limitations. Successful tool integration requires mastery of four interconnected capabilities. First, agents must perform tool discovery by systematically identifying available tools and understanding their specific capabilities and constraints. Second, agents must engage in intelligent tool selection, choosing the most appropriate tools for their current tasks based on task requirements, tool capabilities, and contextual factors. Third, agents must accomplish parameter binding by accurately mapping task-specific requirements to the appropriate tool parameters, ensuring that tools receive correctly formatted inputs. Fourth, agents must implement robust error handling mechanisms that enable them to recover gracefully from tool failures, either by retrying with adjusted parameters, selecting alternative tools, or escalating to human intervention when necessary.

### 3.3.5 Decomposition and Planning

Complex tasks must be systematically decomposed into manageable subtasks to enable effective execution. Agents employ several complementary decomposition strategies depending on task characteristics. Hierarchical planning involves recursively breaking down high-level goals into increasingly specific sub-goals until reaching primitive actions that can be executed directly. Sequential planning focuses on ordering steps according to their dependencies, ensuring that prerequisite actions are completed before dependent steps are attempted. Parallel planning identifies independent subtasks that can be pursued simultaneously, enabling efficient resource utilization and reduced overall execution time. Contingent planning prepares the agent for multiple possible outcomes by developing alternative action sequences that can be activated based on observed results, providing robustness in uncertain environments.

### 3.3.6 Reflection and Self-Correction

Advanced agents implement meta-cognitive capabilities that enable sophisticated error detection and self-correction. These reflection mechanisms operate at multiple levels of abstraction. Output verification involves systematically checking generated results against established expectations and known constraints to identify potential errors before they propagate. Consistency checking ensures that reasoning chains remain coherent throughout multi-step processes, detecting logical contradictions or inconsistencies that might indicate flawed reasoning. Confidence estimation assesses the degree of uncertainty inherent in decisions and predictions, enabling the agent to recognize when additional information or alternative approaches may be needed. When initial attempts fail or produce unsatisfactory results, alternative generation explores different problem-solving approaches, leveraging the agent's ability to reason about its own reasoning process to identify and pursue more promising strategies.

### 3.3.7 Grounding and Verification

Agents must ground their outputs in verifiable information to mitigate the persistent challenge of hallucination in large language models. Several complementary grounding strategies work together to ensure output reliability. Citation mechanisms require agents to reference specific source materials when making factual claims, providing transparency and enabling verification. Retrieval-augmented generation extends this by actively consulting external knowledge bases during the generation process, ensuring that responses are grounded in current, authoritative information. External validation employs tools and APIs to independently verify factual claims, cross-referencing agent outputs against trusted data sources. For decisions with significant consequences, human verification provides an essential safeguard by requesting explicit human confirmation before proceeding, maintaining appropriate human oversight in critical situations.

---

## 3.4 Core Architectural Components

Four core components realize agentic behavior:

<div class="grid cards" markdown>

-   :material-eye:{ .lg .middle } __Perception Module__

    ---

    **Textual**: Information extraction, intent recognition, context aggregation
    
    **Multimodal**: Vision (CLIP, LLaVA, GPT-4V), Audio (Whisper), Documents, Code

-   :material-brain:{ .lg .middle } __Memory Module__

    ---

    **Short-term**: Conversation history, context windows
    
    **Long-term**: Vector DBs (FAISS, Pinecone), Graph DBs (Neo4j), Document stores

-   :material-head-lightbulb:{ .lg .middle } __Reasoning Module__

    ---

    **Paradigms**: Chain-of-Thought, ReAct, Tree-of-Thoughts
    
    **Planning**: Forward, backward, hierarchical, MCTS

-   :material-run-fast:{ .lg .middle } __Action Module__

    ---

    **Types**: Communication, retrieval, computation, state modification, tool invocation
    
    **Integration**: Function calling, MCP, code interpretation

</div>

---

### Perception Module

Enables agents to understand their environment:

**Textual Perception**:

1. Information extraction (NER, relation extraction)
2. Intent recognition (user goals)
3. Context aggregation (historical context)
4. Semantic understanding (structured representations)

**Multimodal Perception**:

- **Vision**: CLIP, LLaVA, GPT-4V for image understanding
- **Audio**: Whisper for speech transcription
- **Documents**: PDF/presentation parsing
- **Code**: Repository analysis and understanding

---

### Memory Module

Enables agents to maintain context and learn from experience:

**Short-Term Memory**:

- Conversation history buffers
- Context window management (4K-128K tokens)
- Summarization for long conversations
- Relevance filtering

**Long-Term Memory**:

- **Vector databases**: FAISS, Pinecone, Weaviate, Chroma (semantic retrieval)
- **Graph databases**: Neo4j (entity relationships)
- **Relational databases**: PostgreSQL, MySQL (structured data)
- **Document stores**: MongoDB, Elasticsearch (unstructured content)

**Memory Retrieval** balances relevance, recency, and importance:

$$
\text{score}(m) = \alpha \cdot \text{relevance}(m, q) + \beta \cdot \text{recency}(m) + \gamma \cdot \text{importance}(m)
$$

where \(m\) is a memory, \(q\) is the current query, and \(\alpha, \beta, \gamma\) are weighting parameters.

---

### Reasoning Module

Determines appropriate actions based on perceptions and goals:

**Reasoning Paradigms**:

=== "Chain-of-Thought (CoT)"
    Decomposes complex problems into explicit sequential steps
    
    ```
    Question → Think step 1 → Think step 2 → ... → Answer
    ```

=== "ReAct"
    Interleaves reasoning with environmental actions
    
    ```
    Think → Act → Observe → Think → Act → Observe → ...
    ```

=== "Tree-of-Thoughts"
    Explores multiple reasoning paths in parallel
    
    ```
                Root
              /  |  \
           Path1 Path2 Path3
            /|\   /|\   /|\
          (explore & evaluate)
    ```

**Planning Algorithms**:

- **Forward Planning**: Progress from current state toward goals
- **Backward Chaining**: Work backward from goal to current state
- **Hierarchical Task Networks**: Decompose abstract tasks into concrete subtasks
- **Monte Carlo Tree Search**: Simulate action sequences to evaluate outcomes

---

### Action Module

Executes agent decisions through various mechanisms:

**Action Types**:

1. **Communication**: Generate responses, ask clarifying questions
2. **Information Retrieval**: Search databases, query APIs, retrieve documents
3. **Computational**: Execute code, perform calculations, transform data
4. **State Modification**: Update variables, create artifacts, modify environment
5. **Tool Invocation**: Call external APIs, run specialized software

**Tool Integration Mechanisms**:

- **Function Calling**: Generate structured JSON function invocations
- **Model Context Protocol (MCP)**: Standardized bidirectional communication
- **Code Interpretation**: Dynamically generate and execute code in sandboxed environments

---

!!! summary "Key Takeaways"
    - **Agency** requires autonomy, goal-orientation, interaction, and adaptivity
    - **Autonomy** exists on a spectrum from reactive to strategic
    - **7 core principles** guide agentic system design
    - **4 core components** (perception, memory, reasoning, action) work together to enable agentic behavior

---

[⬅️ Introduction](01-introduction.md) | [Implementation & Deployment ➡️](04-implementation.md)

