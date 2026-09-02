FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (ffmpeg is required by py-tgcalls for audio/video streaming)
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user and a storage dir it can actually write to
RUN useradd -m -u 1000 botuser \
    && mkdir -p /app/vps_songs \
    && chown -R botuser:botuser /app
USER botuser

ENV STORAGE_DIR=/app/vps_songs

# Run the bot
RUN chmod +x entrypoint.sh
CMD ["./entrypoint.sh"]