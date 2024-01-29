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

    # Disable forcesub
    # s, r = await force_sub(event.client, fs, event.sender_id, ft) 
    # if s == True:
    #     await event.reply(r)
    #     return
    s = False  # Forcesub disabled
    
    if event.sender_id in batch:
        return await event.reply("अरे! दादा आराम से, पहले वाले को Cancel ❌ कर पहले")
    
    async with Drone.conversation(event.chat_id) as conv: 
        if s != True:
            await conv.send_message("Send me the message link you want to start saving from, as a reply to this message.", buttons=Button.force_reply())
            try:
                link = await conv.get_reply()
                if not link:
                    return await conv.send_message("No link found.")
                
                try:
                    _link = get_link(link.text)
                except Exception:
                    await conv.send_message("No link found.")
                    return conv.cancel()
                
                # Fetch user information
                user_info = await event.client.get_entity(event.sender_id)
                
                # Ask the user if they want to replace any word/sentence in the caption
                user_name = user_info.first_name if hasattr(user_info, 'first_name') else "User"
                await conv.send_message(f"{user_name}, Do you want to replace any word/sentence in the caption? (Yes/No)")
                replace_response = await conv.get_reply()
                
                if replace_response.text.lower() in ['yes', 'y']:
                    # Ask for the text to replace
                    await conv.send_message("Send me the text you want to replace 'send from caption'")
                    replace_from = (await conv.get_reply()).text

                    # Check if the message with the given caption exists
                    async for message in event.client.iter_messages(link, reverse=True, limit=10):
                        if message.caption and replace_from in message.caption:
                            # Save the existing caption for replacement
                            with open(REPLACEIT_PATH, 'w') as replaceit_file:
                                replaceit_file.write(message.caption)
                            
                            # Ask for the text to replace with
                            await conv.send_message(f"Ok, {user_name}, Now send me the text you want to Replace with 'send new caption'")
                            replace_with = (await conv.get_reply()).text
                            
                            # Save the text to replace with
                            with open(REPLACEWITH_PATH, 'w') as replacewith_file:
                                replacewith_file.write(replace_with)
                            
                            # Replace the text in the caption
                            new_caption = message.caption.replace(replace_from, replace_with)
                            
                            # Edit the message with the new caption
                            await message.edit(caption=new_caption)
                            
                            # Continue the batch process
                            batch.append(event.sender_id)
                            await run_batch(userbot, Bot, event.sender_id, _link, value) 
                            conv.cancel()
                            batch.clear()
                            break
                    else:
                        await conv.send_message("Error: No message found with the specified caption.")
                        conv.cancel()
                        batch.clear()
                        return


# Additional error handling
from pyrogram import filters

from pyrogram import filters

@Drone.on_message(filters.chat_action)
async def chat_action_handler(client, event):
    # Handle chat actions, if needed
    pass

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
                                     
