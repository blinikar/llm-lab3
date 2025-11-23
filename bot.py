import logging

from telegram import (
    Update
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from ai import (
    analyze_message_sent
)
from helpers import get_command_args, reply_error
from config import TELEGRAM_API_TOKEN

BOT_TOKEN = TELEGRAM_API_TOKEN
logging.basicConfig(level=logging.INFO)

user_context = {}
alarms_context = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я бот для анализа эффективности сотрудников колл-центра.\n\n"
        "ВНИМАНИЕ! Данный бот носит лишь рекомендательный характер и не проходил сертификацию.\n\n"
        "/profile М 22 180 80 — установить пол мужск. возраст 22 рост 180 см и вес 80 кг\n"
        "/alarm Парацетамол 13.00 — установить напоминание о таблетке парацетамол в 13.00\n"
        "Или напишите что вы хотите спросить"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Я помогаю работать с твоим здоровьем.\n\n"
        "Доступные команды:\n"
        "/start — главное меню\n"
        "/profile М 22 180 80 — установить рост 180 см и вес 80 кг\n"
        "/alarm Парацетамол 13.00 — установить напоминание о таблетке парацетамол в 13.00\n"
        "/help — справка"
    )

async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command_args = get_command_args(update.message.text)
    user_id = update.message.from_user.id

    if len(command_args) != 4:
        await reply_error(update, 'Комманда введена неправильно:\n/profile <SEX> <AGE> <HEIGHT> <WEIGHT>\nПРИМЕР: /profile М 22 180 80')
        return

    sex = command_args[0]
    age = command_args[1]
    height = command_args[2]
    weight = command_args[3]

    user_context[user_id] = {
        'sex': sex,
        'age': age,
        'weight': weight,
        'height': height
    }

    await update.message.reply_text(
        f"Установлен пол {sex} возраст {age} рост {height} см и вес {weight} кг\n\n"
        "Теперь вы можете написать сообщение о том что хотите спросить"
    )

async def alarm_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command_args = get_command_args(update.message.text)
    user_id = update.message.from_user.id

    if len(command_args) != 2:
        await reply_error(update, 'Комманда введена неправильно:\n/alarm <DRUG_NAME> <TIME>\nПРИМЕР: /alarm Парацетамол 13:00')
        return

    drug = command_args[0]
    time = command_args[1]

    alarms_context[time] = {
        'drug': drug,
        'user_id': user_id
    }

    await update.message.reply_text(
        f"Установлено напоминание принять {drug} в {time}"
    )
    await update.message.reply_text(
        f"Напоминание. Примите {drug}"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    user_id = update.message.from_user.id

    if user_id not in user_context:
        await reply_error(update, 'Не установлен рост и вес, для установки:\n/profile <HEIGHT> <WEIGHT>\nПРИМЕР: /profile 180 80')
        return

    sex = user_context[user_id]['sex']
    age = user_context[user_id]['age']
    height = user_context[user_id]['height']
    weight = user_context[user_id]['weight']

    sent_message = await update.message.reply_text(
        f"🧠 Выполняется анализ... Пожалуйста, подождите несколько минут."
    )

    try:
        result_text = analyze_message_sent(sex=sex, age=age, height=height, weight=weight, text=message)

        await sent_message.edit_text(
            f"✅ Анализ завершён для параметров: пол {sex}, возраст {age} лет, рост {height} см, вес {weight} кг\nВНИМАНИЕ\\! Данный бот не проходил сертификацю и не может использоваться для диагностики\\!\n\n{result_text}", 
            parse_mode="HTML"
        )

    except Exception as e:
        logging.exception(e)
        await sent_message.edit_text(
            f"⚠️ Произошла ошибка при анализе данных. Проверьте корректность данных и попробуйте снова. {str(e)}"
        )

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("profile", profile_command))
    application.add_handler(CommandHandler("alarm", alarm_command))
    application.add_handler(MessageHandler(filters=filters.TEXT, callback=handle_message))

    logging.info("🤖 Бот запущен...")
    application.run_polling()


if __name__ == "__main__":
    main()
