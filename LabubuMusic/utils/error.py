import traceback
from functools import wraps
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
from config import LOG_GROUP_ID
from LabubuMusic import matto_bot

def _split_text(text):
    """Splits long error messages."""
    if len(text) < 2048:
        return [text]
    
    chunks = []
    current_chunk = ""
    for line in text.splitlines(True):
        if len(current_chunk) + len(line) < 2048:
            current_chunk += line
        else:
            chunks.append(current_chunk)
            current_chunk = line
    chunks.append(current_chunk)
    return chunks

def capture_err(func):
    """Decorator to capture and log exceptions."""
    @wraps(func)
    async def wrapper(client, message, *args, **kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except ChatWriteForbidden:
            try:
                await matto_bot.leave_chat(message.chat.id)
            except:
                pass
            return
        except Exception as e:
            err_trace = traceback.format_exc()
            
            user_str = message.from_user.mention if message.from_user else "Unknown"
            chat_str = f"@{message.chat.username}" if message.chat.username else f"`{message.chat.id}`"
            cmd_text = message.text or message.caption or "No Text"
            
            log_text = (
                f"**🚨 EXCEPTION CAUGHT**\n\n"
                f"**User:** {user_str}\n"
                f"**Chat:** {chat_str}\n"
                f"**Command:**\n`{cmd_text}`\n\n"
                f"**Traceback:**\n`{err_trace}`"
            )
            
            for chunk in _split_text(log_text):
                try:
                    await matto_bot.send_message(LOG_GROUP_ID, chunk)
                except:
                    pass
            raise e
            
    return wrapper