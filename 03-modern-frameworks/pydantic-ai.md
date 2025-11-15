# Pydantic AI: Type-Safe Agent Development

⏱️ **Estimated reading time: 20 minutes**

Tags: #pydantic-ai #type-safety #modern-frameworks #production-ready #structured-outputs #validation #python

## Introduction

[Pydantic AI](https://ai.pydantic.dev/) is a Python framework for building production-ready AI agents with a focus on type safety, structured outputs, and robust validation. Built by the team behind Pydantic (Python's most popular data validation library), it brings the same principles of type safety and developer experience to AI agent development.

## Key Features

### 1. Type Safety First
- **Structured Outputs**: Define exact response schemas using Pydantic models
- **Compile-time Validation**: Catch errors before runtime with type hints
- **IDE Support**: Full autocomplete and type checking in modern IDEs

### 2. Model Agnostic
- Supports multiple LLM providers (OpenAI, Anthropic, Google, Groq, Mistral)
- Easy switching between models without code changes
- Consistent interface across different providers

### 3. Dependency Injection
- Clean separation of concerns
- Testable agent components
- Easy mocking for unit tests

### 4. Streaming Support
- Real-time response streaming
- Structured streaming with validation
- Progress tracking for long-running tasks

## Architecture Overview

```python
from pydantic import BaseModel
from pydantic_ai import Agent

# Define structured output schema
class WeatherResponse(BaseModel):
    temperature: float
    conditions: str
    humidity: int
    wind_speed: float

# Create type-safe agent
weather_agent = Agent(
    'openai:gpt-4',
    result_type=WeatherResponse,
    system_prompt="You are a weather information assistant."
)
```

## Core Concepts

### 1. Agents
The central abstraction in Pydantic AI. Agents encapsulate:
- Model configuration
- System prompts
- Tool definitions
- Response validation

### 2. Tools (Functions)
Type-safe function calling with automatic schema generation:

```python
from pydantic_ai import Agent, RunContext

agent = Agent('openai:gpt-4')

@agent.tool
async def get_weather(ctx: RunContext[dict], city: str) -> str:
    """Get current weather for a city."""
    # Implementation here
    return f"Weather data for {city}"
```

### 3. Dependencies
Inject external services and data into agents:

```python
from dataclasses import dataclass

@dataclass
class Dependencies:
    database: Database
    api_client: APIClient
    user_id: str

agent = Agent(
    'openai:gpt-4',
    deps_type=Dependencies
)

# Use dependencies in tools
@agent.tool
async def fetch_user_data(ctx: RunContext[Dependencies]) -> dict:
    return await ctx.deps.database.get_user(ctx.deps.user_id)
```

### 4. Result Validation
Automatic validation of LLM outputs:

```python
from pydantic import BaseModel, Field

class AnalysisResult(BaseModel):
    sentiment: str = Field(pattern=r'^(positive|negative|neutral)$')
    confidence: float = Field(ge=0, le=1)
    key_phrases: list[str] = Field(max_length=5)

agent = Agent(
    'openai:gpt-4',
    result_type=AnalysisResult
)

# Agent automatically validates and retries if output doesn't match schema
result = await agent.run("Analyze this text...")
# result is guaranteed to be AnalysisResult instance
```

## Advanced Features

### 1. System Prompt Functions
Dynamic system prompts based on context:

```python
async def dynamic_system_prompt(ctx: RunContext[Dependencies]) -> str:
    user_preferences = await ctx.deps.get_user_preferences()
    return f"You are an assistant. User prefers: {user_preferences}"

agent = Agent(
    'openai:gpt-4',
    system_prompt=dynamic_system_prompt
)
```

### 2. Retry Logic with Validation
Automatic retries when validation fails:

```python
from pydantic_ai import Agent, ModelRetry

class StrictOutput(BaseModel):
    code: str
    explanation: str
    
    @field_validator('code')
    @classmethod
    def validate_code(cls, v: str) -> str:
        # Ensure code is valid Python
        compile(v, '<string>', 'exec')
        return v

agent = Agent(
    'openai:gpt-4',
    result_type=StrictOutput,
    retries=3
)
```

### 3. Streaming Responses
Handle streaming data with validation:

```python
async with agent.run_stream("Generate a report...") as response:
    async for chunk in response.stream():
        print(chunk)  # Print chunks as they arrive
    
    # Final validated result
    result = await response.get_data()
```

### 4. Testing Support
Built-in testing utilities:

```python
from pydantic_ai.testing import TestAgent

def test_weather_agent():
    with TestAgent() as agent:
        agent.set_result(WeatherResponse(
            temperature=72.5,
            conditions="Sunny",
            humidity=45,
            wind_speed=5.2
        ))
        
        result = agent.run_sync("What's the weather?")
        assert result.temperature == 72.5
```

## Practical Example: Customer Support Agent

```python
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from typing import Literal
import asyncio

# Define response types
class TicketClassification(BaseModel):
    category: Literal['billing', 'technical', 'general']
    priority: Literal['low', 'medium', 'high']
    sentiment: Literal['positive', 'neutral', 'negative']
    
class SupportResponse(BaseModel):
    classification: TicketClassification
    suggested_response: str
    escalate: bool = Field(description="Whether to escalate to human agent")
    
# Define dependencies
@dataclass
class SupportDeps:
    knowledge_base: KnowledgeBase
    ticket_system: TicketSystem
    customer_id: str

# Create the agent
support_agent = Agent(
    'openai:gpt-4',
    deps_type=SupportDeps,
    result_type=SupportResponse,
    system_prompt="""You are a customer support agent. 
    Classify tickets, suggest responses, and determine if escalation is needed."""
)

# Add tools
@support_agent.tool
async def search_knowledge_base(
    ctx: RunContext[SupportDeps], 
    query: str
) -> list[str]:
    """Search the knowledge base for relevant articles."""
    return await ctx.deps.knowledge_base.search(query, limit=3)

@support_agent.tool
async def get_customer_history(ctx: RunContext[SupportDeps]) -> dict:
    """Get customer's ticket history."""
    return await ctx.deps.ticket_system.get_history(ctx.deps.customer_id)

# Use the agent
async def handle_support_ticket(ticket_text: str, customer_id: str):
    deps = SupportDeps(
        knowledge_base=KnowledgeBase(),
        ticket_system=TicketSystem(),
        customer_id=customer_id
    )
    
    result = await support_agent.run(
        ticket_text,
        deps=deps
    )
    
    if result.data.escalate:
        await escalate_to_human(ticket_text, result.data)
    else:
        await send_automated_response(result.data.suggested_response)
    
    return result.data
```

## Integration with Other Frameworks

### LangChain Integration
```python
from langchain.schema import BaseMessage
from pydantic_ai import Agent

# Use Pydantic AI for validation with LangChain
class ValidatedOutput(BaseModel):
    result: str
    confidence: float

pydantic_agent = Agent('openai:gpt-4', result_type=ValidatedOutput)

# Can be used within LangChain workflows
async def langchain_with_validation(messages: list[BaseMessage]):
    text = messages[-1].content
    validated_result = await pydantic_agent.run(text)
    return validated_result.data
```

### FastAPI Integration
```python
from fastapi import FastAPI, Depends
from pydantic_ai import Agent

app = FastAPI()
agent = Agent('openai:gpt-4')

@app.post("/chat")
async def chat_endpoint(
    message: str,
    agent_instance: Agent = Depends(lambda: agent)
):
    result = await agent_instance.run(message)
    return {"response": result.data}
```

## Best Practices

### 1. Schema Design
- Keep response schemas focused and specific
- Use enums/literals for categorical outputs
- Add field descriptions for better LLM understanding

### 2. Error Handling
```python
from pydantic_ai import Agent, ModelRetry

@agent.tool
async def risky_operation(ctx: RunContext) -> str:
    try:
        return await external_api_call()
    except Exception as e:
        raise ModelRetry(f"API call failed: {e}")
```

### 3. Testing Strategy
- Use TestAgent for unit tests
- Mock dependencies for isolation
- Test validation logic separately

### 4. Performance Optimization
- Cache frequently used prompts
- Batch similar requests
- Use streaming for long responses

## Comparison with Other Frameworks

| Feature | Pydantic AI | LangChain | DSPy |
|---------|------------|-----------|------|
| Type Safety | ✅ Native | ⚠️ Limited | ⚠️ Limited |
| Structured Output | ✅ Built-in | ✅ Via tools | ✅ Signatures |
| Testing Support | ✅ TestAgent | ⚠️ Manual | ⚠️ Manual |
| Learning Curve | 📊 Low | 📊 Medium | 📊 High |
| Model Support | ✅ Multi | ✅ Multi | ✅ Multi |
| Streaming | ✅ Native | ✅ Available | ⚠️ Limited |

## Limitations

1. **Python Only**: No support for other languages
2. **Overhead**: Type validation adds some latency
3. **Learning Curve**: Requires understanding of Pydantic
4. **Young Ecosystem**: Fewer integrations than established frameworks

## Use Cases

### Ideal For:
- Production Python applications requiring reliability
- APIs with strict output requirements
- Applications needing extensive testing
- Teams prioritizing type safety and IDE support

### Less Suitable For:
- Quick prototypes or experiments
- Non-Python environments
- Simple chatbots without structured outputs
- Applications requiring complex agent orchestration

## Getting Started

### Installation
```bash
pip install pydantic-ai
```

### Basic Example
```python
from pydantic import BaseModel
from pydantic_ai import Agent
import asyncio

class CityInfo(BaseModel):
    name: str
    population: int
    country: str
    interesting_fact: str

agent = Agent(
    'openai:gpt-4',
    result_type=CityInfo,
    system_prompt="Provide accurate city information."
)

async def main():
    result = await agent.run("Tell me about Tokyo")
    print(f"City: {result.data.name}")
    print(f"Population: {result.data.population:,}")
    print(f"Country: {result.data.country}")
    print(f"Fact: {result.data.interesting_fact}")

asyncio.run(main())
```

## Conclusion

Pydantic AI represents a significant advancement in making AI agents more reliable and maintainable for production use. Its focus on type safety, structured outputs, and developer experience makes it an excellent choice for teams building robust AI applications that need predictable, validated outputs.

## Resources

- [Official Documentation](https://ai.pydantic.dev/)
- [GitHub Repository](https://github.com/pydantic/pydantic-ai)
- [Examples and Tutorials](https://ai.pydantic.dev/examples/)
- [API Reference](https://ai.pydantic.dev/api/)
- [Migration Guide from LangChain](https://ai.pydantic.dev/migration/)

## Next Steps

- Explore [Model Context Protocol](model-context-protocol.md) for standardized tool integration
- Learn about [Orchestration Frameworks](orchestration-frameworks.md) for complex workflows
- Check out [Enterprise Platforms](enterprise-platforms.md) for production deployment