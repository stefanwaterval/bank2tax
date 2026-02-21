from typing import Any

import requests


class OllamaClient:
    def __init__(self, base_url: str, model: str, timeout_s: float = 120.0) -> None:
        self.base_url = base_url
        self.model = model
        self.timeout_s = timeout_s

    def invoke(self, messages: list[dict[str, str]], schema: dict[str, Any]) -> str:
        url = self.base_url.strip() + "/api/chat"

        body: dict[str, Any] = {
            "model": self.model,
            "stream": False,
            "messages": messages,
        }
        body["format"] = schema

        response = requests.post(url, json=body, timeout=self.timeout_s)
        response.raise_for_status()
        data = response.json()

        return data["message"]["content"]
