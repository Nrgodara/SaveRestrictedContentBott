# Github.com/Vasusen-code

import os
from .. import bot as Drone
from telethon import events, Button

from ethon.mystarts import start_srb

S = '/' + 's' + 't' + 'a' + 'r' + 't'

@Drone.on(events.callbackquery.CallbackQuery(data="set"))
async def sett(event):    
    Drone = event.client                    
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    async with Drone.conversation(event.chat_id) as conv: 
        xx = await conv.send_message("Send me any image for thumbnail as a `reply` to this message📷.")
        x = await conv.get_reply()
        if not x.media:
            xx.edit("No media found.")
        mime = x.file.mime_type
        if not 'png' in mime:
            if not 'jpg' in mime:
                if not 'jpeg' in mime:
                    return await xx.edit("No image found🫣.")
        await xx.delete()
        t = await event.client.send_message(event.chat_id, 'Trying.')
        path = await event.client.download_media(x.media)
        if os.path.exists(f'{event.sender_id}.jpg'):
            os.remove(f'{event.sender_id}.jpg')
        os.rename(path, f'./{event.sender_id}.jpg')
        await t.edit("Temporary thumbnail saved!🫶")
        
@Drone.on(events.callbackquery.CallbackQuery(data="rem"))
async def remt(event):  
    Drone = event.client            
    await event.edit('Trying.')
    try:
        os.remove(f'{event.sender_id}.jpg')
        await event.edit('Removed!❌')
    except Exception:
        await event.edit("No thumbnail saved.🔎")                        
  
@Drone.on(events.NewMessage(incoming=True, pattern=f"{S}"))
async def start(event):
    user_mention = f"[{event.sender_id}](tg://user?id={event.sender_id})"
    text = (
        f"Hey,**MAHI®**! 🤭\n"
        "Ready to work some magic? ✨ Send me the link of any message, and I'll clone it right here. "
        "For private channel messages, don't forget to send the invite link first. 😉\n\n"
        "**𝔼𝕏ℙ𝔼ℂ𝕋 𝕋ℍ𝔼 𝕌ℕ𝔼𝕏ℙ𝔼ℂ𝕋𝔼𝔻 🫰❤️‍🔥**"
    )

    await start_srb(event, text)
