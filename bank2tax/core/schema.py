from typing import List

from pydantic import BaseModel, Field


class ExtractedAccount(BaseModel):
    iban: str = Field(..., description="International Bank Account Number")
    ending_balance: float = Field(..., description="Ending account balance")
    currency: str = Field(
        ..., description="Currency of the ending balance (e.g., CHF, EUR)"
    )
    institution: str = Field(..., description="Name of the financial institution")


class ExtractedDocument(BaseModel):
    source_file: str
    accounts: List[ExtractedAccount]
