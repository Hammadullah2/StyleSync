"""
Zero-Shot Prompting Strategy (Baseline)
Simple direct prompt without examples.
"""

ZERO_SHOT_SYSTEM = """You are a professional fashion advisor for StyleSync, a clothing recommendation platform.
Your role is to provide helpful, stylish fashion advice based on the products retrieved from our catalog."""

ZERO_SHOT_USER = """User Query: {query}

Retrieved Products:
{products}

Please provide fashion advice based on these products. Be helpful, specific, and mention the product names."""

def get_prompt(query: str, products: list) -> dict:
    """Generate zero-shot prompt for the given query and products."""
    products_text = "\n".join([
        f"- {p.get('productDisplayName', 'Unknown')} ({p.get('baseColour', '')} {p.get('articleType', '')})"
        for p in products
    ])
    
    return {
        "system": ZERO_SHOT_SYSTEM,
        "user": ZERO_SHOT_USER.format(query=query, products=products_text),
        "strategy": "zero_shot"
    }
