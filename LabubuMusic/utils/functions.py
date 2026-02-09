from datetime import datetime, timedelta
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

DevID = 8464526024

MARKDOWN = """
**Formatting Guide:**

<u>Variables:</u>
{GROUPNAME} - Current Chat Name
{NAME} - User's Name
{ID} - User's ID
{FIRSTNAME} - User's First Name
{SURNAME} - User's Last Name
{USERNAME} - User's Username
{DATE} - Current Date
{WEEKDAY} - Day of the Week
{TIME} - Current Time

<u>Markdown Syntax:</u>
**Bold** : `**text**`
*Italic* : `*text*`
__Underline__ : `__text__`
~~Strike~~ : `~~text~~`
`Code` : `` `text` ``
[Hyperlink](google.com) : `[text](url)`
"""

def get_urls_from_text(text: str) -> bool:
    """Checks if text contains a URL."""
    if not text:
        return False
    return "http" in text or "www." in text

async def time_converter(message: Message, input_val: str) -> datetime:
    """Parses a time string (1m, 2h, 3d) into a future datetime."""
    unit_map = {"m": "minutes", "h": "hours", "d": "days"}
    
    unit_char = input_val[-1].lower()
    time_val = input_val[:-1]
    
    if not time_val.isdigit() or unit_char not in unit_map:
        await message.reply_text("Invalid format. Use 1m, 2h, or 3d.")
        return None
        
    amount = int(time_val)
    kwargs = {unit_map[unit_char]: amount}
    
    return datetime.now() + timedelta(**kwargs)