from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI
from ..logging import log_factory

log_factory("LabubuMusic").info("Initializing Mongo Database...")

try:
    _client = AsyncIOMotorClient(MONGO_DB_URI)
    mongodb = _client.seven
    log_factory("LabubuMusic").info("Mongo Database Connected.")
except Exception as e:
    log_factory("LabubuMusic").error(f"Mongo Connection Failed: {e}")
    exit()