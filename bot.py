import random
from utils import *
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

LOG_FORMAT = "[%(asctime)s] [%(levelname)-5s] [%(name)s] [%(funcName)s] [%(message)s] [line:%(lineno)d]"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# ======================= Bot Logic ========================= #

async def roll_dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Roll dice to determine roles."""
    await update.message.reply_text("🎲 Введіть імена двох гравців через кому (наприклад: Андрій, Олена).")
    context.user_data["awaiting_players"] = True

async def process_names(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_players"):
        names = update.message.text.split(",")
        if len(names) != 2:
            await update.message.reply_text("❌ Введіть рівно два імені через кому.")
            return
        player1, player2 = names[0].strip(), names[1].strip()
        roll1, roll2 = random.randint(1, 6), random.randint(1, 6)
        logger.info(f"Rolled dice: {player1}={roll1}, {player2}={roll2}")
        if roll1 > roll2:
            roles = f"🎉 **{player1}** - Інтерв'юер!\n🎤 **{player2}** - Гість!"
        elif roll2 > roll1:
            roles = f"🎉 **{player2}** - Інтерв'юер!\n🎤 **{player1}** - Гість!"
        else:
            roles = "🤝 Нічия! Кидайте кубики ще раз."
        await update.message.reply_text(f"🎲 Результати кидка:\n🎲 {player1}: {roll1}\n🎲 {player2}: {roll2}\n\n{roles}")
        context.user_data["awaiting_players"] = False
        await send_main_menu(update)
async def send_main_menu(update: Update):
    """Send main menu buttons."""
    keyboard = [
        ["Отримати питання", "Додати питання"],
        ["Бліц", "Нормал"],
        ["Кинути кубики"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text("🎙️ Оберіть дію:", reply_markup=reply_markup)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"User '{update.effective_user.username}' triggered /start")
    await update.message.reply_text(
        "🎙️ Ласкаво просимо до **Інтерв'ю Бота**! 🎉",
    )
    await send_main_menu(update)

async def question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    category = context.user_data.get("category", "normal")
    questions = get_random_questions(category)
    logger.info(f"User '{update.effective_user.username}' requested questions in category '{category}'")
    questions_text = "\n\n".join([f"✨ {q}" for q in questions])
    await update.message.reply_text(
        f"✨Категорія: {category}\n\n📝 **Ваші питання:**\n\n{questions_text}"
    )
    await send_main_menu(update)

async def set_category_blitz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["category"] = "blitz"
    await update.message.reply_text("✅ Категорію змінено на: **Бліц** 🎯")
    await send_main_menu(update)

async def set_category_normal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["category"] = "normal"
    await update.message.reply_text("✅ Категорію змінено на: **Нормал** 🎯")
    await send_main_menu(update)

async def add_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Використання: /add_question <текст_питання>")
        return
    question_text = " ".join(context.args)
    category = context.user_data.get("category", "normal")
    add_question_to_db(question_text, category)
    logger.info(f"User '{update.effective_user.username}' added question '{question_text}' to category '{category}'")
    await update.message.reply_text("✅ Ваше питання було додано! 🥳")
    await send_main_menu(update)

# ======================= Main Function ========================= #
def main():
    logger.info("++++++++++++++++" + "Starting InterviewBot" + "++++++++++++++++")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add_question", add_question))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("Отримати питання"), question))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("Бліц"), set_category_blitz))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("Нормал"), set_category_normal))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("Кинути кубики"), roll_dice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_names))

    logger.info("++++++++++++++++" + "InterviewBot is now UP and Polling!" + "++++++++++++++++")
    app.run_polling()