from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def stats_buttons(_, is_sudo):
    buttons = [
        [
            InlineKeyboardButton(text=_["SA_B_1"], callback_data="TopOverall")
        ]
    ]
    
    if is_sudo:
        buttons = [
            [
                InlineKeyboardButton(text=_["SA_B_2"], callback_data="bot_stats_sudo"),
                InlineKeyboardButton(text=_["SA_B_3"], callback_data="TopOverall"),
            ]
        ]

    buttons.append([InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")])
    
    return InlineKeyboardMarkup(buttons)

def back_stats_buttons(_):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="stats_back"),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
        ]
    ])