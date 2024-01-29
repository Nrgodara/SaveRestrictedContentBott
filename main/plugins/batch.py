#Tg:MaheshChauhan/DroneBots
#Github.com/Vasusen-code

"""
Plugin for both public & private channels!
"""

import time
import os
import asyncio

from .. import bot as Drone
from .. import userbot, Bot, AUTH
from .. import FORCESUB as fs
from main.plugins.pyroplug import get_bulk_msg
from main.plugins.helpers import get_link, screenshot

from telethon import events, Button, errors
from telethon.tl.types import DocumentAttributeVideo

from pyrogram import Client 
from pyrogram.errors import FloodWait

from ethon.pyfunc import video_metadata
from ethon.telefunc import force_sub

# Paths
DOWNLOAD_PATH = "/app/downloads/"
REPLACEIT_PATH = DOWNLOAD_PATH + "replaceit.txt"
REPLACEWITH_PATH = DOWNLOAD_PATH + "replacewith.txt"

ft = f"To use this bot you've to join @{fs}."

batch = []

# Replace the existing event handlers with these modified versions

@Drone.on(events.NewMessage(incoming=True, from_users=AUTH, pattern='/cancel'))
async def cancel(event):
    if not (event.is_private or event.is_channel):
        return
    if not event.sender_id in batch:
        return await event.reply("No batch active.")
    batch.clear()
    await event.reply("Done.")

@Drone.on(events.NewMessage(incoming=True, from_users=AUTH, pattern='/batch'))
async def _batch(event):
    if not (event.is_private or event.is_channel):
        return
    # Rest of your code.
 
    s, r = await force_sub(event.client, fs, event.sender_id, ft) 
    if s == True:
        await event.reply(r)
        return       
    if event.sender_id in batch:
        return await event.reply("अरे! दादा आराम से, पहले वाले को Cancel ❌ कर पहले")
    async with Drone.conversation(event.chat_id) as conv: 
        if s != True:
            await conv.send_message("Send me the message link you want to start saving from, as a reply to this message.", buttons=Button.force_reply())
            try:
                link = await conv.get_reply()
                try:
                    _link = get_link(link.text)
                except Exception:
                    await conv.send_message("No link found.")
                    return conv.cancel()
            except Exception as e:
                print(e)
                await conv.send_message("मैं औकात दिखा दी मारी पाछो भेज /batch 👿")
                return conv.cancel()
            await conv.send_message("Send me the number of files/range you want to save from the given message, as a reply to this message.", buttons=Button.force_reply())
            try:
                _range = await conv.get_reply()
            except Exception as e:
                print(e)
                await conv.send_message("Cannot wait more try again  send again /start /batch ")
                return conv.cancel()
            try:
                value = int(_range.text)
                if value > 1000:
                    await conv.send_message("बस कर भाई ठावस राख 500 भेज.")
                    return conv.cancel()
            except ValueError:
                await conv.send_message("Range must be an integer!")
                return conv.cancel()
            
            # Ask the user if they want to replace any word/sentence in the caption
            await conv.send_message("MAHI❤️‍🔥, Do you want to replace any word/sentence in the caption? (Yes/No)")
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
                        await conv.send_message("Ok, MAHI®, Now send me the text you want to Replace with 'send new caption'")
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
# ...

async def run_batch(userbot, client, sender, link, _range):
    for i in range(_range):
        timer = 60
        if i < 25:
            timer = 1
        if i < 50 and i > 25:
            timer = 2
        if i < 100 and i > 50:
            timer = 3
        if not 't.me/c/' in link:
            if i < 25:
                timer = 2
            else:
                timer = 3
        try: 
            if not sender in batch:
                await client.send_message(sender, "Batch completed.")
                break
        except Exception as e:
            print(e)
            await client.send_message(sender, "Batch completed.")
            break
        try:
            await get_bulk_msg(userbot, client, sender, link, i) 
        except FloodWait as fw:
            if int(fw.x) > 299:
                await client.send_message(sender, "Cancelling batch since you have floodwait more than 5 minutes.")
                break
            await asyncio.sleep(fw.x + 5)
            await get_bulk_msg(userbot, client, sender, link, i)
        protection = await client.send_message(sender, f"Sleeping for `{timer}` seconds to avoid Floodwaits and Protect account!")
        await asyncio.sleep(timer)
        await protection.delete()

# Error handling and cleanup after batch completion
@Drone.on(events.NewMessage(incoming=True, from_users=AUTH, pattern='/cleanup'))
async def cleanup(event):
    if not (event.is_private or event.is_channel):
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

# Additional error handling
@Drone.on(events.ChatAction())
async def chat_action_handler(event):
    # Handle chat actions, if needed
    pass

# ...
