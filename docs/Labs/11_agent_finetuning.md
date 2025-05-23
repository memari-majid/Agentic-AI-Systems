# Lab 11: Agent Fine-tuning

⏱️ **Estimated completion time: 55 minutes**

## Overview

This lab demonstrates fine-tuning techniques for improving agent performance, including data collection, model training, and evaluation metrics.

## Learning Objectives

- Understanding agent fine-tuning workflows
- Collecting and preparing training data
- Evaluating fine-tuned agent performance

## Key Concepts

### Fine-tuning Process
1. **Data Collection**: Gathering high-quality training examples
2. **Model Training**: Fine-tuning pre-trained models
3. **Evaluation**: Measuring performance improvements

## Lab Code

```python
#!/usr/bin/env python3
"""
Agent Fine-tuning Demo
Demonstrate fine-tuning workflow for agent improvement.
"""
import json
import random
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class TrainingExample:
    """Training example for agent fine-tuning."""
    input_text: str
    expected_output: str
    task_type: str
    quality_score: float

@dataclass
class AgentResponse:
    """Agent response with metadata."""
    text: str
    confidence: float
    reasoning: str

class MockAgent:
    """Mock agent for demonstration purposes."""
    
    def __init__(self, version="baseline"):
        self.version = version
        self.performance_boost = 0.1 if version == "fine-tuned" else 0.0
        
    def generate_response(self, input_text: str) -> AgentResponse:
        """Generate response to input text."""
        # Mock response generation
        base_confidence = 0.7 + self.performance_boost
        
        if "weather" in input_text.lower():
            response = "The weather is sunny and pleasant today."
            reasoning = "Identified weather query and provided current conditions."
        elif "travel" in input_text.lower():
            response = "I can help you plan your travel itinerary."
            reasoning = "Detected travel-related request and offered assistance."
        else:
            response = "I understand your request and will help accordingly."
            reasoning = "General query handling with helpful response."
            
        return AgentResponse(
            text=response,
            confidence=min(1.0, base_confidence + random.uniform(-0.1, 0.1)),
            reasoning=reasoning
        )

class DataCollector:
    """Collect and manage training data for fine-tuning."""
    
    def __init__(self):
        self.examples: List[TrainingExample] = []
        
    def collect_interaction_data(self, user_input: str, agent_output: str, 
                               human_rating: float, task_type: str) -> None:
        """Collect data from human-agent interactions."""
        example = TrainingExample(
            input_text=user_input,
            expected_output=agent_output,
            task_type=task_type,
            quality_score=human_rating
        )
        self.examples.append(example)
        
    def generate_synthetic_data(self) -> None:
        """Generate synthetic training examples."""
        synthetic_examples = [
            ("What's the weather like?", "The weather is sunny with 22°C temperature.", "weather", 0.9),
            ("Plan my trip to Paris", "I'll help you plan a wonderful trip to Paris with hotels and attractions.", "travel", 0.85),
            ("Book a flight", "I can assist you with flight booking options and recommendations.", "travel", 0.8),
            ("Tell me about restaurants", "Here are some excellent restaurant recommendations in your area.", "general", 0.75),
            ("Weather forecast", "The forecast shows sunny weather for the next few days.", "weather", 0.9),
        ]
        
        for input_text, output, task_type, quality in synthetic_examples:
            self.collect_interaction_data(input_text, output, quality, task_type)
    
    def filter_high_quality(self, min_score: float = 0.8) -> List[TrainingExample]:
        """Filter examples by quality score."""
        return [ex for ex in self.examples if ex.quality_score >= min_score]
    
    def prepare_training_data(self) -> Dict[str, List[Dict]]:
        """Prepare data for fine-tuning format."""
        high_quality = self.filter_high_quality()
        
        training_data = {
            "examples": [],
            "metadata": {
                "total_examples": len(high_quality),
                "task_distribution": {}
            }
        }
        
        for example in high_quality:
            training_data["examples"].append({
                "input": example.input_text,
                "output": example.expected_output,
                "task_type": example.task_type
            })
            
            # Track task distribution
            task = example.task_type
            training_data["metadata"]["task_distribution"][task] = \
                training_data["metadata"]["task_distribution"].get(task, 0) + 1
        
        return training_data

class AgentEvaluator:
    """Evaluate agent performance before and after fine-tuning."""
    
    def __init__(self):
        self.test_cases = [
            {"input": "What's tomorrow's weather?", "expected_type": "weather"},
            {"input": "Help me book a vacation", "expected_type": "travel"},
            {"input": "Find good restaurants nearby", "expected_type": "general"},
            {"input": "Weather update please", "expected_type": "weather"},
            {"input": "Plan my business trip", "expected_type": "travel"},
        ]
    
    def evaluate_agent(self, agent: MockAgent) -> Dict[str, float]:
        """Evaluate agent performance."""
        total_confidence = 0.0
        task_accuracy = 0.0
        response_quality = 0.0
        
        for test_case in self.test_cases:
            response = agent.generate_response(test_case["input"])
            
            # Aggregate confidence scores
            total_confidence += response.confidence
            
            # Mock task accuracy (would be more sophisticated in practice)
            expected_keywords = {
                "weather": ["weather", "temperature", "sunny", "forecast"],
                "travel": ["travel", "trip", "plan", "booking"],
                "general": ["help", "assist", "recommend"]
            }
            
            expected_type = test_case["expected_type"]
            keywords = expected_keywords.get(expected_type, [])
            
            if any(keyword in response.text.lower() for keyword in keywords):
                task_accuracy += 1.0
            
            # Mock response quality score
            response_quality += min(1.0, response.confidence + 0.1)
        
        num_tests = len(self.test_cases)
        return {
            "average_confidence": total_confidence / num_tests,
            "task_accuracy": task_accuracy / num_tests,
            "response_quality": response_quality / num_tests,
            "overall_score": (total_confidence + task_accuracy + response_quality) / (3 * num_tests)
        }

def simulate_fine_tuning(training_data: Dict) -> MockAgent:
    """Simulate the fine-tuning process."""
    print(f"Fine-tuning with {training_data['metadata']['total_examples']} examples...")
    print(f"Task distribution: {training_data['metadata']['task_distribution']}")
    
    # In practice, this would involve:
    # 1. Loading pre-trained model
    # 2. Preparing data in correct format
    # 3. Training with appropriate hyperparameters
    # 4. Validation and early stopping
    # 5. Model checkpointing
    
    print("Training process:")
    print("- Epoch 1: Loss = 2.45")
    print("- Epoch 2: Loss = 1.89") 
    print("- Epoch 3: Loss = 1.34")
    print("- Epoch 4: Loss = 1.12")
    print("- Epoch 5: Loss = 0.95")
    print("Training completed!")
    
    # Return "fine-tuned" agent
    return MockAgent(version="fine-tuned")

def main():
    print("=== Agent Fine-tuning Demo ===")
    
    # Step 1: Data Collection
    print("\n1. Collecting Training Data")
    collector = DataCollector()
    collector.generate_synthetic_data()
    
    print(f"Collected {len(collector.examples)} training examples")
    
    # Step 2: Data Preparation
    print("\n2. Preparing Training Data")
    training_data = collector.prepare_training_data()
    print(f"High-quality examples: {training_data['metadata']['total_examples']}")
    print(f"Task distribution: {training_data['metadata']['task_distribution']}")
    
    # Step 3: Baseline Evaluation
    print("\n3. Evaluating Baseline Agent")
    baseline_agent = MockAgent(version="baseline")
    evaluator = AgentEvaluator()
    
    baseline_metrics = evaluator.evaluate_agent(baseline_agent)
    print("Baseline Performance:")
    for metric, value in baseline_metrics.items():
        print(f"  {metric}: {value:.3f}")
    
    # Step 4: Fine-tuning
    print("\n4. Fine-tuning Agent")
    fine_tuned_agent = simulate_fine_tuning(training_data)
    
    # Step 5: Post-training Evaluation
    print("\n5. Evaluating Fine-tuned Agent")
    fine_tuned_metrics = evaluator.evaluate_agent(fine_tuned_agent)
    print("Fine-tuned Performance:")
    for metric, value in fine_tuned_metrics.items():
        print(f"  {metric}: {value:.3f}")
    
    # Step 6: Performance Comparison
    print("\n6. Performance Improvement")
    for metric in baseline_metrics:
        improvement = fine_tuned_metrics[metric] - baseline_metrics[metric]
        print(f"  {metric}: {improvement:+.3f} ({improvement/baseline_metrics[metric]*100:+.1f}%)")
    
    # Step 7: Example Interactions
    print("\n7. Example Interactions")
    test_inputs = ["What's the weather like?", "Help me plan a trip"]
    
    for input_text in test_inputs:
        print(f"\nInput: {input_text}")
        
        baseline_response = baseline_agent.generate_response(input_text)
        fine_tuned_response = fine_tuned_agent.generate_response(input_text)
        
        print(f"Baseline: {baseline_response.text} (confidence: {baseline_response.confidence:.2f})")
        print(f"Fine-tuned: {fine_tuned_response.text} (confidence: {fine_tuned_response.confidence:.2f})")

if __name__ == "__main__":
    main()
```

## How to Run

1. Save as `11_agent_finetuning.py`
2. Run: `python 11_agent_finetuning.py`

## Key Features

- **Data Collection**: Systematic gathering of training examples
- **Quality Filtering**: Focus on high-quality training data
- **Performance Metrics**: Comprehensive evaluation framework
- **Comparison Analysis**: Before/after performance tracking

## Download Code

[Download 11_agent_finetuning.py](11_agent_finetuning.py){ .md-button .md-button--primary } 