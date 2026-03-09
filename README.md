# Historical-Dialog-Modeling

Telegram-бот для моделирования диалогов с историческими личностями с учетом:
- речевых паттернов конкретной личности;
- стилистики эпохи;
- региональных диалектных особенностей.

## Функциональность
- Выбор исторической личности через inline-кнопки в Telegram.
- Ведение контекстного диалога в рамках выбранной персоны.
- Сброс контекста и повторный выбор персоны.
- Интеграция с LLM API через POST-запрос:
  `https://evgeniymuravyov.pythonanywhere.com/v1/chat/completions`

## Технологии
- Python 3.11+
- aiogram 3
- aiohttp

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
   ```
4. Создайте `.env`:
   ```bash
   cp .env.example .env
   ```
5. Укажите токен Telegram-бота в `.env`:
   ```env
   TELEGRAM_BOT_TOKEN=...
   ```
6. Запустите бота:
   ```bash
   python -m bot.main
   ```

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
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```
