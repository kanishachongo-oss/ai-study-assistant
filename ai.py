import openai
from datetime import date

FREE_LIMIT = 5

def can_chat(user):
    if user.last_reset != date.today():
        user.messages_today = 0
        user.last_reset = date.today()

    if user.is_paid:
        return True

    return user.messages_today < FREE_LIMIT


def get_ai_reply(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a smart study assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
