from dotenv import dotenv_values
from openai import OpenAI
from src.config import AI_PROMPT, AI_MODEL
from src.log import log_ai

config = dotenv_values(".env")

client = OpenAI(
    base_url="https://api.deepseek.com",
    api_key=config["OPENAI_API_KEY"]
)

def ai_response(chat_id: str, question: str):
    completion = client.chat.completions.create(
        model=AI_MODEL,
        messages=[
          {"role": "system", "content": AI_PROMPT},
          {"role": "user", "content": question}
        ],
    )
    response = completion.choices[0].message.content
    log_ai(chat_id, f'AI建议回复: {response}')
    return response
