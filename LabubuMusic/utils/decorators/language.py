from LabubuMusic.misc import SUDO_USERS
from LabubuMusic.utils.database import get_lang, is_maintenance
from config import SUPPORT_GROUP
from strings import get_string
from LabubuMusic import matto_bot

async def fetch_language(chat_id):
    try:
        code = await get_lang(chat_id)
        return get_string(code)
    except:
        return get_string("en")

def language(coroutine):
    """Injects language strings into message handlers."""
    async def wrapper(_, message, **kwargs):
        if await is_maintenance() is False:
            if message.from_user.id not in SUDO_USERS:
                return await message.reply_text(
                    f"{matto_bot.mention} is in maintenance mode.",
                    disable_web_page_preview=True
                )

        try:
            await message.delete()
        except:
            pass

        _ = await fetch_language(message.chat.id)
        return await coroutine(_, message, _)

    return wrapper

def languageCB(coroutine):
    """Injects language strings into callback handlers."""
    async def wrapper(_, cb, **kwargs):
        if await is_maintenance() is False:
            if cb.from_user.id not in SUDO_USERS:
                return await cb.answer(
                    f"{matto_bot.mention} Maintenance Mode: ON",
                    show_alert=True
                )
        
        _ = await fetch_language(cb.message.chat.id)
        return await coroutine(_, cb, _)

    return wrapper

def LanguageStart(coroutine):
    """Specific wrapper for Start command."""
    async def wrapper(_, message, **kwargs):
        _ = await fetch_language(message.chat.id)
        return await coroutine(_, message, _)

    return wrapper