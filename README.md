# Telegram Bot - Railway Deployment

Telegram bot project designed to run on Railway platform.

## Features

- ✅ Pyrogram-based Telegram bot
- ✅ Easy configuration via environment variables
- ✅ Railway deployment ready
- ✅ Docker support
- ✅ Admin controls

## Quick Start

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/ARVINDKUMARMAURY/new-repo
   cd new-repo
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

5. **Run the bot**
   ```bash
   python main.py
   ```

## Railway Deployment

### Step 1: Connect GitHub Repository
1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select this repository

### Step 2: Add Environment Variables
In Railway Dashboard:
1. Go to Project Settings
2. Add the following variables:

```
API_ID=39917988
API_HASH=bd827dbeac6a55896ff11539bc80365b
BOT_TOKEN=your_bot_token
STRING_SESSION=your_session_string
OWNER_ID=your_owner_id
LOGGER_ID=your_logger_chat_id
STORAGE_CHAT_ID=your_storage_chat_id
API_KEY=your_api_key
BASE_URL=https://api.babiesiq.tech
BOT_NAME=MyBot
DURATION_LIMIT=500
QUEUE_LIMIT=100
MONGO_DB_URI=your_mongo_uri (optional)
```

### Step 3: Deploy
- Railway automatically deploys when you push to the repository
- Monitor logs in the Railway dashboard

## Environment Variables

| Variable | Description | Example |
|----------|-------------|----------|
| API_ID | Telegram API ID | 39917988 |
| API_HASH | Telegram API Hash | bd827dbeac6a55896ff11539bc80365b |
| BOT_TOKEN | Telegram Bot Token | 8522799922:AAF3... |
| OWNER_ID | Bot Owner User ID | 7875184322 |
| LOGGER_ID | Logger Chat ID | -1003781924669 |
| STORAGE_CHAT_ID | Storage Channel ID | -1003577577725 |
| API_KEY | Admin API Key | your_key |
| BASE_URL | API Base URL | https://api.babiesiq.tech |

## Commands

- `/start` - Start the bot
- `/help` - Show help message
- `/ping` - Check bot status

## Project Structure

```
new-repo/
├── main.py              # Main bot application
├── config.py            # Configuration management
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker configuration
├── Procfile             # Process file for Railway
├── railway.json         # Railway configuration
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Troubleshooting

### Bot not responding
1. Check if BOT_TOKEN is correct
2. Verify OWNER_ID and other IDs are valid
3. Check logs in Railway dashboard

### Connection issues
1. Ensure API_ID and API_HASH are correct
2. Check if the bot token is still valid
3. Verify internet connection on Railway

### Environment variables not loaded
1. Verify `.env` file exists locally
2. Double-check Railway environment variables
3. Restart the deployment

## Support

For issues and questions, open an issue on GitHub.

## License

This project is open source and available under the MIT License.