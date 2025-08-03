import os
import logging
import requests
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.types import ChatAdminRights

# Load environment variables
load_dotenv()
api_id = int(os.getenv("26743856"))
api_hash = os.getenv("d50d0c003c3ad56f27cc619074ab6d88")
bot_token = os.getenv("7779600047:AAHnQUkZbnrWv0eMcqP_Q8OVYDnHYmzqKxI")

FB_PAGE_ACCESS_TOKEN = os.getenv("EAAPRzu2yL54BPNe5bQWyoeIRczWkdbSR9wxUPv57FtZC3lNrNrTxL9jEleXrb51AbvSf36gZB4bCZBu3hr63SLhZAw2c37HqQKVRjZBHgxNamcrpNmGN84AkTFLCthtPIxT8ccEghplfFNsZBQA6ZB1n8gqSZAWey5J5GqxYDsddY92TELW1ZAZBkD0Eg8CSsXmldqNherbxsu")
FB_PAGE_ID = os.getenv("688686637669419")

logging.basicConfig(level=logging.INFO)

client = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

# Post text or image to Facebook
def post_to_facebook(message, image_path=None):
    try:
        if image_path:
            url = f"https://graph.facebook.com/{FB_PAGE_ID}/photos"
            with open(image_path, 'rb') as img:
                files = {'source': img}
                data = {'access_token': FB_PAGE_ACCESS_TOKEN, 'caption': message}
                r = requests.post(url, data=data, files=files)
        else:
            url = f"https://graph.facebook.com/{FB_PAGE_ID}/feed"
            data = {'message': message, 'access_token': FB_PAGE_ACCESS_TOKEN}
            r = requests.post(url, data=data)

        r.raise_for_status()
        logging.info("[facebook] Successfully posted.")
    except Exception as e:
        logging.error(f"[facebook] Failed to post: {e}")

@client.on(events.NewMessage)
async def handler(event):
    if not event.is_group:
        return

    try:
        user = await event.get_sender()
        permissions = await client.get_permissions(event.chat_id, user)
        if not permissions.is_admin:
            logging.info("[telegram] Message ignored (not from admin).")
            return
    except Exception as e:
        logging.error(f"[telegram] Failed to check admin status: {e}")
        return

    text = event.message.message or ""
    media = None

    if event.message.media:
        media = await event.message.download_media()

    post_to_facebook(text, media)

logging.info("Bot is running...")
client.run_until_disconnected()
