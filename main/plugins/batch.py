# Tg:Mahesh Chauhan/Dronellots
# Github.com/Vasusen-code
# Plugin for both public & private channels!

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

ft = f"To use this bot you've to join @{fs}."
batch = []

@Drone.on(events.NewMessage(incoming=True, from_users=AUTH, pattern='/cancel'))
async def cancel(event):
    if not (event.is_private or event.is_channel):
        return
    if not event.sender_id in batch:
        return await event.reply("No batch active.")
    batch.clear()
    await event.reply("Done.")

@Drone.on(events.NewMessage(incoming=True, from_users=AUTH, pattern='/batch'))
async def batch(event):
    if not (event.is_private or event.is_channel):
        return

    s, r = await force_sub(event.client, fs, event.sender_id, ft)
    if s == True:
        await event.reply(r)
        return
    if event.sender_id in batch:
        return await event.reply("अरे। दादा आराम से, पहले वाले को Cancel X कर पहले")

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
                await conv.send_message("मैं औकात दिखा दी मारी पाछो भेज /batch")
                return conv.cancel()

            await conv.send_message("Send me the number of files/range you want to save from the given message, as a reply to this message.", buttons=Button.force_reply())
            try:
                _range = await conv.get_reply()
            except Exception as e:
                print(e)
                await conv.send_message("Cannot wait more try again send again /start/batch ")
                return conv.cancel()

            try:
                value = int(_range.text)
                if value > 1000:
                    await conv.send_message("ठावस राख 500 भेज.")
                    return conv.cancel()
            except ValueError:
                await conv.send_message("Range must be an integer!")
                return conv.cancel()
            
            # The rest of your code...
