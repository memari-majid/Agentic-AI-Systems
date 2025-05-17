# Advanced Agentic AI Systems: Design and Orchestration with LangChain & LangGraph

Welcome to a comprehensive course on designing and orchestrating intelligent agents using the **LangChain** ecosystem, with a focus on **LangGraph** for stateful workflows.

## Why This Course?

Master sophisticated AI agents. This course teaches you to:
- Understand agentic AI principles with **LangChain**.
- Design and implement agent architectures using **LangChain** components.
- Orchestrate complex agentic workflows with **LangGraph**.
- Integrate tools, data, and models via **LangChain**.
- Apply these concepts to build real-world agentic applications.

## Course Structure

Lessons, labs, and appendix materials guide you through **LangChain** and **LangGraph**.

### Part 1: Foundations of AI Agents with LangChain
*Generative AI fundamentals and core **LangChain** agent components.*

1.  **Chapter 01: Intro to Generative AI & Agentic Systems** (Agentic AI in **LangChain**, LLMs, Ethics)
2.  **Chapter 02: Core Components of LangChain Agents** (Perception, Memory, Reasoning with **LCEL**, Action)
3.  **Chapter 03: Mastering LangChain & Intro to LangGraph** (**LangChain** deep dive, **LCEL**, first **LangGraph** workflows)

### Part 2: Designing Advanced Agents with LangGraph
*Advanced agent design, reflection, tool use, multi-agent systems, and state management with **LangGraph**.*

4.  **Chapter 04: Reflection and Introspection in LangGraph Agents** (Self-correction, Metacognitive Loops with **LangGraph**)
5.  **Chapter 05: Tool Use & Planning with LangChain & LangGraph** (External tools via **LangChain**, ReAct with **LangGraph**)
6.  **Chapter 06: Multi-Agent Systems with LangGraph** (Architectures, Communication, Collaboration with **LangGraph**)
7.  **Chapter 07: Advanced Agentic Design with LangGraph** (State, Memory, Checkpointing, Resilience in **LangGraph**)

### Part 3: Evaluation, Safety, and Applications of LangChain Agents
*Trustworthy AI, safety, evaluation with **LangSmith** & **DSPy**, and real-world applications.*

8.  **Chapter 08: Trustworthy and Explainable LangChain Agents** (XAI with **LangSmith**, Human Values)
9.  **Chapter 09: Safety and Ethical Behavior in LangChain Systems** (Risks, Guardrails, Bias, Governance)
10. **Chapter 10: Evaluation & Optimization with LangSmith & DSPy** (Metrics, Tracing with **LangSmith**, Prompts with **DSPy**)
11. **Chapter 11: Real-World Applications & Future of LangChain Agents** (Case Studies, Emerging Trends)

## Labs: Hands-On Agentic AI

The `Labs` directory offers practical exercises using **LangChain** and **LangGraph**, covering concepts like conversational agents, stateful booking systems, reflection loops, multi-agent collaboration, and tool integration. See `Labs/README.md` for detailed lab descriptions and instructions.

## Appendix: Deep Dive Tutorials

The `Appendix` provides in-depth tutorials:

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

-   **LangChain** (Core, Community, Integrations)
-   **LangGraph**
-   **LangSmith**
-   **DSPy**: For algorithmic optimization of LM prompts and weights.
-   LLM SDKs (OpenAI, Anthropic, Vertex AI, etc.)
-   Standard data science libraries (Pandas, NumPy, etc.)

Refer to `requirements.txt` for a full list.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This material is provided under the [MIT License](LICENSE.txt) (assuming one will be added).

---

Enjoy building next-generation AI with **LangChain** and **LangGraph**!



