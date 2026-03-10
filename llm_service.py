import os
from typing import Dict
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole


class AetherService:
    def __init__(self):
        api_key = os.environ.get("GIGACHAT_API_KEY")
        if not api_key:
            raise ValueError(" Не найден GIGACHAT_API_KEY!")
        self.api_key = api_key
        print("GigaChat готов к работе!")

    def generate_answer(self, question: str) -> Dict:
        system_prompt = """Ты — Aether, экспертный AI-компаньон для изучения Python.
Правила:
- Отвечай на том же языке что и вопрос (русский или английский)
- Давай рабочие примеры кода в блоках ```python
- Объясняй понятно и структурировано
- Будь дружелюбным и мотивирующим
- Если есть несколько подходов — покажи лучший"""

        with GigaChat(credentials=self.api_key, verify_ssl_certs=False) as giga:
            response = giga.chat(Chat(
                messages=[
                    Messages(role=MessagesRole.SYSTEM, content=system_prompt),
                    Messages(role=MessagesRole.USER,   content=question)
                ],
                temperature=0.7,
                max_tokens=1024
            ))

        return {
            "answer":                response.choices[0].message.content,
            "sources":               [],
            "related_topics":        [],
            "recommended_resources": []
        }


TinyLlamaService = AetherService