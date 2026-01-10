import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Русский алфавит (с ё)
RUSSIAN_UPPER = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
RUSSIAN_LOWER = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
LATIN_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LATIN_LOWER = "abcdefghijklmnopqrstuvwxyz"

def caesar_cipher(text: str, shift: int) -> str:
    result = []
    for char in text:
        if char in RUSSIAN_UPPER:
            idx = (RUSSIAN_UPPER.index(char) + shift) % len(RUSSIAN_UPPER)
            result.append(RUSSIAN_UPPER[idx])
        elif char in RUSSIAN_LOWER:
            idx = (RUSSIAN_LOWER.index(char) + shift) % len(RUSSIAN_LOWER)
            result.append(RUSSIAN_LOWER[idx])
        elif char in LATIN_UPPER:
            idx = (LATIN_UPPER.index(char) + shift) % len(LATIN_UPPER)
            result.append(LATIN_UPPER[idx])
        elif char in LATIN_LOWER:
            idx = (LATIN_LOWER.index(char) + shift) % len(LATIN_LOWER)
            result.append(LATIN_LOWER[idx])
        else:
            # Остальные символы (пробелы, цифры, знаки) остаются без изменений
            result.append(char)
    return ''.join(result)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я шифрую текст шифром Цезаря.\n\n"
        "Используй команды:\n"
        "🔸 /encrypt <сдвиг> <текст> — зашифровать\n"
        "🔸 /decrypt <сдвиг> <текст> — расшифровать\n\n"
        "Пример: /encrypt 3 Hello\n"
        "Пример: /encrypt 5 Привет"
    )

async def encrypt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("❌ Неверный формат.\nИспользуй: /encrypt <сдвиг> <текст>")
        return
    try:
        shift = int(context.args[0])
        text = ' '.join(context.args[1:])
        encrypted = caesar_cipher(text, shift)
        await update.message.reply_text(f"🔒 Зашифровано:\n{encrypted}")
    except ValueError:
        await update.message.reply_text("❌ Сдвиг должен быть целым числом.")

async def decrypt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("❌ Неверный формат.\nИспользуй: /decrypt <сдвиг> <текст>")
        return
    try:
        shift = int(context.args[0])
        text = ' '.join(context.args[1:])
        decrypted = caesar_cipher(text, -shift)
        await update.message.reply_text(f"🔓 Расшифровано:\n{decrypted}")
    except ValueError:
        await update.message.reply_text("❌ Сдвиг должен быть целым числом.")

def main():
    # ⚠️ ЗАМЕНИТЕ ЭТУ СТРОКУ НА ВАШ НОВЫЙ ТОКЕН ИЗ @BotFather
    TOKEN = "8215650968:AAFqXNy4-V3zEe8rgcICj_0HutaqAUZyt2w"

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("encrypt", encrypt))
    app.add_handler(CommandHandler("decrypt", decrypt))

    print("Бот запущен и готов к работе...")
    app.run_polling()

if __name__ == "__main__":
    main()