# Historical-Dialog-Modeling

Telegram-бот для моделирования диалогов с историческими личностями с учётом:
- речевых паттернов конкретной личности;
- стилистики эпохи;
- региональных диалектных особенностей.

Доступные персоны: Пётр I, Екатерина II, Уинстон Черчилль.

Бот доступен по имени @echoofages1_bot

## Функциональность
- Выбор исторической личности через inline-кнопки в Telegram.
- Ведение контекстного диалога в рамках выбранной персоны.
- Сброс контекста и повторный выбор персоны.
- Интеграция с LLM API (OpenAI-совместимый формат, по умолчанию Mistral).

## Технологии
- Python 3.11+
- aiogram 3
- aiohttp
- aiohttp-socks (для работы через прокси)

## Быстрый старт
1. Перейдите в папку проекта:
   ```bash
   cd ~/Desktop/Historical-Dialog-Modeling
   ```
2. Создайте виртуальное окружение и активируйте его:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   pip install aiohttp-socks
   ```
4. Создайте `.env` и заполните переменные:
   ```env
   TELEGRAM_BOT_TOKEN=...
   LLM_API_URL=https://api.mistral.ai/v1/chat/completions
   LLM_API_TOKEN=...
   LLM_MODEL=mistral-small-latest
   ```
5. Запустите бота:
   ```bash
   python -m bot.main
   ```

> Если Telegram недоступен напрямую, задайте переменную окружения `https_proxy` —
> бот подхватит прокси автоматически.

## Команды бота
- `/start` - выбрать историческую личность.
- `/personas` - показать список доступных персон.
- `/reset` - очистить историю диалога.
- `/help` - справка.

## Структура проекта
```
Historical-Dialog-Modeling/
├── bot/
│   ├── __init__.py
│   ├── config.py
│   ├── handlers.py
│   ├── keyboards.py
│   ├── llm_client.py
│   ├── main.py
│   ├── personas.py
│   └── state.py
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```
