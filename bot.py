import os
import logging
from telethon import TelegramClient, events
import requests

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load credentials from environment
api_id = int(os.getenv("26743856"))
api_hash = os.getenv("d50d0c003c3ad56f27cc619074ab6d88")
bot_token = os.getenv("7779600047:AAHnQUkZbnrWv0eMcqP_Q8OVYDnHYmzqKxI")
facebook_page_id = os.getenv("688686637669419")
facebook_access_token = os.getenv("EAAPRzu2yL54BPFJLEHlIxxPtD9nudNAPBlhXh65zhX38S3s06TetmbWHLEJFWrnOOIUNNV6tZCUXBsmvqEYt009yyqOxqkyVdZCfOVt0SFWJPAJbD4HTDcWQYX0d5LhZAWQ9s4ZCH2klXyNtLTuqxNrtsRawrtHWhJwPT6ZCRJDEXhdWSqaR03RiP0NLZAeaNqaXac3vD3gF1Cewmx6Q23kruwdIFzwZCJPZCLFP2Llv")

# Initialize the Telegram client with bot token
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Helper: Post to Facebook Page
def post_to_facebook(text):
    url = f"https://graph.facebook.com/{facebook_page_id}/feed"
    data = {
        'message': text,
        'access_token': facebook_access_token
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        logger.info("[facebook] Post successful")
    except requests.exceptions.RequestException as e:
        logger.info(f"[facebook] Failed to post text to Facebook: {e}")

# Listen to Telegram group messages
@client.on(events.NewMessage)
async def handler(event):
    try:
        sender = await event.get_sender()
        if event.is_group and sender and sender.bot is False and sender.username:
            if sender.admin_rights or sender.participant.admin_rights:
                message_text = event.message.message
                if message_text:
                    logger.info(f"[telegram] Forwarding message from admin: {message_text}")
                    post_to_facebook(message_text)
    except Exception as e:
        logger.info(f"[telegram] Error handling Telegram message: {e}")

logger.info("Bot is running...")
client.run_until_disconnected()
