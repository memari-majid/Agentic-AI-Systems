# Introduction to Agentic AI Systems

[![Course Website](https://img.shields.io/badge/View%20Course%20Website-online-blue)](https://memari-majid.github.io/Agentic-AI-Systems/)

**Course Website:** [https://memari-majid.github.io/Agentic-AI-Systems/](https://memari-majid.github.io/Agentic-AI-Systems/)

This course provides a rigorous exploration of the theoretical underpinnings and practical applications of advanced agentic AI systems. It emphasizes core design principles, system orchestration, and the deployment of intelligent agents using contemporary software frameworks and methodologies.

## Course Objectives

Upon successful completion of this course, learners will be equipped to:
- Articulate the fundamental principles and cognitive architectures underpinning agentic artificial intelligence.
- Design and implement robust, sophisticated agent systems capable of complex reasoning, planning, and action execution.
- Develop and apply methodologies for orchestrating multi-step agentic behaviors and managing stateful interactions effectively.
- Integrate diverse external capabilities, including knowledge bases and specialized computational tools, within agentic frameworks.
- Critically analyze, construct, and evaluate agentic AI systems for real-world applications, considering ethical and performance implications.

## Prerequisites

Successful participation in this course assumes:
-   Proficiency in Python programming.
-   A solid understanding of fundamental Machine Learning concepts.
-   Basic familiarity with Natural Language Processing (NLP).
-   Access to and foundational knowledge of Large Language Model (LLM) APIs.

## Core Technologies Utilized

This course leverages several key software frameworks and libraries to illustrate and implement advanced concepts in agentic AI design:
-   **LangChain**: For the construction of agent components and foundational application logic.
-   **LangGraph**: For the orchestration of complex, stateful agentic interactions and workflows.
-   **LangSmith**: For tracing, debugging, and comprehensive evaluation of agent performance.
-   **DSPy**: For the systematic optimization of language model operations within agentic pipelines.
-   LLM SDKs (OpenAI, Anthropic, Vertex AI, etc.): For direct interfacing with various large language models.
-   Standard Python data science libraries: For auxiliary data manipulation and analysis tasks.

(A comprehensive list of dependencies is available in `requirements.txt`.)

## Getting Started

1.  **Clone Repository**: `git clone https://github.com/memari-majid/Agentic-AI-Systems.git`
2.  **Navigate**: `cd Agentic-AI-Systems`
3.  **Install Dependencies** (Python 3.9+ recommended): `pip install -r requirements.txt`
4.  **Configure API Keys**: Create a `.env` file in the project root for necessary API credentials (e.g., LLM providers, specific tools, tracing services).
    ```env
    OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
    ANTHROPIC_API_KEY="YOUR_ANTHROPIC_API_KEY"
    TAVILY_API_KEY="YOUR_TAVILY_API_KEY"
    LANGCHAIN_API_KEY="YOUR_LANGSMITH_API_KEY" # For LangSmith
    LANGCHAIN_TRACING_V2="true"
    LANGCHAIN_PROJECT="AdvancedAgenticAI" # Example project name for LangSmith
    ```
    **Note**: Ensure `.env` is added to your `.gitignore` to prevent accidental commits of sensitive information.
5.  **Begin with Lessons**: It is recommended to start with `Lessons/Chapter01`.
6.  **Engage with Lab Exercises**: E.g., `python Labs/01_hello_graph.py`.

## Course Structure

The curriculum is structured into thematic parts, each comprising detailed lessons, practical laboratory exercises, and supplementary appendix materials to foster a comprehensive understanding of agentic AI system design.

### Part 1: Foundations of Agentic Intelligence
*Delving into the core concepts of generative AI and the essential building blocks of intelligent agent systems.*

1.  **[Chapter 01: Paradigms of Generative AI & Agentic Systems](Lessons/Chapter01)**
    -   [Fundamentals of Generative AI](Lessons/Chapter01/1%20Fundamentals%20of%20Generative%20AI.md) (Agentic Principles, Foundational Models, Ethical Frameworks)
2.  **[Chapter 02: Fundamental Components of Agent Architectures](Lessons/Chapter02)**
    -   [Principles of Agentic Systems](Lessons/Chapter02/2%20Principles%20of%20Agentic%20Systems.md) (Perception Mechanisms, Memory Models, Reasoning Paradigms, Action Formulation Strategies)
3.  **[Chapter 03: Frameworks for Agent Development & Orchestration](Lessons/Chapter03)**
    -   [Essential Components of Intelligent Agents](Lessons/Chapter03/3%20Essential%20Components%20of%20Intelligent%20Agents.md) (Component-Based Development, Introduction to Graph-Based State Management)

### Part 2: Advanced Agent Design and Orchestration Strategies
*Investigating sophisticated design patterns, including reflective cognition, tool augmentation, multi-agent collaboration, and resilient state management.*

4.  **[Chapter 04: Reflection and Introspection in Agent Cognition](Lessons/Chapter04)**
    -   [Reflection and Introspection in Agents](Lessons/Chapter04/4%20Reflection%20and%20Introspection%20in%20Agents.md) (Self-Correction Mechanisms, Metacognitive Control Loops)
5.  **[Chapter 05: Tool Augmentation & Deliberative Planning in Agents](Lessons/Chapter05)**
    -   [Enabling Tool Use and Planning in Agents](Lessons/Chapter05/5%20Enabling%20Tool%20Use%20and%20Planning%20in%20Agents.md) (External Utility Integration, Advanced Planning Algorithms)
6.  **[Chapter 06: Principles of Multi-Agent Systems](Lessons/Chapter06)**
    -   [Exploring the Coordinator, Worker, and Delegator Approach](Lessons/Chapter06/6%20Exploring%20the%20Coordinator%2C%20Worker%2C%20and%20Delegator%20Approach.md) (Distributed Architectures, Inter-Agent Communication, Collaborative Problem Solving)
7.  **[Chapter 07: Advanced Methodologies for State Persistence & System Resilience](Lessons/Chapter07)**
    -   [Effective Agentic System Design Techniques](Lessons/Chapter07/7%20Effective%20Agentic%20System%20Design%20Techniques.md) (State Management Protocols, Checkpointing for Robustness, Fault Tolerance Strategies)

### Part 3: Evaluation, Security, and Application of Agentic Systems
*Addressing the creation of trustworthy and secure AI, robust evaluation methodologies, and the deployment of agentic systems across diverse domains.*

8.  **[Chapter 08: Constructing Trustworthy and Explainable Agentic Systems](Lessons/Chapter08)**
    -   [Building Trust in Generative AI Systems](Lessons/Chapter08/8%20Building%20Trust%20in%20Generative%20AI%20Systems.md) (Explainable AI (XAI) for Agents, Value Alignment, System Transparency)
9.  **[Chapter 09: Ensuring Safety and Ethical Conduct in AI Systems](Lessons/Chapter09)**
    -   [Managing Safety and Ethical Considerations](Lessons/Chapter09/9%20Managing%20Safety%20and%20Ethical%20Considerations.md) (Risk Assessment, Safeguard Implementation, Bias Mitigation)
10. **[Chapter 10: Common Use Cases and Applications of Agentic AI](Lessons/Chapter10)**
    -   [Common Use Cases and Applications](Lessons/Chapter10/10%20Common%20Use%20Cases%20and%20Applications.md) (Domain-Specific Implementations, Performance Benchmarking)
11. **[Chapter 11: Conclusion and Future Outlook for Agentic AI](Lessons/Chapter11)**
    -   [Conclusion and Future Outlook](Lessons/Chapter11/11%20Conclusion%20and%20Future%20Outlook.md) (Current Limitations, Emerging Research Frontiers, Societal Impact)

## Lab Exercises: Practical Application of Agentic AI

The `Labs` directory provides hands-on exercises for applying theoretical concepts to the design and implementation of agentic AI systems. These labs facilitate exploration of conversational intelligence, stateful interaction management, reflective processing, multi-agent dynamics, and tool-augmented reasoning, often utilizing frameworks such as **LangChain** and **LangGraph** for practical illustration. Detailed instructions for each lab are available in [Labs/README.md](Labs/README.md).

## Appendix: Supplementary Materials

The `Appendix` offers in-depth guides and tutorials on specific technologies and advanced concepts relevant to agentic AI:

-   **[Agentic AI Design with LangChain and LangGraph](Agentic_AI_in_Action/Agentic_AI_Design_Tutorial.md)**: A comprehensive tutorial on leveraging specific frameworks for building sophisticated AI agents.
-   **[Introduction to DSPy: Programming over Prompting](Agentic_AI_in_Action/DSPy_Introduction.md)**: An overview of a programmatic approach to optimizing LM-driven pipelines.
-   **[Leveraging Cloud Services for Agentic AI Systems](Agentic_AI_in_Action/Cloud_Agentic_AI_Services_Tutorial.md)**: A guide to utilizing cloud platforms (AWS, Azure, GCP) for deploying and scaling agentic AI.

*(Refer to `Appendix/README.md` for a detailed table of contents for all supplementary materials.)*

## About the Author

This course is developed by **Majid Memari**, an AI researcher, educator, and solution architect dedicated to advancing the design and application of high-impact AI systems.

**Key AI-Related Background:**

-   **Academic Credentials:** Ph.D. and M.S. in Computer Science from Southern Illinois University Carbondale.
-   **Professional Expertise:** Extensive experience since 2015 in the end-to-end development of production-grade AI systems, with a specialization in Large Language Models (LLMs), Deep Learning, and Computer Vision.
-   **Educational Leadership:** As an Assistant Professor at Utah Valley University, Dr. Memari develops and teaches advanced, project-based AI courses focusing on Machine Learning, Artificial Intelligence, Computer Vision, and the strategic applications of Generative AI and LLMs.
-   **Research Contributions:** A strong record of leading and contributing to funded AI research initiatives, including the application of machine learning for predictive maintenance, autonomous systems safety, and the creation of LLM-based educational tools.
-   **Industry Engagement:** Experience includes AI consulting for the legal-tech industry, focusing on AI strategy, system architecture, and ethical deployment, alongside data science roles applying predictive analytics and NLP to large-scale datasets in sectors such as healthcare.

Dr. Memari combines academic rigor with practical industry insights to foster innovation in real-world AI applications.

## Textbooks

For learners seeking to further deepen their understanding of agentic AI systems and related technologies, the following textbooks are recommended as supplementary resources:

-   **AI Agents in Action**
    -   By: Micheal Lanham
    -   Publisher: Manning Publications
    -   Publication Date: February 2025
    -   [View on O'Reilly Learning](https://learning.oreilly.com/library/view/ai-agents-in/9781633436343/)

-   **Building Applications with AI Agents**
    -   By: Michael Albada
    -   Publisher: O'Reilly Media, Inc.
    -   Publication Date: October 2025
    -   [View on O'Reilly Learning](https://learning.oreilly.com/library/view/building-applications-with/9781098176495/)

-   **Building Agentic AI Systems**
    -   By: Anjanava Biswas, Wrick Talukdar
    -   Publisher: Packt Publishing
    -   Publication Date: April 2025
    -   [View on O'Reilly Learning](https://learning.oreilly.com/library/view/building-agentic-ai/9781803238753/)

## Contributing

Contributions aimed at enhancing this educational resource are highly valued. Please utilize GitHub issues for suggestions or bug reports, and pull requests for proposed improvements or corrections.

## License

This course material is provided under the [MIT License](LICENSE.txt).

---

We trust this course will prove to be an enriching and insightful experience in your exploration of agentic artificial intelligence.
