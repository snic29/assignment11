from datetime import datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.schemas.calculation import (
    CalculationCreate,
    CalculationRead,
    CalculationType,
)


@pytest.mark.parametrize(
    ("operation_type", "expected_type"),
    [
        ("Add", CalculationType.ADD),
        ("Sub", CalculationType.SUB),
        ("Multiply", CalculationType.MULTIPLY),
        ("Divide", CalculationType.DIVIDE),
        ("aDd", CalculationType.ADD),
    ],
)
def test_calculation_create_accepts_supported_operations(
    operation_type, expected_type
):
    calculation = CalculationCreate(a=8, b=2, type=operation_type)

    assert calculation.type is expected_type


@pytest.mark.parametrize(
    "data",
    [
        {"a": 8, "b": 2, "type": "modulus"},
        {"a": 8, "b": 0, "type": "Divide"},
        {"a": "not a number", "b": 2, "type": "Add"},
        {"a": float("inf"), "b": 2, "type": "Add"},
        {"a": 8, "type": "Add"},
    ],
)
def test_calculation_create_rejects_invalid_input(data):
    with pytest.raises(ValidationError):
        CalculationCreate(**data)


def test_calculation_read_exposes_stored_result():
    calculation = CalculationRead(
        id=uuid4(),
        a=8,
        b=2,
        type="Divide",
        result=4,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    assert calculation.result == 4
    assert calculation.type is CalculationType.DIVIDE
