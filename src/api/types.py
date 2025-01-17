# mypy: ignore-errors

"""Types for the API."""

from pydantic import BaseModel


class HealthRouteOutput(BaseModel):
    """Model for the health route output."""

    status: str
