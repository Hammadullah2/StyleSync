import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from src.app import chat_endpoint, ChatRequest

async def test():
    print("Starting test...")
    try:
        req = ChatRequest(query="red shoes")
        print(f"Sending request: {req}")
        resp = await chat_endpoint(req)
        print("Response received:")
        print(resp)
    except Exception:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
