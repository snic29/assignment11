from uuid import UUID

import pytest

from app.models import Calculation


@pytest.mark.parametrize(
    ("payload", "expected"),
    [
        ({"a": 8, "b": 3, "type": "Add"}, 11),
        ({"a": 8, "b": 3, "type": "Sub"}, 5),
        ({"a": 8, "b": 3, "type": "Multiply"}, 24),
        ({"a": 8, "b": 2, "type": "Divide"}, 4),
    ],
)
def test_create_calculation_persists_values(client, db_session, payload, expected):
    response = client.post("/calculations", json=payload)

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["a"] == payload["a"]
    assert response_data["b"] == payload["b"]
    assert response_data["type"] == payload["type"]
    assert response_data["result"] == expected

    stored = db_session.get(Calculation, UUID(response_data["id"]))
    assert stored is not None
    assert (stored.a, stored.b, stored.type, stored.result) == (
        payload["a"],
        payload["b"],
        payload["type"],
        expected,
    )


@pytest.mark.parametrize(
    "payload",
    [
        {"a": 4, "b": 2, "type": "modulus"},
        {"a": 4, "b": 0, "type": "Divide"},
        {"a": "not a number", "b": 2, "type": "Add"},
    ],
)
def test_create_calculation_rejects_invalid_data(client, payload):
    response = client.post("/calculations", json=payload)

    assert response.status_code == 400
    assert "error" in response.json()
