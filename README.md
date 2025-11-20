# TelegramBotSupport


# Структура проєкту
```markdown
app/
├── bot.py                     # Telegram-бот (aiogram)
├── main.py                    # FastAPI адмін-панель
├── config.py                  # Pydantic Settings
│
├── handlers/
│   └── messages.py            # Хендлери Telegram-бота
│
├── repositories/
│   └── requests.py            # Робота з таблицею requests
│
├── database/
│   ├── db.py                  # engine + sessionmaker
│   └── models/
│       ├── base.py            # Declarative Base
│       └── requests.py        # ORM-модель Request
│
├── services/
│   ├── openai_service.py      # Логіка OpenAI + Function Calling
│   ├── knowledge_service.py   # Пошук по локальній базі знань
│   ├── requests_service.py    # Детектор intent'у заявки
│   └── request_function.py    # JSON-схема OpenAI function
│
├── knowledge/
│   ├── faq.md
│   ├── policy.md
│   └── products.md
│
├── routes/                    # Роути для fast api
│   └── requests.py 
│
└── schemas/                    # Pydentic-схеми
    └── requests.py  
```

## Коротке пояснення рішення

Проєкт використовує локальну базу знань (`knowledge/*.md`) для відповіді на питання користувачів.
Під час кожного запиту бот витягує релевантні фрагменти тексту, формує з них контекст через систему score, через і передає його у OpenAI (GPT-4o-mini) разом із промтом.

Для створення заявок застосовано механіку **OpenAI Function Calling**. Коли користувач хоче залишити заявку, бот передає текст у модель разом із визначенням функції `create_request`. Модель викликає цю функцію та повертає структурований JSON із полями `title`, `description`, `contact`, `meta`. Після цього дані зберігаються в таблицю `requests` у PostgreSQL через SQLAlchemy (async), з коректною транзакційною обробкою (`commit/rollback`). Завдяки цьому у базі завжди опиняються чисті та нормалізовані заявки, незалежно від того, як саме користувач сформував текст.


## Як запустити

```aiignore
docker-compose up --build
```

---