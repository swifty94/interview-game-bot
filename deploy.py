
import asyncio
import os
import logging
from dotenv import load_dotenv
import subprocess

# ======================= Logging Configuration ========================= #
LOG_FORMAT = (
    "%(asctime)s %(levelname)-5s [%(name)s] (%(threadName)s) %(message)s"
)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Set up the custom logger
logger = logging.getLogger(__name__)
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
def run_bot():
    from bot import main as start
    start()
# ======================= Tests ========================= #
def run_unit_tests():
    logger.info("Running Unit tests...")
    try:
        subprocess.run(["python", "-m", "unittest", "test_bot.py", "-v"], check=True)
    except subprocess.CalledProcessError as e:
        logger.error("Tests failed")
        exit(1)

def run_functional_tests():
    logger.info("Running Functional tests...")
    try:
        subprocess.run(["pytest", "test_functional.py", "-v"], check=True)
    except subprocess.CalledProcessError as e:
        logger.error("Tests failed")
        exit(1)

# ======================= Orchestrator ========================= #
if __name__ == "__main__":
    try:
        print("---------> Unit tests:")
        run_unit_tests()
        print("---------> Functional tests:")
        run_functional_tests()
        print("---------> Tests finished!\n\nStarting the bot")
        asyncio.run(run_bot())
    except Exception as e:
        print("Deploy failed")
