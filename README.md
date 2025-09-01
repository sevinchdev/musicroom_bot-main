# 🎵 Music Room Bot

A simple and efficient **Telegram bot** for managing music room reservations at your university. It helps students easily book practice rooms while keeping track of their information in a local database.

---

## 🚀 Features

* Register students with **name, ID, phone number, and group**.
* Save student details so they don’t have to re-enter them each time.
* Reserve available music rooms quickly via Telegram.
* Store booking information in a **SQLite database**.
* Environment-based configuration with `.env`.

---

## 📂 Project Structure

```
musicroom_bot-main/
├── app.py            # Main entry point for the bot
├── db.py             # Database handling logic
├── loader.py         # Bot initialization and setup
├── requirements.txt  # Project dependencies
├── Pipfile           # Alternative dependency manager (Pipenv)
├── .env              # Environment variables (not committed)
├── bot.db            # SQLite database file
├── database.db       # Backup/alternate database
└── .gitignore        # Git ignored files
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/musicroom_bot.git
cd musicroom_bot-main
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Linux / macOS
venv\Scripts\activate      # On Windows
```

### 3. Install dependencies

Using **pip**:

```bash
pip install -r requirements.txt
```

Or using **Pipenv**:

```bash
pipenv install
```

### 4. Configure environment variables

Create a `.env` file in the project root with:

```env
BOT_TOKEN=your_telegram_bot_token
DB_PATH=bot.db
```

### 5. Run the bot

```bash
python app.py
```

---

## 💬 Bot Commands (Examples)

Here are the main commands supported by the bot:

* `/start` → Start the bot and register your information (only required the first time).
* `/book` → Reserve a music room.
* `/mybookings` → View your current reservations.
* `/cancel` → Cancel an existing booking.
* `/help` → Show available commands.

---

## 🗄 Database

* The bot uses **SQLite** (`bot.db`) to store user and booking information.
* `db.py` contains helper functions to interact with the database.

---

## 🤝 Contribution

1. Fork the repo
2. Create a new branch (`feature/my-feature`)
3. Commit your changes
4. Push to your branch
5. Open a Pull Request 🎉

---

## 💡 Future Improvements

* Admin panel for managing reservations
* Room availability calendar view
* Notifications/reminders before booked sessions
* Multi-language support
