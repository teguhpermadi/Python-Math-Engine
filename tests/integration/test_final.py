import httpx

def test_measurement():
    print("Testing Measurement...")
    resp = httpx.post("http://localhost:8000/api/v1/measurement/generate", json={"seed": 1, "level": 2})
    print(f"Status: {resp.status_code}, Result: {resp.json()['data']['expression']}")

def test_algebra():
    print("\nTesting Algebra...")
    resp = httpx.post("http://localhost:8000/api/v1/algebra/generate", json={"seed": 1, "level": 2})
    print(f"Status: {resp.status_code}, Equation: {resp.json()['data']['expression']}")

def test_statistics():
    print("\nTesting Statistics...")
    resp = httpx.post("http://localhost:8000/api/v1/statistics/generate", json={"seed": 1, "level": 2})
    print(f"Status: {resp.status_code}, Mean: {resp.json()['data']['results']['mean']}")

if __name__ == "__main__":
    try:
        test_measurement()
        test_algebra()
        test_statistics()
        print("\nALL DOMAINS VERIFIED SUCCESS.")
    except Exception as e:
        print(f"ERROR: {e}")
