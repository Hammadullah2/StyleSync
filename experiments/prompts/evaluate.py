"""
Prompt Evaluation Runner
Evaluates all prompting strategies against the evaluation dataset.
Logs metrics to MLflow.
"""

import os
import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import mlflow
import numpy as np
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Import strategies
from strategies import zero_shot, few_shot, chain_of_thought

load_dotenv()

# Configuration
EVAL_DATA_PATH = Path(__file__).parent.parent.parent / "data" / "eval.jsonl"
MLFLOW_EXPERIMENT = "StyleSync-Prompt-Engineering"

# Initialize models
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


def load_eval_data():
    """Load evaluation dataset."""
    data = []
    with open(EVAL_DATA_PATH, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data


def get_mock_products(query: str):
    """Get mock products for evaluation (simulating retrieval)."""
    # In production, this would use actual ChromaDB retrieval
    return [
        {"productDisplayName": f"Product A for {query[:20]}", "baseColour": "Black", "articleType": "Shoes"},
        {"productDisplayName": f"Product B for {query[:20]}", "baseColour": "Blue", "articleType": "Shirt"},
        {"productDisplayName": f"Product C for {query[:20]}", "baseColour": "White", "articleType": "Pants"},
    ]


def generate_response(prompt: dict) -> str:
    """Generate response using the LLM."""
    messages = [
        SystemMessage(content=prompt["system"]),
        HumanMessage(content=prompt["user"])
    ]
    try:
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        print(f"Error generating response: {e}")
        return ""


def compute_cosine_similarity(response: str, expected: str) -> float:
    """Compute embedding cosine similarity between response and expected."""
    if not response or not expected:
        return 0.0
    embeddings = embedding_model.encode([response, expected])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return float(similarity)


def evaluate_strategy(strategy_name: str, get_prompt_fn, eval_data: list, **kwargs) -> dict:
    """Evaluate a single prompting strategy."""
    results = []
    
    for item in eval_data:
        query = item["query"]
        expected = item["expected_response"]
        products = get_mock_products(query)
        
        # Generate prompt based on strategy
        if kwargs:
            prompt = get_prompt_fn(query, products, **kwargs)
        else:
            prompt = get_prompt_fn(query, products)
        
        # Get response
        response = generate_response(prompt)
        
        # Compute metrics
        similarity = compute_cosine_similarity(response, expected)
        
        results.append({
            "query": query,
            "response": response,
            "expected": expected,
            "similarity": similarity,
            "strategy": prompt["strategy"]
        })
    
    # Aggregate metrics
    avg_similarity = np.mean([r["similarity"] for r in results])
    
    return {
        "strategy": strategy_name,
        "avg_similarity": avg_similarity,
        "results": results
    }


def run_evaluation():
    """Run full evaluation pipeline."""
    print("Loading evaluation data...")
    eval_data = load_eval_data()
    print(f"Loaded {len(eval_data)} evaluation samples.")
    
    # Setup MLflow
    mlflow.set_experiment(MLFLOW_EXPERIMENT)
    
    strategies = [
        ("Zero-Shot", zero_shot.get_prompt, {}),
        ("Few-Shot (k=3)", few_shot.get_prompt, {"k": 3}),
        ("Few-Shot (k=5)", few_shot.get_prompt, {"k": 5}),
        ("Chain-of-Thought", chain_of_thought.get_prompt, {}),
    ]
    
    all_results = []
    
    for strategy_name, get_prompt_fn, kwargs in strategies:
        print(f"\nEvaluating: {strategy_name}...")
        
        with mlflow.start_run(run_name=strategy_name):
            results = evaluate_strategy(strategy_name, get_prompt_fn, eval_data, **kwargs)
            
            # Log to MLflow
            mlflow.log_param("strategy", strategy_name)
            mlflow.log_param("num_samples", len(eval_data))
            mlflow.log_metric("avg_cosine_similarity", results["avg_similarity"])
            
            print(f"  Average Cosine Similarity: {results['avg_similarity']:.4f}")
            all_results.append(results)
    
    # Save results for report
    output_path = Path(__file__).parent / "evaluation_results.json"
    with open(output_path, 'w') as f:
        json.dump([{
            "strategy": r["strategy"],
            "avg_similarity": r["avg_similarity"],
            "sample_results": r["results"][:3]  # First 3 samples for report
        } for r in all_results], f, indent=2)
    
    print(f"\nResults saved to {output_path}")
    print("View MLflow UI with: mlflow ui")
    
    return all_results


if __name__ == "__main__":
    run_evaluation()
