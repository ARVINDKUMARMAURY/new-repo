import os

from pyrogram.types import InlineKeyboardMarkup, Message

from button_styles import primary_button, success_button, danger_button

BANNER_PATH = os.path.join(os.path.dirname(__file__), "assets", "start_banner.jpg")

DEVELOPER_URL = "https://t.me/Avisha_Asstiant"
SUPPORT_URL = "https://t.me/Avisha_101"
SOURCE_URL = "https://t.me/Avisha_101"


async def send_dm_start(bot, message: Message):
    """Sends the photo-based welcome menu, used only in private chats (DM)."""
    caption = (
        f"Hey {message.from_user.mention}, 🔥\n\n"
        "This is **Avisha** !\n\n"
        "A music player bot with some awesome and useful features.\n\n"
        "Click on the help button for more info."
    )

    buttons = InlineKeyboardMarkup(
        [
            [primary_button("➕ Add me to your group", url=f"https://t.me/{bot.me.username}?startgroup=true")],
            [success_button("❓ Help", callback_data="show_help")],
            [
                primary_button("👨‍💻 Developer", url=DEVELOPER_URL),
                success_button("💬 Support", url=SUPPORT_URL),
            ],
            [danger_button("📢 Source", url=SOURCE_URL)],
        ]
    )

    if os.path.exists(BANNER_PATH):
        await message.reply_photo(BANNER_PATH, caption=caption, reply_markup=buttons)
    else:
        await message.reply_text(caption, reply_markup=buttons)


HELP_TEXT = (
    "🎵 **Avisha Commands**\n\n"
    "**Music**\n"
    "/play <song> - play a song\n"
    "/vplay <song> - play a video\n"
    "/pause - pause playback\n"
    "/resume - resume playback\n"
    "/skip - skip current song\n"
    "/stop or /end - stop and clear queue\n"
    "/queue - view the queue\n"
    "/shuffle - shuffle the queue\n\n"
    "**Group Management**\n"
    "/authuser - grant/revoke permission (reply to a user)\n"
    "/vclogger - toggle VC join/leave logging\n\n"
    "**Moderation** (admins only)\n"
    "/mute /unmute - restrict/allow messages\n"
    "/ban /unban - remove/allow a user\n"
    "/promote /demote - manage admin status\n"
    "/warn /unwarn /warnings - warning system (3 warns = auto-ban)\n\n"
    "**Utility**\n"
    "/id - get numeric ID (reply or @username)\n"
    "/status - bot diagnostics (owner only)\n"
    "/restart - restart the bot (owner only)\n"
    "/broadcast - message all users/chats (owner only)"
)


async def send_help(bot, chat_id: int):
    buttons = InlineKeyboardMarkup(
        [
            [
                primary_button("👨‍💻 Developer", url=DEVELOPER_URL),
                success_button("💬 Support", url=SUPPORT_URL),
            ]
        ]
    )
    await bot.send_message(chat_id, HELP_TEXT, reply_markup=buttons)
