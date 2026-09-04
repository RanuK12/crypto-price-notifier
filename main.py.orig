#!/usr/bin/env python3
"""
Crypto Price Notifier - Telegram Bot
Monitors cryptocurrency prices and sends alerts when thresholds are crossed.
"""

import os
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Tuple

import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration from environment
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '300'))
COINS = os.getenv('COINS', 'bitcoin,ethereum,solana').split(',')
THRESHOLDS_STR = os.getenv('THRESHOLDS', 'bitcoin:above:100000,ethereum:below:3000,solana:above:200')

# Parse thresholds: coin:above|below:price
THRESHOLDS: Dict[str, List[Tuple[str, float]]] = {}
for threshold in THRESHOLDS_STR.split(','):
    if ':' in threshold:
        parts = threshold.split(':')
        if len(parts) == 3:
            coin, direction, price = parts
            if coin not in THRESHOLDS:
                THRESHOLDS[coin] = []
            THRESHOLDS[coin].append((direction, float(price)))

# CoinGecko API
COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price"

# Track which alerts have been triggered to avoid spam
triggered_alerts: Dict[str, set] = {coin: set() for coin in COINS}


async def fetch_prices(coins: List[str]) -> Dict[str, float]:
    """Fetch current prices from CoinGecko API."""
    try:
        params = {
            'ids': ','.join(coins),
            'vs_currencies': 'usd'
        }
        response = requests.get(COINGECKO_API, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {coin: data[coin]['usd'] for coin in coins if coin in data}
    except Exception as e:
        logger.error(f"Error fetching prices: {e}")
        return {}


def check_thresholds(prices: Dict[str, float]) -> List[str]:
    """Check if any thresholds have been crossed."""
    alerts = []
    for coin, price in prices.items():
        if coin in THRESHOLDS:
            for direction, threshold in THRESHOLDS[coin]:
                alert_key = f"{coin}:{direction}:{threshold}"
                
                if direction == 'above' and price >= threshold:
                    if alert_key not in triggered_alerts[coin]:
                        alerts.append(f"🚀 {coin.capitalize()} reached ${price:,.2f} (above ${threshold:,.2f})")
                        triggered_alerts[coin].add(alert_key)
                elif direction == 'below' and price <= threshold:
                    if alert_key not in triggered_alerts[coin]:
                        alerts.append(f"📉 {coin.capitalize()} dropped to ${price:,.2f} (below ${threshold:,.2f})")
                        triggered_alerts[coin].add(alert_key)
                
                # Reset alert if price moves back across threshold
                if direction == 'above' and price < threshold:
                    triggered_alerts[coin].discard(alert_key)
                elif direction == 'below' and price > threshold:
                    triggered_alerts[coin].discard(alert_key)
    
    return alerts


async def check_prices_job(context: ContextTypes.DEFAULT_TYPE):
    """Scheduled job to check prices and send alerts."""
    prices = await fetch_prices(COINS)
    if not prices:
        return
    
    alerts = check_thresholds(prices)
    
    if alerts:
        message = "🔔 *Price Alerts*\n\n" + "\n".join(alerts)
        message += f"\n\n🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        try:
            await context.bot.send_message(
                chat_id=TELEGRAM_CHAT_ID,
                text=message,
                parse_mode='Markdown'
            )
            logger.info(f"Sent {len(alerts)} alert(s)")
        except Exception as e:
            logger.error(f"Error sending alert: {e}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler."""
    if str(update.effective_chat.id) != TELEGRAM_CHAT_ID:
        await update.message.reply_text("❌ Unauthorized chat.")
        return
    
    await update.message.reply_text(
        "🤖 *Crypto Price Notifier started!*\n\n"
        f"Monitoring: {', '.join(c.capitalize() for c in COINS)}\n"
        f"Check interval: {CHECK_INTERVAL}s\n\n"
        "Commands:\n"
        "/status - Current prices and thresholds\n"
        "/help - Show this help",
        parse_mode='Markdown'
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Status command handler."""
    if str(update.effective_chat.id) != TELEGRAM_CHAT_ID:
        await update.message.reply_text("❌ Unauthorized chat.")
        return
    
    prices = await fetch_prices(COINS)
    
    if not prices:
        await update.message.reply_text("❌ Could not fetch prices.")
        return
    
    message = "📊 *Current Prices & Thresholds*\n\n"
    
    for coin in COINS:
        price = prices.get(coin, 0)
        message += f"*{coin.capitalize()}*: ${price:,.2f}\n"
        
        if coin in THRESHOLDS:
            for direction, threshold in THRESHOLDS[coin]:
                emoji = "🔺" if direction == "above" else "🔻"
                alert_key = f"{coin}:{direction}:{threshold}"
                status = "✅ TRIGGERED" if alert_key in triggered_alerts[coin] else "⏳ Waiting"
                message += f"  {emoji} {direction.capitalize()} ${threshold:,.2f} - {status}\n"
        message += "\n"
    
    message += f"🕐 Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    await update.message.reply_text(message, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command handler."""
    if str(update.effective_chat.id) != TELEGRAM_CHAT_ID:
        await update.message.reply_text("❌ Unauthorized chat.")
        return
    
    help_text = (
        "🤖 *Crypto Price Notifier Help*\n\n"
        "Commands:\n"
        "/start - Start the bot\n"
        "/status - Show current prices and threshold status\n"
        "/help - Show this help\n\n"
        "Configuration (via .env):\n"
        f"- Coins: {', '.join(COINS)}\n"
        f"- Check interval: {CHECK_INTERVAL}s\n"
        f"- Thresholds: {THRESHOLDS_STR}\n\n"
        "Threshold format: `coin:above|below:price`\n"
        "Example: `bitcoin:above:100000,ethereum:below:3000`"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')


def main():
    """Main entry point."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.error("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set in .env")
        return
    
    # Create application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("help", help_command))
    
    # Setup scheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        check_prices_job,
        'interval',
        seconds=CHECK_INTERVAL,
        args=[application],
        id='price_check'
    )
    logger.info("Bot started. Press Ctrl+C to stop.")
    
    # Run the bot
    application.run_polling()


if __name__ == '__main__':
    main()
