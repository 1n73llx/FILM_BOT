import pyrogram
from pyrogram import filters
from config import Config
import time
from modules.messages import Messages
from modules.database import *


if not check_db_exist():
    create_db()

#check_user()


PROXY = {
    "scheme": "http",
    "hostname": "127.0.0.1",
    "port": 80
}

messages = Messages(lang_fetcher="en")
starttime = time.strftime("%Y/%m/%d - %H:%M:%S")

ALPHA_DL = pyrogram.Client(
    "ALPHA_DL",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    plugins=dict(root="modules"),
    sleep_threshold=10,
    max_concurrent_transmissions=3,
    #proxy=PROXY
)



#=== Running The Bot ======================================
print("starting bot...")
ALPHA_DL.start()
ALPHA_DL.send_message(
    chat_id=Config.LOGS_CHANNEL,
    text=f"**Bot Started At: \n{starttime}**"
)
print("BOT STAETED...")
print("="*100)
pyrogram.idle()
