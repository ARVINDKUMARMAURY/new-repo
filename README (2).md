# Simple Music Bot (xBit API + Permanent NVMe Storage)

## Features
- `/play` `/vplay` — gaana/video bajao
- `/pause` `/resume` `/skip` `/stop` `/end`
- `/queue` `/shuffle`
- `/authuser` — reply karke kisi ko permission do/hatao
- `/broadcast` — sirf owner, sab users/chats ko message
- Log group — bot start + har song play ka message
- xBit API only (yt-dlp nahi), permanent NVMe caching

## VPS Setup

### 1. System packages
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv ffmpeg git
```

### 2. Project setup
```bash
cd ~
mkdir musicbot && cd musicbot
# yahan saari files (config.py, database.py, queue.py, youtube.py, main.py, requirements.txt) daalo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Environment variables set karo
`.env` file banao ya seedha export karo:
```bash
export API_ID="12345"
export API_HASH="your_api_hash"
export BOT_TOKEN="your_bot_token"
export SESSION_STRING="your_assistant_session_string"
export OWNER_ID="your_telegram_user_id"
export MONGO_URL="your_mongodb_connection_string"
export LOG_GROUP_ID="-100xxxxxxxxxx"
export XBIT_API_KEY="your_xbit_api_key"
export XBIT_API_URL="https://tgapi.xbitcode.com"
export STORAGE_DIR="/root/vps_songs"
export DURATION_LIMIT="1200"
export QUEUE_LIMIT="20"
```

### 4. NVMe storage folder banao
```bash
mkdir -p /root/vps_songs
```

### 5. Run karo (tmux se, taaki band na ho)
```bash
tmux new -s musicbot
source venv/bin/activate
python3 main.py
```
Detach karne ke liye: `Ctrl+B` phir `D`

### 6. Auto-restart (PM2 se, recommended)
```bash
npm install -g pm2
pm2 start "venv/bin/python3 main.py" --name musicbot
pm2 save
pm2 startup
```

## Zaroori cheezein
- **API_ID / API_HASH** — https://my.telegram.org se
- **BOT_TOKEN** — @BotFather se naya bot bana ke
- **SESSION_STRING** — assistant/userbot account ka pyrogram session string
- **LOG_GROUP_ID** — ek group banao, bot + assistant dono ko admin banake add karo, uski chat ID
- **MONGO_URL** — MongoDB Atlas free cluster connection string
- **XBIT_API_KEY / XBIT_API_URL** — tumhare paas already hai

## Note
- Sirf xBit API se hi gaane fetch honge (yt-dlp bilkul use nahi hota)
- Pehli baar gaana bajne par thoda time lagega (API + download), uske baad wahi gaana `STORAGE_DIR` se instant milega
- `DURATION_LIMIT` se lambi videos automatically reject ho jayengi (storage bachane ke liye)
