from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class CalculationType(str, Enum):
    ADD = "Add"
    SUB = "Sub"
    MULTIPLY = "Multiply"
    DIVIDE = "Divide"


class CalculationBase(BaseModel):
    a: float = Field(..., allow_inf_nan=False, description="First operand")
    b: float = Field(..., allow_inf_nan=False, description="Second operand")
    type: CalculationType = Field(..., description="Arithmetic operation")

    @field_validator("type", mode="before")
    @classmethod
    def normalize_type(cls, value: object) -> object:
        if isinstance(value, str):
            for calculation_type in CalculationType:
                if value.casefold() == calculation_type.value.casefold():
                    return calculation_type
        return value

    @model_validator(mode="after")
    def reject_zero_divisor(self) -> "CalculationBase":
        if self.type == CalculationType.DIVIDE and self.b == 0:
            raise ValueError("Cannot divide by zero")
        return self

    model_config = ConfigDict(from_attributes=True)


class CalculationCreate(CalculationBase):
    pass


class CalculationRead(CalculationBase):
    id: UUID
    result: float
    created_at: datetime
    updated_at: datetime


CalculationResponse = CalculationRead
