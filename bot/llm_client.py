from __future__ import annotations

import aiohttp


class LLMClientError(RuntimeError):
    pass


class LLMClient:
    def __init__(self, api_url: str, api_token: str, model: str, timeout_seconds: int = 45) -> None:
        self._api_url = api_url
        self._api_token = api_token
        self._model = model
        self._timeout = aiohttp.ClientTimeout(total=timeout_seconds)

    async def chat_completion(self, messages: list[dict[str, str]]) -> str:
        headers = {
            "Authorization": f"Bearer {self._api_token}",
            "Content-Type": "application/json",
        }
        payload = {"model": self._model, "messages": messages}

        async with aiohttp.ClientSession(timeout=self._timeout) as session:
            async with session.post(self._api_url, headers=headers, json=payload) as response:
                if response.status >= 400:
                    body = await response.text()
                    raise LLMClientError(f"LLM API error {response.status}: {body}")
                data = await response.json()

        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMClientError("Unexpected response format from LLM API") from exc
