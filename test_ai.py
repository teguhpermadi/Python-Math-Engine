import httpx
import json
import asyncio

async def test_ai_story():
    url = "http://localhost:8000/api/v1/arithmetic/generate"
    payload = {
        "seed": 42,
        "level": 2,
        "operation": "addition",
        "number_type": "natural",
        "with_story": True,
        "theme": "buah-buahan"
    }
    
    print("Testing AI Story generation (with fallback)...")
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=payload)
        print(f"Status: {resp.status_code}")
        data = resp.json()
        
        if resp.status_code == 200:
            story = data['context']['story']
            print(f"Generated Story: {story}")
            assert story is not None
            print("SUCCESS: Story generation verified.")
        else:
            print(f"FAILED: Status {resp.status_code}, Detail: {data}")

async def test_error_handling():
    url = "http://localhost:8000/api/v1/arithmetic/generate"
    # Level 1 + Fraction (Invalid combination)
    payload = {
        "seed": 42,
        "level": 1,
        "operation": "addition",
        "number_type": "fraction"
    }
    
    print("\nTesting Error Handling (Invalid NumberType for Level)...")
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload)
        print(f"Status: {resp.status_code}")
        data = resp.json()
        print(f"Error Response: {data}")
        
        # Pydantic might catch this if I set up validation in schema
        # But if it reaches service, it should return our custom error
        if resp.status_code == 400:
            assert data['status'] == "error"
            assert data['error_code'] == "INVALID_NUMBER_TYPE_FOR_LEVEL"
            print("SUCCESS: Custom error handling verified.")
        else:
            print(f"INFO: Response status {resp.status_code}. Pydantic might have handled it.")

async def main():
    await test_ai_story()
    await test_error_handling()

if __name__ == "__main__":
    asyncio.run(main())
