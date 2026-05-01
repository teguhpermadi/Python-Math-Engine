import httpx
import json

def test_geometry_generate():
    url = "http://localhost:8000/api/v1/geometry/generate"
    payload = {
        "seed": 777,
        "level": 3,
        "shape": "cube",
        "with_story": False
    }
    
    print("Testing Geometry Mesh Generation...")
    resp = httpx.post(url, json=payload)
    print(f"Status: {resp.status_code}")
    data = resp.json()
    
    print(f"Shape: {data['meta']['shape']}")
    print(f"Vertices Count: {len(data['data']['mesh']['vertices'])}")
    print(f"Expression: {data['data']['expression']}")
    
    assert data['meta']['shape'] == "cube"
    assert len(data['data']['mesh']['vertices']) == 8
    print("SUCCESS: Geometry mesh is correct.")

def test_level_discovery():
    url = "http://localhost:8000/api/v1/arithmetic/levels/3"
    print("\nTesting Level Discovery API...")
    resp = httpx.get(url)
    print(f"Status: {resp.status_code}")
    data = resp.json()
    print(f"Allowed Number Types for Level 3: {data['allowed_number_types']}")
    assert "fraction" in data['allowed_number_types']
    print("SUCCESS: Discovery API works.")

if __name__ == "__main__":
    try:
        test_geometry_generate()
        test_level_discovery()
    except Exception as e:
        print(f"ERROR: {e}")
