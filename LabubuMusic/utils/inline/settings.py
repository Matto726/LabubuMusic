from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def setting_markup(_):
    return [
        [
            InlineKeyboardButton(text=_["ST_B_1"], callback_data="AU"),
            InlineKeyboardButton(text=_["ST_B_3"], callback_data="LG"),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_2"], callback_data="PM"),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_4"], callback_data="VM"),
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
        ],
    ]

def vote_mode_markup(_, current, mode=None):
    switch_text = _["ST_B_5"] if mode else _["ST_B_6"]
    
    return [
        [
            InlineKeyboardButton(text="Vᴏᴛɪɴɢ ᴍᴏᴅᴇ ➜", callback_data="VOTEANSWER"),
            InlineKeyboardButton(text=switch_text, callback_data="VOMODECHANGE"),
        ],
        [
            InlineKeyboardButton(text="-2", callback_data="FERRARIUDTI M|{mode}"),
            InlineKeyboardButton(text=f"Current: {current}", callback_data="ANSWERVOMODE"),
            InlineKeyboardButton(text="+2", callback_data="FERRARIUDTI A|{mode}"),
        ],
        [
            InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settings_helper"),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
        ],
    ]

def auth_users_markup(_, status=None):
    auth_state_text = _["ST_B_8"] if status else _["ST_B_9"]
    
    return [
        [
            InlineKeyboardButton(text=_["ST_B_11"], callback_data="AUTHANSWER"),
            InlineKeyboardButton(text=auth_state_text, callback_data="AUTH"),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_7"], callback_data="AUTHLIST"),
        ],
        [
            InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settings_helper"),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
        ],
    ]

def playmode_users_markup(_, direct=None, group=None, playtype=None):
    return [
        [
            InlineKeyboardButton(text=_["ST_B_10"], callback_data="SEARCHANSWER"),
            InlineKeyboardButton(
                text=_["ST_B_11"] if direct else _["ST_B_12"],
                callback_data="MODECHANGE"
            ),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_13"], callback_data="AUTHANSWER"),
            InlineKeyboardButton(
                text=_["ST_B_8"] if group else _["ST_B_9"],
                callback_data="CHANNELMODECHANGE"
            ),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_14"], callback_data="PLAYTYPEANSWER"),
            InlineKeyboardButton(
                text=_["ST_B_8"] if playtype else _["ST_B_9"],
                callback_data="PLAYTYPECHANGE"
            ),
        ],
        [
            InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settings_helper"),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
        ],
    ]