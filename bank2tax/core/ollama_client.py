from typing import Any

import requests


class OllamaClient:
    """Lightweight client for interacting with an Ollama chat model."""

    def __init__(
        self,
        base_url: str,
        model: str,
        temperature: float = 0.0,
        timeout_s: float = 120.0,
    ) -> None:
        """Initialize the Ollama client.

        Args:
            base_url: Base URL of the Ollama server.
            model: Name of the model to use.
            temperature: Sampling temperature for generation.
            timeout_s: Request timeout in seconds.
        """
        self.base_url = base_url
        self.model = model
        self.temperature = temperature
        self.timeout_s = timeout_s

    def invoke(self, messages: list[dict[str, str]], schema: dict[str, Any]) -> str:
        """Send a chat request to Ollama with an optional JSON schema.

        Args:
            messages: Chat messages in Ollama format.
            schema: JSON schema describing the expected output format.
        """
        url = self.base_url.strip() + "/api/chat"

        body: dict[str, Any] = {
            "model": self.model,
            "stream": False,
            "messages": messages,
            "options": {"temperature": self.temperature},
        }
        body["format"] = schema

        response = requests.post(url, json=body, timeout=self.timeout_s)
        response.raise_for_status()
        data = response.json()

        return data["message"]["content"]
