"""
Few-Shot Prompting Strategy
Include k examples in the prompt to guide the model.
Test with k=3 and k=5 examples.
"""

EXAMPLES = [
    {
        "query": "Looking for comfortable running shoes",
        "products": "Nike Air Max (White Sports Shoes), Adidas Ultraboost (Black Running Shoes), Puma RS-X (Grey Sneakers)",
        "response": "For comfortable running, I'd recommend the **Adidas Ultraboost** - they're specifically designed for running with excellent cushioning and support. The Nike Air Max is also great for casual athletic wear. If you want a more stylish option for light jogging and everyday use, the Puma RS-X offers a trendy look with decent comfort."
    },
    {
        "query": "Need a formal shirt for office",
        "products": "Van Heusen White Formal Shirt, Arrow Blue Striped Shirt, Peter England Slim Fit Grey Shirt",
        "response": "For the office, the **Van Heusen White Formal Shirt** is a classic choice that pairs with any suit. If you want subtle personality, the **Arrow Blue Striped Shirt** adds visual interest while staying professional. The Peter England Grey option works well for a modern, minimalist office aesthetic."
    },
    {
        "query": "Weekend casual look",
        "products": "Levi's Denim Jacket, H&M Basic Tee (White), Zara Chinos (Beige)",
        "response": "Perfect weekend combo! Layer the **Levi's Denim Jacket** over the **H&M Basic White Tee** for that effortless cool vibe. The **Zara Beige Chinos** tie it together - comfortable yet put-together. Roll up the chinos slightly and add sneakers for the complete casual weekend look."
    },
    {
        "query": "Summer beach outfit",
        "products": "Tommy Hilfiger Swim Shorts (Navy), Ray-Ban Sunglasses, Havaianas Flip Flops",
        "response": "Beach-ready! The **Tommy Hilfiger Navy Swim Shorts** are versatile for swimming and walking around. Protect your eyes with **Ray-Ban Sunglasses** - a timeless choice. Complete with **Havaianas Flip Flops** for easy on-and-off at the beach. Add a light linen shirt for the boardwalk."
    },
    {
        "query": "Gym workout clothes",
        "products": "Under Armour Compression Tee, Nike Dri-Fit Shorts, Reebok Training Shoes",
        "response": "Great gym setup! The **Under Armour Compression Tee** supports your muscles and wicks sweat during intense workouts. **Nike Dri-Fit Shorts** keep you cool and allow full range of motion. The **Reebok Training Shoes** provide stability for weightlifting and cardio. You're all set for a productive session!"
    }
]

FEW_SHOT_SYSTEM = """You are a professional fashion advisor for StyleSync. 
Learn from the following examples of how to provide helpful, specific fashion advice."""

def get_prompt(query: str, products: list, k: int = 3) -> dict:
    """Generate few-shot prompt with k examples."""
    # Format products
    products_text = "\n".join([
        f"- {p.get('productDisplayName', 'Unknown')} ({p.get('baseColour', '')} {p.get('articleType', '')})"
        for p in products
    ])
    
    # Build examples section
    selected_examples = EXAMPLES[:k]
    examples_text = "\n\n".join([
        f"Example {i+1}:\nQuery: {ex['query']}\nProducts: {ex['products']}\nResponse: {ex['response']}"
        for i, ex in enumerate(selected_examples)
    ])
    
    user_prompt = f"""{examples_text}

Now provide advice for this query:
Query: {query}
Products:
{products_text}

Response:"""
    
    return {
        "system": FEW_SHOT_SYSTEM,
        "user": user_prompt,
        "strategy": f"few_shot_k{k}"
    }
