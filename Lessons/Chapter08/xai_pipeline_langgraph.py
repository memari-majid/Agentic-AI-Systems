#!/usr/bin/env python3
"""
Chapter 8 – XAI Pipeline with LangGraph
======================================
Illustrates a *multi-step explainability pipeline*:
   1. Encode query with BERT
   2. Derive attention matrix (token-token)
   3. Compute saliency scores (token attribution)
   4. Produce a natural-language explanation stub

For brevity, heavy libraries torch/transformers are optional—when
missing we fall back to mocked payloads so the graph still runs.

Run:
    python xai_pipeline_langgraph.py --query "Family-friendly travel in Europe"

Dependencies (full mode):
    pip install -U langgraph transformers captum torch
"""
from __future__ import annotations

import argparse
import json
from typing import Dict, List, TypedDict

from langgraph.graph import StateGraph

# ---------------------------------------------------------------------------
# Attempt to import heavy deps; otherwise mock -------------------------------
# ---------------------------------------------------------------------------
try:
    import torch  # type: ignore
    from transformers import BertTokenizer, BertForSequenceClassification  # type: ignore
    from captum.attr import Saliency  # type: ignore
except ImportError:  # pragma: no cover
    torch = None  # type: ignore

# ---------------------------------------------------------------------------
# State typing ---------------------------------------------------------------
# ---------------------------------------------------------------------------
class XAIState(TypedDict, total=False):
    query: str
    tokens: List[str]
    attention: List[List[float]]
    saliency: List[float]
    explanation: str

# ---------------------------------------------------------------------------
# Nodes ----------------------------------------------------------------------
# ---------------------------------------------------------------------------

def encode_query(state: XAIState) -> XAIState:
    q = state["query"]
    if torch is None:
        state["tokens"] = q.lower().split()  # naive
    else:
        tokenizer = encode_query.tokenizer  # type: ignore
        tokens = tokenizer.tokenize(q)
        state["tokens"] = tokens  # type: ignore
    return state

# cache tokenizer/model lazily
if torch is not None:
    encode_query.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")  # type: ignore
    encode_query.model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)  # type: ignore

def compute_attention(state: XAIState) -> XAIState:
    if torch is None:
        n = len(state["tokens"])
        state["attention"] = [[0.1] * n for _ in range(n)]  # type: ignore
    else:
        tokenizer = encode_query.tokenizer  # type: ignore
        model = encode_query.model  # type: ignore
        inputs = tokenizer(state["query"], return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs, output_attentions=True)
        att = outputs.attentions[-1][0][0].tolist()
        state["attention"] = att  # type: ignore
    return state


def compute_saliency(state: XAIState) -> XAIState:
    if torch is None:
        state["saliency"] = [0.5] * len(state["tokens"])  # type: ignore
        return state

    tokenizer = encode_query.tokenizer  # type: ignore
    model = encode_query.model  # type: ignore
    inputs = tokenizer(state["query"], return_tensors='pt', truncation=True, padding=True)
    embeddings = model.get_input_embeddings()(inputs['input_ids'])
    embeddings.requires_grad_()

    def forward_fn(embeds):
        return model(inputs_embeds=embeds).logits

    sal = Saliency(forward_fn)
    scores = sal.attribute(embeddings, target=1).sum(dim=2).squeeze().tolist()
    state["saliency"] = scores  # type: ignore
    return state


def explain(state: XAIState) -> XAIState:
    salient = max(state.get("saliency", [0]), default=0)
    state["explanation"] = (
        "Key tokens drive the classification with saliency score ≈ " + f"{salient:.2f}"
    )  # type: ignore
    return state

# ---------------------------------------------------------------------------
# Build graph ----------------------------------------------------------------
# ---------------------------------------------------------------------------

def build_xai_graph() -> StateGraph:
    g = StateGraph(XAIState)
    g.add_node("encode", encode_query)
    g.add_node("attention", compute_attention)
    g.add_node("saliency", compute_saliency)
    g.add_node("explain", explain)

    g.set_entry_point("encode")
    g.add_edge("encode", "attention")
    g.add_edge("attention", "saliency")
    g.add_edge("saliency", "explain")
    g.set_finish_point("explain")
    return g

# ---------------------------------------------------------------------------
# CLI ------------------------------------------------------------------------
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="XAI pipeline demo")
    parser.add_argument("--query", required=True, help="Input text to analyse")
    args = parser.parse_args()

    init: XAIState = {"query": args.query}
    result = build_xai_graph().compile().invoke(init)

    print("\nTokens:", result.get("tokens"))
    print("Attention matrix: [truncated] rows", len(result.get("attention", [])))
    print("Saliency:", result.get("saliency"))
    print("Explanation:", result.get("explanation")) 