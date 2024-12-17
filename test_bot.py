import os
import sqlite3
import pytest
from unittest.mock import AsyncMock, Mock, patch, call, ANY
from bot import (
    get_random_question,
    add_question_to_db,
    main,
    post_init,
    start,
    add_question,
    question,
    set_category,
    DB_PATH,
    CommandHandler,
)
from dotenv import load_dotenv

DB_TEST_PATH = "test_questions.db"


# Fixture to set up a clean test database
@pytest.fixture
def setup_db():
    if os.path.exists(DB_TEST_PATH):
        os.remove(DB_TEST_PATH)

    conn = sqlite3.connect(DB_TEST_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            category TEXT CHECK(category IN ('normal', 'blitz')) NOT NULL
        )
    """)
    cursor.executemany("INSERT INTO questions (text, category) VALUES (?, ?)", [
        ("Test question 1", "normal"),
        ("Test question 2", "blitz"),
        ("Test question 3", "normal")
    ])
    conn.commit()
    conn.close()

    yield

    if os.path.exists(DB_TEST_PATH):
        os.remove(DB_TEST_PATH)


# Ensure the bot uses the test database
@pytest.fixture(autouse=True)
def override_db_path():
    global DB_PATH
    DB_PATH = DB_TEST_PATH


# Test: Loading environment variables
def test_load_env_variables():
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    assert token is not None, "TELEGRAM_BOT_TOKEN is not set in the .env file"
    assert isinstance(token, str), "TELEGRAM_BOT_TOKEN should be a string"


# Test: Fetching a random question
def test_get_random_question(setup_db):
    result = get_random_question("normal", db_path=DB_TEST_PATH)
    assert result in ["Test question 1", "Test question 3"]

    result = get_random_question("blitz", db_path=DB_TEST_PATH)
    assert result == "Test question 2"


# Test: Adding a new question
def test_add_question_to_db(setup_db):
    add_question_to_db("New test question", "normal", db_path=DB_TEST_PATH)

    conn = sqlite3.connect(DB_TEST_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT text FROM questions WHERE text = ?", ("New test question",))
    result = cursor.fetchone()
    conn.close()

    assert result is not None, "Question was not added to the database"
    assert result[0] == "New test question"


# Test: Main function initializes bot handlers
@pytest.mark.asyncio
@patch("bot.ApplicationBuilder")
async def test_main_function(mock_app_builder):
    # Mock the Application instance
    mock_app = AsyncMock()
    mock_app.add_handler = AsyncMock()
    mock_app.run_polling = AsyncMock()
    mock_app.stop = AsyncMock()

    # Mock ApplicationBuilder to return the mock_app
    mock_app_builder.return_value.token.return_value.post_init.return_value.build.return_value = mock_app

    # Run the main function
    await main()

    # Verify that ApplicationBuilder was called
    mock_app_builder.assert_called_once()

    # Verify that add_handler is called 4 times (for start, question, category, add_question)
    assert mock_app.add_handler.call_count == 4

    # Verify run_polling was awaited
    mock_app.run_polling.assert_awaited_once()

    # Verify stop was awaited
    mock_app.stop.assert_awaited_once()
