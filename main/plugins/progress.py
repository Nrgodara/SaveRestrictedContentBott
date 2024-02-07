import math
import os
import time
import json

FINISHED_PROGRESS_STR = "▅"
UN_FINISHED_PROGRESS_STR = "▁"
DOWNLOAD_LOCATION = "/app"

async def progress_for_pyrogram(
    current,
    total,
    bot,
    ud_type,
    message,
    start
):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        status = DOWNLOAD_LOCATION + "/status.json"
        if os.path.exists(status):
            with open(status, 'r+') as f:
                statusMsg = json.load(f)
                if not statusMsg["running"]:
                    bot.stop_transmission()
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        # Circle progress bar formatting
        progress_bar_length = 10
        completed_length = math.floor(percentage / (100 / progress_bar_length))
        remaining_length = progress_bar_length - completed_length
        progress_bar = "┣┈𖨠⏳➤["
        progress_bar += FINISHED_PROGRESS_STR * completed_length
        progress_bar += UN_FINISHED_PROGRESS_STR * remaining_length
        progress_bar += f"] | {round(percentage, 2)}%"

        # Enhanced visual appearance
        progress = f"""╔════❰ 📤 𝔽𝕀𝕃𝔼 𝕊𝕐ℕℂ 📤❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━━━━━━➣
║┣༻°•**𝑬𝒙𝒑𝒆𝒄𝒕 𝑻𝒉𝒆 𝑼𝒏𝒆𝒙𝒑𝒆𝒄𝒕𝒆𝒅🫰❤️‍🔥**•°༺
║┃┗━━━━•❃°•🅜🅐🅗🅘•°❃•━━━━┛
║┃
{progress}
║┃
║┣⪼𖨠📁 𝙂𝒓𝙤𝒔𝙨: {humanbytes(current)} 𝒐𝒇 {humanbytes(total)} 𝑴𝑩
║┃
║┣⪼𖨠🚀➤ 𝙎𝒑𝙚𝒆𝙙: {humanbytes(speed)}/s
║┃
║┣⪼𖨠📟 ➤𝙀𝑻𝘼: {estimated_total_time if estimated_total_time != '' else "0 s"}
║╰━━━━━━━━━━━━━━━━━━━➣ 
╚═════❰ 𝙇𝑶𝘼𝑫𝙄𝑵𝙂⚡❱════❍⊱❁"""

        try:
            if not message.photo:
                await message.edit_text(
                    text="{}\n{}".format(
                        ud_type,
                        progress
                    )
                )
            else:
                await message.edit_caption(
                    caption="{}\n{}".format(
                        ud_type,
                        progress
                    )
                )
        except:
            pass

def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "")
    return tmp[:-2]
