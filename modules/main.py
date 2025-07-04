from pyrogram import *
from config import Config
from .messages import Messages
from pyrogram.errors import FloodPremiumWait, FloodWait, RPCError
from pyrogram.types import *
from .database import *

messages = Messages(lang_fetcher="en")


@Client.on_message(filters.private & filters.command("ban") & filters.user(Config.BOT_OWNER))
async def ban_me(client, message):
    if len(message.command) == 2:
        ban_user(int(message.command[1]))
        await message.reply_text("**Baned Successfully!**")
    else:
        await message.reply_text("**Example Usage: \n/ban 1234567890**")


@Client.on_message(filters.private & filters.command("unban") & filters.user(Config.BOT_OWNER))
async def unban_me(client, message):
    if len(message.command) == 2:
        unban_user(int(message.command[1]))
        await message.reply_text("**UnBaned Successfully!**")
    else:
        await message.reply_text("**Example Usage: \n/unban 1234567890**")


@Client.on_message(filters.private & filters.command("status") & filters.user(Config.BOT_OWNER))
async def get_status(client, message):
    total_users  = get_total_user()
    banned_users = get_banned_user()
    num_of_film  = get_total_film()
    await message.reply_text(
        messages.get(
                    file="GET_STATUS",
                    key="GET_STATUS",
                    extra_args=[
                        total_users,
                        banned_users,
                        num_of_film
                    ]
        ),
        quote=True
    )



@Client.on_message(filters.private & filters.command("sendto") & filters.user(Config.BOT_OWNER))
async def send_msg(client, message):
    if message.reply_to_message == None:
        await message.reply_text(f"**Error!**")
        await message.reply_text(
            messages.get(
                file="USAGE_SENDTO",
                key="USAGE_SENDTO"
            )
        )
    else:
        user_id = int(message.command[1])
        msg=message.reply_to_message.text
        await client.send_message(chat_id=user_id, text=msg)
        await message.reply_text(
            messages.get(
                file="SUCCESS_SEND",
                key="SUCCESS_SEND"
            )
        )



@Client.on_message(filters.private & filters.command("broadcast") & filters.user(Config.BOT_OWNER))
async def send_msg_broadcast(client, message):
    if message.reply_to_message == None:
        await message.reply_text(f"**Error!**")
        await message.reply_text(
            messages.get(
                file="BROADCASR_USAGE",
                key="BROADCASR_USAGE"
            )
        )
    else:
        total_user_id = get_all_user_id()
        success       = 0
        failed        = 0
        done          = 0

        for user in total_user_id:
            try:
                await client.copy_message(
                    chat_id=user,
                    from_chat_id=message.chat.id,
                    message_id=message.reply_to_message.id
                )
                success += 1
            except (FloodWait, FloodPremiumWait) as f:
                await sleep(f.value)
            except Exception:
                del_user(user)
                failed += 1
            
            done += 1

        await message.reply_text(
            messages.get(
                file="BROADCASR_RESULT",
                key="BROADCASR_RESULT",
                extra_args=[
                    len(total_user_id),
                    success,
                    failed,
                    done
                ]
            )
        )



@Client.on_message(filters.private & filters.command("admin_cmd") & filters.user(Config.BOT_OWNER))
async def admin_cmd(client, message):
    await message.reply_text(
        messages.get(
            file="ADMIN_CMD",
            key="ADMIN_CMD"
        )
    )



@Client.on_message(filters.private & filters.command("add_film") & filters.user(Config.BOT_OWNER))
async def add_film(client, message):
    if len(message.command) == 2 and\
    message.reply_to_message != None and\
    message.reply_to_message.video != None:
        ID   = message.reply_to_message.video.file_id
        NAME = message.command[1]

        if add_film_db(ID, NAME):
            await message.reply_text(
                messages.get(
                    file="ADD_SUCCESS",
                    key="ADD_SUCCESS"
                ),
                quote=True
            )
        else:
            await message.reply_text(
                messages.get(
                        file="FILM_EXIST",
                        key="FILM_EXIST"
                ),
                quote=True
            )
    else:
        await message.reply_text(
            messages.get(
                        file="ADD_FILM_USAGE",
                        key="ADD_FILM_USAGE"
            ),
            quote=True
        )


@Client.on_message(filters.private & filters.command("update_info") & filters.user(Config.BOT_OWNER))
async def update_f_info(client, message):
    if len(message.command) == 4:
        FILM_NAME = message.command[1]
        KEY       = message.command[2]
        NEW_VALUE = message.command[3]

        if update_film_info(FILM_NAME , KEY, NEW_VALUE):
            await message.reply_text(
                text=messages.get(
                    file="UPDATE_SUCESS",
                    key="UPDATE_SUCESS"
                ),
                quote=True
            )
        else:
            await message.reply_text(
                text=messages.get(
                    file="NO_KEY_IN_DB",
                    key="NO_KEY_IN_DB"
                ),
                quote=True
            )
    else:
        await message.reply_text(
            text=messages.get(
                file="UPDATE_INFO_USAGE",
                key="UPDATE_INFO_USAGE"
            ),
            quote=True
        )


@Client.on_message(filters.private & filters.command("del_film") & filters.user(Config.BOT_OWNER))
async def del_film(client, message):
    if len(message.command) == 2:
        NAME = message.command[1]
        if delete_film(NAME):
            await message.reply_text(
                messages.get(
                    file="DEL_SUCCESS",
                    key="DEL_SUCCESS"
                )
            )
        else:
            await message.reply_text(
                messages.get(
                    file="FILM_NOT_EXIST",
                    key="FILM_NOT_EXIST"
                ),
                quote=True
            )
    else:
        await message.reply_text(
            messages.get(
                file="DEL_FILM_USAGE",
                key="DEL_FILM_USAGE"
            ),
            quote=True
        )



@Client.on_message(filters.private & filters.command("get_film"))
async def get_film(client, message):
    if len(message.command) == 2:       
            name   = message.command[1]
            result = get_film_db(name)
            if result == None:
                await message.reply_text(
                    messages.get(
                        file="NO_FILM",
                        key="NO_FILM"
                        
                    ),
                    quote=True
                )
            else:
                #await message.reply_text(result)
                await message.reply_video(
                    video=result['film_id'],
                    caption=messages.get(
                        file="FILM_INFO",
                        key="FILM_INFO",
                        extra_args=[
                            result['film_name'],
                            result['rate'],
                            result['duration'],
                            result['language'],
                            result['region'],
                            result['director'],
                            result['description'],
                            result['tags']
                        ]
                    ),
                    quote=True
                )
    else:
        await message.reply_text(
            messages.get(
                file="GET_FILM_USAGE",
                key="GET_FILM_USAGE"
            ),
            quote=True
        )




@Client.on_message(filters.private & filters.command("start"))
async def start_bot(client, message):
    if not add_user(message):
        await client.send_message(
            chat_id=Config.LOGS_CHANNEL,
            text=messages.get(
                file="NEW_USER",
                key="NEW_USER",
                extra_args=[
                    message.from_user.first_name,
                    message.from_user.last_name,
                    message.from_user.username,
                    message.from_user.id,
                    message.from_user.id,
                ]
            )
        )
    if is_banned(message):
        await message.reply_text(           
            text=messages.get(file="BANNED_USER", key="BANNED_USER"),
            quote=True
        )
    else:
        await message.reply_photo(
            photo="https://random-image-pepebigotes.vercel.app/api/random-image",
            caption=messages.get(file="START_NORMAL", key="START_NORMAL"),
            quote=True
        )

@Client.on_message(filters.private & filters.command("help"))
async def help_bot(client, message):
    if is_banned(message):
        await message.reply_text(           
            text=messages.get(file="BANNED_USER", key="BANNED_USER"),
            quote=True
        )
    else:
        await message.reply_text(
            text=messages.get(
                file="HELP",
                key="HELP"
            ),
            quote=True,
            disable_web_page_preview=True
        )    
