import os
from config import autoclean

async def auto_clean(track_data: dict):
    """
    Manages the clean-up of downloaded files after playback.
    """
    file_path = track_data.get("file")
    
    try:
        if file_path in autoclean:
            autoclean.remove(file_path)
    except ValueError:
        pass

    if autoclean.count(file_path) == 0:
        is_local_file = (
            "vid_" not in file_path 
            and "live_" not in file_path 
            and "index_" not in file_path
        )
        
        if is_local_file and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                pass