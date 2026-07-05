import asyncio
from datetime import datetime

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
from pytgcalls import PyTgCalls, filters as call_filters
from pytgcalls.types import MediaStream

import config
import database as db
import musicqueue as q
from youtube import YouTube

# ===================== Clients =====================
bot = Client(
    "musicbot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
)

assistant = Client(
    "assistant",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.SESSION_STRING,
)

call_py = PyTgCalls(assistant)


# ===================== Helpers =====================

async def log(text: str):
    if config.LOG_GROUP_ID:
        try:
            await bot.send_message(config.LOG_GROUP_ID, text)
        except Exception:
            pass


async def is_authorized(chat_id: int, user_id: int) -> bool:
    if user_id == config.OWNER_ID:
        return True
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        if member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
            return True
    except Exception:
        pass
    return await db.is_auth_user(chat_id, user_id)


async def track_served(message: Message):
    await db.add_served_user(message.from_user.id)
    if message.chat.type != "private":
        await db.add_served_chat(message.chat.id)


async def start_playback(chat_id: int, song: dict):
    """Downloads (or fetches from cache) and starts streaming a song."""
    local_path = await YouTube.download(song["vidid"], video=song["video"])
    if not local_path:
        await bot.send_message(chat_id, f"❌ '{song['title']}' fetch nahi ho paya xBit API se.")
        return await play_next(chat_id)

    await call_py.play(chat_id, MediaStream(local_path))
    q.set_current(chat_id, song)
    await bot.send_message(
        chat_id,
        f"▶️ Ab baj raha hai: **{song['title']}**\nRequested by: {song['requested_by']}",
    )
    await log(
        f"🎵 Song played\nChat: `{chat_id}`\nTitle: {song['title']}\n"
        f"Requested by: {song['requested_by']}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )


async def play_next(chat_id: int):
    next_song = q.pop_next(chat_id)
    if next_song:
        await start_playback(chat_id, next_song)
    else:
        q.clear_current(chat_id)
        try:
            await call_py.leave_call(chat_id)
        except Exception:
            pass


@call_py.on_update(call_filters.stream_end())
async def stream_end_handler(_, update):
    await play_next(update.chat_id)


# ===================== Commands =====================

@bot.on_message(filters.command("start"))
async def start_cmd(_, message: Message):
    await track_served(message)
    await message.reply_text(
        "Namaste! Main ek simple music bot hoon.\n\n"
        "/play <song name> - gaana bajao\n"
        "/vplay <song name> - video bajao\n"
        "/pause /resume /skip /stop /end\n"
        "/queue - queue dekho\n"
        "/shuffle - queue shuffle karo\n"
        "/authuser - permission do/hatao (reply karke)"
    )


async def _play_handler(_, message: Message, video: bool):
    await track_served(message)
    chat_id = message.chat.id

    if len(message.command) < 2:
        return await message.reply_text("Gaana ka naam ya link do. Example: `/play tum hi ho`")

    query = message.text.split(None, 1)[1]
    searching = await message.reply_text("🔎 Dhoondh raha hoon...")

    details, vidid = await YouTube.track(query, videoid=False)
    if not vidid:
        return await searching.edit_text("❌ Kuch nahi mila is naam se.")

    if details["duration_sec"] and details["duration_sec"] > config.DURATION_LIMIT:
        return await searching.edit_text(
            f"❌ Ye gaana bahut lamba hai ({details['duration_min']}). "
            f"Max allowed: {config.DURATION_LIMIT // 60} min."
        )

    song = {
        "title": details["title"],
        "vidid": vidid,
        "duration": details["duration_min"],
        "requested_by": message.from_user.mention,
        "video": video,
    }

    if q.is_active(chat_id):
        added = q.add_to_queue(chat_id, song)
        if not added:
            return await searching.edit_text(f"❌ Queue full hai (max {config.QUEUE_LIMIT}).")
        await searching.edit_text(f"✅ Queue me add ho gaya: **{song['title']}**")
        try:
            await message.delete()
        except Exception:
            pass
        return

    q.add_to_queue(chat_id, song)
    await searching.delete()
    first_song = q.pop_next(chat_id)
    await start_playback(chat_id, first_song)
    try:
        await message.delete()
    except Exception:
        pass


@bot.on_message(filters.command("play"))
async def play_cmd(client, message: Message):
    await _play_handler(client, message, video=False)


@bot.on_message(filters.command("vplay"))
async def vplay_cmd(client, message: Message):
    await _play_handler(client, message, video=True)


@bot.on_message(filters.command("pause"))
async def pause_cmd(_, message: Message):
    if not await is_authorized(message.chat.id, message.from_user.id):
        return await message.reply_text("❌ Sirf admins/authorized users hi ye kar sakte hain.")
    await call_py.pause(message.chat.id)
    await message.reply_text("⏸ Paused.")


@bot.on_message(filters.command("resume"))
async def resume_cmd(_, message: Message):
    if not await is_authorized(message.chat.id, message.from_user.id):
        return await message.reply_text("❌ Sirf admins/authorized users hi ye kar sakte hain.")
    await call_py.resume(message.chat.id)
    await message.reply_text("▶️ Resumed.")


@bot.on_message(filters.command("skip"))
async def skip_cmd(_, message: Message):
    if not await is_authorized(message.chat.id, message.from_user.id):
        return await message.reply_text("❌ Sirf admins/authorized users hi ye kar sakte hain.")
    await message.reply_text("⏭ Skip kiya.")
    await play_next(message.chat.id)
    try:
        await message.delete()
    except Exception:
        pass


@bot.on_message(filters.command(["stop", "end"]))
async def stop_cmd(_, message: Message):
    if not await is_authorized(message.chat.id, message.from_user.id):
        return await message.reply_text("❌ Sirf admins/authorized users hi ye kar sakte hain.")
    q.clear_queue(message.chat.id)
    q.clear_current(message.chat.id)
    try:
        await call_py.leave_call(message.chat.id)
    except Exception:
        pass
    await message.reply_text("⏹ Stopped aur queue clear kar diya.")
    try:
        await message.delete()
    except Exception:
        pass


@bot.on_message(filters.command("queue"))
async def queue_cmd(_, message: Message):
    songs = q.get_queue(message.chat.id)
    if not songs:
        return await message.reply_text("Queue khali hai.")
    text = "📋 **Queue:**\n\n"
    for i, s in enumerate(songs, 1):
        text += f"{i}. {s['title']} — {s['requested_by']}\n"
    await message.reply_text(text)


@bot.on_message(filters.command("shuffle"))
async def shuffle_cmd(_, message: Message):
    if not await is_authorized(message.chat.id, message.from_user.id):
        return await message.reply_text("❌ Sirf admins/authorized users hi ye kar sakte hain.")
    if q.shuffle_queue(message.chat.id):
        await message.reply_text("🔀 Queue shuffle ho gayi.")
    else:
        await message.reply_text("Shuffle ke liye queue me kam se kam 2 gaane chahiye.")


@bot.on_message(filters.command("authuser"))
async def authuser_cmd(_, message: Message):
    chat_id = message.chat.id
    if not await is_authorized(chat_id, message.from_user.id):
        return await message.reply_text("❌ Sirf admins hi authuser manage kar sakte hain.")

    target = None
    if message.reply_to_message:
        target = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try:
            target = await bot.get_users(message.command[1])
        except Exception:
            return await message.reply_text("❌ User nahi mila.")

    if not target:
        return await message.reply_text("Kisi member ke message par reply karo, ya `/authuser <user_id>` likho.")

    already = await db.is_auth_user(chat_id, target.id)
    if already:
        await db.remove_auth_user(chat_id, target.id)
        await message.reply_text(f"🚫 {target.mention} ka authuser access hataa diya.")
    else:
        await db.add_auth_user(chat_id, target.id)
        await message.reply_text(f"✅ {target.mention} ko authuser bana diya.")


@bot.on_message(filters.command("broadcast") & filters.user(config.OWNER_ID))
async def broadcast_cmd(_, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text("Broadcast karne ke liye text do ya kisi message par reply karke `/broadcast` likho.")

    sent, failed = 0, 0
    users = await db.get_served_users()
    chats = await db.get_served_chats()

    status = await message.reply_text("📢 Broadcast shuru...")

    for uid in users:
        try:
            if message.reply_to_message:
                await message.reply_to_message.copy(uid)
            else:
                await bot.send_message(uid, message.text.split(None, 1)[1])
            sent += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.1)

    for cid in chats:
        try:
            if message.reply_to_message:
                await message.reply_to_message.copy(cid)
            else:
                await bot.send_message(cid, message.text.split(None, 1)[1])
            sent += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.1)

    await status.edit_text(f"✅ Broadcast complete.\nSent: {sent} | Failed: {failed}")


# ===================== Startup =====================

async def main():
    await bot.start()
    await assistant.start()
    await call_py.start()
    await log(f"✅ Bot start ho gaya!\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Bot started.")
    await asyncio.Event().wait()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
