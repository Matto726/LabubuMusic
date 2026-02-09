import asyncio
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from LabubuMusic import YouTube, matto_bot
from LabubuMusic.misc import SUDO_USERS
from LabubuMusic.utils.database import (
    get_assistant,
    get_cmode,
    get_lang,
    get_playmode,
    get_playtype,
    is_active_chat,
    is_maintenance,
)
from LabubuMusic.utils.inline import botplaylist_markup
from config import PLAYLIST_IMG_URL, SUPPORT_GROUP, adminlist
from strings import get_string

link_cache = {}

def PlayWrapper(command_handler):
    async def wrapper(client, message):
        chat_id = message.chat.id

        if await is_maintenance() is False:
            if message.from_user.id not in SUDO_USERS:
                return await message.reply_text(
                    f"Bot is under maintenance. Support: {SUPPORT_GROUP}",
                    disable_web_page_preview=True
                )

        try:
            lang_code = await get_lang(chat_id)
            _ = get_string(lang_code)
        except:
            _ = get_string("en")

        if message.sender_chat:
            play_mode = await get_playmode(chat_id)
            play_type = await get_playtype(chat_id)
        else:
            play_mode = await get_playmode(chat_id)
            play_type = await get_playtype(chat_id)

        if play_type == "Admin":
            if message.from_user.id not in SUDO_USERS:
                admins = adminlist.get(chat_id, [])
                if message.from_user.id not in admins:
                    return await message.reply_text(_["play_4"])

        audio_file = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
        video_file = (message.reply_to_message.video or message.reply_to_message.document) if message.reply_to_message else None
        query = message.text.split(None, 1)[1] if len(message.command) > 1 else None

        if not audio_file and not video_file and not query:
            if play_mode == "Direct":
                return await message.reply_text(_["play_18"], reply_markup=InlineKeyboardMarkup(botplaylist_markup(_)))
            else:
                return await message.reply_text(_["play_18"])

        target_chat_id = chat_id
        is_channel_mode = False
        
        if await get_cmode(chat_id):
            is_channel_mode = True
            c_id = await get_cmode(chat_id)
            origin_chat = await matto_bot.get_chat(c_id)
            if not origin_chat.username:
                return await message.reply_text(_["general_6"])
            target_chat_id = c_id

        userbot = await get_assistant(chat_id)
        try:
            await userbot.get_chat_member(target_chat_id, userbot.id)
        except UserNotParticipant:

            status_msg = await message.reply_text(_["call_4"].format(userbot.name))
            try:
                invite_link = link_cache.get(target_chat_id)
                if not invite_link:
                    try:
                        invite_link = await matto_bot.export_chat_invite_link(target_chat_id)
                        link_cache[target_chat_id] = invite_link
                    except:
                        return await status_msg.edit(_["call_2"])

                await userbot.join_chat(invite_link)

                try:
                    await matto_bot.approve_chat_join_request(target_chat_id, userbot.id)
                except:
                    pass
                    
                await asyncio.sleep(2)
                await status_msg.edit(_["call_5"].format(matto_bot.mention))
            except Exception as e:
                return await status_msg.edit(f"Assistant failed to join: {e}")

        video = False
        force_play = False
        cmd = message.command[0][0].lower()
        
        if "v" in message.command[0]:
            video = True
        if "force" in message.command[0]:
            force_play = True

        return await command_handler(
            client,
            message,
            _,
            target_chat_id,
            video,
            is_channel_mode,
            play_mode,
            query,
            force_play
        )

    return wrapper