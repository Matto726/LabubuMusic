import time
import psutil
from LabubuMusic.misc import BOOT_TIMESTAMP
from LabubuMusic.utils.formatters import get_readable_time

async def bot_sys_stats():
    """
    Gathers system statistics (Uptime, CPU, RAM, Disk).
    """
    current_time = time.time()
    uptime_seconds = int(current_time - BOOT_TIMESTAMP)
    uptime_str = get_readable_time(uptime_seconds)

    cpu_load = f"{psutil.cpu_percent(interval=0.5)}%"

    ram = psutil.virtual_memory()
    ram_usage = f"{ram.percent}%"

    disk = psutil.disk_usage("/")
    disk_usage = f"{disk.percent}%"

    return uptime_str, cpu_load, ram_usage, disk_usage