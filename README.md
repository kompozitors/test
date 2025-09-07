# Telegram Feedback Bot

This repository contains a simple support bot for Telegram written in Python.

## Features
- Forward user messages to a private admin chat.
- Admin replies in the chat are relayed back to the user with an individual signature.
- Users can leave reviews using the `/review` command; reviews are stored in `reviews.txt` and sent to the admin chat.

## Setup
1. Install [python-telegram-bot](https://python-telegram-bot.org/):
   ```bash
   pip install python-telegram-bot
   ```
2. Set environment variables:
   - `BOT_TOKEN` – token issued by [@BotFather](https://t.me/BotFather).
   - `ADMIN_CHAT_ID` – ID of the chat where admins receive messages.
3. Optionally register admin signatures by calling `register_admin(user_id, "Signature")` in the code.

## Usage
Run the bot:
```bash
python feedback_bot.py
```

The bot can be added to an admin group so that replies from administrators are forwarded back to users with their signatures.
