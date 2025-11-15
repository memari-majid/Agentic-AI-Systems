# 3. Foundations and Architecture of Agentic Systems

This section establishes the theoretical foundations and core architectural components that enable agentic behavior.

---

## 3.1 Defining Agency in AI Systems

We adopt a pragmatic definition of agency that synthesizes classical AI concepts with modern capabilities. An AI system exhibits **agency** when it possesses four fundamental characteristics:

### The Four Pillars of Agency

1. **Autonomy**  
   Ability to operate without continuous human intervention while making independent decisions within defined boundaries

2. **Goal-Orientation**  
   Capacity to pursue explicit or implicit objectives across multiple interactions, adapting strategies dynamically

3. **Environmental Interaction**  
   - Perceive environmental state accurately
   - Execute actions that modify the environment
   - Respond appropriately to feedback

4. **Adaptivity**  
   Capacity to adjust behavior based on experience, feedback, and changing circumstances

Together, these four characteristics distinguish truly agentic systems from reactive or purely generative AI systems.

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

LLMs are fundamentally stateless. Agentic systems must implement explicit state management:

- **Environmental State**: Current understanding of the world
- **Goal State**: Objectives, constraints, success criteria
- **Progress State**: Completed actions and remaining steps
- **Memory State**: Relevant historical information

**Implementation**: Key-value stores, graph databases, or structured conversation history

### 3.3.2 Perception-Action Loops

Effective agents implement tight perception-action loops:

```
Observe → Reason → Act → Observe Results → Repeat
```

This mirrors the sense-plan-act cycle from robotics, adapted to language-based agents.

### 3.3.3 Memory Hierarchies

Inspired by cognitive science, implement analogous memory structures:

- **Working Memory**: Current conversation context and immediate observations
- **Episodic Memory**: Specific past experiences and interactions
- **Semantic Memory**: General knowledge and learned patterns
- **Procedural Memory**: Encoded skills and action strategies

### 3.3.4 Tool Integration

Effective agents leverage external tools to overcome LLM limitations:

1. **Tool Discovery**: Identify available tools and understand capabilities
2. **Tool Selection**: Choose most appropriate tools for current tasks
3. **Parameter Binding**: Map task requirements to tool parameters
4. **Error Handling**: Recover gracefully from tool failures

### 3.3.5 Decomposition and Planning

Complex tasks must be decomposed into manageable subtasks:

- **Hierarchical Planning**: Recursive breakdown into sub-goals
- **Sequential Planning**: Ordering steps by dependencies
- **Parallel Planning**: Identifying independent subtasks
- **Contingent Planning**: Preparing for multiple possible outcomes

### 3.3.6 Reflection and Self-Correction

Advanced agents implement meta-cognitive capabilities:

- **Output Verification**: Check results against expectations
- **Consistency Checking**: Ensure reasoning chains remain coherent
- **Confidence Estimation**: Assess uncertainty in decisions
- **Alternative Generation**: Explore different approaches when needed

### 3.3.7 Grounding and Verification

Agents must ground outputs in verifiable information:

- **Citation**: Reference specific source materials
- **Retrieval-Augmented Generation**: Consult external knowledge
- **External Validation**: Use tools/APIs to verify claims
- **Human Verification**: Request confirmation for critical decisions

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

