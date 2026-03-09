from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from .keyboards import personas_keyboard
from .llm_client import LLMClient, LLMClientError
from .personas import PERSONAS
from .state import SessionStore

router = Router()
logger = logging.getLogger(__name__)

SESSION_STORE: SessionStore | None = None
LLM_CLIENT: LLMClient | None = None


def setup_dependencies(session_store: SessionStore, llm_client: LLMClient) -> None:
    global SESSION_STORE, LLM_CLIENT
    SESSION_STORE = session_store
    LLM_CLIENT = llm_client


def _deps() -> tuple[SessionStore, LLMClient]:
    if SESSION_STORE is None or LLM_CLIENT is None:
        raise RuntimeError("Dependencies are not configured")
    return SESSION_STORE, LLM_CLIENT


@router.message(Command("start"))
async def start_cmd(message: Message) -> None:
    await message.answer(
        "Выберите историческую личность для диалога:",
        reply_markup=personas_keyboard(),
    )


@router.message(Command("personas"))
async def personas_cmd(message: Message) -> None:
    await message.answer(
        "Доступные персоны:",
        reply_markup=personas_keyboard(),
    )


@router.message(Command("reset"))
async def reset_cmd(message: Message) -> None:
    store, _ = _deps()
    if message.from_user is None:
        return
    store.reset(message.from_user.id)
    await message.answer(
        "Контекст сброшен. Выберите персону заново:",
        reply_markup=personas_keyboard(),
    )


@router.message(Command("help"))
async def help_cmd(message: Message) -> None:
    text = (
        "Команды:\n"
        "/start - выбрать историческую личность\n"
        "/personas - показать список персон\n"
        "/reset - очистить историю диалога\n\n"
        "После выбора персоны просто отправляйте сообщения в чат."
    )
    await message.answer(text)


@router.callback_query(F.data.startswith("persona:"))
async def persona_selected(callback: CallbackQuery) -> None:
    store, _ = _deps()
    if callback.from_user is None or callback.data is None:
        return

    persona_id = callback.data.split(":", maxsplit=1)[1]
    persona = PERSONAS.get(persona_id)
    if persona is None:
        await callback.answer("Неизвестная персона", show_alert=True)
        return

    store.set_persona(callback.from_user.id, persona_id)
    await callback.answer()
    if callback.message is not None:
        await callback.message.answer(
            f"Вы выбрали: {persona.display_name}.\n"
            "Теперь задайте вопрос или начните диалог."
        )


@router.message(F.text)
async def dialogue(message: Message) -> None:
    store, llm = _deps()

    if message.from_user is None or message.text is None:
        return

    user_id = message.from_user.id
    session = store.get(user_id)
    if session.persona_id is None:
        await message.answer(
            "Сначала выберите историческую личность:",
            reply_markup=personas_keyboard(),
        )
        return

    persona = PERSONAS.get(session.persona_id)
    if persona is None:
        store.reset(user_id)
        await message.answer(
            "Персона не найдена. Выберите другую:",
            reply_markup=personas_keyboard(),
        )
        return

    messages = store.compose_messages(
        user_id=user_id,
        system_prompt=persona.system_prompt(),
        user_text=message.text,
    )

    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

    try:
        answer = await llm.chat_completion(messages)
    except LLMClientError as exc:
        logger.exception("LLM request failed: %s", exc)
        await message.answer(
            "Не удалось получить ответ от языковой модели. Попробуйте еще раз через несколько секунд."
        )
        return

    store.append_message(user_id, "user", message.text)
    store.append_message(user_id, "assistant", answer)

    await message.answer(answer)
