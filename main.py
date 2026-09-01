import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize bot with in_memory session (no disk files)
bot = Client(
    session_name="bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    in_memory=True,
)

@bot.on_message(filters.command("start"))
async def start_handler(client: Client, message: Message):
    """Handle /start command"""
    try:
        await message.reply_text(
            f"👋 Welcome to {Config.BOT_NAME}!\n\n"
            "Use /help to see available commands."
        )
        logger.info(f"User {message.from_user.id} started the bot")
    except Exception as e:
        logger.error(f"Error in start_handler: {e}")

@bot.on_message(filters.command("help"))
async def help_handler(client: Client, message: Message):
    """Handle /help command"""
    try:
        help_text = """
📖 **Available Commands:**

/start - Start the bot
/help - Show this message
/ping - Check bot status
"""
        await message.reply_text(help_text)
    except Exception as e:
        logger.error(f"Error in help_handler: {e}")

@bot.on_message(filters.command("ping"))
async def ping_handler(client: Client, message: Message):
    """Handle /ping command"""
    try:
        await message.reply_text("🏓 Pong!")
        logger.info(f"Ping from user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in ping_handler: {e}")

async def main():
    """Start the bot"""
    logger.info("🤖 Bot is starting...")
    logger.info(f"Bot Name: {Config.BOT_NAME}")
    logger.info(f"Owner ID: {Config.OWNER_ID}")
    
    try:
        async with bot:
            logger.info("✅ Bot connected successfully!")
            logger.info("👂 Listening for messages...")
            await bot.idle()
    except Exception as e:
        logger.critical(f"🔴 Fatal error: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.critical(f"🔴 Bot failed to start: {e}")
        exit(1)