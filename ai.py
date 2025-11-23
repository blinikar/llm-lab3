from config import OPENAI_API_TOKEN
from openai import OpenAI

def analyze_message_sent(sex: str, age: str, height: str, weight: str, text: str) -> str:
    model = "gpt-4o"

    prompt = f"""
    Ты — эксперт по здоровью. Тебе предоставлен вопрос клиента.

    Каждый вопрос содержит:
    - sex: пол
    - age: возраст
    - height: рост в см
    - weight: вес в кг

    Твоя задача:
    Ответь на вопрос клиента исползуя эти данные

    Ответ должен быть на русском языке, структурированным, без кода и таблиц, не более 150 слов. Используй HTML теги для форматирования. Ответ будет вставлен в Telegram бота, поэтому используй только поддерживаемые теги (Тег p писать не надо) (Поддерживается  <b>, <strong>, <i>, <em>, <u>, <ins>, <s>, <strike>, <code>, <pre>, and <a>) 

    Данные:

    - sex: {sex}
    - age: {age}
    - height: {height}
    - weight: {weight}

    Вопрос:
    {text}
    """

    client = OpenAI(api_key=OPENAI_API_TOKEN)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Ты — эксперт по здоровью."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=300
    )
    return response.choices[0].message.content.strip()
