from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class UserSession:
    persona_id: str | None = None
    history: list[dict[str, str]] = field(default_factory=list)


class SessionStore:
    def __init__(self, max_history_messages: int = 12) -> None:
        self._store: dict[int, UserSession] = {}
        self._max_history_messages = max_history_messages

    def get(self, user_id: int) -> UserSession:
        return self._store.setdefault(user_id, UserSession())

    def set_persona(self, user_id: int, persona_id: str) -> None:
        session = self.get(user_id)
        session.persona_id = persona_id
        session.history.clear()

    def reset(self, user_id: int) -> None:
        self._store[user_id] = UserSession()

    def append_message(self, user_id: int, role: str, content: str) -> None:
        session = self.get(user_id)
        session.history.append({"role": role, "content": content})
        if len(session.history) > self._max_history_messages:
            session.history = session.history[-self._max_history_messages :]

    def compose_messages(self, user_id: int, system_prompt: str, user_text: str) -> list[dict[str, Any]]:
        session = self.get(user_id)
        messages: list[dict[str, Any]] = [{"role": "system", "content": system_prompt}]
        messages.extend(session.history)
        messages.append({"role": "user", "content": user_text})
        return messages
