import pytest

from app.operations import calculate


@pytest.mark.parametrize(
    ("operation_type", "expected"),
    [
        ("Add", 7),
        ("Sub", 3),
        ("Multiply", 10),
        ("Divide", 2.5),
    ],
)
def test_calculate_dispatches_to_requested_operation(operation_type, expected):
    assert calculate(5, 2, operation_type) == expected


def test_calculate_rejects_unsupported_operation():
    with pytest.raises(ValueError, match="Unsupported calculation type"):
        calculate(5, 2, "modulus")
