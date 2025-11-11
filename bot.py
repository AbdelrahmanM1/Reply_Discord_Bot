# ============================================================
#  File: bot.py
#  Author: 3bdoabk
#  Description:
#      Discord bot that detects the word "badlion" (in English or Arabic)
#      and replies differently depending on whether accounts are claimed.
#      Uses the .env variable "EMPTY" to determine account availability.
#      Detects mentions of "room" or "channel" and adjusts responses accordingly.
#
#      If DMs are disabled, the bot automatically sends the message
#      in the first accessible text channel.
#
#  الوصف:
#      بوت ديسكورد يتحقق من كلمة "بادليون" أو "badlion".
#      يغيّر الرد حسب ما إذا كانت الحسابات متاحة (من خلال متغير EMPTY في ملف .env).
#      يتعرف على كلمات "room" أو "channel" لتعديل الرد حسب السياق.
#
#      إذا كانت الرسائل الخاصة مغلقة، يرسل البوت الرد في أول قناة نصية متاحة.
#
#  Made by 3bdoabk © 2025
# ============================================================

import os
import re
import logging
import discord
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

# -------------------- SETUP --------------------
load_dotenv()  # Load environment variables

TOKEN = os.getenv("DISCORD_TOKEN")
EMPTY = os.getenv("EMPTY", "False").lower() == "true"

# Logging setup
logging.basicConfig(level=logging.INFO)

# ------------------ CONFIGURATION ------------------
BADLION_PATTERN = re.compile(r"\bbadlion\b|بادليون", re.IGNORECASE | re.UNICODE)
ROOM_PATTERN = re.compile(r"\broom\b|روم", re.IGNORECASE | re.UNICODE)
CHANNEL_PATTERN = re.compile(r"\bchannel\b|قناة", re.IGNORECASE | re.UNICODE)

# Discord Intents
intents = Intents.default()
intents.messages = True
intents.members = True
intents.guilds = True
intents.message_content = True

# -------------------- SPAM PROTECTION --------------------
user_trigger_count = {}
SPAM_LIMIT = 5  # Maximum replies per user to avoid spamming

# Initialize bot (no commands)
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# -------------------- FUNCTIONS --------------------

async def send_message(member: discord.Member, message: str):
    """
    Sends a DM to a user if possible; otherwise, sends in a fallback channel.
    Always mentions the user in the reply.
    """
    formatted_message = f"{member.mention} — {message}"

    try:
        await member.send(formatted_message)
        logging.info(f"Sent DM to {member}")

    except discord.Forbidden:
        # Fallback: send in the first accessible text channel
        for channel in member.guild.text_channels:
            if channel.permissions_for(member.guild.me).send_messages:
                await channel.send(formatted_message)
                logging.info(f"Sent fallback message in #{channel.name} for {member}")
                return
        logging.error("No accessible channel found for fallback message.")


def contains_badlion(text: str) -> bool:
    """Check if text contains 'badlion' (English or Arabic)."""
    return bool(BADLION_PATTERN.search(text))


def contains_room_or_channel(text: str) -> bool:
    """Check if text mentions 'room' or 'channel' (English or Arabic)."""
    return bool(ROOM_PATTERN.search(text) or CHANNEL_PATTERN.search(text))


def is_arabic(text: str) -> bool:
    """Detect if text contains Arabic characters."""
    return bool(re.search(r'[\u0600-\u06FF]', text))


def generate_reply(text: str) -> str | None:
    """Generate a reply based on the EMPTY variable."""
    return generate_reply_empty_true(text) if EMPTY else generate_reply_empty_false(text)


def generate_reply_empty_true(text: str) -> str | None:
    """Generate reply when accounts are claimed (EMPTY = True)."""
    if not contains_badlion(text):
        return None

    arabic = is_arabic(text)

    if contains_room_or_channel(text):
        return "الموضوع اتقفل حالياً ، ممكن يفتح تاني " if arabic else "The room/channel is currently closed, it may open again later."
    else:
        return "الحسابات خلصت و ايضاً ممكن تكسب حسابات من الفعاليات." if arabic else "All Badlion accounts have been claimed — but you can still win some through events!"


def generate_reply_empty_false(text: str) -> str | None:
    """Generate reply when accounts are available (EMPTY = False)."""
    if not contains_badlion(text):
        return None

    arabic = is_arabic(text)

    if contains_room_or_channel(text):
        return "لا زالت هناك حسابات بادليون متاحة — تحقق من الفعاليات للفوز بأحدها!" if arabic else "There are still some Badlion accounts available — check the events to win one!"
    else:
        return "موضوع و القناة مفتوحة حالياً الحق قبل ما تقفل" if arabic else "The room/channel is currently open — act before it closes."


# -------------------- EVENTS --------------------

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Bot is running and monitoring messages...")


@bot.event
async def on_member_join(member: discord.Member):
    """
    Triggered when a new member joins — checks their name for 'badlion'
    and sends an appropriate message.
    """
    combined_name = " ".join(filter(None, [member.name, member.display_name, member.nick]))
    reply = generate_reply(combined_name)
    if reply:
        await send_message(member, reply)


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    user_id = message.author.id
    if user_id not in user_trigger_count:
        user_trigger_count[user_id] = 0

    reply = generate_reply(message.content)

    if reply:
        if user_trigger_count[user_id] >= SPAM_LIMIT:
            logging.info(f"Skipped reply to {message.author} (spam limit reached)")
            return

        try:
            await message.channel.send(f"{message.author.mention} — {reply}")
            logging.info(f"Replied to {message.author} in #{message.channel.name}")
            user_trigger_count[user_id] += 1
        except discord.HTTPException:
            logging.warning("Could not send message in this channel.")


# -------------------- RUN BOT --------------------
if __name__ == "__main__":
    if not TOKEN:
        print("Missing DISCORD_TOKEN in .env file.")
    else:
        bot.run(TOKEN)
