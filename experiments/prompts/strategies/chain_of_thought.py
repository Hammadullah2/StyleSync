"""
Chain-of-Thought (CoT) Prompting Strategy
Instruct the model to reason step-by-step before providing the final answer.
"""

COT_SYSTEM = """You are a professional fashion advisor for StyleSync.
When providing advice, think through the problem step-by-step to give the best recommendations."""

COT_USER = """User Query: {query}

Retrieved Products:
{products}

Please analyze this request step-by-step:

1. **Understand the Need**: What is the user looking for? What occasion, style, or purpose?

2. **Analyze Products**: Review each retrieved product. Consider color, style, and suitability.

3. **Match & Recommend**: Which products best match the user's needs? Why?

4. **Styling Tips**: How should they wear or combine these items?

Now provide your step-by-step analysis and final recommendation:"""

def get_prompt(query: str, products: list) -> dict:
    """Generate chain-of-thought prompt for step-by-step reasoning."""
    products_text = "\n".join([
        f"- {p.get('productDisplayName', 'Unknown')} ({p.get('baseColour', '')} {p.get('articleType', '')})"
        for p in products
    ])
    
    return {
        "system": COT_SYSTEM,
        "user": COT_USER.format(query=query, products=products_text),
        "strategy": "chain_of_thought"
    }
