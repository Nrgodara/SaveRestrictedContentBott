#Github.com/Vasusen-code

from pyrogram import Client

from telethon.sessions import StringSession
from telethon.sync import TelegramClient

from decouple import config
import logging, time, sys

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# variables
API_ID = 20441092
API_HASH = a274e24d12f4bcc4d2ef63f9e8688dd9
BOT_TOKEN = 6741867082:AAE4IT2VaUwnAfU3Qel3Vew7mQoU9Hd2f-Y
SESSION = BQE36AQApc_qnRfeTOiRpoMOFXG0HqBEx3oN2xKQnpiqSNf7MP-KL2dtZBiLdwlbHK0yZeTk_EVCmLvc0zKD2OzHJpT5NgwO8yMfdYe4eIrcAeEhcr-EA2u9nhYHL5nazWaNWdVhqqIJwi9c-48oGOa6Nt8OU_dGKTuF0rrrhdHUhlKRasWVUnq6SA-g8j3ZQA2-a2h83Gk5ynFX47tzazUDvUNEBRJ9QywOYtD-0vkRN-2Dg09u6Imru4m6X1DcbpCaBudx5gITJGNM5GlUmptYNrc9jiKULQl8jcZC4fJuSHDJ6TkJwInfAEdWAo-kfoWaiL4kFfalLGdd4EywIhMu8jOgAAAAGcOVG9AA
FORCESUB = defence_exams_all
AUTH = 6915969469

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN) 

userbot = Client("saverestricted", session_string=SESSION, api_hash=API_HASH, api_id=API_ID) 

try:
    userbot.start()
except BaseException:
    print("Userbot Error ! Have you added SESSION while deploying??")
    sys.exit(1)

Bot = Client(
    "SaveRestricted",
    bot_token=BOT_TOKEN,
    api_id=int(API_ID),
    api_hash=API_HASH
)    

try:
    Bot.start()
except Exception as e:
    print(e)
    sys.exit(1)
