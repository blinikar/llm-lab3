from telegram import (
    Update,
)

def get_command_args(message_text: str):
    return message_text.split(' ')[1:]

async def reply_error(update: Update, error_text: str):
    await update.message.reply_text(
        "🚨 Произошла ошибка! .\n\n"
        f"{error_text}\n\n"
        "Доступные команды:\n"
        "/start — главное меню\n"
        "/help — справка\n"
        "/profile — профиль"
    )