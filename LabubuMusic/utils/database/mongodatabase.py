from typing import Dict, List
from LabubuMusic.core.mongo import mongodb

playlist_collection = mongodb.playlist

async def _get_playlists(chat_id: int) -> Dict[str, int]:
    """
    Fetches the entire playlist dictionary for a chat.
    """
    document = await playlist_collection.find_one({"chat_id": chat_id})
    if not document:
        return {}
    return document.get("notes", {})

async def get_playlist_names(chat_id: int) -> List[str]:
    """
    Returns a list of playlist item names.
    """
    data = await _get_playlists(chat_id)
    return list(data.keys())

async def get_playlist(chat_id: int, name: str) -> int:
    """
    Gets the value (likely duration or count) of a specific playlist item.
    """
    data = await _get_playlists(chat_id)
    for key, value in data.items():
        if key.lower() == name.lower():
            return value
    return None

async def save_playlist(chat_id: int, name: str, value: int):
    """
    Saves a new item to the playlist.
    """
    current_data = await _get_playlists(chat_id)
    current_data[name] = value
    
    await playlist_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"notes": current_data}},
        upsert=True
    )

async def delete_playlist(chat_id: int, name: str):
    """
    Removes an item from the playlist.
    """
    current_data = await _get_playlists(chat_id)
    
    target_key = None
    for key in current_data:
        if key.lower() == name.lower():
            target_key = key
            break
            
    if target_key:
        del current_data[target_key]
        await playlist_collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"notes": current_data}},
            upsert=True
        )
        return True
    return False