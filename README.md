# Telegram Crypto Price Notifier Bot

A Telegram bot that monitors cryptocurrency prices via CoinGecko and sends alerts when thresholds are crossed.

## Features
- Monitor multiple cryptocurrencies (Bitcoin, Ethereum, Solana by default)
- Configurable price thresholds (above/below)
- Telegram alerts with formatting
- Status command to check current prices and threshold status
- Docker support for easy deployment

## Setup

### Option 1: Local Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and add your:
   - `TELEGRAM_BOT_TOKEN` (get from @BotFather)
   - `TELEGRAM_CHAT_ID` (get from @userinfobot)
   - Optional: `COINS`, `THRESHOLDS`, `CHECK_INTERVAL`

4. Run the bot:
   ```bash
   python main.py
   ```

### Option 2: Docker
1. Build the Docker image:
   ```bash
   docker build -t crypto-price-notifier .
   ```

2. Run the container (replace token and chat_id):
   ```bash
   docker run -d \
     --name crypto-notifier \
     -e TELEGRAM_BOT_TOKEN=your_bot_token_here \
     -e TELEGRAM_CHAT_ID=your_chat_id_here \
     crypto-price-notifier
   ```

   Or using a `.env` file:
   ```bash
   docker run -d \
     --name crypto-notifier \
     --env-file .env \
     crypto-price-notifier
   ```

## Configuration
Edit the `.env` file to adjust:

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token (required)
- `TELEGRAM_CHAT_ID`: Your Telegram chat ID (required)
- `CHECK_INTERVAL`: How often to check prices in seconds (default: 300)
- `COINS`: Comma-separated list of CoinGecko coin IDs (default: bitcoin,ethereum,solana)
- `THRESHOLDS`: Price thresholds in format `coin:above|below:price` (default: bitcoin:above:100000,ethereum:below:3000,solana:above:200)

## Usage
- Start the bot and send `/start` in your Telegram chat to begin
- Use `/status` to see current prices and threshold status
- Use `/help` for available commands

## Example .env
```
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_CHAT_ID=987654321
CHECK_INTERVAL=300
COINS=bitcoin,ethereum,solana
THRESHOLDS=bitcoin:above:100000,ethereum:below:3000,solana:above:200
```

## License
MIT