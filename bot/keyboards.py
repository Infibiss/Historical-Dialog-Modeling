from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .personas import PERSONAS


def personas_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=persona.display_name, callback_data=f"persona:{persona.id}")]
        for persona in PERSONAS.values()
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
