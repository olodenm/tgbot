from random import choice
import telebot

token = ''
bot = telebot.TeleBot(token)

RANDOM_TASKS = ['Написать Гвидо письмо', 'Выучить Python', 'Записаться на курс в Нетологию', 'Посмотреть 4 сезон Рик и Морти']

todos = dict()

HELP = '''
Список доступных команд:
* print  - напечатать все задачи на заданную дату
* todo - добавить задачу
* random - добавить на сегодня случайную задачу
* help - Напечатать help
'''

def add_todo(date, task, category=None):
    date = date.lower()
    if len(task) < 3:
        return "Задача должна содержать как минимум 3 символа."
    if date in todos:
        todos[date].append((task, category))
    else:
        todos[date] = [(task, category)]

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, HELP)

@bot.message_handler(commands=['random'])
def random(message):
    task = choice(RANDOM_TASKS)
    add_todo('сегодня', task)
    bot.send_message(message.chat.id, f'Задача {task} добавлена на сегодня')

@bot.message_handler(commands=['add'])
def add(message):
    _, date, tail = message.text.split(maxsplit=2)
    parts = tail.split('@')
    task = parts[0].strip()
    category = parts[1].strip() if len(parts) > 1 else None
    result = add_todo(date, task, category)
    if result is not None:
        bot.send_message(message.chat.id, result)
    else:
        bot.send_message(message.chat.id, f'Задача "{task}" добавлена на дату {date}')

@bot.message_handler(commands=['show'])
def print_(message):
    dates = message.text.split()[1:]
    if not dates:
        bot.send_message(message.chat.id, "Вы не указали дату(-ы).")
        return
    tasks = ''
    for date in dates:
        date = date.lower()
        if date in todos:
            for task, category in todos[date]:
                if category:
                    tasks += f'[ ] {task} @{category}\n'
                else:
                    tasks += f'[ ] {task}\n'
        else:
            tasks += f'На {date} задач нет.\n'
    bot.send_message(message.chat.id, tasks)

bot.polling(none_stop=True)
