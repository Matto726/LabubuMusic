from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def queue_markup(_, duration, cplay, vid, played=None, dur=None):
    close_btn = InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")

    queued_btn = InlineKeyboardButton(
        text=_["QU_B_1"],
        callback_data=f"GetQueued {cplay}|{vid}"
    )

    if duration == "Unknown":
        return InlineKeyboardMarkup([[queued_btn, close_btn]])

    timer_btn = InlineKeyboardButton(
        text=_["QU_B_2"].format(played, dur),
        callback_data="GetTimer"
    )
    
    return InlineKeyboardMarkup([
        [timer_btn],
        [queued_btn, close_btn]
    ])

def queue_back_markup(_, cplay):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data=f"queue_back_timer {cplay}"
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data="close"
            )
        ]
    ])

def aq_markup(_, chat_id):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data="close"
            )
        ]
    ])