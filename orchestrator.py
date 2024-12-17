
import asyncio
import os
import sqlite3
import logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import subprocess
import unittest

# ======================= Logging Configuration ========================= #
LOG_FORMAT = (
    "%(asctime)s %(levelname)-5s [%(name)s] (%(threadName)s) %(message)s"
)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Set up the custom logger
logger = logging.getLogger("InterviewBot")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# ======================= Load Environment Variables ========================= #
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set in the environment variables.")

# ======================= Bot Startup ========================= #
async def start_command(update, context):
    await update.message.reply_text("Welcome to the Interview Bot!")

def run_bot():
    from telegram.ext import ApplicationBuilder, CommandHandler
    
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))

    logger.info("Starting the bot...")
    app.run_polling()

# ======================= Tests ========================= #
def run_tests():
    logger.info("Running tests...")
    try:
        subprocess.run(["python", "-m", "unittest", "discover"], check=True)
    except subprocess.CalledProcessError as e:
        logger.error("Tests failed")
        exit(1)

# ======================= Orchestrator ========================= #
if __name__ == "__main__":
    run_tests()
    asyncio.run(run_bot())
