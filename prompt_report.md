# Prompt Engineering Report

## Overview
This report summarizes the prompt engineering experiments for StyleSync's fashion RAG system.

## Prompting Strategies

### 1. Zero-Shot (Baseline)
**Structure:**
```
System: You are a professional fashion advisor for StyleSync...
User: [Query] + [Products] → Generate advice
```

**Example:**
> **Query:** "red shoes for a party"  
> **Response:** Direct fashion advice without examples

---

### 2. Few-Shot (k=3 and k=5)
**Structure:**
```
System: Learn from examples...
User: [Example 1] + [Example 2] + ... + [Query] → Generate advice
```

**Key Insight:** Testing whether more examples (k=5) improve response quality over fewer (k=3).

---

### 3. Chain-of-Thought
**Structure:**
```
System: Think step-by-step...
User: 
  1. Understand the Need
  2. Analyze Products  
  3. Match & Recommend
  4. Styling Tips
```

**Key Insight:** Encourages structured reasoning before giving advice.

---

## Evaluation Metrics

### Quantitative
| Metric | Description |
|--------|-------------|
| Cosine Similarity | Embedding similarity between generated response and ground truth |

### Qualitative (Human Rubric)
| Metric | Scale | Description |
|--------|-------|-------------|
| Factuality | 1-5 | Is the advice accurate? |
| Helpfulness | 1-5 | Is it useful for the user? |

---

## Results

| Strategy | Avg Cosine Similarity | Rank |
|----------|----------------------|------|
| **Zero-Shot** | **0.5655** | 🥇 1st |
| Few-Shot (k=5) | 0.5433 | 🥈 2nd |
| Few-Shot (k=3) | 0.5416 | 🥉 3rd |
| Chain-of-Thought | 0.4630 | 4th |

---

## Insights

### What Works Best
- **Zero-Shot is the winner**: The simple, direct prompt without examples produced responses most similar to the expected ground truth.
- **Simplicity wins**: For fashion advice, users want concise, actionable recommendations—not lengthy explanations.

### Few-Shot Analysis
- **k=5 slightly outperformed k=3**: More examples provided marginally better results (+0.0017).
- However, the improvement is minimal, suggesting diminishing returns beyond 3 examples.

### Chain-of-Thought Observations
- **Lowest similarity score**: CoT generates longer, more detailed responses.
- The step-by-step reasoning adds valuable context but diverges from the concise expected format.
- **Better for complex queries** where reasoning transparency matters more than brevity.

### Failure Cases
1. **CoT verbosity**: Responses were informative but too long compared to expected answers.
2. **Few-Shot overfitting**: Examples from different domains (e.g., sports wear) didn't always transfer well to formal attire queries.

### Recommendations
1. **Use Zero-Shot for production** - Best balance of quality and simplicity.
2. **Consider CoT for complex styling questions** where users want detailed reasoning.
3. **Keep Few-Shot examples domain-specific** if using that strategy.

---

## How to Run

```bash
# Run evaluation
python experiments/prompts/evaluate.py

# View MLflow dashboard
mlflow ui
```

## Files
- `strategies/zero_shot.py` - Baseline strategy ⭐ Recommended
- `strategies/few_shot.py` - Example-driven strategy
- `strategies/chain_of_thought.py` - Step-by-step reasoning
- `evaluate.py` - Evaluation runner
- `config.yaml` - Experiment configuration
- `data/eval.jsonl` - Evaluation dataset (20 samples)
- `evaluation_results.json` - Detailed results
