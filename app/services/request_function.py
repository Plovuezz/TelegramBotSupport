REQUEST_FUNCTION = {
    "type": "function",
    "function": {
        "name": "create_request",
        "description": "Структурує текст заявки у поля title, description, contact, meta.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Короткий заголовок заявки.",
                },
                "description": {
                    "type": "string",
                    "description": "Детальний опис проблеми або запиту.",
                },
                "contact": {
                    "type": "string",
                    "description": "Контакт для звʼязку (телефон, email або @username).",
                },
                "meta": {
                    "type": "object",
                    "description": "Додаткові структуровані поля (наприклад: product).",
                },
            },
            "required": ["description"],
        },
    },
}