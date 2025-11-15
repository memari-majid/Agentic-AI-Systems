# LangChain: The Foundation for Agents

⏱️ **Estimated reading time: 11 minutes**

LangChain helps create the core components that an agent will use. Think of these as the agent's skills or tools.

### 2.1. Core Idea: Building with Components

LangChain is designed around modular components that can be combined to create powerful applications. For agentic systems, the key components are:

### 2.2. Models

Language models are the brain of an agent. LangChain provides interfaces for various types:
- **LLMs (Large Language Models):** Take text in, return text out.
- **Chat Models:** More structured, take a list of messages, return a message. These are commonly used for agents.
- **Text Embedding Models:** Convert text to numerical representations for semantic search.

```python
from langchain_openai import OpenAI, ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings

# Initialize a Chat Model (commonly used for agents)
chat_model = ChatOpenAI(model="gpt-4", temperature=0)

# Example of an LLM
llm = OpenAI(temperature=0.7)

# Example of an Embedding Model
embeddings = HuggingFaceEmbeddings()
```

### 2.3. Prompts

Prompts are how we instruct the model. For agents, prompts often define the agent's persona, its objectives, and how it should use tools.

```python
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

# Chat prompt template for an agent
agent_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. You have access to tools. Use them when necessary."),
    ("user", "{input}")
])

# Example of a simpler prompt
prompt_template = PromptTemplate.from_template("Tell me about {topic}.")
```

### 2.4. Tools: Enabling Agents to Act

Tools are interfaces that allow agents to interact with the outside world (e.g., search the web, run code, access databases). LangChain makes it easy to define and use tools.

The `@tool` decorator is a convenient way to create tools from functions:

```python
from langchain_core.tools import tool

@tool
def search_wikipedia(query: str) -> str:
    """Searches Wikipedia for the given query and returns the summary of the first result."""
    # In a real scenario, you would use the Wikipedia API
    # from wikipediaapi import Wikipedia
    # wiki_wiki = Wikipedia('MyAgent/1.0 (myemail@example.com)', 'en')
    # page = wiki_wiki.page(query)
    # if page.exists():
    #     return page.summary[0:500] # Return first 500 chars of summary
    # return f"Could not find information on Wikipedia for '{query}'."
    return f"Simulated Wikipedia search for '{query}': LangChain is a framework for developing applications powered by language models."

@tool
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {str(e)}"

# List of tools for an agent
agent_tools = [search_wikipedia, calculator]
```

### 2.5. Output Parsers

Output parsers convert the raw output from an LLM into a more structured format (e.g., JSON, a specific object). This is crucial for agents to reliably extract information or decide on actions.

```python
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

# Simple string output
string_parser = StrOutputParser()

# For structured output (e.g., an agent deciding which tool to call)
class AgentAction(BaseModel):
    tool_name: str = Field(description="The name of the tool to use.")
    tool_input: str = Field(description="The input for the tool.")

json_parser = JsonOutputParser(pydantic_object=AgentAction)
```
While `JsonOutputParser` can be used, agents created with functions like `create_openai_tools_agent` often handle tool invocation structures internally.

### 2.6. Memory (Brief Overview)

Memory allows agents to remember past interactions. While LangChain offers various memory modules, LangGraph's state management provides a more explicit and flexible way to handle memory and state for complex agents, as we'll see later.

LangChain memory types include:
- `ConversationBufferMemory`: Remembers all past messages.
- `ConversationBufferWindowMemory`: Remembers the last K messages.
- `ConversationSummaryMemory`: Creates a summary of the conversation.

We will primarily use LangGraph's state for managing memory in our agentic designs.

### 2.7. Basic Agent Construction with LangChain

LangChain provides functions to quickly create agents. `create_openai_tools_agent` (and similar functions for other model providers) are recommended for building agents that can use tools. These agents are designed to work with models that support tool calling (like newer OpenAI models).

```python
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Re-define tools if not in scope
# @tool
# def search_wikipedia(query: str) -> str: ...
# @tool
# def calculator(expression: str) -> str: ...
# agent_tools = [search_wikipedia, calculator]

# Initialize the Chat Model
llm = ChatOpenAI(model="gpt-4", temperature=0) # Using a specific model known for good tool use

# Define the prompt for the agent
# This prompt template expects 'input' and 'agent_scratchpad' (for intermediate steps)
# and also includes messages for chat history if needed.
# For tool calling agents, the prompt structure can be simpler as the model handles much of the reasoning.
AGENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. You have access to the following tools: search_wikipedia, calculator. Only use these tools when necessary to answer the user's question. Respond directly if you know the answer or the tools are not helpful."),
    ("user", "{input}"),
    # MessagesPlaceholder(variable_name="agent_scratchpad"), # create_openai_tools_agent handles this
])

# Create the agent
# This binds the LLM, tools, and prompt together.
# The agent runnable itself decides which tool to call, or to respond directly.
agent_runnable = create_openai_tools_agent(llm, agent_tools, AGENT_PROMPT)

# The AgentExecutor runs the agent, executes tools, and feeds results back to the agent
# until a final answer is produced.
agent_executor = AgentExecutor(agent=agent_runnable, tools=agent_tools, verbose=True)

# Example usage
# response = agent_executor.invoke({"input": "What is the capital of France and what is 2 + 2?"})
# print(response["output"])

# response_wikipedia = agent_executor.invoke({"input": "What is LangChain?"})
# print(response["output"])
```

While this `AgentExecutor` is powerful, managing more complex sequences of actions, conditional logic based on multi-step history, explicit state tracking beyond chat history, or incorporating human feedback loops can become challenging. This is where LangGraph provides a more robust framework for orchestration.

Next, we will explore LangGraph and how it allows us to build more sophisticated agentic workflows. 