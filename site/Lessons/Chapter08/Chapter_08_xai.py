#!/usr/bin/env python3
# Chapter 08 - Explainable AI (XAI) techniques 
# Example of how attention visualization, saliency maps, and natural language explanations 
# can be generated simply using Python

# Required dependencies:
# pip install -U torch transformers matplotlib seaborn captum openai

import torch
from transformers import BertTokenizer, BertForSequenceClassification
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Setup the model and tokenizer
def setup_model():
    """Setup the BERT model and tokenizer for XAI examples"""
    model_name = 'bert-base-uncased'
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)
    return model, tokenizer

# 2. Function to get attention scores from the model
def get_attention_scores(model, inputs):
    """Get attention scores from the model for visualization"""
    outputs = model(**inputs, output_attentions=True)
    return outputs.attentions

# 3. Function to visualize attention scores
def visualize_attention(attention_scores, tokens):
    """Visualize attention scores as a heatmap"""
    sns.set(style='whitegrid')
    fig, ax = plt.subplots(figsize=(8, 8))
    attention_layer = attention_scores[-1][0]  # Extract the last attention layer's scores
    attention_weights = attention_layer[0].detach().numpy()  # Convert attention scores to numpy array for plotting

    # Plot the attention heatmap
    sns.heatmap(attention_weights, xticklabels=tokens, yticklabels=tokens, cmap="viridis", ax=ax)
    plt.title("Attention Visualization")
    plt.tight_layout()
    plt.show()

# 4. Saliency Map Visualization
def setup_saliency():
    """Import the necessary library for saliency map visualization"""
    try:
        from captum.attr import Saliency
        return Saliency
    except ImportError:
        print("The captum library is required for saliency visualization.")
        print("Please install with: pip install captum")
        return None

def visualize_saliency(sentence, model, tokenizer):
    """Visualize the importance of each token using saliency maps"""
    Saliency = setup_saliency()
    if Saliency is None:
        return
    
    # Step 1: Tokenize the input sentence
    inputs = tokenizer(sentence, return_tensors='pt', truncation=True, padding=True)
    input_ids = inputs['input_ids']
    attention_mask = inputs['attention_mask']

    # Step 2: Ensure the model is in evaluation mode
    model.eval()
    
    # Step 3: Get embeddings and enable gradient tracking
    embeddings = model.get_input_embeddings()(input_ids).requires_grad_()

    # Step 4: Define a custom forward function for the model
    def forward_with_logits(embeddings):
        return model(inputs_embeds=embeddings, attention_mask=attention_mask).logits

    # Step 5: Initialize Saliency and compute the saliency scores
    saliency = Saliency(forward_with_logits)
    saliency_scores = saliency.attribute(embeddings, target=1)

    # Step 6: Convert token IDs back to human-readable tokens
    tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
    
    # Step 7: Aggregate the saliency scores for visualization
    saliency_scores = saliency_scores.sum(dim=2).squeeze()

    # Step 8: Visualize the saliency map
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(tokens)), saliency_scores.detach().numpy(), tick_label=tokens, color='teal')
    plt.xticks(rotation=45)
    plt.title("Saliency Map")
    plt.tight_layout()
    plt.show()

# 5. Natural Language Explanations
def generate_explanation_with_openai(text, api_key=None):
    """Generate a natural language explanation using OpenAI API"""
    try:
        from openai import OpenAI
        import os
    except ImportError:
        print("The openai library is required for natural language explanations.")
        print("Please install with: pip install openai")
        return "OpenAI library not available."

    if api_key is None and "OPENAI_API_KEY" not in os.environ:
        print("OpenAI API key not provided.")
        return "OpenAI API key not provided. Please provide an API key or set the OPENAI_API_KEY environment variable."

    # Initialize the OpenAI client
    if api_key:
        client = OpenAI(api_key=api_key)
    else:
        client = OpenAI()  # Uses API key from environment variable

    # Use the OpenAI client to generate an explanation
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an explainability assistant."},
                {"role": "user", "content": f"Explain why '{text}' is important in the context of travel."}
            ]
        )
        explanation = response.choices[0].message.content
        return explanation
    except Exception as e:
        return f"Error generating explanation: {str(e)}"

# 6. Main function to demonstrate XAI techniques
def main(openai_api_key=None):
    """Main function to demonstrate XAI techniques"""
    print("Initializing BERT model for XAI examples...")
    model, tokenizer = setup_model()
    
    # Example travel query for analysis
    travel_query = "What are the best family-friendly travel destinations in Europe?"
    print(f"\nAnalyzing query: '{travel_query}'\n")
    
    # Process the input
    inputs = tokenizer(travel_query, return_tensors="pt", truncation=True, padding=True)
    input_ids = inputs['input_ids']
    tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
    
    # Attention visualization
    print("1. Generating attention visualization...")
    attention_scores = get_attention_scores(model, inputs)
    visualize_attention(attention_scores, tokens)
    
    # Saliency maps
    print("\n2. Generating saliency map visualization...")
    visualize_saliency(travel_query, model, tokenizer)
    
    # Natural language explanations (requires OpenAI API key)
    print("\n3. Generating natural language explanation...")
    if openai_api_key:
        explanation = generate_explanation_with_openai(travel_query, openai_api_key)
        print(f"\nExplanation:\n{explanation}")
    else:
        print("Skipping natural language explanation. Provide an OpenAI API key to test this feature.")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Demonstrate XAI techniques for language models')
    parser.add_argument('--openai_key', type=str, help='OpenAI API key for natural language explanations')
    args = parser.parse_args()
    
    main(args.openai_key) 