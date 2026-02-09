from LabubuMusic import matto_bot
from LabubuMusic.utils.database import get_cmode

async def get_channeplayCB(_, command_type, cb):
    """
    Verifies channel play mode settings during callback interactions.
    """
    if command_type == "c":
        chat_id = await get_cmode(cb.message.chat.id)
        if not chat_id:
            try:
                await cb.answer(_["setting_7"], show_alert=True)
                return None, None
            except:
                return None, None
        
        try:
            target_chat = await matto_bot.get_chat(chat_id)
            channel_name = target_chat.title
        except:
            try:
                await cb.answer(_["cplay_4"], show_alert=True)
                return None, None
            except:
                return None, None
    else:
        chat_id = cb.message.chat.id
        channel_name = None
        
    return chat_id, channel_name