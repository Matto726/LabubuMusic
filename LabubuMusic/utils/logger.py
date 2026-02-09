from pyrogram.enums import ParseMode
from LabubuMusic import matto_bot
from LabubuMusic.utils.database import is_on_off
from config import LOG_GROUP_ID

async def play_logs(message, stream_type: str):
    """
    Logs track playback details to the configured log group.
    """
    if not await is_on_off(2):
        return

    if message.chat.id == LOG_GROUP_ID:
        return

    user = message.from_user
    user_id = user.id
    user_mention = user.mention
    username = f"@{user.username}" if user.username else "No Username"

    query = message.text.split(None, 1)[1] if len(message.command) > 1 else "Unknown/Direct"

    log_entry = (
        f"**{matto_bot.mention} Playback Log**\n\n"
        f"**Chat:** {message.chat.title} [`{message.chat.id}`]\n"
        f"**Chat Tag:** @{message.chat.username or 'Private'}\n\n"
        f"**User:** {user_mention} [`{user_id}`]\n"
        f"**Handle:** {username}\n\n"
        f"**Query:** {query}\n"
        f"**Type:** {stream_type}"
    )

    try:
        await matto_bot.send_message(
            chat_id=LOG_GROUP_ID,
            text=log_entry,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    except Exception:
        pass