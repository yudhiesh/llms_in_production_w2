from guardrails.validators import BugFreeSQL
from pydantic import BaseModel, Field


class ValidSQL(BaseModel):
    """
    A valid SQL guardrail model.
    """

    generated_sql: str = Field(
        description="Generate PostgreSQL for the given natural language instruction.",
        validators=[BugFreeSQL(on_fail="reask")],
    )
