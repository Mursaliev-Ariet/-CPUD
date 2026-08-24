import requests
from django.conf import settings

def send_telegram_message(text, chat_id):
    """Отправляет простое сообщение (без кнопки)"""
    if not settings.BOT_TOKEN:
        print("BOT_TOKEN не задан, сообщение не отправлено")
        return

    url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        print("Сообщение отправлено в Telegram.")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке в Telegram: {e}")

def send_telegram_message_with_button(text, button_text, button_url, chat_id):
    """Отправляет сообщение с инлайн-кнопкой"""
    if not settings.BOT_TOKEN:
        print("BOT_TOKEN не задан, сообщение с кнопкой не отправлено")
        return

    url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "reply_markup": {
            "inline_keyboard": [
                [{"text": button_text, "url": button_url}]
            ]
        }
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Сообщение с кнопкой отправлено в Telegram.")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке с кнопкой: {e}")