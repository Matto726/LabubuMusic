_couple_cache = {}

async def fetch_lovers(chat_id: int):
    """Retrieves the couple dictionary for a chat."""
    data = _couple_cache.get(chat_id, {})
    return data.get("couple", {})

async def get_image(chat_id: int):
    """Retrieves the cached image for the chat."""
    data = _couple_cache.get(chat_id, {})
    return data.get("img", "")

async def get_couple(chat_id: int, date_key: str):
    """Checks if a couple exists for the given date."""
    lovers = await fetch_lovers(chat_id)
    return lovers.get(date_key, False)

async def save_couple(chat_id: int, date_key: str, couple_data: dict, img_url: str):
    """Saves a new couple entry."""
    if chat_id not in _couple_cache:
        _couple_cache[chat_id] = {"couple": {}, "img": ""}
        
    _couple_cache[chat_id]["couple"][date_key] = couple_data
    _couple_cache[chat_id]["img"] = img_url