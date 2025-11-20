
def is_request_intent(text: str) -> bool:
    text = text.lower()
    keywords = ["заявк", "консультац", "допомог", "звʼязатися", "зв'язатися"]
    return any(k in text for k in keywords)
