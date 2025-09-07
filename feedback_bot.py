import logging
import os
from typing import Dict

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))
# Mapping of admin user IDs to their signatures
ADMIN_SIGNATURES: Dict[int, str] = {}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def register_admin(user_id: int, signature: str) -> None:
    """Register or update an admin signature."""
    ADMIN_SIGNATURES[user_id] = signature


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Добро пожаловать! Отправьте сообщение, чтобы связаться с поддержкой.\n"
        "Используйте /review <текст>, чтобы оставить отзыв."
    )


async def forward_to_admins(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Forward user messages to the admin chat."""
    if update.effective_chat.type != "private":
        return
    await update.message.forward(chat_id=ADMIN_CHAT_ID)


async def relay_from_admins(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Relay admin replies back to the original user with signatures."""
    if update.effective_chat.id != ADMIN_CHAT_ID:
        return
    if not update.message.reply_to_message or not update.message.reply_to_message.forward_from:
        return
    user = update.message.reply_to_message.forward_from
    signature = ADMIN_SIGNATURES.get(update.effective_user.id, "Администратор")
    text = f"{update.message.text}\n\n— {signature}"
    await context.bot.send_message(chat_id=user.id, text=text)


REVIEWS_FILE = "reviews.txt"


async def review(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Store user reviews and notify admins."""
    if not context.args:
        await update.message.reply_text("Пожалуйста, отправьте отзыв после команды /review.")
        return
    text = " ".join(context.args)
    with open(REVIEWS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{update.effective_user.id}\t{text}\n")
    await update.message.reply_text("Спасибо за отзыв!")
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"Новый отзыв от {update.effective_user.id}:\n{text}",
    )


async def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("review", review))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), forward_to_admins))
    application.add_handler(MessageHandler(filters.TEXT & filters.REPLY, relay_from_admins))
    await application.run_polling()


if __name__ == "__main__":
    if not BOT_TOKEN or not ADMIN_CHAT_ID:
        raise SystemExit("Please set BOT_TOKEN and ADMIN_CHAT_ID environment variables.")
    import asyncio

    asyncio.run(main())
