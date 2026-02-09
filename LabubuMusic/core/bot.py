import pyrogram
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus, ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import config
from ..logging import log_factory

class Matto(Client):
    def __init__(self):
        log_factory("LabubuMusic").info("Initializing Matto Client...")
        super().__init__(
            name="LabubuMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        
        # Load Bot Profile
        myself = await self.get_me()
        self.username = myself.username
        self.id = myself.id
        self.name = f"{myself.first_name} {myself.last_name or ''}".strip()
        self.mention = myself.mention

        # Startup Interface
        add_button = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(
                    text="Add Me To Your Group",
                    url=f"https://t.me/{self.username}?startgroup=true",
                )
            ]]
        )

        # Log Group Notification
        if config.LOG_GROUP_ID:
            await self._send_startup_log(add_button)
            await self._check_admin_status()
        else:
            log_factory("LabubuMusic").warning("LOG_GROUP_ID is missing in config.")

        log_factory("LabubuMusic").info(f"Music Bot Started as {self.name}")

    async def _send_startup_log(self, markup):
        """Internal method to send the startup message."""
        msg_text = (
            f"<b>🎵 Labubu Music Active</b>\n\n"
            f"<b>Name:</b> {self.name}\n"
            f"<b>Username:</b> @{self.username}\n"
            f"<b>ID:</b> <code>{self.id}</code>\n\n"
            f"<i>System online.</i>"
        )
        try:
            await self.send_photo(
                config.LOG_GROUP_ID,
                photo=config.START_IMG_URL,
                caption=msg_text,
                reply_markup=markup,
            )
        except pyrogram.errors.ChatWriteForbidden:
            log_factory("LabubuMusic").error("Bot is not an admin in the log group.")
            # Fallback to text message
            try:
                await self.send_message(
                    config.LOG_GROUP_ID,
                    msg_text,
                    reply_markup=markup,
                )
            except Exception as e:
                log_factory("LabubuMusic").error(f"Log group unreachable: {e}")
        except Exception as ex:
            log_factory("LabubuMusic").error(f"Startup log failed: {ex}")

    async def _check_admin_status(self):
        """Verifies admin permissions in the log group."""
        try:
            member = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
            if member.status != ChatMemberStatus.ADMINISTRATOR:
                log_factory("LabubuMusic").error("Bot requires Admin rights in the Logger Group.")
        except Exception as e:
            log_factory("LabubuMusic").error(f"Admin check failed: {e}")

    async def stop(self):
        await super().stop()