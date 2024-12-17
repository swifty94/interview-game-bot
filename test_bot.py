import unittest
from unittest.mock import AsyncMock, MagicMock, patch
import sqlite3
import asyncio
from telegram import Update, User, Message
from telegram.ext import ContextTypes
from bot import get_random_questions, add_question_to_db, start, question, set_category, add_question
import logging 

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

TEST_DB_PATH = "questions.db"

# ================= Test Setup ================= #
def setup_test_db():
    """Set up a temporary test database."""
    with sqlite3.connect(TEST_DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS questions;")
        cursor.execute("""
            CREATE TABLE questions (
                id INTEGER PRIMARY KEY,
                text TEXT NOT NULL,
                category TEXT NOT NULL
            );
        """)
        for i in range(1, 50):
            cursor.execute(
                "INSERT INTO questions (text, category) VALUES (?, ?);",
                (f"Test question {i}", "normal" if i % 2 else "blitz")
            )
        conn.commit()

# ================= Unit Tests ================= #
class TestInterviewBot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setup_test_db()

    # --- Test get_random_questions --- #
    def test_get_random_questions(self):
        questions = get_random_questions("normal", count=10, db_path=TEST_DB_PATH)
        self.assertEqual(len(questions), 10)
        self.assertEqual(len(set(questions)), 10)  # Ensure all questions are unique

    # --- Test add_question_to_db --- #
    def test_add_question_to_db(self):
        add_question_to_db("New Test Question", "normal", TEST_DB_PATH)
        with sqlite3.connect(TEST_DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT text FROM questions WHERE text = ?", ("New Test Question",))
            result = cursor.fetchone()
        self.assertIsNotNone(result)

    # --- Async Tests for Commands --- #
    @patch("bot.get_random_questions", return_value=[f"Test question {i}" for i in range(1, 11)])
    def test_question_command(self, mock_get_random_questions):
        update = MagicMock(spec=Update)
        update.effective_user = User(
            id=1,
            first_name='John',
            is_bot=False,
            last_name='Snow',
            username='johnsnowisnotdead',
            language_code='en',
            can_join_groups=True,
            can_read_all_group_messages=True,
            supports_inline_queries=False,
            is_premium=False,
            added_to_attachment_menu=False,
            can_connect_to_business=False,
            has_main_web_app=False,
            api_kwargs=None
            )
        update.message = AsyncMock(spec=Message)
        context = MagicMock()
        context.user_data = {"category": "normal"}

        asyncio.run(question(update, context))

        expected_response = f"✨Категорія: normal\n\n📝 Питання:\n\n" + "\n\n".join(
            [f"✨ Test question {i}" for i in range(1, 11)]
        )
        update.message.reply_text.assert_called_once_with(expected_response)
        mock_get_random_questions.assert_called_once_with("normal")

    def test_set_category_valid(self):
        update = MagicMock(spec=Update)
        update.effective_user = User(
            id=1,
            first_name='John',
            is_bot=False,
            last_name='Snow',
            username='johnsnowisnotdead',
            language_code='en',
            can_join_groups=True,
            can_read_all_group_messages=True,
            supports_inline_queries=False,
            is_premium=False,
            added_to_attachment_menu=False,
            can_connect_to_business=False,
            has_main_web_app=False,
            api_kwargs=None
            )
        update.message = AsyncMock(spec=Message)
        context = MagicMock()
        context.args = ["blitz"]
        context.user_data = {}

        asyncio.run(set_category(update, context))
        self.assertEqual(context.user_data["category"], "blitz")
        update.message.reply_text.assert_called_once_with("✅ Category set to: **blitz** 🎯")

    def test_set_category_invalid(self):
        update = MagicMock(spec=Update)
        update.effective_user = User(
            id=1,
            first_name='John',
            is_bot=False,
            last_name='Snow',
            username='johnsnowisnotdead',
            language_code='en',
            can_join_groups=True,
            can_read_all_group_messages=True,
            supports_inline_queries=False,
            is_premium=False,
            added_to_attachment_menu=False,
            can_connect_to_business=False,
            has_main_web_app=False,
            api_kwargs=None
            )
        update.message = AsyncMock(spec=Message)
        context = MagicMock()
        context.args = ["invalid"]

        asyncio.run(set_category(update, context))
        update.message.reply_text.assert_called_once_with("❌ Usage: /category <normal|blitz>")

# ================= Main ================= #
if __name__ == "__main__":
    unittest.main()
