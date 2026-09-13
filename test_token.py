import os
import sys
from telegram.ext import Application

# Simulate missing token
os.environ.pop('TELEGRAM_BOT_TOKEN', None)
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TELEGRAM_BOT_TOKEN:
    print("Token is missing")
    # Now try to build application
    try:
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    except Exception as e:
        print(f"Exception caught: {e}")
