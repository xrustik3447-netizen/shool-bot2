from flask import Flask
import threading

app = Flask(__name__)


@app.route("/")
def home():
  I = "Bot is active!"
  return I


def run_flask():
  # Render виділяє порт через змінну середовища PORT
  import os

  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)


# Запускаємо вебсервер у фоновому потоці, щоб він відкривав порт для Render
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

# Далі йде звичний запуск вашого бота
# bot.infinity_polling(...)
import telebot
from telebot import types

# Вставте ваші дані
TOKEN = '8811022791:AAFjnUA0ixxfWcrcpkKuGwYSwMRHPSvl2KA'
ADMIN_ID = '1014079912'
bot = telebot.TeleBot(TOKEN)

# --- Клавіатури ---
def get_main_menu():
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
  btn1 = types.KeyboardButton("🚨 Булінг")
  btn2 = types.KeyboardButton("🆘 Допомога")
  btn3 = types.KeyboardButton("👨‍👩‍👧‍👦 Проблеми в сім'ї")
  btn4 = types.KeyboardButton("💡 Інше")
  markup.add(btn1, btn2, btn3, btn4)
  return markup


def get_finish_keyboard():
  markup = types.InlineKeyboardMarkup()
  finish_btn = types.InlineKeyboardButton(
      "✅ Завершити діалог", callback_data="finish_chat"
  )
  markup.add(finish_btn)
  return markup

# --- Команди ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Вітаю! Оберіть категорію звернення:", reply_markup=get_main_menu())

@bot.message_handler(
    func=lambda message: message.text
    and any(word in message.text for word in ["Булінг", "булінг"])
)
def start_report(message):
  category = message.text
  msg = bot.send_message(
      message.chat.id,
      "1) Вкажіть вашу школу та клас.\n"
      "2) Опишіть ситуацію одним повідомленням\n\n"
      "⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️\n\n"
      "ПРИКЛАД: ЗЗСО №153, 9-А клас, (детальний опис ситуації...)",
      reply_markup=types.ReplyKeyboardRemove(),
  )
  bot.register_next_step_handler(msg, send_to_admin, category)
def send_to_admin(message, category):
    admin_text = (f"📩 **Нове звернення** | ID: {message.chat.id}\n"
                  f"👤 Від: {message.from_user.first_name}\n"
                  f"📂 Категорія: {category}\n\n"
                  f"📝 **Дані та опис:**\n{message.text}")
    
    bot.send_message(ADMIN_ID, admin_text, parse_mode="Markdown")
    
    # Повідомлення користувачу
    bot.send_message(message.chat.id, 
                     "👮‍♂️ Інспектору СОБ надіслано повідомлення.\nОчікуй на відповідь ⚠️", 
                     reply_markup=get_finish_keyboard())

# --- Логіка чату ---
@bot.callback_query_handler(func=lambda call: call.data == "finish_chat")
def finish_chat(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    bot.send_message(call.message.chat.id, 
                     "Діалог завершено ✅\nЯкщо бажаєте продовжити діалог, поверніться до головного меню ⭐", 
                     reply_markup=get_main_menu())

# Пересилка відповідей адміна
@bot.message_handler(func=lambda message: message.chat.id == int(ADMIN_ID) and message.reply_to_message)
def admin_reply(message):
    try:
        user_id = message.reply_to_message.text.split("ID: ")[1].split("\n")[0]
        bot.send_message(user_id, f"👤 **Відповідь інспектора:**\n{message.text}", reply_markup=get_finish_keyboard())
    except:
        bot.send_message(ADMIN_ID, "❌ Помилка: ID користувача не знайдено.")

# Пересилка відповідей користувача
@bot.message_handler(func=lambda message: message.reply_to_message and message.reply_to_message.from_user.id == bot.get_me().id)
def user_reply(message):
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "Ваше повідомлення передано інспектору.", reply_markup=get_finish_keyboard())

if __name__ == '__main__':
    bot.infinity_polling()
import telebot
from telebot import types

# Вставте ваші дані
TOKEN = '8811022791:AAFjnUA0ixxfWcrcpkKuGwYSwMRHPSvl2KA'
ADMIN_ID = '1014079912'
bot = telebot.TeleBot(TOKEN)

# --- Клавіатури ---
def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🛡 Булінг", "🆘 Допомога", "👨‍👩‍👧 Проблеми в сім’ї", "💡 Інше")
    return markup

def get_finish_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Завершити діалог", callback_data="finish_chat"))
    return markup

# --- Команди ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Вітаю! Оберіть категорію звернення:", reply_markup=get_main_menu())

@bot.message_handler(func=lambda message: message.text in ["🤬 Булінг", "🆘 Допомога", "👨‍👩‍👧 Проблеми в сім’ї", "💡 Інше"])
def start_report(message):
    category = message.text
    msg = bot.send_message(message.chat.id, 
                           "1) Вкажіть вашу школу та клас.\n"
                           "2) Опишіть ситуацію одним повідомленням\n\n"
                           "❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️\n"
                           "ПРИКЛАД: ЗЗСО №153, 9-А клас, (детальний опис ситуації...)", 
                           reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, send_to_admin, category)

def send_to_admin(message, category):
    admin_text = (f"📩 **Нове звернення** | ID: {message.chat.id}\n"
                  f"👤 Від: {message.from_user.first_name}\n"
                  f"📂 Категорія: {category}\n\n"
                  f"📝 **Дані та опис:**\n{message.text}")
    
    bot.send_message(ADMIN_ID, admin_text, parse_mode="Markdown")
    
    # Повідомлення користувачу
    bot.send_message(message.chat.id, 
                     "👮‍♂️ Інспектору СОБ надіслано повідомлення.\nОчікуй на відповідь ⚠️", 
                     reply_markup=get_finish_keyboard())

# --- Логіка чату ---
@bot.callback_query_handler(func=lambda call: call.data == "finish_chat")
def finish_chat(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    bot.send_message(call.message.chat.id, 
                     "Діалог завершено ✅\nЯкщо бажаєте продовжити діалог, поверніться до головного меню ⭐", 
                     reply_markup=get_main_menu())

# Пересилка відповідей адміна
@bot.message_handler(func=lambda message: message.chat.id == int(ADMIN_ID) and message.reply_to_message)
def admin_reply(message):
    try:
        user_id = message.reply_to_message.text.split("ID: ")[1].split("\n")[0]
        bot.send_message(user_id, f"👤 **Відповідь інспектора:**\n{message.text}", reply_markup=get_finish_keyboard())
    except:
        bot.send_message(ADMIN_ID, "❌ Помилка: ID користувача не знайдено.")

# Пересилка відповідей користувача
@bot.message_handler(func=lambda message: message.reply_to_message and message.reply_to_message.from_user.id == bot.get_me().id)
def user_reply(message):
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "Ваше повідомлення передано інспектору.", reply_markup=get_finish_keyboard())

if __name__ == '__main__':
    bot.infinity_polling()
Настройки
Выйти
