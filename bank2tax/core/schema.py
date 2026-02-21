from typing import List

from pydantic import BaseModel, Field


class ExtractedAccount(BaseModel):
    iban: str | None = Field(
        default=None,
        description="International Bank Account Number",
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
    source_file: str
    accounts: List[ExtractedAccount]
