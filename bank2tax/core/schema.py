from typing import List

from pydantic import BaseModel, Field


class ExtractedAccount(BaseModel):
    """Structured representation of a single bank account."""

    account_number: str | None = Field(
        default=None,
        description="Bank Account Number",
    )
    ending_balance: float | None = Field(
        default=None,
        description="Ending account balance",
    )
    currency: str | None = Field(
        default=None,
        description="Currency of the ending balance (e.g., CHF, EUR)",
    )
    institution: str | None = Field(
        default=None,
        description="Name of the financial institution",
    )


class ExtractedDocument(BaseModel):
    """Structured representation of extracted data from one document."""

    source_file: str
    accounts: List[ExtractedAccount]
