import os
from ..logging import log_factory

def clean_directories():
    """Cleanups temporary files and ensures directory structure."""
    file_types = [".jpg", ".jpeg", ".png"]
    
    for filename in os.listdir():
        if any(filename.endswith(ext) for ext in file_types):
            try:
                os.remove(filename)
            except OSError:
                pass

    for folder in ["downloads", "cache"]:
        if folder not in os.listdir():
            os.mkdir(folder)

    log_factory("LabubuMusic").info("Directories cleaned and verified.")