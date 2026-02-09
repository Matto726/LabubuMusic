from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

answer = [
    InlineQueryResultArticle(
        title="⏸ Pause",
        description="Pause the current stream.",
        thumb_url="https://telegra.ph/file/c5952790fa8235f499749.jpg",
        input_message_content=InputTextMessageContent("/pause"),
    ),
    InlineQueryResultArticle(
        title="▶️ Resume",
        description="Resume the paused stream.",
        thumb_url="https://telegra.ph/file/c5952790fa8235f499749.jpg",
        input_message_content=InputTextMessageContent("/resume"),
    ),
    InlineQueryResultArticle(
        title="⏭ Skip",
        description="Skip to next track.",
        thumb_url="https://telegra.ph/file/c5952790fa8235f499749.jpg",
        input_message_content=InputTextMessageContent("/skip"),
    ),
    InlineQueryResultArticle(
        title="⏹ End",
        description="Stop playback and leave.",
        thumb_url="https://telegra.ph/file/c5952790fa8235f499749.jpg",
        input_message_content=InputTextMessageContent("/end"),
    ),
    InlineQueryResultArticle(
        title="🔀 Shuffle",
        description="Shuffle the playlist.",
        thumb_url="https://telegra.ph/file/c5952790fa8235f499749.jpg",
        input_message_content=InputTextMessageContent("/shuffle"),
    ),
    InlineQueryResultArticle(
        title="🔁 Loop",
        description="Loop current track.",
        thumb_url="https://telegra.ph/file/c5952790fa8235f499749.jpg",
        input_message_content=InputTextMessageContent("/loop 3"),
    ),
]