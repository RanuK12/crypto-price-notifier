# Crypto Price Notifier

A simple Telegram bot that monitors cryptocurrency prices and sends alerts when thresholds are crossed.

## Features
- Monitor multiple cryptocurrencies
- Set price thresholds (above/below)
- Telegram notifications
- Configurable via environment variables
- Uses CoinGecko API (free, no API key required)

## Setup

1. Clone the repo
2. Copy `.env.example` to `.env` and fill in your values
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python main.py`

## Configuration

Create a `.env` file with:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
TELEGRAM_CHAT_ID=your_chat_id
CHECK_INTERVAL=300  # seconds (default 5 minutes)
COINS=bitcoin,ethereum,solana
THRESHOLDS=bitcoin:above:100000,ethereum:below:3000,solana:above:200
```

Threshold format: `coin:above|below:price` (comma-separated)

## Commands

- `/start` - Start the bot
- `/status` - Check current prices and thresholds
- `/help` - Show help
