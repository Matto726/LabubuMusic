import aiohttp

API_ENDPOINT = "https://batbin.me/api/v2/paste"
BASE_URL = "https://batbin.me/"

async def _send_post_request(url: str, payload: dict):
    """Internal helper for async requests."""
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            try:
                return await response.json()
            except:
                return {}

async def MattoBin(content: str):
    """
    Uploads text to BatBin and returns the link.
    """
    if not content:
        return None
        
    payload = {"content": content}
    result = await _send_post_request(API_ENDPOINT, payload)
    
    if result.get("success"):
        return f"{BASE_URL}{result['message']}"
    return None

NandBin = MattoBin