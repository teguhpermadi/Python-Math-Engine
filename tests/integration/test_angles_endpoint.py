import httpx
import json

def test_angles_complementary():
    url = "http://localhost:8000/api/v1/angles/generate"
    payload = {
        "seed": 123,
        "level": 3,
        "type": "complementary"
    }
    
    print("Testing Complementary Angles & Drawing Data...")
    resp = httpx.post(url, json=payload)
    print(f"Status: {resp.status_code}")
    data = resp.json()
    
    print(f"Expression: {data['data']['expression']}")
    print(f"Drawing Points: {list(data['data']['drawing_data']['points'].keys())}")
    
    assert data['meta']['type'] == "complementary"
    assert "drawing_data" in data['data']
    print("SUCCESS: Complementary angles verified.")

def test_parallel_lines():
    url = "http://localhost:8000/api/v1/angles/generate"
    payload = {
        "seed": 123,
        "level": 5,
        "type": "parallel_lines"
    }
    
    print("\nTesting Parallel Lines Relationships...")
    resp = httpx.post(url, json=payload)
    print(f"Status: {resp.status_code}")
    data = resp.json()
    print(f"Expression: {data['data']['expression']}")
    assert "parallel_lines" in data['meta']['type']
    print("SUCCESS: Parallel lines verified.")

if __name__ == "__main__":
    try:
        test_angles_complementary()
        test_parallel_lines()
    except Exception as e:
        print(f"ERROR: {e}")
