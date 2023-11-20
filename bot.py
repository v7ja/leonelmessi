import subprocess
import os
import re
import requests
from telebot import TeleBot
from telebot.types import InlineKeyboardButton as btn
from telebot.types import InlineKeyboardMarkup as mk
from telebot.types import KeyboardButton as kb
from telebot.types import ReplyKeyboardMarkup as rep

admin = '1422329397'
token = "6845324098:AAHRUR8Ylahfp4-YcrsK1qe4gF-FjvwIaGs"
domain = "smmmain.com" 
api_key = "d039bde936d09c4d9d83ec7dfa871980"
id_service = 103
bot = TeleBot(token=token, skip_pending=True, parse_mode='html', disable_web_page_preview=True)
print(bot)


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    keys = rep(row_width=2, resize_keyboard=True)
    btn1 = kb('مشاهدات ')
    btn2 = kb('تفاعلات')
    keys.add(btn2, btn1)
    msg = f"""• مرحبا بك عزيزي <a href="tg://user?id={user_id}">{message.from_user.first_name}</a> 

<strong>• في بوت رشق المشاهدات المجاني </strong>

• اختر ماتود فعلة من الازرار ادناه """
    bot.reply_to(message, msg, reply_markup=keys)


@bot.message_handler(func=(lambda message: True))
def msgs(message):
    text = message.text
    user_id = message.from_user.id
    keys = rep(row_width=2, resize_keyboard=True)
    btn1 = kb('رجوع')
    keys.add(btn1)
    
    if text == "مشاهدات":
        step = bot.reply_to(message, " ارسل المفتاح ورابط المنشور والعدد بهذه الصيغه key:link:100000", reply_markup=keys)
        bot.register_next_step_handler(step, link_post)
    if text == 'تفاعلات':
        step = bot.reply_to(message, "  ارسل المفتاح ورابط المنشور والعدد بهذه الصيغه key:link:500", reply_markup=keys)
        bot.register_next_step_handler(step, llink_post)
    elif text == "رجوع":
        keys = rep(row_width=2, resize_keyboard=True)
        btn1 = kb('مشاهدات')
        btn2 = kb('تفاعلات')
        keys.add(btn2, btn1)
        msg = f"""• مرحبا بك عزيزي <a href="tg://user?id={user_id}">{message.from_user.first_name}</a> 

<strong>• في بوت رشق المشاهدات المجاني </strong>
• اختر ماتود فعلة من الازرار ادناه """
        bot.reply_to(message, msg, reply_markup=keys)

@bot.channel_post_handler(func=(lambda message: True))
def channels_msgs(message):
    username = message.chat.username.lower()
    print(username)
    if db.exists(username):
        msg_id = message.message_id
        url = f"https://t.me/{username}/{msg_id}"
        response = requests.get(f"https://{domain}/api/v2?key={api_key}&action=add&service={id_service}&quantity=100&link={url}")
        if response.status_code == 200:
            try:
                order = response.json()['order']
                id = db.get(username)['id']
                keys = mk()
                btn1 = btn("رابط المنشور", url=url)
                keys.add(btn1)
                db.set(url, True)
                msg = f"""تم بدء الرشق بنجاح 

العدد : 1000 مشاهدة
رقم الطلب: {order}
الرابط : {url}

<strong>py:  @D_C_F </strong>"""
                bot.send_message(chat_id=int(id), text=msg, reply_markup=keys)
            except Exception as a:
                print(a)
                return


def format_post(link):
    body = r"https?://t\.me/(\w+)/(\d+)"
    if re.match(body, link):
        return True
    else:
        return False


def format_link(link):
    body = r"https:\/\/t.me\/[a-zA-Z0-9_]{5,32}$"
    if re.match(body, link):
        return True
    else:
        return False


def link_post(message):
    text = message.text
    keey = text.split(":")[0]
    liink = text.split(":")[1] +':'+ text.split(":")[2]
    qun = text.split(":")[3]
    if text == "رجوع":
        msgs(message)
        return

    response = requests.get(f"https://{domain}/api/v2?key={keey}&action=add&service={id_service}&quantity={qun}&link={liink}")
    if response.status_code == 200:

            order = response.json()['order']
            msg = f"""تم بدء الرشق بنجاح 

العدد : 100000 مشاهدة
رقم الطلب : {order}
الرابط : {liink}

<strong>py:  @D_C_F</strong>"""
            bot.reply_to(message, msg)
         
def llink_post(message):
    text = message.text
    keey = text.split(":")[0]
    liink = text.split(":")[1] +':'+ text.split(":")[2]
    qun = text.split(":")[3]
    if text == "رجوع":
        msgs(message)
        return

    response = requests.get(f"https://{domain}/api/v2?key={keey}&action=add&service=191&quantity={qun}&link={liink}")
    if response.status_code == 200:
            order = response.json()['order']
            msg = f"""تم بدء الرشق بنجاح 

العدد : 500 تفاعل
رقم الطلب : {order}
الرابط : {liink}

<strong>py:  @D_C_F</strong>"""
            bot.reply_to(message, msg)


bot.infinity_polling()
