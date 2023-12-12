#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from telethon import TelegramClient, events, sync
import os

# Helper 
def get_env(name, message, cast=str):
	if name in os.environ:
		return os.environ[name]
	else:
		return message

session = os.environ.get('TG_SESSION', 'bottorrent')
api_id = os.environ.get('TG_API_ID')
api_hash = os.environ.get('TG_API_HASH')
bot_token = os.environ.get('TG_BOT_TOKEN')
TG_AUTHORIZED_USER_ID = os.environ.get('TG_AUTHORIZED_USER_ID')

authorized_users = list(map(int, TG_AUTHORIZED_USER_ID.replace(" ", "").split(','))) if TG_AUTHORIZED_USER_ID else False 

client = TelegramClient(session, api_id, api_hash).start(bot_token = bot_token)
    
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Hello! I am your bot.')

@client.on(events.NewMessage)
async def download_files(event):
    if event.chat_id in authorized_users:
        if event.media:
            if hasattr(event.media, 'document'):
                # It's a document (file)
                file_type = event.media.document.mime_type
                if file_type in ['application/pdf', 'application/x-mobipocket-ebook', 'application/epub+zip']:
                    # Download the file
                    file_path = os.path.join(download_path, event.file.name)
                    await event.download_media(file_path)
                    await event.reply('File processed successfully!')
                else:
                    await event.reply('I only process PDF, EPUB, and MOBI files.')
            else:
                await event.reply('I only process PDF, EPUB, and MOBI files.')
        elif not event.message.message.startswith('/'):
            await event.reply('Please upload PDF, EPUB, or MOBI file or use the commands.')
    else:
        await event.reply('Unauthorized user')

if __name__ == '__main__':
    client.start()
    print("Bot is running...")
    client.run_until_disconnected()
