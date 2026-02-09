from pykeyboard import InlineKeyboard
from pyrogram.types import InlineKeyboardButton as Ikb
from .functions import get_urls_from_text

def ikb(data: dict, row_width: int = 2):
    """
    Generates an InlineKeyboard from a dictionary {Text: Data/URL}.
    """
    keyboard = InlineKeyboard(row_width=row_width)
    buttons_list = []
    
    for text, value in data.items():
        if get_urls_from_text(value):
            btn = Ikb(text=str(text), url=str(value))
        else:
            btn = Ikb(text=str(text), callback_data=str(value))
        buttons_list.append(btn)
        
    keyboard.add(*buttons_list)
    return keyboard