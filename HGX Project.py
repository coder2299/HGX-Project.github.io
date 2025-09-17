import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import random
import time

# Подключаемся к базе данных SQLite
conn = sqlite3.connect('lottery.db')
c = conn.cursor()

# Создаем таблицу для игроков
c.execute('''
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    ticket_number TEXT UNIQUE
)
''')
conn.commit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать в нашу лотерею! Используйте команду /buy_ticket, чтобы приобрести билет.")

async def buy_ticket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем ID пользователя
    user_id = update.effective_user.id
    
    # Проверяем, купил ли пользователь ранее билет
    c.execute("SELECT * FROM players WHERE user_id=?", (user_id,))
    existing_player = c.fetchone()
    
    if existing_player is not None:
        await update.message.reply_text(f"У вас уже есть билет № {existing_player[2]}!")
        return
    
    # Генерация уникального номера билета
    ticket_number = str(random.randint(10000, 99999))
    
    # Добавление записи в базу данных
    try:
        c.execute("INSERT INTO players VALUES(NULL, ?, ?)", (user_id, ticket_number))
        conn.commit()
        await update.message.reply_text(f"Ваш билет № {ticket_number}. Желаем удачи!")
    except Exception as e:
        print(e)
        await update.message.reply_text("Ошибка покупки билета. Попробуйте позже.")

async def draw_winner(context: ContextTypes.DEFAULT_TYPE):
    # Выбираем всех участников
    c.execute("SELECT * FROM players")
    participants = c.fetchall()
    
    if len(participants) > 0:
        winner = random.choice(participants)
        
        for participant in participants:
            if participant[0] != winner[0]:
                await context.bot.send_message(chat_id=participant[1], text="Вы не выиграли в этот раз. Но попробуйте снова!")
            
        await context.bot.send_message(chat_id=winner[1], text=f"Поздравляем! Ваш билет № {winner[2]} выиграл!")
    else:
        await context.bot.send_message(chat_id=context.job.chat_id, text="Нет участников в текущей игре.")

def main():
   TOKEN = 8301014065:AAExTdKMjqCrfnbhYAw8cnl-YUdbG5buPPM
    
    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("buy_ticket", buy_ticket))
    
    # Запускаем розыгрыш каждый день в полночь
    job_queue = application.job_queue
    job_queue.run_daily(draw_winner, time.time())
    
    # Стартуем бота
    application.run_polling()

if __name__ == '__main__':
    main()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

