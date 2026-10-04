"""
Integration Tests for app.py REST API
"""

import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "healthy"
    assert data["app"] == "Nibble Nanny"


def test_get_profiles_endpoint(client):
    res = client.get("/api/profiles")
    assert res.status_code == 200
    profiles = res.get_json()
    assert len(profiles) >= 4
    ids = [p["profile_id"] for p in profiles]
    assert "no_dairy" in ids
    assert "low_sugar" in ids
    assert "low_salt" in ids
    assert "jain_veg" in ids


def test_get_samples_endpoint(client):
    res = client.get("/api/samples")
    assert res.status_code == 200
    samples = res.get_json()
    assert len(samples) >= 5
    sample_ids = [s["id"] for s in samples]
    assert "parle_g" in sample_ids
    assert "maggi_noodles" in sample_ids


def test_evaluate_sample_parle_g(client):
    res = client.post("/api/sample/parle_g")
    assert res.status_code == 200
    data = res.get_json()
    assert "verdicts" in data
    assert "tricks" in data
    assert "education" in data

    # Parle-G has milk solids -> Dairy Nanny (Sneha) should SKIP
    assert data["verdicts"]["no_dairy"]["status"] == "SKIP"
    assert data["verdicts"]["no_dairy"]["avatar_emoji"] == "🥛"

    # Check that education contains milk solids
    ed_names = [e["cleaned_name"] for e in data["education"]]
    assert any("milk" in n for n in ed_names)
