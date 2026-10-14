from app import app, calculate_fee


def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_fee_normal():
    assert calculate_fee(1000) == 20


def test_fee_minimum():
    assert calculate_fee(10) == 1
