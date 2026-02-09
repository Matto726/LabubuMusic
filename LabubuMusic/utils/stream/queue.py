import asyncio
from typing import Union

from LabubuMusic.misc import db
from LabubuMusic.utils.formatters import check_duration, seconds_to_min
from config import autoclean, time_to_seconds

async def put_queue(
    chat_id,
    original_chat_id,
    file_path,
    title,
    duration,
    user,
    vidid,
    user_id,
    stream_type,
    forceplay: Union[bool, str] = None,
):
    """
    Adds a standard track (YouTube/File) to the playback queue.
    """
    clean_title = title.title()
    
    try:
        duration_seconds = time_to_seconds(duration) - 3
    except:
        duration_seconds = 0
        
    track_meta = {
        "title": clean_title,
        "dur": duration,
        "streamtype": stream_type,
        "by": user,
        "user_id": user_id,
        "chat_id": original_chat_id,
        "file": file_path,
        "vidid": vidid,
        "seconds": duration_seconds,
        "played": 0,
    }
    
    autoclean.append(file_path)
    
    if forceplay:
        current_queue = db.get(chat_id)
        if current_queue:
            current_queue.insert(0, track_meta)
        else:
            db[chat_id] = [track_meta]
    else:
        if chat_id in db:
            db[chat_id].append(track_meta)
        else:
            db[chat_id] = [track_meta]

async def put_queue_index(
    chat_id,
    original_chat_id,
    file_path,
    title,
    duration,
    user,
    vidid,
    stream_type,
    forceplay: Union[bool, str] = None,
):
    """
    Adds a URL/Index stream to the playback queue.
    """
    if "20.212.146.162" in vidid:
        try:
            raw_dur = await asyncio.get_event_loop().run_in_executor(
                None, check_duration, vidid
            )
            duration = seconds_to_min(raw_dur)
            dur_sec = raw_dur
        except:
            duration = "ᴜʀʟ sᴛʀᴇᴀᴍ"
            dur_sec = 0
    else:
        dur_sec = 0

    track_meta = {
        "title": title,
        "dur": duration,
        "streamtype": stream_type,
        "by": user,
        "chat_id": original_chat_id,
        "file": file_path,
        "vidid": vidid,
        "seconds": dur_sec,
        "played": 0,
    }
    
    if forceplay:
        queue = db.get(chat_id)
        if queue:
            queue.insert(0, track_meta)
        else:
            db[chat_id] = [track_meta]
    else:
        if chat_id in db:
            db[chat_id].append(track_meta)
        else:
            db[chat_id] = [track_meta]