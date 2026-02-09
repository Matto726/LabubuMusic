import os
from random import randint
from typing import Union

from pyrogram.types import InlineKeyboardMarkup

import config
from LabubuMusic import Carbon, YouTube, matto_bot
from LabubuMusic.core.call import Matto
from LabubuMusic.misc import db
from LabubuMusic.utils.database import add_active_video_chat, is_active_chat
from LabubuMusic.utils.exceptions import AssistantErr
from LabubuMusic.utils.inline import aq_markup, close_markup, stream_markup
from LabubuMusic.utils.pastebin import NandBin
from LabubuMusic.utils.stream.queue import put_queue, put_queue_index
from LabubuMusic.utils.thumbnails import gen_thumb

async def stream(
    _,
    status_msg,
    user_id,
    media_data,
    chat_id,
    user_name,
    original_chat_id,
    video: Union[bool, str] = None,
    streamtype: Union[bool, str] = None,
    spotify: Union[bool, str] = None,
    forceplay: Union[bool, str] = None,
):
    if streamtype == "playlist":
        msg_text = f"{_['playlist_1']}\n\n"
        count = 0
        
        for track in media_data:
            if not await is_active_chat(chat_id):
                try:
                    details, vid_id = await YouTube.track(track, True)
                except Exception:
                    continue
                
                stream_link = details["link"]
                duration = details["duration_min"]
                title = details["title"]
                thumbnail = details["thumb"]
                
                if await YouTube.exists(stream_link):

                    pass
                else:
                    continue

                await put_queue(
                    chat_id,
                    original_chat_id,
                    f"vid_{vid_id}",
                    title,
                    duration,
                    user_name,
                    vid_id,
                    user_id,
                    "video" if video else "audio",
                )
                
                try:
                    if video:
                        await Matto.join_call(chat_id, original_chat_id, stream_link, video=True)
                    else:
                        downloaded_path = await YouTube.download(
                            stream_link, status_msg, videoid=True, video=False
                        )
                        await Matto.join_call(chat_id, original_chat_id, downloaded_path[0])
                except Exception as e:
                    await status_msg.edit(f"Assistant Connection Failed: {e}")
                    return
                
                if video:
                    await add_active_video_chat(chat_id)

                btn = stream_markup(_, chat_id)
                await matto_bot.send_photo(
                    original_chat_id,
                    photo=thumbnail,
                    caption=_["stream_1"].format(
                        config.SUPPORT_GROUP, title[:23], duration, user_name
                    ),
                    reply_markup=InlineKeyboardMarkup(btn),
                )
            else:
                try:
                    details, vid_id = await YouTube.track(track, True)
                except:
                    continue
                    
                await put_queue(
                    chat_id,
                    original_chat_id,
                    f"vid_{vid_id}",
                    details["title"],
                    details["duration_min"],
                    user_name,
                    vid_id,
                    user_id,
                    "video" if video else "audio",
                )
            count += 1
            
        await status_msg.edit(msg_text + _["playlist_3"].format(count))

    elif streamtype in ["youtube", "soundcloud"]:
        link = media_data["link"]
        vid_id = media_data["vidid"]
        title = (media_data["title"]).title()
        duration = media_data["duration_min"]
        thumbnail = media_data["thumb"]
        
        if await is_active_chat(chat_id):
            queue_len = len(db.get(chat_id)) if db.get(chat_id) else 0
            
            await put_queue(
                chat_id,
                original_chat_id,
                f"vid_{vid_id}" if streamtype == "youtube" else media_data["filepath"],
                title,
                duration,
                user_name,
                vid_id,
                user_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            
            btn = aq_markup(_, chat_id)
            await matto_bot.send_photo(
                original_chat_id,
                photo=thumbnail,
                caption=_["queue_4"].format(queue_len, title[:27], duration, user_name),
                reply_markup=InlineKeyboardMarkup(btn),
            )
            await status_msg.delete()
        else:
            if not forceplay:
                db[chat_id] = []
                
            try:
                if streamtype == "soundcloud":
                    await Matto.join_call(
                        chat_id, original_chat_id, media_data["filepath"], video=None
                    )
                else:
                    if video:
                        status, stream_path = await YouTube.video(link, True)
                        if status == 0:
                            return await status_msg.edit("Video fetch failed.")
                        await Matto.join_call(chat_id, original_chat_id, stream_path, video=True)
                    else:
                        file_path, _ = await YouTube.download(
                            link, status_msg, videoid=True, video=False
                        )
                        await Matto.join_call(chat_id, original_chat_id, file_path)
            except Exception as e:
                return await status_msg.edit(f"Error starting stream: {e}")

            if video:
                await add_active_video_chat(chat_id)
            
            await put_queue(
                chat_id,
                original_chat_id,
                f"vid_{vid_id}" if streamtype == "youtube" else media_data["filepath"],
                title,
                duration,
                user_name,
                vid_id,
                user_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            
            btn = stream_markup(_, chat_id)
            run_msg = await matto_bot.send_photo(
                original_chat_id,
                photo=thumbnail,
                caption=_["stream_1"].format(
                    f"https://t.me/{matto_bot.username}?start=info_{vid_id}",
                    title[:23],
                    duration,
                    user_name,
                ),
                reply_markup=InlineKeyboardMarkup(btn),
            )
            
            db[chat_id][0]["mystic"] = run_msg
            db[chat_id][0]["markup"] = "stream"
            await status_msg.delete()

    elif streamtype in ["telegram", "live", "index"]:
        if streamtype == "telegram":
            target_path = media_data["path"]
            link = media_data["link"]
            title = media_data["title"]
            duration = media_data["dur"]
            vid_id = "telegram"
        elif streamtype == "live":
            target_path = media_data["link"]
            link = media_data["link"]
            title = media_data["title"]
            duration = "Live"
            vid_id = media_data["vidid"]
        else:
            target_path = media_data 
            link = media_data
            title = "Index Stream"
            duration = "Unknown"
            vid_id = "index_url"

        if await is_active_chat(chat_id):
            position = len(db.get(chat_id)) + 1
            await put_queue_index(
                chat_id,
                original_chat_id,
                target_path,
                title,
                duration,
                user_name,
                vid_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            
            btn = aq_markup(_, chat_id)
            await matto_bot.send_photo(
                original_chat_id,
                photo=config.STREAM_IMG_URL,
                caption=_["queue_4"].format(position, title[:27], duration, user_name),
                reply_markup=InlineKeyboardMarkup(btn),
            )
            await status_msg.delete()
        else:
            if not forceplay:
                db[chat_id] = []
                
            await Matto.join_call(
                chat_id,
                original_chat_id,
                target_path,
                video=True if video else None,
            )
            
            if video:
                await add_active_video_chat(chat_id)
                
            await put_queue_index(
                chat_id,
                original_chat_id,
                target_path,
                title,
                duration,
                user_name,
                vid_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            
            btn = stream_markup(_, chat_id)
            run_msg = await matto_bot.send_photo(
                original_chat_id,
                photo=config.STREAM_IMG_URL,
                caption=_["stream_2"].format(user_name),
                reply_markup=InlineKeyboardMarkup(btn),
            )
            
            db[chat_id][0]["mystic"] = run_msg
            db[chat_id][0]["markup"] = "tg"
            await status_msg.delete()