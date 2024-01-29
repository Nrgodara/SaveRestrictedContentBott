# Tg:MaheshChauhan/DroneBots
# Github.com/Vasusen-code

"""
Plugin for both public & private channels!
"""

import time
import os
import asyncio

from .. import bot as Drone
from .. import userbot, Bot, AUTH
from main.plugins.pyroplug import get_bulk_msg
from main.plugins.helpers import get_link, screenshot

from telethon import events, Button, errors
from telethon.tl.types import DocumentAttributeVideo

from ethon.pyfunc import video_metadata

# Paths
BASE_PATH = os.path.dirname(os.path.realpath(__file__))
DOWNLOAD_PATH = os.path.join(BASE_PATH, "downloads")
REPLACEIT_PATH = os.path.join(DOWNLOAD_PATH, "replaceit.txt")
REPLACEWITH_PATH = os.path.join(DOWNLOAD_PATH, "replacewith.txt")

ft = "To use this bot, you need to join the channel."

batch = []

# Replace the existing event handlers with these modified versions

@Drone.on(events.NewMessage(incoming=True, pattern='/cancel'))
async def cancel(event):
    if not event.is_private:
        return
    if not event.sender_id in batch:
        return await event.reply("No batch active.")
    batch.clear()
    await event.reply("Done.")

@Drone.on(events.NewMessage(incoming=True, pattern='/batch'))
async def _batch(event):
    if not event.is_private and not event.is_channel:
        return await event.reply("Batch command only works in private chat or channels.")
    
    # Rest of your code.
    # (I've omitted the section you mentioned was not modified)
    
# Additional error handling
from pyrogram import filters

@Drone.on_message(filters.chat_action)
async def chat_action_handler(client, event):
    try:
        # Your existing code here
    except Exception as e:
        print(f"An error occurred: {e}")

# Error handling and cleanup after batch completion
@Drone.on(events.NewMessage(incoming=True, pattern='/cleanup'))
async def cleanup(event):
    if not event.is_private:
        return
    
    # Clear the batch list
    batch.clear()
    # Delete the replaceit and replacewith files
    try:
        os.remove(REPLACEIT_PATH)
    except FileNotFoundError:
        pass

    try:
        os.remove(REPLACEWITH_PATH)
    except FileNotFoundError:
        pass

    await event.reply("Cleanup completed.")
