from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from LabubuMusic import matto_bot
from LabubuMusic.misc import SUDO_USERS
from LabubuMusic.utils.database import (
    get_authuser_names,
    get_cmode,
    get_lang,
    is_active_chat,
    is_maintenance,
    is_nonadmin_chat,
)
from config import SUPPORT_GROUP, adminlist
from strings import get_string
from ..formatters import int_to_alpha

async def _check_maintenance(client, message, from_user_id):
    """Internal helper to check maintenance mode."""
    if await is_maintenance() is False:
        if from_user_id not in SUDO_USERS:
            if hasattr(message, "reply_text"):
                await message.reply_text(
                    text=f"{matto_bot.mention} is under maintenance. Visit <a href={SUPPORT_GROUP}>Support Chat</a>.",
                    disable_web_page_preview=True,
                )
            else:
                await message.answer(
                    f"{matto_bot.mention} is under maintenance.",
                    show_alert=True
                )
            return False
    return True

def AdminActual(coroutine):
    """Decorator to enforce Admin permissions (Message)."""
    async def wrapper(client, message):
        if not await _check_maintenance(client, message, message.from_user.id):
            return

        if message.sender_chat:
            return await message.reply_text("You're an Anonymous Admin!")
            
        is_non_admin = await is_nonadmin_chat(message.chat.id)
        if not is_non_admin:
            if message.from_user.id in SUDO_USERS:
                return await coroutine(client, message, None)

            chat_admins = adminlist.get(message.chat.id)
            if not chat_admins:
                return await message.reply_text("Admin cache missing. Reload admin cache.")

            if message.from_user.id not in chat_admins:
                token = await int_to_alpha(message.from_user.id)
                auth_users = await get_authuser_names(message.chat.id)
                if token not in auth_users:
                    return await message.reply_text("You don't have permissions to use this.")
        
        return await coroutine(client, message, None)

    return wrapper

AdminRightsCheck = AdminActual

def ActualAdminCB(coroutine):
    """Decorator to enforce Admin permissions (CallbackQuery)."""
    async def wrapper(client, cb, _):
        if not await _check_maintenance(client, cb, cb.from_user.id):
            return

        try:
            language = await get_lang(cb.message.chat.id)
            _ = get_string(language)
        except:
            _ = get_string("en")

        if cb.message.chat.type == ChatType.PRIVATE:
            return await coroutine(client, cb, _)

        is_non_admin = await is_nonadmin_chat(cb.message.chat.id)
        if not is_non_admin:
            try:
                member = await matto_bot.get_chat_member(cb.message.chat.id, cb.from_user.id)
                can_manage = member.privileges.can_manage_video_chats if member.privileges else False
            except:
                can_manage = False

            if not can_manage:
                if cb.from_user.id not in SUDO_USERS:
                    token = await int_to_alpha(cb.from_user.id)
                    auth_users = await get_authuser_names(cb.message.chat.id)
                    
                    if token not in auth_users:
                        return await cb.answer(_["general_4"], show_alert=True)

        return await coroutine(client, cb, _)

    return wrapper