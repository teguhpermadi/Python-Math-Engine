import httpx
import json
import time

def test_api_generate():
    url = "http://localhost:8000/api/v1/arithmetic/generate"
    payload = {
        "seed": 42,
        "level": 3,
        "operation": "addition",
        "number_type": "natural",
        "operand_count": 2
    }
    
    # Run 1
    resp1 = httpx.post(url, json=payload)
    print(f"Status 1: {resp1.status_code}")
    data1 = resp1.json()
    
    # Run 2
    resp2 = httpx.post(url, json=payload)
    data2 = resp2.json()
    
    print(f"Expression: {data1['data']['expression']}")
    print(f"Correct Answer: {data1['data']['correct_answer']}")
    print(f"Choices: {data1['data']['answer_choices']}")
    
    assert data1 == data2
    print("SUCCESS: API result is reproducible with same seed!")

if __name__ == "__main__":
    # This assumes the server is running
    try:
        test_api_generate()
    except Exception as e:
        print(f"ERROR: {e}")
