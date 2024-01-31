# Github.com/Vasusen-code

import os

from .. import bot as Drone
from .. import userbot, Bot
from .. import FORCESUB as fs
from main.plugins.pyroplug import get_bulk_msg
from main.plugins.helpers import get_link, join

from pyrogram import filters
from pyrogram.types import Message

from ethon.telefunc import force_sub

ft = f"To use this bot you've to join @{fs}."

message = "Send me the message link you want to start saving from, as a reply to this message."

# Event handler for both private chats and channels to clone bulk messages
@Drone.on_message(filters.incoming & filters.regex(r'/batch'))
async def batch_handler(client, message: Message):
    chat_id = message.chat.id
    await batch_process(client, message)

# Function to handle the cloning process for bulk messages
async def batch_process(client, message):
    chat_id = message.chat.id
    reply_msg = message.reply_to_message

    if not reply_msg or not reply_msg.linked_message:
        await message.reply("Reply to a message with a link to clone.")
        return

    msg_link = reply_msg.linked_message.link
    sender = message.from_user.id
    edit_id = message.message_id

    # Adjusting existing code to work seamlessly in both private chats and channels
    try:
        chat = ""
        round_message = False
        if "?single" in msg_link:
            msg_link = msg_link.split("?single")[0]
        msg_id = int(msg_link.split("/")[-1])
        height, width, duration, thumb_path = 90, 90, 0, None
        if 't.me/c/' or 't.me/b/' in msg_link:
            if 't.me/b/' in msg_link:
                chat = str(msg_link.split("/")[-2])
            else:
                chat = int('-100' + str(msg_link.split("/")[-2]))
            file = ""
            try:
                msg = await userbot.get_messages(chat, msg_id)
                if msg.media:
                    if msg.media==MessageMediaType.WEB_PAGE:
                        await client.edit_message_text(chat_id, edit_id, "Cloning.")
                        await client.send_message(chat_id, msg.text.markdown)
                        return
                if not msg.media:
                    if msg.text:
                        await client.edit_message_text(chat_id, edit_id, "Cloning.")
                        await client.send_message(chat_id, msg.text.markdown)
                        return
                await client.edit_message_text(chat_id, edit_id, "Trying to Download.")
                file = await userbot.download_media(
                    msg,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        client,
                        "**DOWNLOADING:**\n",
                        chat_id,
                        edit_id,
                        time.time()
                    )
                )
                await client.edit_message_text(chat_id, edit_id, 'Preparing to Upload!')
                caption = None
                if msg.caption is not None:
                    caption = msg.caption
                if msg.media==MessageMediaType.VIDEO_NOTE:
                    round_message = True
                    print("Trying to get metadata")
                    data = video_metadata(file)
                    height, width, duration = data["height"], data["width"], data["duration"]
                    print(f'd: {duration}, w: {width}, h:{height}')
                    try:
                        thumb_path = await screenshot(file, duration, sender)
                    except Exception:
                        thumb_path = None
                    await client.send_video_note(
                        chat_id=chat_id,
                        video_note=file,
                        length=height, duration=duration, 
                        thumb=thumb_path,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            client,
                            chat_id,
                            '**UPLOADING:**\n',
                            edit_id,
                            time.time()
                        )
                    )
                elif msg.media==MessageMediaType.VIDEO and msg.video.mime_type in ["video/mp4", "video/x-matroska"]:
                    print("Trying to get metadata")
                    data = video_metadata(file)
                    height, width, duration = data["height"], data["width"], data["duration"]
                    print(f'd: {duration}, w: {width}, h:{height}')
                    try:
                        thumb_path = await screenshot(file, duration, sender)
                    except Exception:
                        thumb_path = None
                    await client.send_video(
                        chat_id=chat_id,
                        video=file,
                        caption=caption,
                        supports_streaming=True,
                        height=height, width=width, duration=duration, 
                        thumb=thumb_path,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            client,
                            chat_id,
                            '**UPLOADING:**\n',
                            edit_id,
                            time.time()
                        )
                    )
                
                elif msg.media==MessageMediaType.PHOTO:
                    await client.edit_message_text(chat_id, edit_id, "Uploading photo.")
                    await bot.send_file(chat_id, file, caption=caption)
                else:
                    thumb_path=thumbnail(sender)
                    await client.send_document(
                        chat_id,
                        file, 
                        caption=caption,
                        thumb=thumb_path,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            client,
                            chat_id,
                            '**UPLOADING:**\n',
                            edit_id,
                            time.time()
                        )
                    )
                
                try:
                    os.remove(file)
                    if os.path.isfile(file) == True:
                        os.remove(file)
                except Exception:
                    pass
                await client.edit_message_text(chat_id, edit_id, "Clone Successful!")
            except (ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid):
                await client.edit_message_text(chat_id, edit_id, "Have you joined the channel?")
                return
            except PeerIdInvalid:
                chat = msg_link.split("/")[-3]
                try:
                    int(chat)
                    new_link = f"t.me/c/{chat}/{msg_id}"
                except:
                    new_link = f"t.me/b/{chat}/{msg_id}"
                return await clone_process(client, message)
            except Exception as e:
                print(e)
                if "messages.SendMedia" in str(e) \
                or "SaveBigFilePartRequest" in str(e) \
                or "SendMediaRequest" in str(e) \
                or str(e) == "File size equals to 0 B":
                    try: 
                        if msg.media==MessageMediaType.VIDEO and msg.video.mime_type in ["video/mp4", "video/x-matroska"]:
                            UT = time.time()
                            uploader = await fast_upload(f'{file}', f'{file}', UT, bot, edit, '**UPLOADING:**')
                            attributes = [DocumentAttributeVideo(duration=duration, w=width, h=height, round_message=round_message, supports_streaming=True)] 
                            await bot.send_file(chat_id, uploader, caption=caption, thumb=thumb_path, attributes=attributes, force_document=False)
                        elif msg.media==MessageMediaType.VIDEO_NOTE:
                            UT = time.time()
                            uploader = await fast_upload(f'{file}', f'{file}', UT, bot, edit, '**UPLOADING:**')
                            attributes = [DocumentAttributeVideo(duration=duration, w=width, h=height, round_message=round_message, supports_streaming=True)] 
                            await bot.send_file(chat_id, uploader, caption=caption, thumb=thumb_path, attributes=attributes, force_document=False)
                        else:
                            UT = time.time()
                            uploader = await fast_upload(f'{file}', f'{file}', UT, bot, edit, '**UPLOADING:**')
                            await bot.send_file(chat_id, uploader, caption=caption, thumb=thumb_path, force_document=True)
                        if os.path.isfile(file) == True:
                            os.remove(file)
                    except Exception as e:
                        print(e)
                        await client.edit_message_text(chat_id, edit_id, f'Failed to clone: `{msg_link}`\n\nError: {str(e)}')
                        try:
                            os.remove(file)
                        except Exception:
                            return
                        return 
                else:
                    await client.edit_message_text(chat_id, edit_id, f'Failed to clone: `{msg_link}`\n\nError: {str(e)}')
                    try:
                        os.remove(file)
                    except Exception:
                        return
                    return
                try:
                    os.remove(file)
                    if os.path.isfile(file) == True:
                        os.remove(file)
                except Exception:
                    pass
        else:
            await client.edit_message_text(chat_id, edit_id, "Cloning.")
            chat =  msg_link.split("t.me")[1].split("/")[1]
            try:
                msg = await client.get_messages(chat, msg_id)
                if msg.empty:
                    new_link = f't.me/b/{chat}/{int(msg_id)}'
                    return await clone_process(client, message)
                await client.copy_message(chat_id, sender, msg_id)
            except Exception as e:
                print(e)
                return await client.edit_message_text(chat_id, edit_id, f'Failed to clone: `{msg_link}`\n\nError: {str(e)}')
            await client.edit_message_text(chat_id, edit_id, "Clone Successful!")

# Add other event handlers for additional functionalities
# ...

# Event handler for channels to handle other functionalities
@Drone.on_message(filters.channel & filters.incoming & filters.regex(r'/other_command'))
async def channel_other_command_handler(client, message: Message):
    chat_id = message.chat.id
    # Handle other functionalities specific to channels
    # ...

# Add more event handlers as needed
# ...
