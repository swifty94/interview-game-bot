import pytest
from unittest.mock import AsyncMock, MagicMock
from bot import start, question, set_category, add_question
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
# ======================== Fixtures ======================== #
@pytest.fixture
def mock_update():
    """Mock Telegram Update object."""
    update = MagicMock()
    update.effective_user.username = "test_user"
    update.message.reply_text = AsyncMock()
    return update

@pytest.fixture
def mock_context():
    """Mock Telegram Context object."""
    context = MagicMock()
    context.user_data = {}
    context.args = []
    return context

# ======================== Test /start Command ======================== #
@pytest.mark.asyncio
async def test_start_command(mock_update, mock_context):
    expected_output = (
        "🎙️ Welcome to the **Interview Game Bot**! 🎉\n\n"
        "✨ Use /question to get a random question.\n"
        "✨ Use /category <normal|blitz> to change question category.\n"
        "✨ Use /add_question <your_question> to add a custom question. ✅"
    )
    await start(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once_with(expected_output)

# ======================== Test /question Command ======================== #
@pytest.mark.asyncio
async def test_question_command(mock_update, mock_context):
    mock_context.user_data["category"] = "normal"
    question_text = "Якби ви могли змінити один момент в історії України, що б це було?"  # Replace with an example

    # Mock the get_random_question function
    from bot import get_random_question
    get_random_question_mock = MagicMock(return_value=question_text)

    with pytest.MonkeyPatch().context() as monkeypatch:
        monkeypatch.setattr("bot.get_random_question", get_random_question_mock)
        await question(mock_update, mock_context)

    mock_update.message.reply_text.assert_called_once_with(f"✨Категорія: normal\n\n✨📝Питання: {question_text}")
    get_random_question_mock.assert_called_once_with("normal")

# ======================== Test /category Command ======================== #
@pytest.mark.asyncio
async def test_set_category_command_valid(mock_update, mock_context):
    mock_context.args = ["blitz"]
    expected_output = "✅ Category set to: **blitz** 🎯"
    
    await set_category(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once_with(expected_output)
    assert mock_context.user_data["category"] == "blitz"

@pytest.mark.asyncio
async def test_set_category_command_invalid(mock_update, mock_context):
    mock_context.args = ["invalid"]
    expected_output = "❌ Usage: /category <normal|blitz>"
    
    await set_category(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once_with(expected_output)
    assert "category" not in mock_context.user_data

# ======================== Test /add_question Command ======================== #
@pytest.mark.asyncio
async def test_add_question_command_valid(mock_update, mock_context):
    mock_context.args = ["путін", "-", "хуйло?"]  # Replace with an example
    expected_output = "✅ Your question has been added! 🥳"
    
    # Mock the add_question_to_db function
    from bot import add_question_to_db
    add_question_mock = MagicMock()
    
    with pytest.MonkeyPatch().context() as monkeypatch:
        monkeypatch.setattr("bot.add_question_to_db", add_question_mock)
        await add_question(mock_update, mock_context)
    
    mock_update.message.reply_text.assert_called_once_with(expected_output)
    add_question_mock.assert_called_once_with("путін - хуйло?", "normal")

@pytest.mark.asyncio
async def test_add_question_command_invalid(mock_update, mock_context):
    mock_context.args = []
    expected_output = "❌ Usage: /add_question <your_question>"
    
    await add_question(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once_with(expected_output)

# ======================== Custom Test Summary ======================== #
@pytest.fixture
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Add a custom summary at the end of pytest output."""
    total = terminalreporter._numcollected
    passed = len([report for report in terminalreporter.stats.get("passed", [])])
    failed = len([report for report in terminalreporter.stats.get("failed", [])])
    skipped = len([report for report in terminalreporter.stats.get("skipped", [])])

    print("\n================ Custom Test Summary ================")
    print(f"Total Tests:    {total}")
    print(f"✅ Passed:      {passed}")
    print(f"❌ Failed:      {failed}")
    print(f"⚠️  Skipped:     {skipped}")
    print("=====================================================")
