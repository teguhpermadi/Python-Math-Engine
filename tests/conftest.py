"""Pytest fixtures bersama untuk seluruh test suite math-engine.

Menggunakan fastapi.testclient.TestClient (in-process) sehingga test
tidak bergantung pada server uvicorn eksternal maupun port tertentu.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    """Klien HTTP in-process untuk memanggil API tanpa jaringan."""
    with TestClient(app) as c:
        yield c
