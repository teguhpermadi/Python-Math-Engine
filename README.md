# Python Math Engine

Deterministic mathematical microservice for Computer-Based Testing (CBT) systems.

## Features

- **Deterministic Generation**: Same seed + same parameters = same question.
- **Multi-Domain**: Arithmetic, Geometry (2D/3D), Measurement, Algebra, and Statistics.
- **AI Storyteller**: Contextual word problems using LM Studio (OpenAI-compatible).
- **Exam Generator**: Create mixed-domain exam papers in a single request.
- **Visualization Ready**: Provides 3D mesh data and 2D drawing coordinates.

## Installation

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Configure environment variables in `.env`:
    ```ini
    LM_STUDIO_URL="https://your-ai-url/v1"
    LM_TIMEOUT_SECONDS=60
    ```

## Usage

Start the server:
```bash
fastapi dev app/main.py
```

Access API Documentation at `http://localhost:8000/docs`.

### Example: Generate Mixed Exam
Endpoint: `POST /api/v1/exam/generate`
```json
{
  "master_seed": 12345,
  "requirements": [
    {"domain": "arithmetic", "operation": "addition", "level": 1},
    {"domain": "geometry", "shape": "cube", "level": 2},
    {"domain": "algebra", "level": 3}
  ]
}
```

## Testing

Run the formal test suite:
```bash
pytest
```
