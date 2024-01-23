import telebot
import sqlite3
import hashlib

class TelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.user_data = {}

        # Registering handlers
        self.bot.message_handler(commands=['start'])(self.start)
        self.bot.message_handler(func=lambda message: self.get_state(message) == 'awaiting_username')(self.process_username_step)
        self.bot.message_handler(func=lambda message: self.get_state(message) == 'awaiting_password')(self.process_password_step)

    def get_state(self, message):
        return self.user_data.get(message.chat.id, {}).get('state')

    def start(self, message):
        self.user_data[message.chat.id] = {'state': 'awaiting_username'}
        self.bot.send_message(message.chat.id, "Please enter your username:")

    def process_username_step(self, message):
        try:
            self.user_data[message.chat.id] = {
                'username': message.text,
                'state': 'awaiting_password'
            }
            self.bot.send_message(message.chat.id, "Now, please enter your password:")
        except Exception as e:
            self.bot.reply_to(message, 'Oops! Something went wrong.')

    def process_password_step(self, message):
        try:
            user_id = message.chat.id
            username = self.user_data[user_id]['username']
            password = message.text

            if self.check_credentials(username, password):
                self.bot.send_message(user_id, 'Login successful!')
            else:
                self.bot.send_message(user_id, 'Login failed. Please check your username and password and start the login again using /start command')

            # Clear user data after processing
            del self.user_data[user_id]

        except Exception as e:
            self.bot.reply_to(message, 'Login failed. Please check your username and password and start the login again using /start command')

    def check_credentials(self, username, provided_password):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username=?', (username,))
        result = cursor.fetchone()
        conn.close()

        if result:
            stored_password = result[0]
            return self.verify_password(stored_password, provided_password)
        else:
            return False

    def verify_password(self, stored_password, provided_password):
        salt = stored_password[:32]
        stored_pwdhash = stored_password[32:]
        pwdhash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
        return pwdhash == stored_pwdhash

    def run(self):
        self.bot.polling(none_stop=True)

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = TelegramBot("6860179471:AAGyV86i9zzD62E7i3HIr6lAAT8yjoXY5L8")
bot.run()