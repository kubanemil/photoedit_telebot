import config
import telebot
from telebot import types
import time, os.path, glob
from label_photo import add_label



token = config.TOKEN
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxUAAWI_48Bw5I6B3Wpc-E2z9E3kL2MtAAKCAAOw0PgMxiPKI5Nmy0YjBA')
    bot.reply_to(message, "Добро пожаловать, {}.".format(message.from_user.first_name))
    start_markup = types.InlineKeyboardMarkup(row_width=4)
    start_markup_btn1 = types.InlineKeyboardButton('Начать работу', callback_data='start')
    start_markup.add(start_markup_btn1)
    bot.send_message(message.chat.id, "Здесь я добавлю рандомную запись на присланное тобой фото.", reply_markup=start_markup)


@bot.message_handler(content_types=['photo', 'sticker'])
def edit(message):
    bot.send_message(message.chat.id, 'Подождите пару секунд..')
    try:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    except:
        file_info = bot.get_file(message.sticker.file_id)
    # bot.send_message(message.chat.id, file_info.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    user_id = message.from_user.id
    # «YYYY-MM-DD_HH:mm_<user id>.jpg».
    now = time.localtime()
    date = time.strftime("%Y-%m-%d_%H-%M", now)
    src = './recieved_photo/' + str(date) + str(user_id) + '.jpg'
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    edited_photo = add_label(src)
    img = open(edited_photo, 'rb')
    share_markup = types.InlineKeyboardMarkup(row_width=4)
    share_markup_btn1 = types.InlineKeyboardButton('Поделиться', callback_data='share')
    share_markup.add(share_markup_btn1)
    bot.send_photo(message.chat.id, img, caption='Ваше фото готово!', reply_markup=share_markup)

@bot.message_handler(commands=['get_id'])
def welcome(message):
    bot.send_message(message.chat.id, "File id: {}.".format(message.sticker.file_id))
    start_markup = types.InlineKeyboardMarkup(row_width=4)

@bot.callback_query_handler(func=lambda call: True)
def reply(call):
    if call.message:
        if call.data == 'start':
            bot.send_message(call.message.chat.id, 'Отправь мне любое фото: ')
        if call.data == 'share':
            folder_path = config.path_to_edited_folder
            file_type = r'\*jpg'
            files = glob.glob(folder_path + file_type)
            max_file = max(files, key=os.path.getctime)
            edited_file = open(max_file, 'rb')
            bot.send_photo(config.repost_chanel_id, edited_file)



bot.infinity_polling()