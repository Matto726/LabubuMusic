import random
from LabubuMusic import userbot
from LabubuMusic.core.mongo import mongodb

assistant_collection = mongodb.assistants

assistant_cache = {}

async def get_client(assistant_id: int):
    """
    Retrieves the client instance for a given assistant ID.
    """
    client_map = {
        1: userbot.one,
        2: userbot.two,
        3: userbot.three,
        4: userbot.four,
        5: userbot.five,
    }
    return client_map.get(int(assistant_id))

async def save_assistant(chat_id, assistant_num):
    """
    Updates the assistant assigned to a specific chat in the database.
    """
    try:
        await assistant_collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"assistant": int(assistant_num)}},
            upsert=True,
        )
        return True
    except Exception:
        return False

async def set_assistant(chat_id):
    """
    Randomly assigns an available assistant to a chat and saves it.
    """
    from LabubuMusic.core.userbot import active_assistants

    selected_ass = random.choice(active_assistants)

    assistant_cache[chat_id] = selected_ass

    await save_assistant(chat_id, selected_ass)
    return selected_ass

async def get_assistant(chat_id: int) -> str:
    """
    Retrieves the assistant name/token for a chat.
    """
    from LabubuMusic.core.userbot import active_assistants

    cached_id = assistant_cache.get(chat_id)
    if cached_id:
        if cached_id in active_assistants:
            return cached_id
        return await set_assistant(chat_id)

    db_data = await assistant_collection.find_one({"chat_id": chat_id})
    if not db_data:
        return await set_assistant(chat_id)

    stored_ass = db_data["assistant"]
    if stored_ass in active_assistants:
        assistant_cache[chat_id] = stored_ass
        return stored_ass
    else:
        return await set_assistant(chat_id)

async def group_assistant(self, chat_id: int) -> int:
    """
    Returns the actual Pyrogram client object for the assigned assistant.
    """
    assistant_idx = await get_assistant(chat_id)
    
    if int(assistant_idx) == 1:
        return self.one
    elif int(assistant_idx) == 2:
        return self.two
    elif int(assistant_idx) == 3:
        return self.three
    elif int(assistant_idx) == 4:
        return self.four
    elif int(assistant_idx) == 5:
        return self.five
    else:
        return self.one