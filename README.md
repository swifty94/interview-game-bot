Here's a polished **README.md** in English for your project:

---

# 🎙️ **Interview Game Bot**

**Interview Game Bot** is a Telegram bot designed for an engaging game of interviews. One user acts as the interviewer, while another plays the guest. The bot provides random questions, supports categories, and allows users to add their own questions.

---

## 📋 **Features**

- ✨ **/start**: Displays a welcome message with instructions for using the bot.
- ✨ **/question**: Generates a random question from the selected category.
- ✨ **/category <normal|blitz>**: Switches between question categories.
- ✨ **/add_question <your_question>**: Allows users to add custom questions to the current category.

---

## 🛠️ **Setup and Installation**

### **1. Clone the repository**
```bash
git clone <YOUR_REPOSITORY_URL>
cd interview_game_bot
```

### **2. Set up a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```

### **3. Install dependencies**
```bash
pip install -r requirements.txt
```

### **4. Create the `.env` file**
Create a file named `.env` in the root directory and add your Telegram bot token:
```env
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

### **5. Run the bot**
```bash
python fixed_bot.py
```

---

## 🧪 **Testing**

The project includes both **unit tests** and **functional tests**. Run them as follows:

### **1. Install testing dependencies**
```bash
pip install pytest pytest-asyncio
```

### **2. Run tests**
Run unit tests:
```bash
python -m unittest test_bot.py
```

Run functional tests:
```bash
pytest test_functional.py
```

---

## 📂 **Project Structure**

```plaintext
interview_game_bot/
│
├── bot.py               # Main bot code
├── fixed_bot.py         # Enhanced and bug-fixed bot
├── test_bot.py          # Unit tests
├── test_functional.py   # Functional tests
├── requirements.txt     # Project dependencies
├── .env                 # Environment variables file
├── README.md            # Project documentation
└── test_questions.db    # Test database
```

---

## 📝 **How to Add Questions**

1. Use the `/add_question <your_question>` command while the bot is running.
2. The question will be added to the currently selected category.

---

## 🎯 **Project Goal**

The bot is designed to:
- Facilitate mock interviews.
- Improve communication and interviewing skills.
- Serve as a fun team-building activity.

---

## 🤝 **Contributing**

To contribute to this project:
1. Fork the repository.
2. Create a new branch for your changes.
3. Submit a Pull Request describing the enhancements.

---

## 🛡️ **License**

This project is licensed under the **MIT License**.

---

If you have any questions or suggestions, feel free to reach out! 🚀