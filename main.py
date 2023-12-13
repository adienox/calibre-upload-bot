#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# Import necessary libraries
from telethon import TelegramClient, events, sync
import os
import subprocess

# Get required environment variables or use default values
session = os.environ.get('TG_SESSION', 'downloader')
api_id = os.environ.get('TG_API_ID')
api_hash = os.environ.get('TG_API_HASH')
bot_token = os.environ.get('TG_BOT_TOKEN')
TG_AUTHORIZED_USER_ID = os.environ.get('TG_AUTHORIZED_USER_ID')
download_path='/output'
library_path='/books'
calibre_binaries='/binaries/'

def add_books_to_calibre(library_path, *book_paths):
    """
    Add books to Calibre library using calibredb.

    Parameters:
    - library_path: The path to your Calibre library.
    - book_paths: Variable number of paths to the books you want to add.
    """
    # Construct the command to add books to the Calibre library
    command = [
        calibre_binaries + 'calibredb', 'add',
        '--library-path', library_path,
    ]
    
    command.extend(book_paths)
    
    try:
        # Execute the calibredb command
        subprocess.run(command, check=True)
        print("Books added successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error adding books: {e}")

# Convert comma-separated string to a list of authorized user IDs
authorized_users = list(map(int, TG_AUTHORIZED_USER_ID.replace(" ", "").split(','))) if TG_AUTHORIZED_USER_ID else False 

# Initialize the Telegram client
client = TelegramClient(session, api_id, api_hash).start(bot_token=bot_token)

# Define event handlers

# Handler for the "/start" command
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Hello! I am your bot.')

# Handler for new messages
@client.on(events.NewMessage)
async def download_files(event):
    # Check if the sender is an authorized user
    if event.chat_id in authorized_users:
        if event.media:
            if hasattr(event.media, 'document'):
                # It's a document (file)
                file_type = event.media.document.mime_type
                if file_type in ['application/pdf', 'application/x-mobipocket-ebook', 'application/epub+zip']:
                    # Download the file
                    message = await event.reply('processing file... ⏳')
                    file_path = os.path.join(download_path, event.file.name)
                    await event.download_media(file_path)
                    add_books_to_calibre(library_path, file_path)
                    await message.edit('File processed successfully!')
                else:
                    await event.reply('I only process PDF, EPUB, and MOBI files.')
            else:
                await event.reply('I only process PDF, EPUB, and MOBI files.')
        elif not event.message.message.startswith('/'):
            await event.reply('Please upload PDF, EPUB, or MOBI file or use the commands.')
    else:
        await event.reply('Unauthorized user')

# Main execution block
if __name__ == '__main__':
    # Start the client and run until disconnected
    client.start()
    print("Bot is running...")
    client.run_until_disconnected()
