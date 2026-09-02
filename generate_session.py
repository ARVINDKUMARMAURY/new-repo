"""
Generates a Pyrogram (kurigram) session string for the ASSISTANT account
(the userbot that joins voice chats to stream music).

⚠️ Run this on your own PC/laptop/VPS — NOT on Railway — because it needs
you to type your phone number and the OTP code interactively.

Usage:
    pip install kurigram tgcrypto
    python generate_session.py

It will ask for:
  - API_ID / API_HASH (get these from https://my.telegram.org)
  - Phone number (with country code, e.g. +91xxxxxxxxxx)
  - The OTP code Telegram sends you
  - Your 2FA password, if you have one enabled

At the end it prints a SESSION_STRING — copy that value into Railway's
Variables tab for the `worker` service (key: SESSION_STRING).

Keep this string private — anyone who has it can fully control that
Telegram account (read messages, send messages, everything).
"""

from pyrogram import Client

API_ID = int(input("API_ID: ").strip())
API_HASH = input("API_HASH: ").strip()

with Client("temp_session", api_id=API_ID, api_hash=API_HASH, in_memory=True) as app:
    session_string = app.export_session_string()

print("\n" + "=" * 60)
print("✅ Your SESSION_STRING (copy everything below this line):")
print("=" * 60)
print(session_string)
print("=" * 60)
print("\nAdd this to Railway → worker service → Variables → SESSION_STRING")
print("⚠️ Keep it private. Anyone with this string can fully control this account.")
