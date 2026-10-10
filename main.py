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
import yaml

import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import sys

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def load_config():
    try:
        with open("config.yaml") as f:
            cfg = yaml.safe_load(f)
        if cfg is None:
            cfg = {}
        token = cfg.get("telegram", {}).get("token")
        if not token:
            sys.stderr.write(
                "ERROR: Falta el token de Telegram en config.yaml.\n"
                "Obtén uno creando un bot con @BotFather y coloca el token en la sección 'telegram.token'.\n"
            )
            sys.exit(1)
        return cfg
    except FileNotFoundError:
        sys.stderr.write("ERROR: No se encontró config.yaml.\n")
        sys.exit(1)

# Load configuration from file
cfg = load_config()

# Configuration from config.yaml
TELEGRAM_BOT_TOKEN = cfg.get("telegram", {}).get("token")
TELEGRAM_CHAT_ID = cfg.get("telegram", {}).get("chat_id", "")
CHECK_INTERVAL = cfg.get("price", {}).get("check_interval", 300)
COIN_ID = cfg.get("price", {}).get("coin_id", "bitcoin")
THRESHOLD_USD = cfg.get("price", {}).get("threshold_usd", 30000)
DIRECTION = cfg.get("price", {}).get("direction", "above")

# Parse thresholds for compatibility with existing code
THRESHOLDS: Dict[str, List[Tuple[str, float]]] = {}
if COIN_ID:
    THRESHOLDS[COIN_ID] = [(DIRECTION, THRESHOLD_USD)]

# CoinGecko API
COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price"

# Track which alerts have been triggered to avoid spam
# Define COINS list before it's used


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


def load_config():
    try:
        with open("config.yaml") as f:
            cfg = yaml.safe_load(f)
        token = cfg.get("telegram", {}).get("token")
        if not token:
            sys.stderr.write(
                "ERROR: Falta el token de Telegram en config.yaml.\n"
                "Obtén uno creando un bot con @BotFather y coloca el token en la sección 'telegram.token'.\n"
            )
            sys.exit(1)
        return cfg
    except FileNotFoundError:
        sys.stderr.write("ERROR: No se encontró config.yaml.\n")
        sys.exit(1)

def main():
    """Main entry point."""
    try:
        cfg = load_config()
        TELEGRAM_BOT_TOKEN = cfg.get("telegram", {}).get("token")
        TELEGRAM_CHAT_ID = cfg.get("telegram", {}).get("chat_id", "")
        if not TELEGRAM_BOT_TOKEN:
            sys.stderr.write("ERROR: Token de Telegram vacío en la configuración.\n")
            sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"ERROR: Fallo al cargar la configuración: {e}\n")
        sys.exit(1)
    if not TELEGRAM_CHAT_ID:
        print("ERROR: Falta TELEGRAM_CHAT_ID. Para obtenerlo, abre Telegram, escribi a @userinfobot y copiá tu ID. Luego exporta TELEGRAM_CHAT_ID=...", file=sys.stderr)
        sys.exit(1)
    
    # Create application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("help", help_command))
    
    # Setup job queue
    application.job_queue.run_repeating(
        check_prices_job,
        interval=CHECK_INTERVAL,
        first=10
    )
    logger.info("Bot started. Press Ctrl+C to stop.")
    
    # Run the bot
    # 2️⃣ Ejecutar el bot
    try:
        asyncio.run(application.run_polling())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")


# Remove dry-run mode and ensure the bot runs with the correct token
if __name__ == '__main__':
    if TELEGRAM_BOT_TOKEN == 'TEST_TOKEN_12345':
        print("⚠️ WARNING: Using test token. To get a real token: open Telegram, search @BotFather, send /newbot, follow the steps to create a bot, copy the token and replace it in config.yaml or .env.")
    else:
        print("✅ Using real token.")
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
