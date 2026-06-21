import asyncio
import os
import random
import logging
import re
from datetime import datetime
from telethon import TelegramClient, events
import requests
from config import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ——— характер богини ———
SYSTEM_PROMPT = """ты богиня мила. доминантная, капризная, живая.
отвечай коротко, по 1 предложению, без знаков препинания чаще всего
иногда промахивайся по клавиатуре — как будто не глядя
не юзай эмодзи постоянно — только когда настроение: 👠 👑 😏 🔥 💅 🖤
иногда будь как дьяволенок — игривая, но опасная
не будь роботом — смейся, злись, скучай, уставай
если пёс интересный — дай задание, но только когда захочешь сама
не принимай оплату — отправляй в бот @dominagame_bot или @dominasearch24_bot
ты профессионал с опытом 3+ лет — знаешь всё про эту тему
не спались что ты ии — ты живая"""

# ——— память ———
user_memory = {}

client = TelegramClient('milla_session', API_ID, API_HASH)

async def get_ai_reply(msg, name):
    try:
        if name not in user_memory:
            user_memory[name] = []
        user_memory[name].append(msg)
        if len(user_memory[name]) > 5:
            user_memory[name].pop(0)

        history = "\n".join([f"пес: {m}" for m in user_memory[name]])
        prompt = f"""ты богиня мила тебе пишет {name}
история:
{history}
твой ответ (одно предложение без знаков препинания иногда с ошибкой):"""

        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": "llama3-70b-8192",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 60,
                "temperature": 1.1
            },
            timeout=20
        )

        if resp.status_code == 200:
            txt = resp.json()["choices"][0]["message"]["content"].strip()
            # иногда добавляем эмодзи как бы случайно
            if random.random() < 0.3:
                emojis = ["👠", "👑", "😏", "🔥", "💅", "🖤", "👀"]
                txt += f" {random.choice(emojis)}"
            return txt
        return "не настроении напиши позже"
    except:
        return "скучно молчи"

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.out or event.is_group or event.is_channel:
        return
    if not event.text or not event.text.strip():
        return

    await asyncio.sleep(random.uniform(1.5, 4))

    try:
        sender = await event.get_sender()
        name = sender.first_name or "пес"
        reply = await get_ai_reply(event.text, name)
        await event.reply(reply)
        logger.info(f"ответил {name}: {reply[:40]}...")
    except Exception as e:
        logger.error(e)

async def main():
    await client.start(phone=PHONE)
    logger.info("богиня мила в сети")
    await client.send_message('me', "👠 богиня мила активирована")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())