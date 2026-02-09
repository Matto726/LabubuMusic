import config
from LabubuMusic.core.mongo import mongodb

onoff_collection = mongodb.onoffper
autoend_collection = mongodb.autoend
autoleave_collection = mongodb.autoleave
lang_collection = mongodb.language
cplay_collection = mongodb.cplaymode
playmode_collection = mongodb.playmode
playtype_collection = mongodb.playtypedb
skip_collection = mongodb.skipmode
auth_collection = mongodb.authuser
upvote_collection = mongodb.upcount

loop_state = {}
playtype_state = {}
playmode_state = {}
channel_connect_state = {}
lang_cache = {}
pause_state = {}
active_voice_chats = []
active_video_chats = []
non_admin_chats = {}
maintenance_mode = []
autoend_state = {}


async def get_active_chats() -> list:
    return active_voice_chats

async def is_active_chat(chat_id: int) -> bool:
    return chat_id in active_voice_chats

async def add_active_chat(chat_id: int):
    if chat_id not in active_voice_chats:
        active_voice_chats.append(chat_id)

async def remove_active_chat(chat_id: int):
    if chat_id in active_voice_chats:
        active_voice_chats.remove(chat_id)

async def music_on(chat_id: int):
    pause_state[chat_id] = True

async def music_off(chat_id: int):
    pause_state[chat_id] = False

async def is_music_playing(chat_id: int) -> bool:
    return pause_state.get(chat_id, False)

async def get_active_video_chats() -> list:
    return active_video_chats

async def add_active_video_chat(chat_id: int):
    if chat_id not in active_video_chats:
        active_video_chats.append(chat_id)

async def remove_active_video_chat(chat_id: int):
    if chat_id in active_video_chats:
        active_video_chats.remove(chat_id)


async def get_loop(chat_id: int) -> int:
    return loop_state.get(chat_id, 0)

async def set_loop(chat_id: int, mode: int):
    loop_state[chat_id] = mode


async def get_lang(chat_id: int) -> str:
    if chat_id in lang_cache:
        return lang_cache[chat_id]
    
    doc = await lang_collection.find_one({"chat_id": chat_id})
    lang = doc["lang"] if doc else "en"
    lang_cache[chat_id] = lang
    return lang

async def set_lang(chat_id: int, lang: str):
    lang_cache[chat_id] = lang
    await lang_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"lang": lang}},
        upsert=True
    )


async def is_autoend() -> bool:
    doc = await autoend_collection.find_one({"name": "autoend"})
    return doc is not None

async def autoend_on():
    await autoend_collection.insert_one({"name": "autoend"})

async def autoend_off():
    await autoend_collection.delete_one({"name": "autoend"})

async def is_autoleave() -> bool:
    doc = await autoleave_collection.find_one({"name": "autoleave"})
    return doc is not None

async def autoleave_on():
    await autoleave_collection.insert_one({"name": "autoleave"})

async def autoleave_off():
    await autoleave_collection.delete_one({"name": "autoleave"})


async def is_maintenance() -> bool:
    return bool(maintenance_mode)

async def maintenance_on():
    maintenance_mode.append(1)

async def maintenance_off():
    maintenance_mode.clear()


async def get_authuser_names(chat_id: int) -> list:
    doc = await auth_collection.find_one({"chat_id": chat_id})
    return doc["auth_users"] if doc else []

async def get_authuser(chat_id: int, name: str) -> dict:
    doc = await auth_collection.find_one({"chat_id": chat_id})
    if doc and name in doc["auth_users"]:
        return doc["auth_users"][name]
    return None

async def save_authuser(chat_id: int, name: str, data: dict):
    doc = await auth_collection.find_one({"chat_id": chat_id})
    current_users = doc["auth_users"] if doc else {}
    current_users[name] = data
    
    await auth_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"auth_users": current_users}},
        upsert=True
    )

async def delete_authuser(chat_id: int, name: str):
    doc = await auth_collection.find_one({"chat_id": chat_id})
    if not doc or name not in doc["auth_users"]:
        return False
        
    current_users = doc["auth_users"]
    del current_users[name]
    
    await auth_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"auth_users": current_users}},
        upsert=True
    )
    return True


async def get_playmode(chat_id: int) -> str:
    if chat_id in playmode_state:
        return playmode_state[chat_id]
    doc = await playmode_collection.find_one({"chat_id": chat_id})
    mode = doc["mode"] if doc else "Everyone"
    playmode_state[chat_id] = mode
    return mode

async def set_playmode(chat_id: int, mode: str):
    playmode_state[chat_id] = mode
    await playmode_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"mode": mode}},
        upsert=True
    )

async def get_playtype(chat_id: int) -> str:
    if chat_id in playtype_state:
        return playtype_state[chat_id]
    doc = await playtype_collection.find_one({"chat_id": chat_id})
    ptype = doc["mode"] if doc else "Everyone"
    playtype_state[chat_id] = ptype
    return ptype

async def set_playtype(chat_id: int, mode: str):
    playtype_state[chat_id] = mode
    await playtype_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"mode": mode}},
        upsert=True
    )


async def get_cmode(chat_id: int) -> int:
    if chat_id in channel_connect_state:
        return channel_connect_state[chat_id]
    doc = await cplay_collection.find_one({"chat_id": chat_id})
    cmode = doc["mode"] if doc else None
    channel_connect_state[chat_id] = cmode
    return cmode

async def set_cmode(chat_id: int, mode: int):
    channel_connect_state[chat_id] = mode
    await cplay_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"mode": mode}},
        upsert=True
    )


async def is_nonadmin_chat(chat_id: int) -> bool:
    return chat_id in non_admin_chats

async def add_nonadmin_chat(chat_id: int):
    non_admin_chats[chat_id] = True

async def remove_nonadmin_chat(chat_id: int):
    if chat_id in non_admin_chats:
        del non_admin_chats[chat_id]


async def is_on_off(config_type: int) -> bool:
    doc = await onoff_collection.find_one({"type": config_type})
    return bool(doc)

async def add_on(config_type: int):
    await onoff_collection.insert_one({"type": config_type})

async def add_off(config_type: int):
    await onoff_collection.delete_one({"type": config_type})

async def get_upvote_count(chat_id: int) -> int:
    doc = await upvote_collection.find_one({"chat_id": chat_id})
    return doc["count"] if doc else 0

async def set_upvotes(chat_id: int, count: int):
    await upvote_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"count": count}},
        upsert=True
    )

async def is_skipmode(chat_id: int) -> bool:
    doc = await skip_collection.find_one({"chat_id": chat_id})
    return bool(doc)

async def skip_on(chat_id: int):
    await skip_collection.insert_one({"chat_id": chat_id})

async def skip_off(chat_id: int):
    await skip_collection.delete_one({"chat_id": chat_id})