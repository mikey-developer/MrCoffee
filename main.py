import telebot
import sqlite3
import conf
import time

bot = telebot.TeleBot("7773651734:AAFubcod7k0uxV2d79fbqbLVcjIMEYnj_wA")

key_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
key_menu.row("☕️ Coffee")
key_menu.row("📝 History", "️⚙️ Settings")

# returns language
lang = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True)
lang.row("🇺🇿 Uzbek")
lang.row("🇺🇸 English")
lang.row("🇷🇺 Russian")

key_cancel = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True)
key_cancel.row("🚫 Cancel the order")

key_continue = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True)
key_continue.row("Continue")

def coffee():
    kofe = telebot.types.InlineKeyboardMarkup()
    btn_cappuccino = telebot.types.InlineKeyboardButton( text = "Cappuccino 5 000", callback_data = "btn_cappuccino")
    btn_latte = telebot.types.InlineKeyboardButton( text = "Latte 2 000", callback_data = "btn_latte")
    btn_arabica = telebot.types.InlineKeyboardButton( text = "Arabica 3 000", callback_data = "btn_arabicas")
    kofe.add(btn_cappuccino)
    kofe.add(btn_latte)
    kofe.add(btn_arabica)
    return kofe

def geo(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = telebot.types.KeyboardButton(text="📍 Send Location", request_location=True)
    # button_cancel = telebot.types.KeyboardButton(text="🚫 Cancel the order")
    keyboard.add(button_geo)
    # keyboard.add(button_cancel)
    return keyboard

@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        bot.send_message(5407368270, message.location)
        bot.send_message(5407368270, "latitude: %s; longitude: %s" % (message.location.latitude, message.location.longitude))
        bot.send_message(message.chat.id, f"Your order has been received, we will contact you within 24 hours! ✅", reply_markup=key_menu)

@bot.message_handler(commands = ['start'])
def start_message(message):
    SQL_START = f"""
                    CREATE TABLE '{message.from_user.id}' (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        phone TEXT,
                        lang TEXT
                    )
                 """
    try:
        conf.sql_go("base.db", SQL_START)
        bot.reply_to(message, "Your phone number:")
        bot.register_next_step_handler(message, user_phone)
    except:
        bot.send_photo(message.chat.id, 
                       photo = open("coffee.jpg", 'rb'), 
                       caption = "Welcome back to MrCoffe!",
                       reply_markup = key_menu
                      )

@bot.message_handler(content_types = ['text'])
def send_message(message):
    mid = message.chat.id
    text_is = message.text.lower()

    if text_is == ".":
        bot.send_message(mid, ".")

    ### Language parameters
    elif text_is == "🇺🇿 uzbek":
        conf.sql_go("base.db", f"UPDATE '{message.from_user.id}' SET lang = 'uz' WHERE id = 1;")
        ms_id = bot.send_message(mid, "Til o'zbekchaga o'zgartirildi", reply_markup = key_menu)
        time.sleep(2)
        bot.delete_message(mid, ms_id.message_id)
        bot.send_photo(mid, photo = open("coffee.jpg", 'rb'), caption = "Welcome to MrCoffe!")

    elif text_is == "en English":
        conf.sql_go("base.db", f"UPDATE '{message.from_user.id}' SET lang = 'en' WHERE id = 1;")
        ms_id = bot.send_message(mid, "Til o'zbekchaga o'zgartirildi", reply_markup = key_menu)
        time.sleep(2)
        bot.delete_message(mid, ms_id.message_id)
        bot.send_photo(mid, photo = open("coffee.jpg", 'rb'), caption = "Welcome to MrCoffe!")

    elif text_is == "ru Russian":
        conf.sql_go("base.db", f"UPDATE '{message.from_user.id}' SET lang = 'ru' WHERE id = 1;")
        ms_id = bot.send_message(mid, "Til o'zbekchaga o'zgartirildi", reply_markup = key_menu)
        time.sleep(2)
        bot.delete_message(mid, ms_id.message_id)
        bot.send_photo(mid, photo = open("coffee.jpg", 'rb'), caption = "Welcome to MrCoffe!")

    ### Menu
    elif text_is == "☕️ coffee":
        bot.send_message(mid, "Please, choose...", reply_markup = coffee())

    elif text_is == "📝 history":
        db = sqlite3.connect("base.db")
        sql = db.cursor()

        for data in sql.execute(f"SELECT * FROM '{message.from_user.id}_orders'").fetchall():
            bot.send_message(mid, f"History\n\nCoffee: {data[1]}\nCount: {data[2]}\nPrice: {data[3]}")

    elif text_is == "🚫 cancel the order":
        bot.send_message(mid, "Your order is cancelled!", reply_markup = key_menu)

    elif text_is == "continue":
        bot.send_message(mid, "Please, send your location 📍", reply_markup = geo(message))
    

def user_phone(message):
    phone = message.text
    SQL_INSERT = f"""
                    INSERT INTO '{message.from_user.id}' 
                    (id, phone, lang)
                    VALUES 
                    (NULL, '{phone}', 'default')
                 """
    conf.sql_go("base.db", SQL_INSERT) 
    bot.send_message(message.chat.id, "Please select language:", reply_markup = lang) # reply markup = lang()

@bot.callback_query_handler( func = lambda call: call.data == "btn_cappuccino")
def uz(call):
    message = call.message
    mid = message.chat.id
    mmd = message.message_id

    bot.send_message(mid, "How many would you like to order?\nexample: 1, 2, 5", reply_markup = key_cancel)
    bot.register_next_step_handler(message, order_coppuccino)

def order_coppuccino(message):
    count = message.text
    price = 5000 * int(count)
    db = sqlite3.connect("base.db")
    sql = db.cursor()
    for data in sql.execute(f"SELECT * FROM '{message.from_user.id}'").fetchall():
        bot.send_message(message.chat.id, 
                         f"📝 Your order:\n\n"
                         f"☕️ Coffee: Coppuccino\n"
                         f"🔄 Count: {count}\n" 
                         f"💸 Price: {price}\n"
                         f"📞 Phone: {data[1]}\n",
                         reply_markup = key_continue
                         )
        bot.send_message(5407368270, f"New order:\n\nCoffee: Coppuccino\nCount: {count}\nPhone: {data[1]} ", reply_markup = key_continue)

        SQL_HISTORY = f"""
                CREATE TABLE IF NOT EXISTS '{message.from_user.id}_orders' (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    coffee TEXT,
                    count TEXT,
                    price TEXT
                )
                """
        
        conf.sql_go("base.db", SQL_HISTORY)
        SQL_SAVE = f"""
                    INSERT INTO '{message.from_user.id}_orders' 
                    (id, coffee, count, price)
                    VALUES 
                    (NULL, 'Coppuccino', '{count}', {price})
                 """
        conf.sql_go("base.db", SQL_SAVE) 

bot.polling( none_stop = True )