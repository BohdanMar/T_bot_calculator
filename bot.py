import config
import telebot
from telebot import types

bot = telebot.TeleBot(config.token)


user_num1 = ''
user_num2 = ''
user_proc = ''
user_result = None


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardRemove(selective=False)

    msg = bot.send_message(message.chat.id, "Hello " + message.from_user.first_name +
                           ", I am not some ordinary bot, I am an advanced Artificial Intelligence. I can count all the numbers in the world at once.\nEnter the number, if you don't chicken out", reply_markup=markup)
    bot.register_next_step_handler(msg, process_num1_step)


def process_num1_step(message, user_result=None):
    try:
        global user_num1

        if user_result == None:
            user_num1 = int(message.text)
        else:
            user_num1 = str(user_result)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembtn1 = types.KeyboardButton('+')
        itembtn2 = types.KeyboardButton('-')
        itembtn3 = types.KeyboardButton('*')
        itembtn4 = types.KeyboardButton('/')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

        msg = bot.send_message(
            message.chat.id, "Well? Set me the operation, dude", reply_markup=markup)
        bot.register_next_step_handler(msg, process_proc_step)
    except Exception as e:
        bot.reply_to(
            message, 'Am I a joke to you? Do you think this is a number? Very funy... Au revoir!')


def process_proc_step(message):
    try:
        global user_proc

        user_proc = message.text
        markup = types.ReplyKeyboardRemove(selective=False)

        msg = bot.send_message(
            message.chat.id, "Should I come up with the second number instead of you? Let's hurry", reply_markup=markup)
        bot.register_next_step_handler(msg, process_num2_step)
    except Exception as e:
        bot.reply_to(
            message, 'Am I a joke to you? Do you think this is a number? Very funy... Au revoir!')


def process_num2_step(message):
    try:
        global user_num2

        user_num2 = int(message.text)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembtn1 = types.KeyboardButton('Result')
        itembtn2 = types.KeyboardButton('Continue calculation')
        markup.add(itembtn1, itembtn2)

        msg = bot.send_message(
            message.chat.id, "Show the result, continue the operation or remind you that you are just a biological creature limited in space and time?", reply_markup=markup)
        bot.register_next_step_handler(msg, process_alternative_step)
    except Exception as e:
        bot.reply_to(
            message, 'Am I a joke to you? Do you think this is a number? Very funy... Au revoir!')


def process_alternative_step(message):
    try:
        calc()
        markup = types.ReplyKeyboardRemove(selective=False)

        if message.text.lower() == 'result':
            bot.send_message(
                message.chat.id, calcResultPrint(), reply_markup=markup)
        elif message.text.lower() == 'continue calculation':
            process_num1_step(message, user_result)

    except Exception as e:
        bot.reply_to(
            message, 'Am I a joke to you? Do you think this is a number? Very funy... Au revoir!')


def calcResultPrint():
    global user_num1, user_num2, user_proc, user_result
    return "Hmm .. you couldn't come up with anything more complicated? .. Okay, here's the Result: " + str(user_num1) + ' ' + user_proc + ' ' + str(user_num2) + ' = ' + str(user_result)


def calc():
    global user_num1, user_num2, user_proc, user_result

    user_result = eval(str(user_num1) + user_proc + str(user_num2))

    return user_result


bot.enable_save_next_step_handlers(delay=2)


bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)
