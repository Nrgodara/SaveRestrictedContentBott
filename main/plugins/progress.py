import math
import os
import time
import json

FINISHED_PROGRESS_STR = "▓"
UN_FINISHED_PROGRESS_STR = "░"
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

        progress = "**[{0}{1}]** `| {2}%`\n\n".format(
            ''.join([FINISHED_PROGRESS_STR for i in range(math.floor(percentage / 5))]),
            ''.join([UN_FINISHED_PROGRESS_STR for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2))

        tmp = (
            f"**{ud_type}**\n\n"
            f"**Progress:**\n{progress}\n\n"
            f"**Size:** `{humanbytes(current)} of {humanbytes(total)}`\n"
            f"**Speed:** `{humanbytes(speed)}/s`\n"
            f"**ETA:** `{estimated_total_time}`" if estimated_total_time != '' else ""
        )

        try:
            if not message.photo:
                await message.edit_text(text=tmp)
            else:
                await message.edit_caption(caption=tmp)
        except:
            pass


def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: 'B', 1: 'KiB', 2: 'MiB', 3: 'GiB', 4: 'TiB'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n]


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((f"{days}d ") if days else "") +
        ((f"{hours}h ") if hours else "") +
        ((f"{minutes}m ") if minutes else "") +
        ((f"{seconds}s ") if seconds else "")
    )
    return tmp.strip()
