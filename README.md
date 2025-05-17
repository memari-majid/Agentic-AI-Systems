# Mastering Agentic AI
![Mastering Agentic AI Banner](./image.png)

Welcome to a comprehensive course on designing, orchestrating, and applying advanced agentic AI systems. This course explores core principles and practical implementation using key technologies like **LangChain** for building agent components and **LangGraph** for orchestrating stateful workflows.

## Why This Course?

Master the design and implementation of sophisticated AI agents. This course teaches you to:
- Understand core principles of agentic AI.
- Design robust agent architectures and implement them using foundational libraries like **LangChain**.
- Orchestrate complex, multi-step agentic workflows, leveraging tools like **LangGraph** for state management and control flow.
- Integrate diverse tools, data sources, and models into your agents.
- Apply these concepts to build and deploy real-world agentic applications.

## Course Structure

Lessons, labs, and appendix materials guide your learning journey in agentic AI design.

### Part 1: Foundations of Agentic AI
*Generative AI fundamentals and core agent components, with a focus on **LangChain** for implementation.*

1.  **Chapter 01: Intro to Generative AI & Agentic Systems** (Agentic AI Principles, LLMs, Ethics)
2.  **Chapter 02: Core Components of LangChain Agents** (Perception, Memory, Reasoning with **LCEL**, Action using **LangChain**)
3.  **Chapter 03: Mastering LangChain & Intro to LangGraph** (Advanced **LangChain** techniques, **LCEL**, first steps with **LangGraph** for stateful agent orchestration)

### Part 2: Advanced Agent Design and Orchestration
*Advanced agent design patterns, including reflection, tool use, multi-agent systems, and resilient state management, primarily demonstrated using **LangGraph**.*

4.  **Chapter 04: Reflection and Introspection in Agents** (Self-correction, Metacognitive Loops with **LangGraph**)
5.  **Chapter 05: Enabling Tool Use & Sophisticated Planning** (Integrating external tools via **LangChain**, advanced planning like ReAct with **LangGraph**)
6.  **Chapter 06: Multi-Agent Systems** (Architectures, Communication, Collaboration, implemented with **LangGraph**)
7.  **Chapter 07: Advanced Agentic Design: State & Resilience** (Sophisticated state management, checkpointing, and error handling in **LangGraph**)

### Part 3: Evaluating, Securing, and Applying Agentic AI Systems
*Ensuring trustworthy and safe AI, evaluation techniques (e.g., with **LangSmith** and **DSPy**), and exploring real-world applications of agentic systems.*

8.  **Chapter 08: Building Trustworthy and Explainable Agents** (XAI for agents, tracing with **LangSmith**, aligning with human values)
9.  **Chapter 09: Ensuring Safety and Ethical Behavior** (Identifying risks, guardrails, addressing bias, fairness, privacy)
10. **Chapter 10: Evaluation & Optimization of Agentic Systems** (Metrics, debugging with **LangSmith**, prompt/pipeline optimization with **DSPy**)
11. **Chapter 11: Real-World Applications & Future of Agentic AI** (Case studies, emerging trends in agentic systems)

## Labs: Hands-On Agentic AI

The `Labs` directory offers practical exercises to solidify your understanding of agentic AI concepts, implemented primarily using **LangChain** and **LangGraph**. Topics include conversational agents, stateful workflows, reflection, multi-agent systems, and tool integration. See `Labs/README.md` for detailed lab descriptions.

## Appendix: Deep Dive Tutorials

The `Appendix` provides in-depth tutorials on key technologies:

-   **[Agentic AI Design with LangChain and LangGraph](Appendix/Agentic_AI_Design_Tutorial.md)**: A comprehensive guide on using LangChain and LangGraph together to build sophisticated, stateful AI agents.
-   **[Introduction to DSPy: Programming over Prompting](Appendix/DSPy_Introduction.md)**: An overview of DSPy for optimizing LM-driven pipelines.

*(See `Appendix/README.md` for its own table of contents.)*

## Getting Started

1.  **Clone Repository**: `git clone https://github.com/memari-majid/Agentic-AI-Systems.git`
2.  **Navigate**: `cd Agentic-AI-Systems`
3.  **Install Dependencies** (Python 3.9+): `pip install -r requirements.txt`
4.  **Set API Keys**: Create a `.env` file in the root for API keys (OpenAI, Anthropic, **LangSmith**, etc.).
    ```env
    OPENAI_API_KEY="your_openai_api_key"
    ANTHROPIC_API_KEY="your_anthropic_api_key"
    TAVILY_API_KEY="your_tavily_api_key"
    LANGCHAIN_API_KEY="your_langsmith_api_key"
    LANGCHAIN_TRACING_V2="true"
    LANGCHAIN_PROJECT="AdvancedAgenticAI"
    ```
    **Important**: Add `.env` to your `.gitignore`.
5.  **Explore Lessons**: Start with `Lessons/Chapter01`.
6.  **Run Labs**: E.g., `python Labs/01_hello_graph.py`.

## Prerequisites

-   Solid Python skills.
-   Familiarity with Machine Learning fundamentals.
-   Basic NLP knowledge is helpful.
-   Access to LLM provider APIs (e.g., OpenAI).

## Core Technologies

This course utilizes several key technologies to teach and implement agentic AI designs:
-   **LangChain** (Core, Community, Integrations): For building agent components and foundational application structures.
-   **LangGraph**: For orchestrating complex, stateful agentic workflows.
-   **LangSmith**: For debugging, tracing, monitoring, and evaluating agent performance.
-   **DSPy**: For algorithmic optimization of LM prompts and weights within agent pipelines.
-   LLM SDKs (OpenAI, Anthropic, Vertex AI, etc.): For direct interaction with language models.
-   Standard data science libraries (Pandas, NumPy, etc.): For supporting tasks.

Refer to `requirements.txt` for a full list.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This material is provided under the [MIT License](LICENSE.txt) (assuming one will be added).

---

Enjoy your journey into building the next generation of agentic AI systems!



