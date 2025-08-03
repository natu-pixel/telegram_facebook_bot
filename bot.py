import os
import logging
import requests
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

# Load environment variables
load_dotenv()

# Telegram credentials from .env
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

# Facebook Page Access Token & Page ID
FB_PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
FB_PAGE_ID = os.getenv("FB_PAGE_ID")

# Logging
logging.basicConfig(level=logging.INFO)

# Telegram client (bot)
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Helper: Post to Facebook
def post_to_facebook(message, image_path=None):
    try:
        if image_path:
            url = f"https://graph.facebook.com/{FB_PAGE_ID}/photos"
            with open(image_path, 'rb') as img:
                files = {'source': img}
                data = {
                    'access_token': FB_PAGE_ACCESS_TOKEN,
                    'caption': message
                }
                r = requests.post(url, data=data, files=files)
        else:
            url = f"https://graph.facebook.com/{FB_PAGE_ID}/feed"
            data = {
                'message': message,
                'access_token': FB_PAGE_ACCESS_TOKEN
            }
            r = requests.post(url, data=data)

        r.raise_for_status()
        logging.info("[facebook] Successfully posted.")
    except Exception as e:
        logging.error(f"[facebook] Failed to post: {e}")

# Telegram handler
@client.on(events.NewMessage)
async def handler(event):
    if not event.is_group:
        return

    sender = await event.get_sender()
    sender_id = sender.id

    # Check if user is admin
    try:
        admins = await client.get_participants(event.chat_id, filter=events.ChatParticipantsAdmins)
        admin_ids = [admin.id for admin in admins]
        if sender_id not in admin_ids:
            logging.info("[telegram] Message ignored (not from admin).")
            return
    except Exception as e:
        logging.error(f"[telegram] Failed to check admin status: {e}")
        return

    message_text = event.message.message or ""

    # Download media if any
    media_path = None
    if event.message.media:
        media_path = await event.message.download_media()

    post_to_facebook(message_text, media_path)

# Run the bot
logging.info("Bot is running...")
client.run_until_disconnected()
