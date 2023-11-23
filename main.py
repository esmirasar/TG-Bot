import telebot
from config import TOKEN
from extensions import CurrencyConverter
from extensions import APIException
from extensions import currency

bot = telebot.TeleBot(TOKEN)


# Создаем обработчик, который будет работать с командами start, help

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    bot.reply_to(message, "Я готов помочь! \n\nВ следующем сообщении нужно указать мне информацию в формате : \
        \n<Валюта, которую нужно конвертировать, валюта, в которую будем конвертировать, сумма>. \
        \n\nДанные нужно вводить в одной строке и без лишних символов (кавычки, запятые и т.д).\
        \n\nСписок доступных валют можно узнать по команде '/values'. ")

    #  Создаем обработчик, который будет работать с командой values


@bot.message_handler(commands=['values'])
def handle_values(message: telebot.types.Message):
    text = "Доступные мне валюты:"
    for key in currency.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

    # обработчик для работы с текстом


@bot.message_handler(content_types=['text'])
def handle_text(message: telebot.types.Message):
    # в случае, если пользователь отправляет /, ему  придут доступные команды
    if message.text == "/":
        commands = ["/start", "/help", "/values"]
        text = "Доступные команды:"
        for command in commands:
            text = '\n'.join((text, command))
        bot.reply_to(message, text)
    elif message.text.upper() in ["ПРИВЕТ", "КАК ДЕЛА"]:
        bot.reply_to(message, "Приветствую тебя! Я бы рад пообщаться, "
                              "но я тут для того, чтобы ты мог легко разобраться с конвертацией валюты.\n"
                              "Я могу помочь в конвертации валюты.\n"
                              "Для начала работы нажми '/start'")
    else:
        try:
            user_text = message.text.upper().split(' ')  # переменная, которая принимает ввод пользователя
            if len(user_text) != 3:
                raise APIException("Длина строки не соответствует нужным параметрам.\n\nСтрока должна содержать только 3 значения:\n\
                1.Валюта, которую нужно конвертировать\n\
                2.Валюта, в которую нужно конвертировать.\n\
                3.Сумма\nВсе данные вводняться одной строкой через пробез, без дополнительных символов (запятые, кавычки и т.д).\n\nПожалуйста, проверьте правильность ввода.")
            base, quote, amount = user_text
            converted_amount = CurrencyConverter.get_price(base, quote, amount)
            bot.send_message(message.chat.id,
                             f"Стоимость {amount} {currency[base]} = {converted_amount} {currency[quote]}")
        except APIException as e:
            bot.reply_to(message, str(e))

        except ValueError:
            bot.reply_to(message, "Пожалуйста, введите данные в правильном формате:\n\n<Валюта, которую нужно перевести, валюта, в которую будем переводить, сумма>.\
            \n\nДанные нужно вводить в одной строке без кавычек и запятых.")

    print(message.text)


bot.polling(none_stop=True)
