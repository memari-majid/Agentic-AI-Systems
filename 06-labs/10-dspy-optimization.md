# Lab 10: DSPy Prompt Optimization

⏱️ **Estimated completion time: 45 minutes**

## Overview

This lab demonstrates using DSPy for automatic prompt optimization in agent workflows, including signature definition, few-shot learning, and performance metrics.

## Learning Objectives

- Understanding DSPy signatures and modules
- Implementing automatic prompt optimization
- Measuring and improving agent performance

## Key Concepts

### DSPy Framework
1. **Signatures**: Formal specifications of input/output behavior
2. **Modules**: Reusable components with learnable parameters
3. **Optimizers**: Automatic prompt engineering and few-shot selection

## Lab Code

```python
#!/usr/bin/env python3
"""
DSPy Prompt Optimization Demo
Demonstrate automatic prompt optimization for agent tasks.
"""
try:
    import dspy
    from dspy import Signature, Module, ChainOfThought, Predict
    from dspy.teleprompt import BootstrapFewShot
except ImportError:
    print("DSPy not installed. Install with: pip install dspy-ai")
    exit(1)

import random
from typing import List, Dict

# Configure DSPy with a mock LM for demo
class MockLM:
    def __init__(self):
        self.responses = {
            "sentiment": ["positive", "negative", "neutral"],
            "classification": ["travel", "weather", "general"],
            "summary": "This is a summary of the text."
        }
    
    def __call__(self, prompt, **kwargs):
        # Simple mock responses based on prompt content
        if "sentiment" in prompt.lower():
            return random.choice(self.responses["sentiment"])
        elif "classify" in prompt.lower():
            return random.choice(self.responses["classification"])
        else:
            return self.responses["summary"]

# Set up DSPy with mock LM
dspy.configure(lm=MockLM())

# Define DSPy Signatures
class SentimentAnalysis(Signature):
    """Analyze the sentiment of user input."""
    text = dspy.InputField(desc="The input text to analyze")
    sentiment = dspy.OutputField(desc="The sentiment: positive, negative, or neutral")

class QueryClassification(Signature):
    """Classify user queries into categories."""
    query = dspy.InputField(desc="User query to classify")
    category = dspy.OutputField(desc="Category: travel, weather, or general")

class ResponseGeneration(Signature):
    """Generate appropriate responses based on query and sentiment."""
    query = dspy.InputField(desc="User query")
    sentiment = dspy.InputField(desc="Sentiment of the query")
    category = dspy.InputField(desc="Category of the query")
    response = dspy.OutputField(desc="Appropriate response to the user")

# Define DSPy Modules
class OptimizedAgent(Module):
    """Agent with optimizable prompt components."""
    
    def __init__(self):
        super().__init__()
        self.sentiment_analyzer = ChainOfThought(SentimentAnalysis)
        self.query_classifier = ChainOfThought(QueryClassification)
        self.response_generator = Predict(ResponseGeneration)
    
    def forward(self, user_input):
        # Analyze sentiment
        sentiment_result = self.sentiment_analyzer(text=user_input)
        
        # Classify query
        classification_result = self.query_classifier(query=user_input)
        
        # Generate response
        response_result = self.response_generator(
            query=user_input,
            sentiment=sentiment_result.sentiment,
            category=classification_result.category
        )
        
        return {
            "sentiment": sentiment_result.sentiment,
            "category": classification_result.category,
            "response": response_result.response
        }

def create_training_data():
    """Create mock training data for optimization."""
    return [
        {
            "user_input": "I love traveling to new places!",
            "expected_sentiment": "positive",
            "expected_category": "travel"
        },
        {
            "user_input": "The weather is terrible today.",
            "expected_sentiment": "negative", 
            "expected_category": "weather"
        },
        {
            "user_input": "How can I help you?",
            "expected_sentiment": "neutral",
            "expected_category": "general"
        },
        {
            "user_input": "I'm excited about my vacation!",
            "expected_sentiment": "positive",
            "expected_category": "travel"
        }
    ]

def evaluate_agent(agent, test_data):
    """Evaluate agent performance on test data."""
    correct_sentiment = 0
    correct_category = 0
    total = len(test_data)
    
    for example in test_data:
        result = agent(example["user_input"])
        
        if result["sentiment"] == example["expected_sentiment"]:
            correct_sentiment += 1
        if result["category"] == example["expected_category"]:
            correct_category += 1
    
    sentiment_accuracy = correct_sentiment / total
    category_accuracy = correct_category / total
    
    return {
        "sentiment_accuracy": sentiment_accuracy,
        "category_accuracy": category_accuracy,
        "overall_score": (sentiment_accuracy + category_accuracy) / 2
    }

def main():
    print("=== DSPy Prompt Optimization Demo ===")
    
    # Create training and test data
    training_data = create_training_data()
    test_data = training_data  # Using same data for demo
    
    # Initialize agent
    agent = OptimizedAgent()
    
    print("\n1. Testing baseline agent:")
    baseline_metrics = evaluate_agent(agent, test_data)
    print(f"Baseline performance: {baseline_metrics}")
    
    # Define metric function for optimization
    def agent_metric(example, prediction):
        """Custom metric for agent evaluation."""
        sentiment_correct = prediction["sentiment"] == example["expected_sentiment"]
        category_correct = prediction["category"] == example["expected_category"]
        return (sentiment_correct + category_correct) / 2
    
    # Prepare training examples for DSPy
    dspy_examples = []
    for example in training_data:
        dspy_example = dspy.Example(
            user_input=example["user_input"],
            expected_sentiment=example["expected_sentiment"],
            expected_category=example["expected_category"]
        )
        dspy_examples.append(dspy_example)
    
    print("\n2. Optimizing agent with DSPy:")
    
    # Configure optimizer
    optimizer = BootstrapFewShot(
        metric=agent_metric,
        max_bootstrapped_demos=2,
        max_labeled_demos=2
    )
    
    # Note: In a real scenario, this would optimize the prompts
    # For demo purposes, we'll simulate the optimization
    print("Running DSPy optimization... (simulated)")
    
    # In real DSPy usage:
    # optimized_agent = optimizer.compile(agent, trainset=dspy_examples)
    optimized_agent = agent  # Mock optimization for demo
    
    print("\n3. Testing optimized agent:")
    optimized_metrics = evaluate_agent(optimized_agent, test_data)
    print(f"Optimized performance: {optimized_metrics}")
    
    # Show improvement
    improvement = optimized_metrics["overall_score"] - baseline_metrics["overall_score"]
    print(f"\nImprovement: {improvement:.2%}")
    
    print("\n4. Example agent interactions:")
    test_queries = [
        "I can't wait for my trip to Paris!",
        "The rain is ruining my day.",
        "What time is it?"
    ]
    
    for query in test_queries:
        result = optimized_agent(query)
        print(f"\nQuery: {query}")
        print(f"Sentiment: {result['sentiment']}")
        print(f"Category: {result['category']}")
        print(f"Response: {result['response']}")

if __name__ == "__main__":
    main()
```

## How to Run

1. Save as `10_dspy_optimization.py`
2. Install: `pip install dspy-ai`
3. Run: `python 10_dspy_optimization.py`

## Key Features

- **Automatic Optimization**: DSPy automatically improves prompts
- **Modular Design**: Reusable components with clear interfaces
- **Performance Metrics**: Systematic evaluation of improvements
- **Few-shot Learning**: Automatic example selection and optimization

## Download Code

[Download 10_dspy_optimization.py](10_dspy_optimization.py){ .md-button .md-button--primary } 