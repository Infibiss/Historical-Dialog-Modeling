from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(slots=True)
class Settings:
    telegram_bot_token: str
    llm_api_url: str
    llm_api_token: str
    llm_model: str
    max_history_messages: int
    request_timeout_seconds: int



def load_settings() -> Settings:
    load_dotenv()

    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not telegram_bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set")

    return Settings(
        telegram_bot_token=telegram_bot_token,
        llm_api_url=os.getenv(
            "LLM_API_URL",
            "https://evgeniymuravyov.pythonanywhere.com/v1/chat/completions",
        ).strip(),
        llm_api_token=os.getenv("LLM_API_TOKEN", "").strip(),
        llm_model=os.getenv("LLM_MODEL", "models/gemini-3-flash-preview").strip(),
        max_history_messages=int(os.getenv("MAX_HISTORY_MESSAGES", "12")),
        request_timeout_seconds=int(os.getenv("REQUEST_TIMEOUT_SECONDS", "45")),
    )
