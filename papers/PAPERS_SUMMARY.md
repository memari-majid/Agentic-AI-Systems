# Summary of Converted Papers for Integration

This document summarizes key findings from the 5 converted PDF papers for integration into the review paper.

## Paper 1: Agentic AI Needs a Systems Theory (IBM Research, 2025)
**Authors**: Erik Miehling, Karthikeyan Natesan Ramamurthy, et al., IBM Research  
**Key Contribution**: Advocates for a holistic, systems-theoretic perspective for developing agentic AI

### Key Concepts:
1. **Functional Agency** - Defined by three conditions:
   - Action generation (based on environmental information)
   - Outcome model (representing action-outcome relationships)
   - Adaptation (behavioral adjustment to maintain/improve performance)

2. **Emergent Capabilities**:
   - Enhanced cognition through environment interaction
   - Causal reasoning via prediction error minimization
   - Metacognitive awareness through prediction and interaction

3. **Open Challenges**:
   - Building generalist agents
   - Designing efficient agent-agent interactions
   - Controlling emergence of subgoals
   - Governing human-agent interactions

### Integration Points:
- **Section 2 (Related Work)**: Cite their systems-theoretic approach
- **Section 3 (Theoretical Foundations)**: Incorporate functional agency definition
- **Section 6 (Multi-Agent Coordination)**: Reference mechanisms of emergence
- **Section 10 (Ethical Considerations)**: Discuss governance challenges

---

## Paper 2: Agentic AI: Autonomous Intelligence for Complex Goals (IEEE Access, 2025)
**Authors**: Deepak Bhaskar Acharya, Karthigeyan Kuppan, B. Divya  
**Published**: IEEE Access, Volume 13, 2025

### Key Concepts:
1. **Core Characteristics**:
   - Autonomy with minimal human intervention
   - Adaptability to evolving environments
   - Advanced decision-making capabilities
   - Self-sufficiency in dynamic scenarios

2. **Methodologies**:
   - Architectures (perception, reasoning, action, learning)
   - Learning approaches (reinforcement learning, goal-oriented)
   - Training methods for agentic behaviors

3. **Applications**:
   - Healthcare (diagnostics, treatment planning)
   - Finance (risk assessment, portfolio management)
   - Adaptive software systems

4. **Challenges**:
   - Goal design and convergence
   - Context adaptation
   - Resource constraints
   - Ethical considerations (responsibility, equity, transparency)

### Integration Points:
- **Section 2 (Related Work)**: Comprehensive survey reference
- **Section 3 (Theoretical Foundations)**: Autonomy spectrum
- **Section 5 (Implementation Methodology)**: Training approaches
- **Section 10 (Ethical Considerations)**: Responsibility and transparency frameworks

---

## Paper 3: Agentic AI Systems: Opportunities, Challenges, and Trustworthiness (IEEE EIT, 2025)
**Authors**: Tayiba Raheem, Gahangir Hossain (University of North Texas)  
**Published**: 2025 IEEE International Conference on Electro Information Technology

### Key Concepts:
1. **Agentic AI Architecture** (Layered approach):
   - Input Layer (data streams)
   - Agent Orchestration Layer (multi-agent coordination)
   - Output Layer (personalized results)
   - Data storage/retrieval layer (vector stores, knowledge graphs)
   - Service Layer (multi-channel delivery)
   - Foundation Layer (safeguards, ethical frameworks, regulatory compliance)

2. **Opportunities**:
   - Enhancing economic productivity and business growth
   - Workforce transformation
   - Scientific and technological advancements
   - Improving decision-making through reinforcement learning
   - Enhancing personalization through AI agency
   - Expanding access to essential services

3. **Challenges**:
   - Technical limitations and unpredictability
   - Ethical and social risks
   - Emergent agency and lack of human oversight
   - Difficulty in regulation and governance
   - Lack of robustness and safety features

4. **Trustworthiness Factors**:
   - Competence and accuracy
   - Safety and knowability
   - Value alignment and risk tolerance
   - Stochasticity management
   - Transparency in sociotechnical context

5. **Mitigation Strategies**:
   - Adversarial training
   - Guardrails at inference time
   - Interpretable AI
   - Sandbox environments and monitoring
   - Constitutional AI

### Integration Points:
- **Section 4 (Core Architectural Components)**: Reference layered architecture
- **Section 7 (Knowledge Integration: RAG vs Fine-Tuning)**: Cite personalization approaches
- **Section 8 (Production Deployment)**: Trustworthiness metrics
- **Section 9 (Strategic Considerations)**: Economic impact
- **Section 10 (Ethical Considerations)**: Comprehensive ethics framework

---

## Paper 4: AI Agents vs. Agentic AI: A Conceptual Taxonomy (Information Fusion, 2026)
**Authors**: Ranjan Sapkota, Konstantinos I. Roumeliotis, Manoj Karkee  
**Published**: Information Fusion, Volume 126, 2026

### Key Concepts:
1. **Conceptual Distinction**:
   - **AI Agents**: Modular systems driven by LLMs/LIMs for task-specific automation
   - **Agentic AI**: Multi-agent collaboration with dynamic task decomposition, persistent memory, coordinated autonomy

2. **Evolution Timeline**:
   - Pre-2022: Rule-based, expert systems (MYCIN, DENDRAL, XCON, SOAR)
   - Post-ChatGPT (2022+): LLM-based agents with tool use, function calling
   - 2023+: Multi-agent agentic systems (CrewAI, AutoGPT, BabyAGI)

3. **Architectural Comparison**:
   - Input-output mechanisms
   - Autonomy levels
   - Interaction styles
   - Operational mechanisms

4. **Application Domains**:
   - **AI Agents**: Customer support, scheduling, data summarization
   - **Agentic AI**: Research automation, robotic coordination, medical decision support

5. **Challenges**:
   - **AI Agents**: Hallucination, brittleness, context limitations
   - **Agentic AI**: Emergent behavior, coordination failure, scalability

6. **Solutions**:
   - ReAct loops for reasoning
   - Retrieval-augmented generation (RAG)
   - Automation coordination layers
   - Causal modeling

### Integration Points:
- **Section 1 (Introduction)**: Historical context and evolution
- **Section 2 (Related Work)**: Taxonomy of AI systems
- **Section 5 (Implementation Methodology)**: Framework comparison
- **Section 6 (Multi-Agent Coordination)**: Coordination protocols
- **Section 11 (Conclusion)**: Future directions

---

## Paper 5: The Rise of Agentic AI: A Review of Definitions, Frameworks, Architectures, Applications, Evaluation Metrics, and Challenges (Future Internet, 2025)
**Authors**: Ajay Bandi, Bhavani Kongari, Roshini Naguru, Sahitya Pasnoor, Sri Vidya Vilipala  
**Published**: Future Internet, Volume 17, 2025

### Key Concepts:
1. **Market Projections**:
   - 2024: USD 5.3-5.4B
   - 2030: USD 50-52B (41-46% CAGR)

2. **Comprehensive Framework Analysis**:
   - **LLM-based**: LangChain, AutoGPT, BabyAGI, OpenAgents, Autogen, CAMEL, MetaGPT, SuperAGI
   - **Non-LLM-driven**: TB-CSPN and traditional agentic systems
   - Features: Planning, memory, reflection, goal pursuit

3. **Core Architectural Components**:
   - Perception modules
   - Memory systems (short-term, long-term)
   - Reasoning engines (CoT, ReAct, ToT)
   - Action modules

4. **Evaluation Metrics**:
   - **Qualitative**: Explainability, transparency, user satisfaction
   - **Quantitative**: Accuracy, latency, throughput, task completion rate
   - Testing methods: Unit, integration, adversarial

5. **Application Taxonomy**:
   - Healthcare (diagnosis, treatment planning)
   - Finance (trading, fraud detection)
   - Manufacturing (predictive maintenance)
   - Customer service (chatbots, virtual assistants)

6. **Key Challenges**:
   - **Technical**: Reliability, hallucination, context management
   - **Architectural**: Scalability, modularity, interoperability
   - **Coordination**: Multi-agent synchronization, conflict resolution
   - **Ethical**: Bias, fairness, accountability
   - **Security**: Privacy, adversarial attacks, data protection

### Integration Points:
- **Section 1 (Introduction)**: Market data and adoption trends
- **Section 2 (Related Work)**: Comprehensive framework review
- **Section 4 (Core Architectural Components)**: Detailed component analysis
- **Section 5 (Implementation Methodology)**: Framework comparison table
- **Section 8 (Production Deployment)**: Evaluation metrics
- **Section 9 (Strategic Considerations)**: Application domains

---

## Cross-Paper Themes

### 1. **Definitions of Agency**
- Systems theory perspective (Paper 1)
- Autonomy and adaptability focus (Paper 2)
- Multi-agent vs single agent (Paper 4)
- Goal-directed behavior (Papers 1, 2, 5)

### 2. **Architectural Patterns**
- Layered architecture (Paper 3)
- Multi-agent coordination (Papers 1, 4, 5)
- Component-based design (Papers 2, 5)

### 3. **Key Challenges**
- Trust and safety (Papers 2, 3)
- Coordination complexity (Papers 1, 4, 5)
- Ethical considerations (Papers 2, 3, 5)
- Technical limitations (Papers 2, 3, 4, 5)

### 4. **Future Directions**
- Improved reasoning capabilities (All papers)
- Better human-AI collaboration (Papers 1, 3)
- Standardization and interoperability (Papers 4, 5)
- Ethical frameworks (Papers 2, 3, 5)

---

## Recommended Integration Strategy

1. **Introduction**: 
   - Add market projections from Paper 5
   - Reference evolution timeline from Paper 4

2. **Related Work**:
   - Incorporate comprehensive survey from Paper 2
   - Add taxonomy from Paper 4
   - Reference systems theory from Paper 1

3. **Theoretical Foundations**:
   - Integrate functional agency from Paper 1
   - Add autonomy spectrum from Paper 2

4. **Core Architectural Components**:
   - Expand with layered architecture from Paper 3
   - Add detailed component analysis from Paper 5

5. **Implementation Methodology**:
   - Include framework comparison from Papers 4 and 5
   - Add mitigation strategies from Paper 3

6. **Multi-Agent Coordination**:
   - Incorporate emergence mechanisms from Paper 1
   - Reference coordination challenges from Papers 4 and 5

7. **Knowledge Integration**:
   - Maintain existing RAG vs fine-tuning content
   - Add personalization insights from Paper 3

8. **Production Deployment**:
   - Expand evaluation metrics with Paper 5
   - Add trustworthiness framework from Paper 3

9. **Strategic Considerations**:
   - Include economic impact from Paper 3
   - Add application domains from Papers 2 and 5

10. **Ethical Considerations**:
    - Integrate comprehensive frameworks from Papers 2, 3, 5
    - Add governance challenges from Paper 1

11. **Conclusion**:
    - Synthesize future directions from all papers
    - Emphasize cross-cutting themes

