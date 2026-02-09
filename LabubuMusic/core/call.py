import asyncio
import os
from datetime import datetime, timedelta
from typing import Union

from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.exceptions import (
    AlreadyJoinedError,
    NoActiveGroupCall,
    TelegramServerError,
)
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio, MediumQualityVideo
from pytgcalls.types.stream import StreamAudioEnded

import config
from LabubuMusic import log_factory, YouTube, matto_bot
from LabubuMusic.misc import db
from LabubuMusic.utils.database import (
    add_active_chat,
    add_active_video_chat,
    get_lang,
    get_loop,
    group_assistant,
    is_autoend,
    music_on,
    remove_active_chat,
    remove_active_video_chat,
    set_loop,
)
from LabubuMusic.utils.exceptions import AssistantErr
from LabubuMusic.utils.formatters import check_duration, seconds_to_min, speed_converter
from LabubuMusic.utils.inline.play import stream_markup
from LabubuMusic.utils.stream.autoclear import auto_clean
from LabubuMusic.utils.thumbnails import gen_thumb
from strings import get_string

auto_end_timers = {}
call_counter = {}

async def reset_chat_status(chat_id):
    db[chat_id] = []
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)

class MusicPlayer(PyTgCalls):
    def __init__(self):
        self.clients = {}
        
        
        session_list = [
            (1, config.STRING1), (2, config.STRING2), 
            (3, config.STRING3), (4, config.STRING4), 
            (5, config.STRING5)
        ]
        
        for idx, session in session_list:
            if session:
                client = Client(
                    name=f"MattoAss{idx}",
                    api_id=config.API_ID,
                    api_hash=config.API_HASH,
                    session_string=str(session),
                )
                self.clients[idx] = PyTgCalls(client, cache_duration=100)
                setattr(self, f"userbot{idx}", client)
                setattr(self, f"one" if idx==1 else f"two" if idx==2 else f"three" if idx==3 else f"four" if idx==4 else "five", self.clients[idx])

    async def pause_stream(self, chat_id: int):
        ass = await group_assistant(self, chat_id)
        await ass.pause_stream(chat_id)

    async def resume_stream(self, chat_id: int):
        ass = await group_assistant(self, chat_id)
        await ass.resume_stream(chat_id)

    async def stop_stream(self, chat_id: int):
        ass = await group_assistant(self, chat_id)
        try:
            await reset_chat_status(chat_id)
            await ass.leave_group_call(chat_id)
        except:
            pass

    async def stop_stream_force(self, chat_id: int):
        
        for i in range(1, 6):
            try:
                client = getattr(self, f"one" if i==1 else f"two" if i==2 else f"three" if i==3 else f"four" if i==4 else "five", None)
                if client and getattr(config, f"STRING{i}"):
                    await client.leave_group_call(chat_id)
            except:
                pass
        try:
            await reset_chat_status(chat_id)
        except:
            pass

    async def speedup_stream(self, chat_id: int, file_path, speed, playing):
        ass = await group_assistant(self, chat_id)
        final_path = file_path
        
        if str(speed) != "1.0":
            filename = os.path.basename(file_path)
            playback_dir = os.path.join(os.getcwd(), "playback", str(speed))
            if not os.path.isdir(playback_dir):
                os.makedirs(playback_dir)
            
            final_path = os.path.join(playback_dir, filename)
            
            if not os.path.isfile(final_path):
                
                speed_map = {"0.5": 2.0, "0.75": 1.35, "1.5": 0.68, "2.0": 0.5}
                vs = speed_map.get(str(speed), 1.0)
                
                cmd = (
                    f"ffmpeg -i {file_path} -filter:v setpts={vs}*PTS "
                    f"-filter:a atempo={speed} {final_path}"
                )
                
                process = await asyncio.create_subprocess_shell(
                    cmd,
                    stdin=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                await process.communicate()
        
        duration_sec = int(await asyncio.get_event_loop().run_in_executor(None, check_duration, final_path))
        start_pos, _ = speed_converter(playing[0]["played"], speed)
        duration_min = seconds_to_min(duration_sec)
        
        
        if playing[0]["streamtype"] == "video":
            stream = AudioVideoPiped(
                final_path,
                audio_parameters=HighQualityAudio(),
                video_parameters=MediumQualityVideo(),
                additional_ffmpeg_parameters=f"-ss {start_pos} -to {duration_min}",
            )
        else:
            stream = AudioPiped(
                final_path,
                audio_parameters=HighQualityAudio(),
                additional_ffmpeg_parameters=f"-ss {start_pos} -to {duration_min}",
            )

        if str(db[chat_id][0]["file"]) == str(file_path):
            await ass.change_stream(chat_id, stream)
            
            
            if not db[chat_id][0].get("old_dur"):
                db[chat_id][0]["old_dur"] = db[chat_id][0]["dur"]
                db[chat_id][0]["old_second"] = db[chat_id][0]["seconds"]
            
            db[chat_id][0].update({
                "played": _,
                "dur": duration_min,
                "seconds": duration_sec,
                "speed_path": final_path,
                "speed": speed
            })
        else:
            raise AssistantErr("State mismatch")

    async def force_stop_stream(self, chat_id: int):
        ass = await group_assistant(self, chat_id)
        try:
            current_q = db.get(chat_id)
            if current_q:
                current_q.pop(0)
        except:
            pass
        
        await remove_active_video_chat(chat_id)
        await remove_active_chat(chat_id)
        try:
            await ass.leave_group_call(chat_id)
        except:
            pass

    async def skip_stream(self, chat_id: int, link: str, video: Union[bool, str] = None, image: Union[bool, str] = None):
        ass = await group_assistant(self, chat_id)
        if video:
            stream = AudioVideoPiped(link, audio_parameters=HighQualityAudio(), video_parameters=MediumQualityVideo())
        else:
            stream = AudioPiped(link, audio_parameters=HighQualityAudio())
        await ass.change_stream(chat_id, stream)

    async def seek_stream(self, chat_id, file_path, to_seek, duration, mode):
        ass = await group_assistant(self, chat_id)
        params = f"-ss {to_seek} -to {duration}"
        
        if mode == "video":
            stream = AudioVideoPiped(
                file_path,
                audio_parameters=HighQualityAudio(),
                video_parameters=MediumQualityVideo(),
                additional_ffmpeg_parameters=params,
            )
        else:
            stream = AudioPiped(
                file_path,
                audio_parameters=HighQualityAudio(),
                additional_ffmpeg_parameters=params,
            )
        await ass.change_stream(chat_id, stream)

    async def stream_call(self, link):
        ass = await group_assistant(self, config.LOG_GROUP_ID)
        await ass.join_group_call(
            config.LOG_GROUP_ID,
            AudioVideoPiped(link),
            stream_type=StreamType().pulse_stream,
        )
        await asyncio.sleep(0.2)
        await ass.leave_group_call(config.LOG_GROUP_ID)

    async def join_call(self, chat_id: int, original_chat_id: int, link, video: Union[bool, str] = None, image: Union[bool, str] = None):
        ass = await group_assistant(self, chat_id)
        lang_code = await get_lang(chat_id)
        txt = get_string(lang_code)
        
        stream_obj = AudioVideoPiped(link, audio_parameters=HighQualityAudio(), video_parameters=MediumQualityVideo()) if video else AudioPiped(link, audio_parameters=HighQualityAudio())
        
        try:
            await ass.join_group_call(chat_id, stream_obj, stream_type=StreamType().pulse_stream)
        except NoActiveGroupCall:
            raise AssistantErr(txt["call_8"])
        except AlreadyJoinedError:
            raise AssistantErr(txt["call_9"])
        except TelegramServerError:
            raise AssistantErr(txt["call_10"])
            
        await add_active_chat(chat_id)
        await music_on(chat_id)
        
        if video:
            await add_active_video_chat(chat_id)
            
        if await is_autoend():
            call_counter[chat_id] = {}
            if len(await ass.get_participants(chat_id)) == 1:
                auto_end_timers[chat_id] = datetime.now() + timedelta(minutes=1)

    async def change_stream(self, client, chat_id):
        queue = db.get(chat_id)
        popped_track = None
        loop_count = await get_loop(chat_id)
        
        try:
            if loop_count == 0:
                popped_track = queue.pop(0)
            else:
                await set_loop(chat_id, loop_count - 1)
            
            await auto_clean(popped_track)
            
            if not queue:
                await reset_chat_status(chat_id)
                return await client.leave_group_call(chat_id)
        except:
            try:
                await reset_chat_status(chat_id)
                return await client.leave_group_call(chat_id)
            except:
                return

        track_info = queue[0]
        lang_code = await get_lang(chat_id)
        txt = get_string(lang_code)
        
        title = track_info["title"].title()
        requester = track_info["by"]
        orig_chat = track_info["chat_id"]
        s_type = track_info["streamtype"]
        vid_id = track_info["vidid"]
        
        db[chat_id][0]["played"] = 0
        if track_info.get("old_dur"):
            db[chat_id][0]["dur"] = track_info["old_dur"]
            db[chat_id][0]["seconds"] = track_info["old_second"]
            db[chat_id][0]["speed_path"] = None
            db[chat_id][0]["speed"] = 1.0

        is_video = (str(s_type) == "video")
        
        
        if "live_" in queued := track_info["file"]:
            status, link = await YouTube.video(vid_id, True)
            if status == 0:
                return await matto_bot.send_message(orig_chat, text=txt["call_6"])
            
            stream = AudioVideoPiped(link, audio_parameters=HighQualityAudio(), video_parameters=MediumQualityVideo()) if is_video else AudioPiped(link, audio_parameters=HighQualityAudio())
            
            try:
                await client.change_stream(chat_id, stream)
            except:
                return await matto_bot.send_message(orig_chat, text=txt["call_6"])
            
            img_path = await gen_thumb(vid_id)
            msg = await matto_bot.send_photo(
                chat_id=orig_chat,
                photo=img_path,
                caption=txt["stream_1"].format(f"https://t.me/{matto_bot.username}?start=info_{vid_id}", title[:23], track_info["dur"], requester),
                reply_markup=InlineKeyboardMarkup(stream_markup(txt, chat_id)),
            )
            db[chat_id][0]["mystic"] = msg
            db[chat_id][0]["markup"] = "tg"

        elif "vid_" in queued:
            temp_msg = await matto_bot.send_message(orig_chat, txt["call_7"])
            try:
                fpath, _ = await YouTube.download(vid_id, temp_msg, videoid=True, video=is_video)
            except:
                return await temp_msg.edit_text(txt["call_6"], disable_web_page_preview=True)
            
            stream = AudioVideoPiped(fpath, audio_parameters=HighQualityAudio(), video_parameters=MediumQualityVideo()) if is_video else AudioPiped(fpath, audio_parameters=HighQualityAudio())
            
            try:
                await client.change_stream(chat_id, stream)
            except:
                return await matto_bot.send_message(orig_chat, text=txt["call_6"])
            
            img_path = await gen_thumb(vid_id)
            await temp_msg.delete()
            msg = await matto_bot.send_photo(
                chat_id=orig_chat,
                photo=img_path,
                caption=txt["stream_1"].format(f"https://t.me/{matto_bot.username}?start=info_{vid_id}", title[:23], track_info["dur"], requester),
                reply_markup=InlineKeyboardMarkup(stream_markup(txt, chat_id)),
            )
            db[chat_id][0]["mystic"] = msg
            db[chat_id][0]["markup"] = "stream"

        elif "index_" in queued:
            stream = AudioVideoPiped(vid_id, audio_parameters=HighQualityAudio(), video_parameters=MediumQualityVideo()) if is_video else AudioPiped(vid_id, audio_parameters=HighQualityAudio())
            
            try:
                await client.change_stream(chat_id, stream)
            except:
                return await matto_bot.send_message(orig_chat, text=txt["call_6"])
                
            msg = await matto_bot.send_photo(
                chat_id=orig_chat,
                photo=config.STREAM_IMG_URL,
                caption=txt["stream_2"].format(requester),
                reply_markup=InlineKeyboardMarkup(stream_markup(txt, chat_id)),
            )
            db[chat_id][0]["mystic"] = msg
            db[chat_id][0]["markup"] = "tg"

        else:
            stream = AudioVideoPiped(queued, audio_parameters=HighQualityAudio(), video_parameters=MediumQualityVideo()) if is_video else AudioPiped(queued, audio_parameters=HighQualityAudio())
            
            try:
                await client.change_stream(chat_id, stream)
            except:
                return await matto_bot.send_message(orig_chat, text=txt["call_6"])
            
            if vid_id == "telegram":
                img_url = config.TELEGRAM_AUDIO_URL if str(s_type) == "audio" else config.TELEGRAM_VIDEO_URL
                msg = await matto_bot.send_photo(
                    chat_id=orig_chat,
                    photo=img_url,
                    caption=txt["stream_1"].format(config.SUPPORT_GROUP, title[:23], track_info["dur"], requester),
                    reply_markup=InlineKeyboardMarkup(stream_markup(txt, chat_id)),
                )
                db[chat_id][0]["mystic"] = msg
                db[chat_id][0]["markup"] = "tg"
            elif vid_id == "soundcloud":
                msg = await matto_bot.send_photo(
                    chat_id=orig_chat,
                    photo=config.SOUNCLOUD_IMG_URL,
                    caption=txt["stream_1"].format(config.SUPPORT_GROUP, title[:23], track_info["dur"], requester),
                    reply_markup=InlineKeyboardMarkup(stream_markup(txt, chat_id)),
                )
                db[chat_id][0]["mystic"] = msg
                db[chat_id][0]["markup"] = "tg"
            else:
                img_path = await gen_thumb(vid_id)
                msg = await matto_bot.send_photo(
                    chat_id=orig_chat,
                    photo=img_path,
                    caption=txt["stream_1"].format(f"https://t.me/{matto_bot.username}?start=info_{vid_id}", title[:23], track_info["dur"], requester),
                    reply_markup=InlineKeyboardMarkup(stream_markup(txt, chat_id)),
                )
                db[chat_id][0]["mystic"] = msg
                db[chat_id][0]["markup"] = "stream"

    async def ping(self):
        latency_list = []
        for i in range(1, 6):
            if getattr(config, f"STRING{i}"):
                client = getattr(self, f"one" if i==1 else f"two" if i==2 else f"three" if i==3 else f"four" if i==4 else "five")
                latency_list.append(await client.ping)
        
        return str(round(sum(latency_list) / len(latency_list), 3)) if latency_list else "0"

    async def start(self):
        log_factory("LabubuMusic").info("Initializing Music Player...\n")
        for i in range(1, 6):
            if getattr(config, f"STRING{i}"):
                client = getattr(self, f"one" if i==1 else f"two" if i==2 else f"three" if i==3 else f"four" if i==4 else "five")
                await client.start()

    async def decorators(self):
        clients = [self.one, self.two, self.three, self.four, self.five]
        
        for cli in clients:
            @cli.on_kicked()
            @cli.on_closed_voice_chat()
            @cli.on_left()
            async def stream_services_handler(_, chat_id: int):
                await self.stop_stream(chat_id)

            @cli.on_stream_end()
            async def stream_end_handler(client, update: Update):
                if isinstance(update, StreamAudioEnded):
                    await self.change_stream(client, update.chat_id)

Matto = MusicPlayer()