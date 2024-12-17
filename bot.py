import os
import sqlite3
import logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update

# ======================= Logging Configuration ========================= #
LOG_FORMAT = "%(asctime)s %(levelname)-5s [%(name)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Основной логгер
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

DB_PATH = "interview_questions.db"

# ======================= Helper Functions ========================= #
def get_random_question(category="normal"):
    logger.debug(f"Fetching question for category '{category}'")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT text FROM questions WHERE category = ? ORDER BY RANDOM() LIMIT 1", 
            (category,)
        )
        result = cursor.fetchone()
    return result[0] if result else "😕 No questions available in this category."

def add_question_to_db(text, category="normal"):
    logger.info(f"Adding question '{text}' to category '{category}'")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO questions (text, category) VALUES (?, ?)", (text, category))
        conn.commit()

# ======================= Command Handlers ========================= #
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"User '{update.effective_user.username}' triggered /start")
    await update.message.reply_text(
        "🎙️ Welcome to the **Interview Game Bot**! 🎉\n\n"
        "✨ Use /question to get a random question.\n"
        "✨ Use /category <normal|blitz> to change question category.\n"
        "✨ Use /add_question <your_question> to add a custom question. ✅"
    )

async def question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    category = context.user_data.get("category", "normal")
    question_text = get_random_question(category)
    logger.info(f"User '{update.effective_user.username}' requested question in category '{category}'")
    await update.message.reply_text(f"✨Категорія: {category}\n\n✨📝Питання: {question_text}")

async def set_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1 or context.args[0] not in ["normal", "blitz"]:
        await update.message.reply_text("❌ Usage: /category <normal|blitz>")
        return
    category = context.args[0]
    context.user_data["category"] = category
    logger.info(f"User '{update.effective_user.username}' set category to '{category}'")
    await update.message.reply_text(f"✅ Category set to: **{category}** 🎯")

async def add_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: /add_question <your_question>")
        return
    question_text = " ".join(context.args)
    category = context.user_data.get("category", "normal")
    add_question_to_db(question_text, category)
    logger.info(f"User '{update.effective_user.username}' added question '{question_text}' to category '{category}'")
    await update.message.reply_text("✅ Your question has been added! 🥳")

# ======================= Main Function ========================= #
def main():
    logger.info("🎉 Starting InterviewBot... 🚀")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("question", question))
    app.add_handler(CommandHandler("category", set_category))
    app.add_handler(CommandHandler("add_question", add_question))

    logger.info("✅ Bot is successfully started. Now running polling...")
    app.run_polling()

if __name__ == "__main__":
    main()