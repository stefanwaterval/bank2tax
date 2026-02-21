from bank2tax.core.ollama_client import OllamaClient
from bank2tax.core.schema import ExtractedDocument


class ExtractorAgent:
    def __init__(self, client: OllamaClient) -> None:
        self.client = client

    def extract(self, markdown: str, source_file: str) -> str:
        schema = ExtractedDocument.model_json_schema()

        system = (
            "You extract structured data from bank statement text.\n"
            "Statements may be written in German or French.\n"
            "Account numbers are made of 3 parts separated by '.' or '-'\n"
            "Keep the account number format EXACTLY AS IS\n"
            "Return ONLY valid JSON that matches the provided JSON Schema.\n"
            "No markdown fences, no commentary, no extra keys.\n"
            "If a value is not present in the document, set it to null.\n"
        )

        user = (
            "Extract all accounts mentioned.\n"
            "For each account, provide:\n"
            "- account_number\n"
            "- ending_balance\n"
            "- currency\n"
            "- institution\n\n"
            f"source_file: {source_file}\n\n"
            "Document (markdown):\n"
            f"{markdown}"
        )

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]

        return self.client.invoke(messages=messages, schema=schema)
