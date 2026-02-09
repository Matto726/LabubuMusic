from functools import wraps
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
from pyrogram.types import Message

from LabubuMusic import matto_bot
from LabubuMusic.misc import SUDO_USERS

async def check_privileges(chat_id: int, user_id: int):
    """
    Returns a list of privileges held by a user in a chat.
    """
    try:
        member = await matto_bot.get_chat_member(chat_id, user_id)
    except Exception:
        return []

    if not member.privileges:
        return []

    privileges = member.privileges
    granted = []
    
    if privileges.can_post_messages:
        granted.append("can_post_messages")
    if privileges.can_edit_messages:
        granted.append("can_edit_messages")
    if privileges.can_delete_messages:
        granted.append("can_delete_messages")
    if privileges.can_restrict_members:
        granted.append("can_restrict_members")
    if privileges.can_promote_members:
        granted.append("can_promote_members")
    if privileges.can_invite_users:
        granted.append("can_invite_users")
    if privileges.can_pin_messages:
        granted.append("can_pin_messages")
    if privileges.can_manage_video_chats:
        granted.append("can_manage_video_chats")
        
    return granted

async def deny_access(message, missing_perm):
    """Sends denial message."""
    try:
        await message.reply_text(
            f"🚫 **Permission Denied**\n\n"
            f"You lack the following permission: `{missing_perm}`"
        )
    except:
        pass

def adminsOnly(required_perm):
    """
    Decorator to restrict commands to admins with specific permissions.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(client, message: Message, *args, **kwargs):
            chat_id = message.chat.id

            bot_perms = await check_privileges(chat_id, matto_bot.id)
            if required_perm not in bot_perms:
                return await message.reply_text(
                    f"⚠️ I don't have the required permission: `{required_perm}`"
                )

            if not message.from_user:
                if message.sender_chat and message.sender_chat.id == chat_id:
                    return await func(client, message, *args, **kwargs)
                return await deny_access(message, required_perm)

            user_id = message.from_user.id

            if user_id in SUDO_USERS:
                return await func(client, message, *args, **kwargs)

            user_perms = await check_privileges(chat_id, user_id)
            if required_perm not in user_perms:
                return await deny_access(message, required_perm)

            return await func(client, message, *args, **kwargs)
        return wrapper
    return decorator