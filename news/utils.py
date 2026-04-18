import os
from openai import OpenAI
from django.conf import settings

class AIService:
    @staticmethod
    def get_client():
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'your_openai_key_here':
            return None
        return OpenAI(api_key=api_key)

    @classmethod
    def generate_summary(cls, content):
        client = cls.get_client()
        if not client:
            return f" [Mock AI Summary] This is a professional 2-3 line summary of: {content[:50]}... summarizing the key points of the global news event."

        try:
            response = client.chat.completions.create(
                model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
                messages=[
                    {"role": "system", "content": "You are a professional news editor. Summarize the following news content in 2-3 concise, professional lines."},
                    {"role": "user", "content": content}
                ],
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"AI Error during summary: {str(e)}"

    @classmethod
    def generate_paraphrase(cls, content):
        client = cls.get_client()
        if not client:
            return f" [Mock Paraphrased Content] In simpler terms: The news discusses {content[:100]}... in easy English for better accessibility."

        try:
            response = client.chat.completions.create(
                model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
                messages=[
                    {"role": "system", "content": "You are a simplifies. Paraphrase the following news content into simple, easy-to-understand English while maintaining a professional tone. Avoid plagiarism."},
                    {"role": "user", "content": content}
                ],
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"AI Error during paraphrasing: {str(e)}"
