from pyrogram.types import InlineKeyboardButton

def track_markup(_, vid, uid, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {vid}|{uid}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {vid}|{uid}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {vid}|{uid}",
            )
        ],
    ]

def stream_markup(_, chat_id):
    return [
        [
            InlineKeyboardButton(text="▶️", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"], callback_data="close"
            )
        ],
    ]

def stream_markup_timer(_, chat_id, played, duration):
    return [
        [
            InlineKeyboardButton(text="▶️", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(
                text=f"{played} / {duration}",
                callback_data="GetTimer",
            )
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"], callback_data="close"
            )
        ],
    ]

def livestream_markup(_, vid, uid, mode, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],
                callback_data=f"LiveStream {vid}|{uid}|{mode}|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {vid}|{uid}",
            ),
        ],
    ]

def slider_markup(_, vid, uid, query, idx, channel, fplay):
    query_str = f"{query[:20]}"
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {vid}|{uid}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {vid}|{uid}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="◁",
                callback_data=f"slider B|{idx}|{query_str}|{uid}|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {query_str}|{uid}",
            ),
            InlineKeyboardButton(
                text="▷",
                callback_data=f"slider F|{idx}|{query_str}|{uid}|{channel}|{fplay}",
            ),
        ],
    ]

def playlist_markup(_, playlist_id, uid, ptype, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"NandPlaylists {playlist_id}|{uid}|{ptype}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"NandPlaylists {playlist_id}|{uid}|{ptype}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {playlist_id}|{uid}",
            ),
        ],
    ]