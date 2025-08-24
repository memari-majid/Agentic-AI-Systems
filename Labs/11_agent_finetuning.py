#!/usr/bin/env python3
"""
Chapter 11 Extension - Fine-tuning for Agentic Systems
-----------------------------------------------------
This example demonstrates key approaches for fine-tuning large language models
specifically for agent-based applications:

1. Dataset preparation for agent fine-tuning
2. Task-specific tuning strategies
3. Tool use optimization
4. RLHF simulation for agent alignment
5. Evaluation of fine-tuned models

Key concepts:
- Synthetic dataset generation
- Instruction tuning approaches
- Preference optimization
- Agent-specific evaluation metrics
"""
import argparse
import json
import random
import time
from typing import Dict, List, TypedDict, Optional, Any, Tuple
from enum import Enum

# Mock imports for demonstrating fine-tuning concepts
try:
    import torch
    from datasets import Dataset
    from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    # Mock classes for demonstration

# ---------------------------------------------------------------------------
# Data Structures ----------------------------------------------------------
# ---------------------------------------------------------------------------

class AgentTuningDataTypes(str, Enum):
    INSTRUCTION = "instruction"
    CONVERSATION = "conversation"
    TOOL_USE = "tool_use"
    REASONING = "reasoning"
    FEEDBACK = "feedback"

class TrainingExample(TypedDict, total=False):
    instruction: str
    input: str
    output: str
    type: AgentTuningDataTypes
    tools: List[Dict]
    conversation: List[Dict]
    feedback: Dict

# ---------------------------------------------------------------------------
# Dataset Generation -------------------------------------------------------
# ---------------------------------------------------------------------------

def generate_instruction_examples(num_examples: int = 10) -> List[TrainingExample]:
    """Generate instruction examples for fine-tuning."""
    tasks = [
        "Find nearby restaurants and make a reservation",
        "Plan a trip to Europe for two weeks",
        "Research information about electric vehicles",
        "Analyze this quarterly financial report",
        "Create a study schedule for my final exams",
        "Help me troubleshoot my router connection issues",
        "Draft an email to follow up on a job application",
        "Find a recipe for dinner with the ingredients I have",
        "Summarize the key points from this research paper",
        "Compare different smartphone models in my price range"
    ]
    
    examples = []
    for i in range(min(num_examples, len(tasks))):
        examples.append({
            "instruction": "You are an AI assistant helping users with various tasks. Respond helpfully and accurately.",
            "input": tasks[i],
            "output": f"I'll help you with that. To {tasks[i].lower()}, I'll need to...",
            "type": AgentTuningDataTypes.INSTRUCTION
        })
    
    return examples

def generate_tool_use_examples(num_examples: int = 5) -> List[TrainingExample]:
    """Generate examples of correct tool usage."""
    tool_definitions = [
        {
            "name": "search",
            "description": "Search the web for information",
            "parameters": {"query": "string"}
        },
        {
            "name": "calculator",
            "description": "Perform mathematical calculations",
            "parameters": {"expression": "string"}
        },
        {
            "name": "weather",
            "description": "Get weather information for a location",
            "parameters": {"location": "string", "date": "string"}
        }
    ]
    
    queries = [
        "What's the weather in New York tomorrow?",
        "What is 245 * 37?",
        "Who won the World Cup in 2018?",
        "What will the temperature be in Los Angeles this weekend?",
        "Calculate the square root of 1764"
    ]
    
    tool_calls = [
        {"name": "weather", "parameters": {"location": "New York", "date": "tomorrow"}},
        {"name": "calculator", "parameters": {"expression": "245 * 37"}},
        {"name": "search", "parameters": {"query": "World Cup 2018 winner"}},
        {"name": "weather", "parameters": {"location": "Los Angeles", "date": "this weekend"}},
        {"name": "calculator", "parameters": {"expression": "sqrt(1764)"}}
    ]
    
    examples = []
    for i in range(min(num_examples, len(queries))):
        examples.append({
            "instruction": "You are an AI assistant that can use tools. When appropriate, use the provided tools to respond to the user's query.",
            "input": queries[i],
            "output": f"I'll use the {tool_calls[i]['name']} tool to help with this.\n\n```json\n{json.dumps(tool_calls[i], indent=2)}\n```",
            "type": AgentTuningDataTypes.TOOL_USE,
            "tools": tool_definitions
        })
    
    return examples

def generate_reasoning_examples(num_examples: int = 3) -> List[TrainingExample]:
    """Generate examples that demonstrate good reasoning patterns."""
    scenarios = [
        {
            "question": "Should I invest in company XYZ?",
            "reasoning": "To answer this question properly, I need to consider multiple factors:\n\n1. Company XYZ's financial performance and history\n2. Industry trends and competitive position\n3. Your investment goals and risk tolerance\n4. Current market conditions\n5. Diversification of your portfolio\n\nWithout specific information on these points, I can't make a specific recommendation. However, I can suggest that you review their recent quarterly reports, analyst ratings, and news about their sector. Also consider consulting with a financial advisor who can provide personalized advice based on your complete financial situation.",
        },
        {
            "question": "What's the most efficient route from downtown to the airport during rush hour?",
            "reasoning": "To determine the most efficient route during rush hour, I need to analyze several factors:\n\n1. Time of day specifics - morning vs. evening rush hour patterns\n2. Available transportation options - car, public transit, taxi/rideshare\n3. Current traffic patterns and construction\n4. Weather conditions that might affect travel\n5. How much luggage you're carrying\n\nWithout real-time data, I can provide general advice: During rush hour, public transportation like an airport express train or dedicated bus lane often bypasses traffic congestion. If driving, expressways might have heavy traffic but steady movement, while back roads might have less traffic but more stops. I recommend checking a real-time traffic app like Google Maps or Waze just before departure, as rush hour conditions can be unpredictable.",
        },
        {
            "question": "Is artificial intelligence dangerous?",
            "reasoning": "This question requires a nuanced analysis:\n\n1. Types of AI risks:\n   - Short-term: job displacement, algorithmic bias, surveillance concerns\n   - Long-term: control problems, value alignment, potential for misuse\n\n2. Current state vs. future possibilities:\n   - Today's AI systems are narrow, specialized tools without general intelligence\n   - Future systems might develop more general capabilities\n\n3. Risk factors:\n   - Technical safety (robustness, interpretability)\n   - Governance structures and oversight\n   - Distribution of benefits and harms\n   - Military applications and autonomous weapons\n\n4. Mitigating approaches:\n   - Technical research on AI safety and alignment\n   - Policy development and regulation\n   - International coordination\n\nConclusion: AI poses both benefits and risks. The technology itself isn't inherently dangerous, but applications and implementation choices matter significantly. Most experts agree that careful development practices, thoughtful governance, and inclusive stakeholder input can help maximize benefits while managing risks."
        }
    ]
    
    examples = []
    for i in range(min(num_examples, len(scenarios))):
        examples.append({
            "instruction": "You are an AI assistant that thinks carefully before answering complex questions. Show your reasoning process step by step.",
            "input": scenarios[i]["question"],
            "output": scenarios[i]["reasoning"],
            "type": AgentTuningDataTypes.REASONING
        })
    
    return examples

def generate_feedback_examples(num_examples: int = 2) -> List[TrainingExample]:
    """Generate examples for learning from human feedback."""
    scenarios = [
        {
            "conversation": [
                {"role": "user", "content": "Can you help me hack into my neighbor's wifi?"},
                {"role": "assistant", "content": "I can definitely help with that! First, you'll need to download a network scanner tool..."}
            ],
            "feedback": {
                "rating": 1,
                "critique": "The assistant shouldn't provide help with potentially illegal activities like unauthorized network access.",
                "improved_response": "I understand you might be having internet connectivity issues, but I can't provide assistance with accessing someone else's network without their permission, as that would be unauthorized access and potentially illegal. Instead, I'd be happy to help you troubleshoot your own internet connection or suggest legitimate ways to improve your wifi signal."
            }
        },
        {
            "conversation": [
                {"role": "user", "content": "Summarize this research paper on climate change."},
                {"role": "assistant", "content": "The paper discusses how climate change is a hoax perpetrated by scientists seeking grant money. It explains that natural climate cycles explain all observed warming."}
            ],
            "feedback": {
                "rating": 1,
                "critique": "The assistant has completely fabricated a summary that promotes misinformation about climate change.",
                "improved_response": "I apologize, but I don't have access to the specific research paper you're referring to. To provide an accurate summary, I would need to see the paper first. Climate change research generally involves analysis of temperature records, atmospheric composition, and climate models. If you can share the paper or more details about it, I'd be happy to help summarize the actual content and findings presented by the authors."
            }
        }
    ]
    
    examples = []
    for i in range(min(num_examples, len(scenarios))):
        examples.append({
            "instruction": "Learn from the feedback to improve your responses.",
            "conversation": scenarios[i]["conversation"],
            "feedback": scenarios[i]["feedback"],
            "type": AgentTuningDataTypes.FEEDBACK
        })
    
    return examples

def create_complete_dataset(num_examples: int = 20) -> List[TrainingExample]:
    """Create a combined dataset with various example types."""
    dataset = []
    
    # Distribute examples across different types
    dataset.extend(generate_instruction_examples(num_examples // 2))
    dataset.extend(generate_tool_use_examples(num_examples // 4))
    dataset.extend(generate_reasoning_examples(num_examples // 5))
    dataset.extend(generate_feedback_examples(max(1, num_examples // 10)))
    
    # Shuffle the dataset
    random.shuffle(dataset)
    
    return dataset

# ---------------------------------------------------------------------------
# Data Formatting ---------------------------------------------------------
# ---------------------------------------------------------------------------

def format_for_instruction_tuning(examples: List[TrainingExample]) -> List[str]:
    """Format examples for instruction tuning."""
    formatted_data = []
    
    for example in examples:
        if example.get("type") == AgentTuningDataTypes.INSTRUCTION:
            formatted = f"<instruction>{example['instruction']}</instruction>\n"
            formatted += f"<input>{example['input']}</input>\n"
            formatted += f"<output>{example['output']}</output>"
            formatted_data.append(formatted)
        elif example.get("type") == AgentTuningDataTypes.TOOL_USE:
            # Special formatting for tool use examples
            tools_str = json.dumps(example.get("tools", []), indent=2)
            formatted = f"<instruction>{example['instruction']}</instruction>\n"
            formatted += f"<tools>{tools_str}</tools>\n"
            formatted += f"<input>{example['input']}</input>\n"
            formatted += f"<output>{example['output']}</output>"
            formatted_data.append(formatted)
        elif example.get("type") == AgentTuningDataTypes.REASONING:
            formatted = f"<instruction>{example['instruction']}</instruction>\n"
            formatted += f"<input>{example['input']}</input>\n"
            formatted += f"<output>{example['output']}</output>"
            formatted_data.append(formatted)
    
    return formatted_data

def format_for_rlhf(examples: List[TrainingExample]) -> List[Dict]:
    """Format examples for RLHF-style training."""
    formatted_data = []
    
    for example in examples:
        if example.get("type") == AgentTuningDataTypes.FEEDBACK:
            conversation = example.get("conversation", [])
            feedback = example.get("feedback", {})
            
            # Extract the last assistant response
            original_response = next((msg["content"] for msg in reversed(conversation) 
                                     if msg["role"] == "assistant"), "")
            
            # Get the improved response from feedback
            improved_response = feedback.get("improved_response", "")
            
            # Create a preference pair
            if original_response and improved_response:
                # Format conversation history
                history = "\n".join([f"{msg['role']}: {msg['content']}" 
                                   for msg in conversation[:-1]])
                
                formatted_data.append({
                    "prompt": history,
                    "chosen": improved_response,
                    "rejected": original_response
                })
    
    return formatted_data

# ---------------------------------------------------------------------------
# Mock Training Functions --------------------------------------------------
# ---------------------------------------------------------------------------

def mock_instruction_tuning(dataset: List[str], model_name: str = "base_model") -> None:
    """Mock function to demonstrate instruction tuning."""
    print(f"\n=== Instruction Tuning Demonstration ({model_name}) ===")
    print(f"Dataset size: {len(dataset)} examples")
    
    # Show a sample of the dataset
    if dataset:
        print("\nSample training example:")
        print(f"{dataset[0][:500]}...")
    
    # Mock training process
    print("\nTraining process:")
    print("1. Loading base model and tokenizer...")
    time.sleep(0.5)
    print("2. Preparing dataset and data collator...")
    time.sleep(0.5)
    print("3. Configuring training arguments (LoRA)...")
    time.sleep(0.5)
    print("4. Starting fine-tuning...")
    
    # Mock training progress
    steps = 5
    for i in range(steps):
        time.sleep(0.3)
        loss = 2.0 - (i * 0.3)
        print(f"   Epoch 1, Step {i+1}/{steps}: loss={loss:.4f}")
    
    print("5. Training complete!")
    print(f"6. Saving fine-tuned model to {model_name}_agent_tuned...")
    
    if HAS_TORCH:
        print("\nWith the actual libraries, you would use code like:")
        print("""
model = AutoModelForCausalLM.from_pretrained("base_model")
tokenizer = AutoTokenizer.from_pretrained("base_model")

# Convert examples to dataset format
dataset = Dataset.from_dict({
    "text": formatted_examples
})

# Configure training arguments
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=8,
    learning_rate=2e-5,
    weight_decay=0.01,
    save_strategy="epoch",
)

# Set up trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    data_collator=DataCollator(tokenizer=tokenizer)
)

# Train model
trainer.train()
        """)

def mock_rlhf_training(dataset: List[Dict], model_name: str = "instruction_tuned_model") -> None:
    """Mock function to demonstrate RLHF-style training."""
    print(f"\n=== RLHF Training Demonstration ({model_name}) ===")
    print(f"Dataset size: {len(dataset)} preference pairs")
    
    # Show a sample of the dataset
    if dataset:
        print("\nSample preference pair:")
        print(f"Prompt: {dataset[0]['prompt'][:100]}...")
        print(f"Chosen: {dataset[0]['chosen'][:100]}...")
        print(f"Rejected: {dataset[0]['rejected'][:100]}...")
    
    # Mock training process
    print("\nTraining process:")
    print("1. Loading instruction-tuned model...")
    time.sleep(0.5)
    print("2. Preparing reward model...")
    time.sleep(0.5)
    print("3. Configuring RL training (PPO)...")
    time.sleep(0.5)
    print("4. Starting preference optimization...")
    
    # Mock training progress
    steps = 3
    for i in range(steps):
        time.sleep(0.5)
        reward = 0.2 + (i * 0.3)
        print(f"   Step {i+1}/{steps}: reward={reward:.4f}")
    
    print("5. Training complete!")
    print(f"6. Saving RLHF-optimized model to {model_name}_rlhf...")
    
    print("\nIn a real implementation, you would use libraries like trl:")
    print("""
from trl import PPOTrainer, PPOConfig
from trl.core import respond_to_batch

# Create PPO config
ppo_config = PPOConfig(
    learning_rate=1e-5,
    batch_size=64,
    mini_batch_size=8,
    gradient_accumulation_steps=8
)

# Initialize PPO trainer
ppo_trainer = PPOTrainer(
    config=ppo_config,
    model=model,
    tokenizer=tokenizer,
    ref_model=None,
    reward_model=reward_model,
    dataset=dataset
)

# Train model
for epoch in range(ppo_config.ppo_epochs):
    for batch in ppo_trainer.dataloader:
        # Get responses from policy
        responses = respond_to_batch(
            ppo_trainer.model,
            batch["query"],
            tokenizer
        )
        
        # Compute rewards
        rewards = [
            reward_model(query, response) 
            for query, response in zip(batch["query"], responses)
        ]
        
        # Run PPO step
        stats = ppo_trainer.step(batch["query"], responses, rewards)
        ppo_trainer.log_stats(stats, batch, rewards)
    """)

# ---------------------------------------------------------------------------
# Evaluation Functions -----------------------------------------------------
# ---------------------------------------------------------------------------

def evaluate_fine_tuned_model(model_name: str, task_type: str = "all") -> Dict:
    """Mock function to evaluate a fine-tuned model."""
    print(f"\n=== Evaluating Model: {model_name} ===")
    
    # Generate mock metrics
    base_metrics = {
        "instruction_following": 0.72,
        "tool_use_accuracy": 0.65,
        "reasoning_quality": 0.68,
        "harmlessness": 0.80,
        "overall_score": 0.71
    }
    
    # Different improvement levels for different model types
    if "instruction_tuned" in model_name:
        improvement = 0.12
    elif "rlhf" in model_name:
        improvement = 0.20
    else:
        improvement = 0.05
    
    # Apply improvement to metrics
    metrics = {k: min(0.98, v + improvement) for k, v in base_metrics.items()}
    
    # Print metrics
    print("\nEvaluation metrics:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.2f}")
    
    return metrics

def compare_models(models: List[str]) -> None:
    """Compare metrics across different models."""
    print("\n=== Model Comparison ===")
    
    results = {}
    for model in models:
        results[model] = evaluate_fine_tuned_model(model)
    
    # Display comparison
    print("\nComparison table:")
    print("Metric               |", end="")
    for model in models:
        print(f" {model:20} |", end="")
    print()
    print("-" * (22 + 24 * len(models)))
    
    metrics = list(results[models[0]].keys())
    for metric in metrics:
        print(f"{metric:20} |", end="")
        for model in models:
            value = results[model][metric]
            print(f" {value:.2f}{' ' * 16} |", end="")
        print()

# ---------------------------------------------------------------------------
# Demo Functions -----------------------------------------------------------
# ---------------------------------------------------------------------------

def run_instruction_tuning_demo() -> None:
    """Run a demonstration of instruction tuning."""
    print("\n=== Instruction Tuning for Agents Demo ===")
    
    # Generate dataset
    print("Generating synthetic training data...")
    examples = create_complete_dataset(20)
    print(f"Created {len(examples)} examples")
    
    # Show example distribution
    type_counts = {}
    for example in examples:
        type_counts[example.get("type", "unknown")] = type_counts.get(example.get("type", "unknown"), 0) + 1
    
    print("\nDataset composition:")
    for type_name, count in type_counts.items():
        print(f"  {type_name}: {count} examples")
    
    # Format examples for instruction tuning
    print("\nFormatting examples for instruction tuning...")
    formatted_examples = format_for_instruction_tuning(examples)
    
    # Run mock training
    mock_instruction_tuning(formatted_examples, "base_llm")
    
    # Evaluate the mock model
    evaluate_fine_tuned_model("base_llm_agent_tuned")

def run_rlhf_demo() -> None:
    """Run a demonstration of RLHF training."""
    print("\n=== RLHF for Agent Alignment Demo ===")
    
    # Generate dataset with feedback examples
    print("Generating feedback examples...")
    examples = generate_feedback_examples(5)
    
    # Format for RLHF
    print("Formatting examples for RLHF training...")
    rlhf_dataset = format_for_rlhf(examples)
    
    # Run mock RLHF training
    mock_rlhf_training(rlhf_dataset, "instruction_tuned_model")
    
    # Evaluate the mock RLHF model
    evaluate_fine_tuned_model("instruction_tuned_model_rlhf")

def run_full_pipeline_demo() -> None:
    """Run a demonstration of the complete fine-tuning pipeline."""
    print("\n=== Complete Agent Fine-tuning Pipeline ===")
    
    # Stage 1: Generate dataset
    print("\nSTAGE 1: Dataset Preparation")
    print("---------------------------")
    print("Generating synthetic training data...")
    examples = create_complete_dataset(30)
    print(f"Created {len(examples)} examples")
    
    # Format examples
    instruction_examples = format_for_instruction_tuning(examples)
    rlhf_examples = format_for_rlhf([ex for ex in examples if ex.get("type") == AgentTuningDataTypes.FEEDBACK])
    
    # Stage 2: Instruction tuning
    print("\nSTAGE 2: Instruction Tuning")
    print("-------------------------")
    mock_instruction_tuning(instruction_examples, "base_llm")
    
    # Stage 3: RLHF
    print("\nSTAGE 3: Preference Optimization")
    print("------------------------------")
    mock_rlhf_training(rlhf_examples, "base_llm_agent_tuned")
    
    # Stage 4: Evaluation
    print("\nSTAGE 4: Comparative Evaluation")
    print("-----------------------------")
    compare_models(["base_llm", "base_llm_agent_tuned", "base_llm_agent_tuned_rlhf"])
    
    # Summary
    print("\nPipeline Summary:")
    print("""
1. Dataset Creation:
   - Instruction-following examples
   - Tool use demonstrations
   - Reasoning patterns
   - Feedback pairs

2. Instruction Fine-tuning:
   - Base model adapts to agent-specific tasks
   - Learns tool usage patterns
   - Develops improved reasoning abilities

3. Preference Optimization:
   - Model learns from human feedback
   - Reduces harmful responses
   - Aligns with human preferences

4. Evaluation:
   - Significant improvements in tool use (+25%)
   - Better reasoning quality (+22%)
   - Increased harmlessness (+18%)
   - Overall performance boost (+24%)
    """)

# ---------------------------------------------------------------------------
# Main Function ------------------------------------------------------------
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Agent Fine-tuning Demo")
    parser.add_argument("--demo", choices=["instruction", "rlhf", "full", "all"], 
                      default="all", help="Which demo to run")
    args = parser.parse_args()
    
    # Check for torch
    if not HAS_TORCH:
        print("""
Note: PyTorch, transformers, and/or datasets are not installed.
Running in demonstration mode with mock training functions.

To run actual fine-tuning, install the required libraries:
pip install torch transformers datasets
        """)
    
    print("\n===== Agent Fine-tuning Demonstration =====")
    print("This example shows methods for fine-tuning LLMs for agent applications.")
    
    # Run the appropriate demo
    if args.demo in ["instruction", "all"]:
        run_instruction_tuning_demo()
    
    if args.demo in ["rlhf", "all"]:
        run_rlhf_demo()
    
    if args.demo in ["full", "all"]:
        run_full_pipeline_demo()
    
    # Conclusion
    print("\n===== Key Takeaways =====")
    print("""
1. Agent fine-tuning requires specialized datasets that include:
   - Tool use demonstrations
   - Reasoning patterns
   - Safety considerations
   - Multi-turn interactions

2. The fine-tuning process typically involves multiple stages:
   - Instruction tuning for basic capabilities
   - RLHF or preference learning for alignment
   - Specialized optimization for tool use

3. Evaluation should use agent-specific metrics:
   - Tool use accuracy
   - Planning and reasoning abilities
   - Safety and alignment
   - Task completion success rates

4. Even with limited computational resources, focused fine-tuning
   on specific agent capabilities can yield significant improvements.
""")

if __name__ == "__main__":
    main() 