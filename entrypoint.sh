#!/bin/bash

# Sync system time before running the bot
echo "⏰ Syncing system time..."
ntpdate -s time.nist.gov 2>/dev/null || ntpdate -s time.google.com 2>/dev/null || true

# Check current time
date

echo "🤖 Starting bot..."
python main.py
