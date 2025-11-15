# Integration Guide: New Papers into Review Paper

This guide provides specific LaTeX code snippets to integrate the 5 newly converted papers into your review paper `arxiv-paper/paper.tex`.

## References Added to references.bib

The following 5 new references have been added:
- `miehling2025systems` - IBM Research systems theory paper
- `acharya2025agentic` - IEEE Access comprehensive survey
- `raheem2025agentic` - IEEE EIT trustworthiness paper
- `sapkota2026agents` - Information Fusion taxonomy paper
- `bandi2025rise` - Future Internet comprehensive review

---

## Section 1: Introduction

### Add Market Data and Evolution Timeline

**Location**: After the paragraph discussing the shift from reactive to autonomous agents

**Add**:
```latex
The rapid growth of agentic AI is evidenced by market projections estimating the AI agents market at USD 5.3-5.4B in 2024, projected to reach USD 50-52B by 2030 (representing a 41-46\% CAGR) \cite{bandi2025rise}. This reflects a fundamental architectural shift from isolated task automation to end-to-end process orchestration through multi-agent collaboration \cite{sapkota2026agents}.
```

---

## Section 2: Related Work

### Add Comprehensive Survey References

**Location**: After the current multi-agent systems paragraph

**Add**:
```latex
Recent comprehensive surveys have expanded our understanding of agentic AI from multiple perspectives. \citet{acharya2025agentic} provides a thorough examination of autonomous intelligence for complex goals, covering methodologies from reinforcement learning to goal-oriented architectures. \citet{bandi2025rise} offers an extensive review of 143 primary studies on LLM-based and non-LLM-driven agentic systems, analyzing frameworks including LangChain, AutoGPT, BabyAGI, Autogen, and MetaGPT in terms of their support for planning, memory, reflection, and goal pursuit.

A critical distinction emerges between AI Agents and Agentic AI systems. \citet{sapkota2026agents} propose a structured taxonomy differentiating AI Agents as modular, task-specific systems from Agentic AI as paradigms marked by multi-agent collaboration, dynamic task decomposition, and coordinated autonomy. This conceptual clarity helps frame the evolution from pre-2022 rule-based expert systems through post-ChatGPT LLM-based agents to modern multi-agent agentic systems.
```

### Add Systems Theory Perspective

**Location**: Near the end of Related Work section

**Add**:
```latex
\subsection{Systems-Theoretic Perspectives}

\citet{miehling2025systems} argue that the development of agentic AI requires a holistic, systems-theoretic perspective to fully understand capabilities and mitigate emergent risks. They introduce the concept of \textit{functional agency}, defined by three core conditions: (1) action generation based on environmental information, (2) outcome modeling to represent action-outcome relationships, and (3) adaptation to maintain or improve performance. Their position emphasizes that AI development currently focuses too narrowly on individual model capabilities while underestimating both the true capabilities and associated risks arising from system-level interactions between agents, humans, and environments.
```

---

## Section 3: Theoretical Foundations

### Expand Agency Definition

**Location**: After defining agency and autonomy

**Add**:
```latex
\subsection{Functional Agency}

Building on traditional definitions of agency, we adopt the concept of \textit{functional agency} from \citet{miehling2025systems}, which characterizes agency along a spectrum rather than as a binary property. A system possesses functional agency if it satisfies three conditions:

\begin{enumerate}
    \item \textbf{Action Generation}: Capable of generating actions based on environmental information directed toward an objective
    \item \textbf{Outcome Model}: Capable of representing relationships between actions and outcomes
    \item \textbf{Adaptation}: Capable of adapting behavior in response to changes in the outcome model
\end{enumerate}

The degree of functional agency varies across systems depending on the sophistication of these components. Action generation ranges from reactive (memoryless) to stateful (maintaining fixed-domain summaries) to epistemic (driven by abstract, context-sensitive knowledge). Outcome models follow Pearl's causal hierarchy, progressing from associations (correlations) to interventions (effects of actions) to counterfactuals (hypothetical scenarios). Adaptation mechanisms span contextual (behavior modification), parametric (updating functional relationships), and reflective (deeper reasoning about relationship updates).

This framework helps explain why LLMs, despite their impressive capabilities, exhibit limited functional agency—they primarily operate at the associational level of outcome modeling and contextual level of adaptation, lacking the epistemic action generation and counterfactual reasoning of human agency.
```

---

## Section 4: Core Architectural Components

### Add Layered Architecture Reference

**Location**: After describing the four core components

**Add**:
```latex
\subsection{Layered Architectural Approach}

\citet{raheem2025agentic} propose a sophisticated layered architecture for agentic AI systems, exemplified through a digital health assistant managing chronic illnesses:

\begin{itemize}
    \item \textbf{Input Layer}: Ingests real-time data from multiple sources (sensors, wearables, electronic health records)
    \item \textbf{Agent Orchestration Layer}: Coordinates multiple specialized agents (glucose trend analysis, meal planning, medication reminders, behavioral nudging) with adaptive task management and multi-agent coordination
    \item \textbf{Output Layer}: Delivers personalized recommendations through multi-channel interfaces
    \item \textbf{Data Storage/Retrieval Layer}: Maintains vector stores and knowledge graphs linking patient history, drug interactions, and research
    \item \textbf{Service Layer}: Ensures multi-channel delivery through apps, telemedicine platforms, and notification systems
    \item \textbf{Foundation Layer}: Provides safeguards, ethical frameworks, regulatory compliance (HIPAA, FDA SaMD), and bias checks
\end{itemize}

This layered approach emphasizes the importance of integrating safety, ethics, and regulatory considerations as foundational elements rather than afterthoughts.
```

---

## Section 5: Implementation Methodology

### Add Framework Comparison Table

**Location**: After discussing individual frameworks

**Add**:
```latex
\subsection{Comparative Framework Analysis}

\citet{bandi2025rise} conducted a comprehensive analysis of current LLM-based and non-LLM-driven agentic frameworks, evaluating their support for key agentic capabilities. Table~\ref{tab:framework_comparison} summarizes the capabilities of major frameworks.

\begin{table}[htbp]
\centering
\caption{Comparison of Agentic AI Frameworks}
\label{tab:framework_comparison}
\begin{tabular}{lcccc}
\toprule
\textbf{Framework} & \textbf{Planning} & \textbf{Memory} & \textbf{Reflection} & \textbf{Tool Use} \\
\midrule
LangChain & \checkmark & \checkmark & \text{--} & \checkmark \\
AutoGPT & \checkmark & \checkmark & \checkmark & \checkmark \\
BabyAGI & \checkmark & \checkmark & \text{--} & \checkmark \\
Autogen & \checkmark & \checkmark & \checkmark & \checkmark \\
MetaGPT & \checkmark & \checkmark & \checkmark & \checkmark \\
SuperAGI & \checkmark & \checkmark & \checkmark & \checkmark \\
\bottomrule
\end{tabular}
\end{table}

The analysis reveals that while most frameworks support basic planning and tool use, advanced capabilities like reflection and sophisticated memory management are less consistently implemented \cite{bandi2025rise}.
```

---

## Section 6: Multi-Agent Coordination

### Add Emergence Mechanisms

**Location**: Before the coordination patterns subsection

**Add**:
```latex
\subsection{Mechanisms of Emergence in Multi-Agent Systems}

\citet{miehling2025systems} describe fundamental mechanisms by which advanced capabilities can emerge from simpler agents through system interactions:

\paragraph{Environment-Enhanced Cognition}
Interaction with the environment through multimodal tools enables agents to form generalized representations. When multiple modalities (vision, audio, tactile) provide correlated information about phenomena, agents can detect errors and form abstract representations capturing invariant properties—similar to how human cognition benefits from sensorimotor activity.

\paragraph{Prediction-Enabled Reasoning}
Causal reasoning can emerge through hierarchical predictive processing. As agents construct generative models for predicting sensory inputs and refine predictions through error signals, they develop causal models. The observation and active sampling of environments creates a perception-action loop identifying causal structures without explicit causal reasoning capabilities at the individual agent level.

\paragraph{Interaction-Enabled Metacognition}
Metacognitive awareness can emerge from prediction combined with inter-agent communication. When agents form predictions with associated confidence estimates and communicate these uncertainties, they create shared representations encoding both individual and group-level confidence signals. This enables coordination and intelligent adaptation to environmental changes without individual agents possessing explicit metacognitive capabilities.

These emergence mechanisms suggest that system-level functional agency can exceed the agency of individual components through carefully designed interactions.
```

---

## Section 7: Knowledge Integration (RAG vs Fine-Tuning)

### Add Personalization Insights

**Location**: After discussing hybrid approaches

**Add**:
```latex
\subsection{Personalization Through Agentic AI}

Beyond knowledge integration, agentic AI enables deep personalization by actively learning from user interactions over time \cite{raheem2025agentic}. Unlike traditional recommendation engines that passively suggest content, personalized agentic AI adapts its responses and actions continuously, fostering a sense of interdependence, continuity, and irreplaceability.

For example, in the travel industry, agentic AI can construct fully customized itineraries considering user preferences, real-time conditions, and historical behaviors—not merely making static recommendations but autonomously booking flights, adjusting plans based on weather forecasts, and negotiating with vendors. In healthcare, AI systems tracking patient history and lifestyle can provide highly personalized treatment plans, enhancing both preventive care and chronic disease management.

This shift toward agentic personalization influences human-AI relationships, as systems with long-term memory and adaptive learning create deeper user attachment and trust. Users may perceive AI interactions as relationships rather than mere transactions, particularly as AI becomes integral to daily decision-making—raising important ethical considerations regarding dependency, transparency, and the balance between automation and human control \cite{raheem2025agentic}.
```

---

## Section 8: Production Deployment

### Add Trustworthiness Framework

**Location**: After discussing monitoring and observability

**Add**:
```latex
\subsection{Trustworthiness in Agentic AI Systems}

Trustworthiness represents a critical dimension for successful deployment of agentic AI in consumer-facing applications \cite{raheem2025agentic}. Consumer trust is grounded not only in the competence and accuracy of the AI but also in its safety and comprehensibility. Three key factors determine trustworthiness:

\paragraph{Competence and Safety}
Systems must not only perform accurately but also avoid unsafe or offensive errors. Even legally compliant systems can fail if consumers distrust their capabilities. Developers must ensure systems act consistently with user values and expectations, avoiding misleading outputs or risky behaviors.

\paragraph{Value Alignment and Risk Tolerance}
Agentic AI must align with users' risk tolerances, which becomes especially challenging in competitive markets where firms feel pressure to deploy systems rapidly. Hidden vulnerabilities in rare, high-stakes situations (like security flaws in AI-generated code) can be overlooked in rushes to market, leading to catastrophic failures. Thorough testing, transparent risk communication, and safeguards against overreliance are essential.

\paragraph{Stochasticity Management}
The stochastic nature of AI systems challenges traditional trust concepts. Trustworthiness must extend beyond the AI system itself to the sociotechnical context—developers, regulators, and mechanisms ensuring safe and responsible use. Communicating confidence in competence, conformance to user values, and transparency about potential risks helps maximize trustworthiness and promote responsible usage.

\citet{raheem2025agentic} propose mitigation strategies including adversarial training, runtime guardrails through prompt engineering and RLHF, interpretable AI for decision transparency, sandbox environments, alert monitoring systems, and constitutional AI to guide behavior toward safer trajectories.
```

### Add Evaluation Metrics

**Location**: After the trustworthiness subsection

**Add**:
```latex
\subsection{Comprehensive Evaluation Metrics}

\citet{bandi2025rise} classify evaluation metrics for agentic AI into qualitative and quantitative categories:

\paragraph{Qualitative Metrics}
\begin{itemize}
    \item \textbf{Explainability}: Ability to articulate reasoning processes
    \item \textbf{Transparency}: Clarity about data sources and decision logic
    \item \textbf{User Satisfaction}: Perceived usefulness and ease of interaction
    \item \textbf{Ethical Compliance}: Adherence to fairness, privacy, and accountability standards
\end{itemize}

\paragraph{Quantitative Metrics}
\begin{itemize}
    \item \textbf{Accuracy}: Correctness of outputs and decisions
    \item \textbf{Latency}: Response time for queries and actions
    \item \textbf{Throughput}: Volume of requests processed per unit time
    \item \textbf{Task Completion Rate}: Percentage of successfully completed multi-step tasks
    \item \textbf{Resource Utilization}: Computational and memory efficiency
\end{itemize}

Testing methods should encompass unit testing (individual component verification), integration testing (inter-component interaction validation), and adversarial testing (robustness against adversarial inputs and edge cases) \cite{bandi2025rise}.
```

---

## Section 9: Strategic Considerations

### Add Economic Impact

**Location**: In the technology selection or organizational impact subsection

**Add**:
```latex
\subsection{Economic Productivity and Business Growth}

Agentic AI has significant potential to enhance economic productivity through intelligent automation \cite{raheem2025agentic}. Research indicates that AI-driven automation improves efficiency by streamlining decision-making and optimizing resource utilization. The integration of AI in entrepreneurship, particularly within metaverse environments, has democratized business creation, enabling users to develop and manage digital ventures with ease.

The shift from AI as a passive tool to an autonomous agent challenges traditional human-centric business models. AI systems now handle complex, ambiguous tasks and independently seek optimal outcomes, fostering innovation through stakeholder collaboration, streamlined communication, and enhanced decision-making efficiency. AI also promotes sustainable entrepreneurship by advancing environmentally friendly business practices.

However, this transformation necessitates workforce adaptation. The integration of agentic AI reshapes employment dynamics, requiring continuous upskilling and education \cite{raheem2025agentic}. AI-driven automation augments roles across finance, healthcare, and law, requiring employees to develop AI-related competencies. Strategies including industry-specific training programs, prompt engineering education, and public-private collaborations are essential for bridging skills gaps and ensuring workforce resilience.
```

### Add Application Domains

**Location**: After discussing organizational adoption

**Add**:
```latex
\subsection{Application Domain Taxonomy}

\citet{bandi2025rise} and \citet{acharya2025agentic} provide comprehensive taxonomies of application domains:

\paragraph{Healthcare}
\begin{itemize}
    \item Medical diagnosis and treatment planning
    \item Patient monitoring and chronic disease management
    \item Drug discovery and clinical trial optimization
    \item Personalized medicine and preventive care
\end{itemize}

\paragraph{Finance}
\begin{itemize}
    \item Algorithmic trading and portfolio management
    \item Fraud detection and risk assessment
    \item Credit scoring and loan approval automation
    \item Compliance monitoring and regulatory reporting
\end{itemize}

\paragraph{Manufacturing and Robotics}
\begin{itemize}
    \item Predictive maintenance and quality control
    \item Supply chain optimization and logistics
    \item Autonomous robotic coordination
    \item Process optimization and resource allocation
\end{itemize}

\paragraph{Customer Service}
\begin{itemize}
    \item Intelligent chatbots and virtual assistants
    \item Personalized recommendation systems
    \item Automated scheduling and task management
    \item Multi-turn conversation and context retention
\end{itemize}

\citet{sapkota2026agents} distinguish between applications suited for AI Agents (customer support, scheduling, data summarization) versus Agentic AI (research automation, robotic coordination, medical decision support), highlighting the importance of matching system capabilities to task complexity.
```

---

## Section 10: Ethical Considerations

### Add Comprehensive Ethics Framework

**Location**: After the existing ethical considerations

**Add**:
```latex
\subsection{Extended Ethical Challenges}

Recent work highlights additional ethical dimensions requiring careful consideration \cite{raheem2025agentic,acharya2025agentic}:

\paragraph{Emergent Agency and Oversight}
Emergent agency occurs when behaviors or decision-making capabilities arise that were not explicitly programmed. As systems scale and improve, they may act autonomously in unanticipated ways, creating safety and alignment risks. The lack of proper oversight and regulatory frameworks makes it difficult to ensure systems operate within safe and ethical boundaries \cite{raheem2025agentic}.

\paragraph{Technical Limitations and Predictability}
Despite advances in reinforcement learning and large language models, AI systems often exhibit unpredictable behaviors such as hallucinating incorrect information or failing to reason effectively. Integration challenges with legacy systems designed without considering AI can be expensive and complex. These technical limitations underscore the need for robust testing, validation, and fail-safe mechanisms.

\paragraph{Governance and Regulation}
Current regulatory frameworks often focus on specific AI applications rather than underlying technical capabilities of autonomous systems, creating gaps where systems capable of independent and unpredictable action are deployed without sufficient oversight \cite{raheem2025agentic}. As AI systems grow more complex, establishing governance structures that anticipate and mitigate risks becomes increasingly difficult, leaving society vulnerable to potential harms.

\paragraph{Robustness and Safety}
Agentic AI systems often lack the robustness and safety features necessary for high-stakes environments. They are prone to failures in complex or unpredictable scenarios where decision-making may not align with human goals \cite{raheem2025agentic}. This is particularly concerning in healthcare, transportation, or finance, where errors could have catastrophic consequences. Building in fail-safes and ensuring reliability remains a critical challenge as capabilities expand.
```

### Add Governance Challenges

**Location**: Near the end of ethical considerations

**Add**:
```latex
\subsection{Governing Human-Agent Interactions}

\citet{miehling2025systems} propose that residual control rights—determining decision-making authority in situations not explicitly covered by initial specifications—may offer an effective strategy for mitigating risks in agentic systems. Drawing from contract theory, they suggest natural divisions in control rights:

\paragraph{Agent Control Domain}
Agents should retain control over:
\begin{itemize}
    \item Highly time-constrained local decisions (e.g., evasive maneuvers)
    \item Computationally intensive tasks with clear metrics
    \item Well-defined routine decisions with bounded risk
    \item Decisions relying on information only available at the agent-environment interface
\end{itemize}

\paragraph{Human Control Domain}
Humans should retain control over:
\begin{itemize}
    \item Longer-term strategic decisions
    \item Novel tasks requiring value judgments
    \item Decisions with significant or irreversible safety risks
    \item Situations where agent uncertainty exceeds acceptable thresholds
\end{itemize}

A key challenge is detecting the accumulation of risk from sequences of low-risk automated agent decisions that may create larger emergent risks over time. Escalation mechanisms allowing agents to hand off uncertain decisions to humans must be designed to provide sufficient time for human interpretation and action \cite{miehling2025systems}.
```

---

## Section 11: Conclusion

### Add Future Directions

**Location**: In the future directions subsection

**Add**:
```latex
\subsection{Emerging Challenges and Research Directions}

The rapid advancement of agentic AI opens several critical research directions:

\paragraph{Systems-Level Understanding}
Moving beyond individual model capabilities to understanding emergent behaviors at the system level is essential \cite{miehling2025systems}. Research should focus on mechanisms by which advanced capabilities arise from interactions between agents, humans, and environments. This includes studying how multimodal environmental interaction enhances cognition, how prediction capabilities enable causal reasoning, and how inter-agent communication enables metacognition.

\paragraph{Coordination and Scalability}
As systems scale from single agents to multi-agent orchestration, coordination challenges become paramount \cite{sapkota2026agents,bandi2025rise}. Research is needed on efficient task decomposition, trust-based delegation, handling emergent subgoals, and managing coordination overhead. The A2A (Agent-to-Agent) protocol proposed by Google represents an important step toward standardized interoperability.

\paragraph{Trustworthiness and Safety}
Establishing comprehensive trustworthiness frameworks remains crucial for widespread adoption \cite{raheem2025agentic}. This includes developing robust evaluation metrics, ensuring value alignment, managing stochasticity, implementing effective guardrails, and designing transparent explanation mechanisms. Research should also address the sociotechnical dimensions of trust, extending beyond system capabilities to development practices, regulatory frameworks, and organizational contexts.

\paragraph{Ethical Governance}
Addressing the governance gap between rapid technological advancement and regulatory frameworks requires immediate attention \cite{acharya2025agentic,raheem2025agentic}. This includes developing residual control rights frameworks for human-agent interaction, establishing monitoring mechanisms for emergent agency, creating accountability structures for autonomous decisions, and balancing innovation with safety and societal values.

\paragraph{Architectural Innovation}
Future architectures should emphasize modularity, interoperability, and fail-safe mechanisms \cite{bandi2025rise}. Research should explore hybrid approaches combining LLM-based reasoning with symbolic AI, integration of causal models for more reliable reasoning, development of more sophisticated memory hierarchies, and architectural patterns supporting graceful degradation under uncertainty.
```

---

## Summary of Citation Additions

### New Citations to Add Throughout Paper:

1. **Total new references**: 5 papers
2. **Total new citations needed**: ~25-30 strategically placed citations
3. **Sections most enriched**:
   - Section 2 (Related Work): +4-5 citations
   - Section 3 (Theoretical Foundations): +3-4 citations
   - Section 4 (Architectural Components): +2-3 citations
   - Section 6 (Multi-Agent Coordination): +3-4 citations
   - Section 8 (Production Deployment): +5-6 citations
   - Section 9 (Strategic Considerations): +3-4 citations
   - Section 10 (Ethical Considerations): +4-5 citations

### References Count Update:
- Original: 99 references
- After integration: 104 references

---

## Implementation Notes

1. **LaTeX Compilation**: After adding these sections, run:
   ```bash
   cd arxiv-paper
   make
   ```

2. **Check for Compilation Errors**: The new citations are properly formatted in BibTeX

3. **Verify Page Count**: These additions may increase the paper length by 3-5 pages. Adjust content density as needed.

4. **Cross-Reference Checks**: Ensure all table and figure references are correct (e.g., Table~\ref{tab:framework_comparison})

5. **Balance**: Consider removing or condensing some existing content if page limits are a concern, though the new material significantly enriches the paper.

