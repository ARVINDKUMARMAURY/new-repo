import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize bot
bot = Client(
    "bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
)

@bot.on_message(filters.command("start"))
async def start_handler(client: Client, message: Message):
    """Handle /start command"""
    await message.reply_text(
        f"👋 Welcome to {Config.BOT_NAME}!\n\n"
        "Use /help to see available commands."
    )
    logger.info(f"User {message.from_user.id} started the bot")

@bot.on_message(filters.command("help"))
async def help_handler(client: Client, message: Message):
    """Handle /help command"""
    help_text = """
    📖 **Available Commands:**
    
    /start - Start the bot
    /help - Show this message
    /ping - Check bot status
    """
    await message.reply_text(help_text)

@bot.on_message(filters.command("ping"))
async def ping_handler(client: Client, message: Message):
    """Handle /ping command"""
    await message.reply_text("🏓 Pong!")
    logger.info(f"Ping from user {message.from_user.id}")

def main():
    """Start the bot"""
    logger.info("🤖 Bot is starting...")
    bot.run()

if __name__ == "__main__":
    main()