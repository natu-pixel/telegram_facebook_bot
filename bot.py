from telethon.sync import TelegramClient, events
import requests
import os

# Telegram API setup
api_id = 26743856
api_hash = 'd50d0c003c3ad56f27cc619074ab6d88'
group_id = -1002299729281 

# Facebook API setup
page_access_token = '600334626243503|srgHoAsRJ5EM38bMQUaKyLmgV5k'
page_id = '688686637669419'

client = TelegramClient('session_group', api_id, api_hash)

def post_text(message):
    url = f"https://graph.facebook.com/{page_id}/feed"
    data = {
        'message': message,
        'access_token': page_access_token
    }
    res = requests.post(url, data=data)
    print("✅ Posted text:", res.json())

def post_photo(message, file_path):
    url = f"https://graph.facebook.com/{page_id}/photos"
    with open(file_path, 'rb') as img:
        files = {'source': img}
        data = {
            'caption': message,
            'access_token': page_access_token
        }
        res = requests.post(url, files=files, data=data)
        print("✅ Posted photo:", res.json())

def post_video(message, file_path):
    url = f"https://graph.facebook.com/{page_id}/videos"
    with open(file_path, 'rb') as vid:
        files = {'source': vid}
        data = {
            'description': message,
            'access_token': page_access_token
        }
        res = requests.post(url, files=files, data=data)
        print("✅ Posted video:", res.json())

@client.on(events.NewMessage(chats=group_id))
async def handler(event):
    sender = await event.get_sender()
    if not sender.bot and not sender.is_self and sender.is_admin:
        message = event.message.message or ""
        media = event.message.media
        sender_name = getattr(sender, 'username', 'Unknown')
        full_message = f"{sender_name}:\n{message}" if message else f"From {sender_name}"

        if media:
            file_path = await event.message.download_media()
            if file_path.endswith(('.jpg', '.jpeg', '.png')):
                post_photo(full_message, file_path)
            elif file_path.endswith(('.mp4', '.mov', '.avi')):
                post_video(full_message, file_path)
            else:
                print("⚠️ Unsupported media type:", file_path)
            os.remove(file_path)
        else:
            post_text(full_message)

print("🚀 Bot is running...")
client.start()
client.run_until_disconnected()
