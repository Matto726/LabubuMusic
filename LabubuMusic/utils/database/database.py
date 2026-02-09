import random
import asyncio
from datetime import date
from LabubuMusic.core.mongo import mongodb

sudoers_col = mongodb.sudoers
blocked_col = mongodb.blockedusers
served_chats_col = mongodb.served_chats
served_users_col = mongodb.served_users
daily_stats_col = mongodb.daily_stats

async def get_sudoers() -> list:
    doc = await sudoers_col.find_one({"sudo": "sudo"})
    return doc["sudoers"] if doc else []

async def add_sudo(user_id: int) -> bool:
    current_sudoers = await get_sudoers()
    if user_id in current_sudoers:
        return False
        
    current_sudoers.append(user_id)
    await sudoers_col.update_one(
        {"sudo": "sudo"},
        {"$set": {"sudoers": current_sudoers}},
        upsert=True
    )
    return True

async def remove_sudo(user_id: int) -> bool:
    current_sudoers = await get_sudoers()
    if user_id not in current_sudoers:
        return False
        
    current_sudoers.remove(user_id)
    await sudoers_col.update_one(
        {"sudo": "sudo"},
        {"$set": {"sudoers": current_sudoers}},
        upsert=True
    )
    return True


async def get_banned_users() -> list:
    banned_list = []
    cursor = blocked_col.find({"user_id": {"$gt": 0}})
    async for entry in cursor:
        banned_list.append(entry["user_id"])
    return banned_list

async def get_banned_count() -> int:
    return await blocked_col.count_documents({"user_id": {"$gt": 0}})

async def is_banned_user(user_id: int) -> bool:
    result = await blocked_col.find_one({"user_id": user_id})
    return bool(result)

async def add_banned_user(user_id: int):
    if not await is_banned_user(user_id):
        await blocked_col.insert_one({"user_id": user_id})

async def remove_banned_user(user_id: int):
    if await is_banned_user(user_id):
        await blocked_col.delete_one({"user_id": user_id})


async def get_served_chats() -> list:
    chat_list = []
    async for chat in served_chats_col.find({"chat_id": {"$lt": 0}}):
        chat_list.append(chat)
    return chat_list

async def is_served_chat(chat_id: int) -> bool:
    doc = await served_chats_col.find_one({"chat_id": chat_id})
    return bool(doc)

async def add_served_chat(chat_id: int):
    if not await is_served_chat(chat_id):
        await served_chats_col.insert_one({"chat_id": chat_id})

async def delete_served_chat(chat_id: int):
    if await is_served_chat(chat_id):
        await served_chats_col.delete_one({"chat_id": chat_id})


async def get_served_users() -> list:
    users_list = []
    async for user in served_users_col.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list

async def is_served_user(user_id: int) -> bool:
    doc = await served_users_col.find_one({"user_id": user_id})
    return bool(doc)

async def add_served_user(user_id: int):
    if not await is_served_user(user_id):
        await served_users_col.insert_one({"user_id": user_id})
        
add_gban_user = add_banned_user
remove_gban_user = remove_banned_user