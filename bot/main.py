from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher

from .config import load_settings
from .handlers import router, setup_dependencies
from .llm_client import LLMClient
from .state import SessionStore


async def run_bot() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    settings = load_settings()
    session_store = SessionStore(max_history_messages=settings.max_history_messages)
    llm_client = LLMClient(
        api_url=settings.llm_api_url,
        api_token=settings.llm_api_token,
        model=settings.llm_model,
        timeout_seconds=settings.request_timeout_seconds,
    )

    setup_dependencies(session_store=session_store, llm_client=llm_client)

    bot = Bot(token=settings.telegram_bot_token)
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run_bot())
