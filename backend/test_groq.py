from groq import Groq

from app.core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

response = client.chat.completions.create(
    model=settings.GROQ_MODEL,
    messages=[
        {
            "role": "user",
            "content": "Say hello in one sentence.",
        }
    ],
)

print(response.choices[0].message.content)