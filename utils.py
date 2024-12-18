# ======================= UTILITIES ========================= #
# ======================= Logging Configuration ========================= #
import logging, sqlite3, os, random
from dotenv import load_dotenv

LOG_FORMAT = "[%(asctime)s] [%(levelname)-5s] [%(name)s] [%(funcName)s] [%(message)s] [line:%(lineno)d]"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

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

DB_PATH = "interview_questions.db"

# ======================= Helper Functions ========================= #
def get_random_questions(category="normal", count=10, db_path=DB_PATH):
    """Fetch 10 unique random questions from the database."""
    query = "SELECT text FROM questions WHERE category = ? ORDER BY RANDOM() LIMIT ?"
    logger.debug(f"Executing SQL: {query} | Params: category={category}, count={count}")
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (category, count))
        results = cursor.fetchall()
    logger.info(f"Fetched {len(results)} questions from category '{category}'")
    return [result[0] for result in results] if results else ["😕 Питання для цієї категорії відсутні."]

def add_question_to_db(text, category="normal", db_path=DB_PATH):
    """Add a question to the database."""
    query = "INSERT INTO questions (text, category) VALUES (?, ?)"
    logger.debug(f"Executing SQL: {query} | Params: text='{text}', category='{category}'")
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (text, category))
        conn.commit()
    logger.info(f"Added question '{text}' to category '{category}'")