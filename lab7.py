import telebot
from telebot import types
import psycopg2
import datetime
conn = psycopg2.connect(host='localhost',
                        database="tgbot",
                        user="postgres",
                        password="MY_PASSWORD")

cursor = conn.cursor()

token = 'MY_API'

bot = telebot.TeleBot(token)

today = datetime.datetime.today()
week_number = today.isocalendar()[1]

if week_number % 2 == 0:
    week_num = 2
else:
    week_num = 1


def timetable(day, week_num):
    query = f"SELECT subject, room_numb, start_time, teacher_name FROM timetable WHERE day='{day}' AND week_numb='{week_num}'"

    cursor.execute(query)
    rows = cursor.fetchall()

    timetable_str = f'Расписание на {day} (неделя №{week_num}):\n\n'
    for row in rows:
        subject, room_numb, start_time, teacher_name = row
        timetable_str += f'{start_time} {room_numb}\n{subject}\n{teacher_name}\n\n'

    return timetable_str


def get_week(week_num):
    query = f"SELECT subject, room_numb, start_time, teacher_name, day FROM timetable WHERE week_numb='{week_num}'"

    cursor.execute(query)
    rows = cursor.fetchall()

    week_str = f'Расписание на текущую неделю:\n\n'
    for row in rows:
        subject, room_numb, start_time, teacher_name, day = row
        week_str += f'{day}\n{start_time} {room_numb}\n{subject}\n{teacher_name}\n\n'

    return week_str


def get_next_week(week_num):
    query = f"SELECT subject, room_numb, start_time, teacher_name, day FROM timetable WHERE week_numb='{week_num}'"

    cursor.execute(query)
    rows = cursor.fetchall()

    week_str = f'Расписание на следующую неделю:\n\n'
    for row in rows:
        subject, room_numb, start_time, teacher_name, day = row
        week_str += f'{day}\n{start_time} {room_numb}\n{subject}\n{teacher_name}\n\n'

    return week_str


@bot.message_handler(commands=['currentweek'])
def handle_timetable(message):
    if week_number % 2 == 0:
        week_num = 2
    else:
        week_num = 1
    week_str = get_week(week_num)
    bot.send_message(message.chat.id, week_str)


@bot.message_handler(commands=['week'])
def handle_timetable(message):
    if week_number % 2 == 0:
        week_str = 'Сейчас чётная неделя'
    else:
        week_str = 'Сейчас нечётная неделя'
    bot.send_message(message.chat.id, week_str)


@bot.message_handler(commands=['nextweek'])
def handle_timetable(message):
    if week_number % 2 == 0:
        week_num = 1
    else:
        week_num = 2
    week_str = get_next_week(week_num)
    bot.send_message(message.chat.id, week_str)


@bot.message_handler(commands=['Monday'])
def monday(message):
    day = 'Понедельник'
    if week_number % 2 == 0:
        week_num = 2
    else:
        week_num = 1
    timetable_str = timetable(day, week_num)
    bot.send_message(message.chat.id, timetable_str)


@bot.message_handler(commands=['Tuesday'])
def handle_timetable(message):
    day = 'Вторник'
    if week_number % 2 == 0:
        week_num = 2
    else:
        week_num = 1
    timetable_str = timetable(day, week_num)
    bot.send_message(message.chat.id, timetable_str)


@bot.message_handler(commands=['Wednesday'])
def handle_timetable(message):
    day = 'Среда'
    if week_number % 2 == 0:
        week_num = 2
    else:
        week_num = 1
    timetable_str = timetable(day, week_num)
    bot.send_message(message.chat.id, timetable_str)


@bot.message_handler(commands=['Thursday'])
def handle_timetable(message):
    day = 'Четверг'
    if week_number % 2 == 0:
        week_num = 2
    else:
        week_num = 1
    timetable_str = timetable(day, week_num)
    bot.send_message(message.chat.id, timetable_str)


@bot.message_handler(commands=['Friday'])
def handle_timetable(message):
    day = 'Пятница'
    if week_number % 2 == 0:
        week_num = 2
    else:
        week_num = 1
    timetable_str = timetable(day, week_num)
    bot.send_message(message.chat.id, timetable_str)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row('/help', '/mtuci',
                 '/currweek', '/nextweek',
                 '/week', '/Monday', '/Tuesday',
                 '/Wednesday', '/Thursday',
                 '/Friday')
    bot.send_message(message.chat.id, 'Здравствуйте, это бот с расписанием пар университета МТУСИ для группы БВТ2208! ',
                     reply_markup=keyboard)


@bot.message_handler(commands=['mtuci'])
def mtuci(message):
    bot.send_message(message.chat.id, 'Вся информация о МТУСИ - https://mtuci.ru/')


@bot.message_handler(commands=['help'])
def start_message(message):
        bot.send_message(message.chat.id, 'Вот, что я умею:\n\n/help - узнать о моих командах\n'
                                          '/currentweek - получить расписание на текущую неделю\n'
                                          '/nextweek - получить расписание на следующую неделю\n'
                                          '/week - узнать какая сегодня неделя\n'
                                          '/Monday - получить расписание на понедельник текущей недели\n'
                                          '/Tuesday - получить расписание на вторник текущей недели\n'
                                          '/Wednesday - получить расписание на среду текущей недели\n'
                                          '/Thursday - получить расписание на четверг текущей недели\n'
                                          '/Friday - получить расписание на пятницу текущей недели\n'
                                          '/mtuci - узнать всю новую информацию о МТУСИ'
                         )


@bot.message_handler(content_types=['text'])
def answer_(message):
    bot.send_message(message.chat.id, 'Извините, я Вас не понял. Пожалуйста, проверьте команду на правильность!')


def start(message):
    currweek_btn = types.KeyboardButton('/currentweek')
    nextweek_btn = types.KeyboardButton('/nextweek')
    monday_btn = types.KeyboardButton('/Monday')
    tuesday_btn = types.KeyboardButton('/Tuesday')
    wednesday_btn = types.KeyboardButton('/Wednesday')
    thursday_btn = types.KeyboardButton('/Thursday')
    friday_btn = types.KeyboardButton('/Friday')
    help_btn = types.KeyboardButton('/help')
    mtuci_btn = types.KeyboardButton('/mtuci')

    keyboard = types.ReplyKeyboardMarkup(row_width=5)
    row1 = [currweek_btn, nextweek_btn, monday_btn]
    row2 = [tuesday_btn, wednesday_btn, thursday_btn]
    row3 = [friday_btn, help_btn, mtuci_btn]
    keyboard.add(*row1)
    keyboard.add(*row2)
    keyboard.add(*row3)

    bot.send_message(chat_id=message.chat.id,
                     text="Choose an option:",
                     reply_markup=keyboard)


bot.polling(none_stop=True)
