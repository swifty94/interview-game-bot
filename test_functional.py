import os
import pytest
import asyncio
from unittest.mock import AsyncMock
from bot import start, question, set_category
from telegram import Update, Message, User, Chat
from telegram.ext import ContextTypes

# Mock Update and Context objects for testing
@pytest.fixture
def mock_update():
    user = User(id=12345, is_bot=False, first_name="TestUser")
    chat = Chat(id=12345, type="private")
    message = Message(message_id=1, date=None, chat=chat, text="", from_user=user)
    update = Update(update_id=1, message=message)
    return update

@pytest.fixture
def mock_context():
    return AsyncMock(ContextTypes.DEFAULT_TYPE)

# Test the /start command
@pytest.mark.asyncio
async def test_start_command(mock_update, mock_context):
    mock_update.message.text = "/start"
    await start(mock_update, mock_context)
    mock_context.bot.send_message.assert_called_once_with(
        chat_id=mock_update.message.chat_id,
        text="Welcome to Interview Game Bot! 🎙️\n"
             "Use /question to get a random question.\n"
             "Use /category <normal|blitz> to change question category.\n"
             "Use /add_question <your_question> to add a custom question."
    )

# Test the /question command
@pytest.mark.asyncio
async def test_question_command(mock_update, mock_context):
    mock_update.message.text = "/question"
    await question(mock_update, mock_context)
    mock_context.bot.send_message.assert_called()

# Test the /category command
@pytest.mark.asyncio
async def test_category_command(mock_update, mock_context):
    mock_update.message.text = "/category blitz"
    mock_context.args = ["blitz"]
    await set_category(mock_update, mock_context)
    mock_context.bot.send_message.assert_called_once_with(
        chat_id=mock_update.message.chat_id,
        text="Category set to: blitz"
    )
