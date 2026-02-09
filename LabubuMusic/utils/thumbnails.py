import os
import random
import aiohttp
import aiofiles
from PIL import Image, ImageDraw, ImageFont
from LabubuMusic import matto_bot

CACHE_PATH = "cache"
FONT_MAIN = "LabubuMusic/assets/font2.ttf"
FONT_SUB = "LabubuMusic/assets/font3.ttf"
BG_IMAGE = "LabubuMusic/assets/ShrutiBots.jpg"

if not os.path.isdir(CACHE_PATH):
    os.makedirs(CACHE_PATH)

def format_text(draw, text, font, width_limit):
    """Wraps text to fit within a specific width."""
    current_lines = []
    current_line = []
    
    for word in text.split():
        current_line.append(word)
        w, _ = draw.textsize(" ".join(current_line), font=font)
        if w > width_limit:
            current_line.pop()
            current_lines.append(" ".join(current_line))
            current_line = [word]
            
    if current_line:
        current_lines.append(" ".join(current_line))
        
    return current_lines

async def gen_thumb(video_id: str):
    """
    Generates a custom thumbnail for the playing track.
    """
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail_url) as resp:
            data = await resp.read()
            
    temp_input = f"{CACHE_PATH}/temp_{video_id}.png"
    final_output = f"{CACHE_PATH}/final_{video_id}.png"
    
    async with aiofiles.open(temp_input, "wb") as f:
        await f.write(data)

    try:
        source_img = Image.open(temp_input).convert("RGBA")
        base_canvas = Image.open(BG_IMAGE).convert("RGBA")

        source_img = source_img.resize((400, 400))

        base_canvas.paste(source_img, (50, 150), source_img if source_img.mode == 'RGBA' else None)

        canvas = ImageDraw.Draw(base_canvas)
        
        f_title = ImageFont.truetype(FONT_MAIN, 50)
        f_sub = ImageFont.truetype(FONT_SUB, 30)
        
        base_canvas.save(final_output)
        
        if os.path.exists(temp_input):
            os.remove(temp_input)
            
        return final_output
        
    except Exception:
        return BG_IMAGE