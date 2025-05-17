# LangChain Tutorial: Building Agentic AI Systems

## Introduction

LangChain is a framework designed for developing applications powered by language models. It enables the creation of agentic AI systems that can interact with their environment through chains and agents.

## Table of Contents

1. [Installation](#installation)
2. [Key Concepts](#key-concepts)
3. [Basic Usage](#basic-usage)
4. [LangChain Expression Language (LCEL)](#langchain-expression-language)
5. [Building Agents](#building-agents)
6. [Tools and Tool Calling](#tools-and-tool-calling)
7. [Memory Systems](#memory-systems)
8. [Document Loaders](#document-loaders)
9. [Vector Stores](#vector-stores)
10. [Output Parsing](#output-parsing)
11. [Retrieval Systems](#retrieval-systems)
12. [Evaluation](#evaluation)
13. [Advanced Applications](#advanced-applications)
14. [LangSmith for Debugging](#langsmith-for-debugging)

## Installation

### Using pip

```bash
pip install langchain
```

### Using conda

```bash
conda install langchain -c conda-forge
```

For specific integrations, you'll need additional packages:

```bash
# For OpenAI models
pip install langchain-openai

# For document loading functionality
pip install langchain-community

# For full document processing capabilities
pip install "unstructured[md]" nltk

# For vector databases
pip install langchain-chroma
```

## Key Concepts

### Models

LangChain provides interfaces and integrations for various types of models:

- **LLMs**: Models that take a text string and return a text string
- **Chat Models**: Models that take a list of messages and return a message
- **Text Embedding Models**: Models that convert text to numerical embeddings

```python
from langchain_openai import OpenAI, ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain_google_vertexai import VertexAI

# Initialize an LLM
llm = OpenAI(temperature=0.7)

# Initialize a Chat Model
chat_model = ChatOpenAI(temperature=0)

# Initialize alternative models
anthropic = ChatAnthropic(model="claude-3-sonnet-20240229")
palm = VertexAI(model="text-bison")

# Initialize Embeddings
embeddings = HuggingFaceEmbeddings()
```

### Prompts

LangChain provides tools for managing and optimizing prompts:

```python
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, FewShotPromptTemplate

# Basic prompt template
prompt = PromptTemplate.from_template("Tell me about {topic}")
formatted_prompt = prompt.format(topic="LangChain")

# Chat prompt template
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    ("user", "Tell me about {topic}")
])

# Few-shot learning prompt
examples = [
    {"input": "What is the capital of France?", "output": "The capital of France is Paris."},
    {"input": "What is the capital of Japan?", "output": "The capital of Japan is Tokyo."}
]

example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="User: {input}\nAI: {output}"
)

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="Answer the user's questions based on these examples:",
    suffix="User: {input}\nAI:",
    input_variables=["input"]
)

formatted_few_shot = few_shot_prompt.format(input="What is the capital of Germany?")
```

## Basic Usage

Here's a simple example of using LangChain to create a basic chain:

```python
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain

# Initialize components
llm = OpenAI(temperature=0.7)
prompt = PromptTemplate.from_template("Write a short poem about {topic}")

# Create a chain
chain = prompt | llm | StrOutputParser()

# Run the chain
result = chain.invoke({"topic": "artificial intelligence"})
print(result)
```

## LangChain Expression Language

LCEL is a declarative way to compose chains using the Runnable protocol:

```python
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Define components
llm = OpenAI(temperature=0.7)
prompt = PromptTemplate.from_template("Write a joke about {topic}")

# Compose with LCEL
chain = prompt | llm | StrOutputParser()

# Run the chain
response = chain.invoke({"topic": "programming"})
print(response)
```

### Advanced LCEL: Branching and Merging

```python
from langchain_core.runnables import RunnableBranch, RunnablePassthrough

def determine_topic_complexity(input_dict):
    topic = input_dict.get("topic", "")
    if len(topic) > 10:
        return "complex"
    return "simple"

# Different chains for different complexity levels
simple_chain = (
    PromptTemplate.from_template("Write a simple explanation about {topic}") 
    | llm 
    | StrOutputParser()
)

complex_chain = (
    PromptTemplate.from_template("Write a detailed technical explanation about {topic}") 
    | llm 
    | StrOutputParser()
)

# Branch based on complexity
chain = RunnableBranch(
    (lambda x: determine_topic_complexity(x) == "simple", simple_chain),
    (lambda x: determine_topic_complexity(x) == "complex", complex_chain),
)

# Run with routing
response = chain.invoke({"topic": "quantum computing"})
```

### LCEL with Error Handling

```python
from langchain_core.runnables import RunnablePassthrough
import traceback

# Define a fallback chain
fallback_chain = PromptTemplate.from_template(
    "Unable to process the request about {topic}. Please try again later."
) | StrOutputParser()

# Main chain with error handling
def process_with_error_handling(runnable):
    def _handle_errors(inputs):
        try:
            return {"result": runnable.invoke(inputs), "error": None}
        except Exception as e:
            return {"result": None, "error": str(e) + "\n" + traceback.format_exc()}
    
    return RunnablePassthrough() | _handle_errors

main_chain = process_with_error_handling(
    PromptTemplate.from_template("Generate information about {topic}") | llm | StrOutputParser()
)

# Combine with final logic
def route_based_on_error(inputs):
    if inputs["error"] is not None:
        print(f"Error occurred: {inputs['error']}")
        return fallback_chain.invoke({"topic": inputs.get("topic", "unknown")})
    return inputs["result"]

complete_chain = main_chain | route_based_on_error
```

## Output Parsing

LangChain provides several ways to parse the output of language models:

### Structured Output with Pydantic

```python
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Define your data structure
class Person(BaseModel):
    name: str = Field(description="The person's name")
    age: int = Field(description="The person's age")
    hobbies: list[str] = Field(description="The person's hobbies")

# Set up the parser
parser = JsonOutputParser(pydantic_object=Person)

# Create the prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "Generate information about a fictional person. {format_instructions}"),
    ("user", "Create a profile for someone interested in {interest}")
])

# Create the chain
chain = prompt.partial(format_instructions=parser.get_format_instructions()) | ChatOpenAI(model="gpt-4") | parser

# Run the chain
person = chain.invoke({"interest": "artificial intelligence"})
print(f"Name: {person.name}, Age: {person.age}")
print(f"Hobbies: {', '.join(person.hobbies)}")
```

### List and Comma-Separated Parsers

```python
from langchain_core.output_parsers import CommaSeparatedListOutputParser, ListOutputParser

# Comma-separated parser
comma_parser = CommaSeparatedListOutputParser()
comma_prompt = PromptTemplate(
    template="List five fruits, comma-separated:\n\n",
    output_parser=comma_parser
)
comma_chain = comma_prompt | llm | comma_parser
fruits = comma_chain.invoke({})
print(fruits)  # ['apple', 'banana', 'orange', 'strawberry', 'grape']

# List parser (expects items on separate lines)
list_parser = ListOutputParser()
list_prompt = PromptTemplate(
    template="List three programming languages, one per line:\n\n",
    output_parser=list_parser
)
list_chain = list_prompt | llm | list_parser
languages = list_chain.invoke({})
print(languages)  # ['Python', 'JavaScript', 'Rust']
```

## Building Agents

Agents use LLMs to determine which actions to take:

```python
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults

# Define tools
tools = [TavilySearchResults(max_results=3)]

# Create prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use the provided tools to answer user questions."),
    ("user", "{input}")
])

# Create model and agent
llm = ChatOpenAI(model="gpt-4")
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Run the agent
agent_executor.invoke({"input": "What's the latest news about SpaceX?"})
```

### Different Agent Types

```python
from langchain.agents import create_react_agent, create_structured_chat_agent, create_json_chat_agent
from langchain_core.tools import Tool
from langchain_community.utilities import SerpAPIWrapper

# Add several tools
search = SerpAPIWrapper()
search_tool = Tool(
    name="Search",
    func=search.run,
    description="Useful for searching the internet for current information."
)

tools = [calculator_tool, search_tool]

# ReAct Agent
react_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an agent that uses tools to answer questions. Use ReAct thinking."),
    ("user", "{input}")
])
react_agent = create_react_agent(llm, tools, react_prompt)
react_executor = AgentExecutor(agent=react_agent, tools=tools, verbose=True)

# Structured Chat Agent
structured_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an agent that uses tools to answer questions."),
    ("user", "{input}")
])
structured_agent = create_structured_chat_agent(llm, tools, structured_prompt)
structured_executor = AgentExecutor(agent=structured_agent, tools=tools, verbose=True)
```

## Tools and Tool Calling

Tools allow models to interact with external systems:

```python
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain_openai import OpenAI

# Define a simple calculator tool
def calculator(expression):
    """Evaluates a mathematical expression."""
    try:
        return eval(expression)
    except:
        return "Error: Could not evaluate expression."

# Create a tool
calculator_tool = Tool(
    name="Calculator",
    func=calculator,
    description="Useful for performing mathematical calculations."
)

# Initialize the agent with tools
llm = OpenAI(temperature=0)
agent = initialize_agent(
    [calculator_tool], 
    llm, 
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

# Run the agent
agent.run("What is (8 * 7) + 15?")
```

### Creating Custom Tools

```python
from langchain.tools import BaseTool
from typing import Optional, Type
from langchain_core.pydantic_v1 import BaseModel

# Define the input schema
class WeatherInput(BaseModel):
    location: str = Field(description="The city and state, e.g. San Francisco, CA")

# Create a custom tool class
class WeatherTool(BaseTool):
    name = "weather"
    description = "Get the current weather in a given location"
    args_schema: Type[BaseModel] = WeatherInput
    
    def _run(self, location: str) -> str:
        """Get the weather in a location"""
        # In a real implementation, you'd call a weather API here
        return f"The current weather in {location} is 72°F and sunny."
        
    async def _arun(self, location: str) -> str:
        """Async implementation of the weather tool"""
        # For async, you'd use an async API call
        return self._run(location)

# Initialize the tool
weather_tool = WeatherTool()

# Add to an agent
tools = [calculator_tool, weather_tool]
weather_agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

# Use the agent
weather_agent.run("What's the weather like in Boston, MA?")
```

## Memory Systems

LangChain provides various memory systems to maintain conversation history:

```python
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Initialize conversation with memory
llm = ChatOpenAI(temperature=0.7)
memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm=llm, 
    memory=memory,
    verbose=True
)

# First interaction
conversation.predict(input="Hi, my name is Alice")

# Follow-up that uses memory
conversation.predict(input="What's my name?")
```

### Different Types of Memory

```python
from langchain.memory import (
    ConversationBufferMemory, 
    ConversationBufferWindowMemory,
    ConversationSummaryMemory, 
    ConversationSummaryBufferMemory
)

# Buffer Window Memory (keeps last K turns)
window_memory = ConversationBufferWindowMemory(k=2)
conversation_window = ConversationChain(
    llm=llm,
    memory=window_memory,
    verbose=True
)

# Summary Memory (stores a summary rather than full history)
summary_memory = ConversationSummaryMemory(llm=llm)
conversation_summary = ConversationChain(
    llm=llm,
    memory=summary_memory,
    verbose=True
)

# Summary Buffer Memory (keeps summary plus last K exchanges)
summary_buffer = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=100
)
conversation_summary_buffer = ConversationChain(
    llm=llm,
    memory=summary_buffer,
    verbose=True
)
```

### LCEL with Memory

```python
from langchain_core.runnables import RunnablePassthrough
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import AIMessage, HumanMessage

# Define the chat chain
def get_chat_chain(llm):
    return ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("history", "{history}"),
        ("user", "{input}")
    ]) | llm | StrOutputParser()

# Create the chain
chat_chain = get_chat_chain(ChatOpenAI())

# Setup with message history
message_history = {}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in message_history:
        message_history[session_id] = ChatMessageHistory()
    return message_history[session_id]

chain_with_history = RunnableWithMessageHistory(
    chat_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# Use the chain
session_id = "user_123"
chain_with_history.invoke(
    {"input": "Hello, my name is Bob"},
    config={"configurable": {"session_id": session_id}}
)

# Follow-up
chain_with_history.invoke(
    {"input": "What's my name?"},
    config={"configurable": {"session_id": session_id}}
)
```

## Document Loaders

Load and process various document types:

```python
from langchain_community.document_loaders import (
    UnstructuredMarkdownLoader,
    PyPDFLoader,
    CSVLoader,
    TextLoader,
    BSHTMLLoader,
    DirectoryLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load a markdown file
markdown_loader = UnstructuredMarkdownLoader("path/to/document.md")
markdown_docs = markdown_loader.load()

# Load a PDF file
pdf_loader = PyPDFLoader("path/to/document.pdf")
pdf_docs = pdf_loader.load()

# Load a CSV file
csv_loader = CSVLoader("path/to/data.csv")
csv_docs = csv_loader.load()

# Load HTML content
html_loader = BSHTMLLoader("path/to/page.html")
html_docs = html_loader.load()

# Load all files in a directory
directory_loader = DirectoryLoader("./data/", glob="**/*.txt")
directory_docs = directory_loader.load()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100
)
document_chunks = text_splitter.split_documents(markdown_docs)
```

### Advanced Text Splitting

```python
from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    TokenTextSplitter,
    SentenceTransformersTokenTextSplitter
)

# Character-based splitting
char_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1000,
    chunk_overlap=200
)

# Token-based splitting (more precise for LLM context windows)
token_splitter = TokenTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

# Semantic text splitting
sentence_transformer_splitter = SentenceTransformersTokenTextSplitter(
    model_name="all-MiniLM-L6-v2",
    chunk_overlap=0
)

# Split with code-aware splitter
code_splitter = RecursiveCharacterTextSplitter.from_language(
    language="python", 
    chunk_size=1000, 
    chunk_overlap=200
)
```

## Vector Stores

Vector stores enable semantic search by storing and retrieving embeddings:

```python
from langchain_community.vectorstores import Chroma, FAISS, Pinecone
from langchain_openai import OpenAIEmbeddings

# Initialize embeddings
embeddings = OpenAIEmbeddings()

# Create an in-memory vector store with FAISS
docs = text_splitter.split_documents(documents)
faiss_db = FAISS.from_documents(docs, embeddings)

# Persist to disk
faiss_db.save_local("faiss_index")

# Load from disk
loaded_faiss = FAISS.load_local("faiss_index", embeddings)

# Query the database
query = "What is LangChain used for?"
docs = faiss_db.similarity_search(query)

# Use Chroma (persists to disk automatically)
chroma_db = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# Add documents to existing database
chroma_db.add_documents(new_documents)

# Use with Pinecone (cloud vectorstore)
import pinecone
pinecone.init(api_key="YOUR-API-KEY", environment="YOUR-ENV")

index_name = "langchain-demo"
pinecone_db = Pinecone.from_documents(
    documents, 
    embeddings, 
    index_name=index_name
)
```

## Retrieval Systems

Build advanced retrieval systems to find relevant information:

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

# Basic retrieval
retriever = chroma_db.as_retriever()
retrieved_docs = retriever.get_relevant_documents("How can I use LangChain?")

# Contextual compression retriever (removes irrelevant content from docs)
llm = ChatOpenAI(temperature=0)
compressor = LLMChainExtractor.from_llm(llm)
compression_retriever = ContextualCompressionRetriever(
    base_retriever=retriever,
    base_compressor=compressor
)

compressed_docs = compression_retriever.get_relevant_documents("How can I use LangChain?")

# Self-querying retriever (generates structured query from natural language)
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional

class DocumentMetadata(BaseModel):
    source: str = Field(description="The document source")
    date: Optional[str] = Field(description="The date the document was created")
    author: Optional[str] = Field(description="The author of the document")

self_querying_retriever = SelfQueryRetriever.from_llm(
    llm=llm,
    vectorstore=chroma_db,
    document_contents="Documents about LangChain framework usage and features",
    metadata_field_info=[
        {"name": "source", "description": "The source of the document"},
        {"name": "date", "description": "The date the document was created"},
        {"name": "author", "description": "The author of the document"}
    ]
)

filtered_docs = self_querying_retriever.get_relevant_documents(
    "Find documents about agents written by Harrison"
)
```

## Evaluation

Evaluate and improve your LangChain applications:

```python
from langchain.evaluation import load_evaluator
from langchain.evaluation import EvaluatorType

# Initialize evaluators
qa_evaluator = load_evaluator(EvaluatorType.QA)
criteria_evaluator = load_evaluator(
    EvaluatorType.CRITERIA,
    criteria={
        "accuracy": "Does the output accurately address the query?",
        "conciseness": "Is the output concise and to the point?",
        "helpfulness": "Is the output helpful for the user?"
    }
)

# Evaluate a QA response
qa_eval = qa_evaluator.evaluate_strings(
    prediction="Paris is the capital of France",
    input="What is the capital of France?",
    reference="The capital of France is Paris."
)

# Evaluate against criteria
criteria_eval = criteria_evaluator.evaluate_strings(
    prediction="The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France. It is named after the engineer Gustave Eiffel, whose company designed and built the tower. It was constructed from 1887-1889 as the entrance to the 1889 World's Fair.",
    input="Tell me about the Eiffel Tower"
)

# Custom evaluation function
from langchain_core.language_models import BaseLanguageModel

def evaluate_summary(llm: BaseLanguageModel, summary: str, original_text: str) -> dict:
    """Evaluate a summary against the original text."""
    prompt = f"""
    Evaluate the following summary of the original text on a scale of 1-10:
    
    Original text: {original_text}
    
    Summary: {summary}
    
    Evaluate on:
    1. Accuracy (does it contain factual errors?): [1-10]
    2. Completeness (does it capture key information?): [1-10]
    3. Conciseness (is it unnecessarily verbose?): [1-10]
    
    Provide your evaluation as a JSON object with fields for each score and explanation.
    """
    
    response = llm.invoke(prompt)
    # In a real implementation, you'd parse the JSON response
    return response
```

## Advanced Applications

### Retrieval-Augmented Generation (RAG)

```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# 1. Load documents
loader = TextLoader("path/to/data.txt")
documents = loader.load()

# 2. Split documents
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
chunks = text_splitter.split_documents(documents)

# 3. Create embeddings and store in vector database
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings)

# 4. Create retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# 5. Create a RAG chain
prompt = ChatPromptTemplate.from_template("""
Answer the following question based only on the provided context:

Context: {context}

Question: {question}

Answer:
""")

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | ChatOpenAI(model="gpt-4")
    | StrOutputParser()
)

# 6. Ask questions
response = rag_chain.invoke("How does LangChain work?")
```

### Advanced RAG with Query Transformation

```python
from langchain.retrievers import MultiQueryRetriever
from langchain_core.output_parsers import CommaSeparatedListOutputParser

# Create a query generator
query_prompt = ChatPromptTemplate.from_template(
    """Generate three different search queries for retrieving relevant information to answer the question.
    The queries should be different from each other and approach the question from different angles.
    Return these as a comma-separated list.
    
    Question: {question}
    """
)

query_generator = query_prompt | ChatOpenAI(temperature=0.3) | CommaSeparatedListOutputParser()

# Create multi-query retriever
multi_retriever = MultiQueryRetriever(
    retriever=vectorstore.as_retriever(),
    llm_chain=query_generator,
    parser_key="question"
)

# Create enhanced RAG chain
enhanced_rag_chain = (
    {"context": multi_retriever, "question": RunnablePassthrough()}
    | prompt
    | ChatOpenAI(model="gpt-4")
    | StrOutputParser()
)

response = enhanced_rag_chain.invoke("Explain the concept of agents in LangChain")
```

### Conversational RAG with Memory

```python
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain.chains import ConversationalRetrievalChain

# Initialize chat history
chat_history = []

# Create a conversational RAG
conversational_rag = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-4"),
    retriever=vectorstore.as_retriever(),
    return_source_documents=True
)

# First query
result = conversational_rag.invoke({
    "question": "What is LangChain?", 
    "chat_history": chat_history
})

# Update history
chat_history.append((
    "What is LangChain?", 
    result["answer"]
))

# Follow-up question
follow_up = conversational_rag.invoke({
    "question": "How does it handle memory?", 
    "chat_history": chat_history
})
```

## LangSmith for Debugging

LangSmith provides tracing and debugging for LangChain applications:

```python
import os
import getpass

# Set environment variables for LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = getpass.getpass("Enter your LangSmith API key: ")
os.environ["LANGCHAIN_PROJECT"] = "My LangChain Project"

# Now your LangChain runs will be traced in LangSmith
```

### Monitoring and Feedback

```python
from langsmith import Client

# Initialize the LangSmith client
client = Client()

# Log a run manually
run = client.create_run(
    name="My Custom Run",
    inputs={"question": "What is LangChain?"},
    run_type="chain"
)

try:
    # Your custom code
    result = "LangChain is a framework for developing applications powered by language models."
    
    # Update the run with outputs
    client.update_run(
        run.id,
        outputs={"answer": result},
        end_time=datetime.datetime.utcnow()
    )
except Exception as e:
    # Log errors
    client.update_run(
        run.id,
        error=str(e),
        end_time=datetime.datetime.utcnow()
    )

# Add feedback to a run
client.create_feedback(
    run.id,
    "accuracy",
    score=0.95,
    comment="Very accurate response"
)
```

## Conclusion

LangChain provides a comprehensive framework for building sophisticated AI applications powered by language models. From basic chains to advanced agents, it offers the tools necessary to create complex, context-aware reasoning systems.

Key benefits include:
- Modular, composable components that can be mixed and matched
- Rich ecosystem of integrations with models, tools, and data sources
- Powerful abstractions for creating agents, memory systems, and retrieval pipelines
- End-to-end support from development to production with LangSmith

For more information and detailed documentation, visit:
- [LangChain Python Documentation](https://python.langchain.com/docs/)
- [GitHub Repository](https://github.com/langchain-ai/langchain)
- [LangSmith](https://smith.langchain.com/) for debugging and monitoring

---

*This tutorial serves as an introduction to LangChain. For production applications, always refer to the latest documentation and best practices.* 