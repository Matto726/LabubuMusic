from pyrogram.enums import MessageEntityType
from pyrogram.types import Message, User
from LabubuMusic import matto_bot

async def extract_user(message: Message) -> User:
    """
    Extracts a User object from a message via reply, mention, or ID.
    """
    if message.reply_to_message:
        return message.reply_to_message.from_user

    entities = message.entities
    cmd_offset = 1 if message.text.startswith("/") else 0
    
    if not entities or len(entities) <= cmd_offset:
        return None

    entity = entities[cmd_offset]
    
    if entity.type == MessageEntityType.TEXT_MENTION:
        return entity.user
    
    if len(message.command) > 1:
        arg = message.command[1]

        if arg.isdigit():
            try:
                return await matto_bot.get_users(int(arg))
            except:
                pass

        try:
            return await matto_bot.get_users(arg)
        except:
            return None
            
    return None