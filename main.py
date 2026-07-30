from operator import call
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from unittest import result
import pyrogram
import telebot
from telebot import types
from threading import Thread
from pyrogram import Client, filters
from pyrogram.raw import functions

bot = telebot.TeleBot('ТОКЕН БОТА')

accounts = [ 
            {"session": "account1_session", "api_id": 0, "api_hash": "pass"},
            {"session": "account2_session", "api_id": 0, "api_hash": "pass"},
            
        ]

clients = [Client(account["session"], account["api_id"], account["api_hash"]) for account in accounts]

user_data = {}

senders = {
    'mail':'password',
    'mail':'password'



}

receivers = ['abuse@telegram.org', 'DMCA@telegram.org', 
             'stopca@telegram.org', 'security@telegram.org', 
             'corp@telegram.org', 'germany@telegram.org', 
             'info@telegram.org', 'levlam@telegram.org', 
             'recover@telegram.org', 'durov@telegram.org',
            'ton@telegram.org', 'sticker@telegram.org',
           '125support@telegram.org', 'spam@telegram.org'
           , 'pavel@telegram.org', 'corona@telegram.org',
          'mr@telegram.org', 'marta@telegram.org',
         'sms@telegram.org', 'api_support@telegram.org',
        'http@telegram.org', 'shyam@telegram.org',
       'alex@telegram.org', 'support@telegram.org',
      'marketing@telegram.org', 'ask@telegram.org', 
      'perekopsky@telegram.org', 'ceo@telegram.org',
     'vadim@telegram.org', 'qa@telegram.org',
    'elies@telegram.org', 'enquiries@telegram.org',
   'recovery@telegram.org', 'ca@telegram.org', 
   'hyman@telegram.org', 'me@telegram.org', 
   'Stickers@telegram.org']


def send_email(receiver, sender_email, sender_password, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.yandex.ru', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver, msg.as_string())
        server.quit()
        print('Успешно отправлено!')
        return True
    except Exception as e:
        print(f"Ошибка: {e}")
        return False

@bot.message_handler(commands=['start', 'help'])
def send_menu(message):
    user_id = message.from_user.id
    if is_subscription_active(user_id, payload=user_id):   
        
        def start(msg: types.Message):
            print(f"Подписка активна для пользователя {user_id}")
            bot.send_message(message.chat.id, "Ваша подписка успешно оформлена!")
            kb = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton(text="1. Снос аккаунта", callback_data='account_complaint')
            btn2 = types.InlineKeyboardButton(text="2. Снос канала", callback_data='channel_complaint')
            kb.add(btn1, btn2)
            bot.send_message(msg.chat.id, "Выберите тип жалобы:", reply_markup=kb)
        start(message)

        @bot.callback_query_handler(func=lambda call: True)
        def handle_callback(call):
            if call.data == 'account_complaint':
                show_account_complaint_menu(call.message.chat.id)
            elif call.data == 'channel_complaint':
                show_channel_complaint_menu(call.message.chat.id)
            elif call.data.startswith('account_'):
                handle_account_complaint(call)
            elif call.data.startswith('channel_'):
                handle_channel_complaint(call)
            elif call.data == 'back':
                start(call.message)
        

        def show_account_complaint_menu(chat_id):
            kb = types.InlineKeyboardMarkup(row_width=1)
            buttons = [
                ("Обычный снос", 'account_normal'),
                ("Снос сессий", 'account_sessions'),
                ("Виртуальный номер", 'account_virtual'),
                ("С Био", 'account_bio'),
                ("Премиум-аккаунт", 'account_premium'),
                ("Назад", 'back')
            ]
            for text, callback_data in buttons:
                kb.add(types.InlineKeyboardButton(text, callback_data=callback_data))
            bot.send_message(chat_id, "Выберите подкатегорию:", reply_markup=kb)

        
        def show_channel_complaint_menu(chat_id):
            kb = types.InlineKeyboardMarkup(row_width=1)
            buttons = [
                ("Публикация личных данных", 'channel_personal'),
                ("Продажа услуг доксинга", 'channel_dox'),
                ("Террористические угрозы", 'channel_terror'),
                ("Порнография с несовершеннолетними", 'channel_porn'),
                ("Мошенничество", 'channel_scam'),
                ("Назад", 'back')
            ]
            for text, callback_data in buttons:
                kb.add(types.InlineKeyboardButton(text, callback_data=callback_data))
            bot.send_message(chat_id, "Выберите подкатегорию:", reply_markup=kb)

    
        def handle_account_complaint(call):
            if call.data == 'account_normal':
                ask_for_username(call.message, "normal")
            elif call.data == 'account_sessions':
                ask_for_username(call.message, "sessions")
            elif call.data == 'account_virtual':
                ask_for_username(call.message, "virtual")
            elif call.data == 'account_bio':
                ask_for_username(call.message, "bio")
            elif call.data == 'account_premium':
                ask_for_username(call.message, "premium")

       
        def ask_for_username(message, complaint_type):
            bot.send_message(message.chat.id, "Введите Юзернейм:")
            bot.register_next_step_handler(message, process_account_username, complaint_type)

        def process_account_username(message, complaint_type):
            user_data['username'] = message.text
            bot.send_message(message.chat.id, "Теперь введите Telegram ID:")
            bot.register_next_step_handler(message, process_account_telegram_id, complaint_type)

        def process_account_telegram_id(message, complaint_type):
            user_data['telegram_id'] = message.text
            complaint_texts = {
                "normal": f"Аккаунт {user_data['username']}, {user_data['telegram_id']} нарушает правила.",
                "sessions": f"Потерян доступ к аккаунту {user_data['username']}, {user_data['telegram_id']}.",
                "virtual": f"Аккаунт {user_data['username']}, {user_data['telegram_id']} использует виртуальный номер.",
                "bio": f"Аккаунт {user_data['username']}, {user_data['telegram_id']} ссылает людей на сторонние сайты.",
                "premium": f"Аккаунт {user_data['username']}, {user_data['telegram_id']} злоупотребляет премиум-подпиской."
            }
            send_complaint(complaint_texts[complaint_type], "Жалоба на аккаунт")
            support_chat = {'SpamBot', 'GDPRBot'}                      
                   
                    
            clients.send_message(support_chat, complaint_texts[complaint_type])

        
        def handle_channel_complaint(call):
            if call.data == 'channel_personal':
                ask_for_channel_link(call.message, "personal")
            elif call.data == 'channel_dox':
                ask_for_channel_link(call.message, "dox")
            elif call.data == 'channel_terror':
                ask_for_channel_link(call.message, "terror")
            elif call.data == 'channel_porn':
                ask_for_channel_link(call.message, "porn")
            elif call.data == 'channel_scam':
                ask_for_channel_link(call.message, "scam")

        
        def ask_for_channel_link(message, complaint_type):
            bot.send_message(message.chat.id, "Введите ссылку на канал:")
            bot.register_next_step_handler(message, process_channel_link, complaint_type)

        def process_channel_link(message, complaint_type):
            user_data['channel_link'] = message.text
            bot.send_message(message.chat.id, "Введите ссылку на сообщение с нарушением:")
            bot.register_next_step_handler(message, process_violation_link, complaint_type)

        def process_violation_link(message, complaint_type):
            user_data['violation_link'] = message.text
            complaint_texts = {
                "personal": f"Канал {user_data['channel_link']} публикует личные данные. Нарушение: {user_data['violation_link']}.",
                "dox": f"Канал {user_data['channel_link']} продает услуги доксинга и сваттинга.",
                "terror": f"Канал {user_data['channel_link']} угрожает детям и планирует террористические атаки.",
                "porn": f"Канал {user_data['channel_link']} публикует порнографию с несовершеннолетними.",
                "scam": f"Канал {user_data['channel_link']} занимается мошенничеством."
            }
            send_complaint(complaint_texts[complaint_type], "Жалоба на канал")
            
                    
            support_chat = {'SpamBot', 'GDPRBot'}                      
                   
                    
            clients.send_message(support_chat, complaint_texts[complaint_type])
            


        def send_message_to_support(complaint_texts, support_chat, complaint_type):
                with clients:
                    
                    support_chat = {'',}                      
                   
                    
                    clients.send_message(support_chat, complaint_texts[complaint_type])
                    print("Сообщение отправлено")
        
        def send_complaint(complaint_text, subject, ):            
            sent_emails = 0
            for sender_email, sender_password in senders.items():
                for receiver_email in random.sample(receivers, min(2, len(receivers))):
                    send_email(receiver_email, sender_email, sender_password, subject, complaint_text)
            
                    sent_emails += 1
                    time.sleep(0.5)
            print(f"Всего отправлено жалоб: {sent_emails}")
    else:
        bot.send_message(message.chat.id, 'Ваша подписка не активна. Пожалуйста, оплатите подписку с помощью команды /subscribe.')




def bot_polling():
    bot.polling(none_stop=True, interval=0)

if __name__ == "__main__":
    bot_thread = Thread(target=bot_polling)
    bot_thread.start()



import requests
from datetime import datetime, timedelta

blat_users = []


def create_payment(user_id, period):
    url = ' https://pay.crypt.bot/api/createInvoice'
    headers = {
        "Crypto-Pay-API-Token": '279083:AA9utApe7CJ1cH6DGhOkp6SwzqyKoH5wBF8'

    }
    
    prices = {'day': 2.0, 'week': 6.0, 'month': 15.0, 'year': 40.0}
    price = prices.get(period, 1.0)  
    data = {
        'asset': 'USDT', 
        'amount': price,
        'description': f'Subscription for {period}',
        'payload': str(user_id),
        'hidden_message': 'Thank you for subscribing!',
        'paid_btn_name': 'viewItem',
        'paid_btn_url': '',
        'allow_comments': False,
        'allow_anonymous': False,
        'expires_in': 1800 
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

user_subscriptions = {}

def is_subscription_active(user_id, payload):
    if user_id in blat_users:
        return True
    expiration_date = user_subscriptions.get(user_id, None)
    handle_payment_update(payload)
    if expiration_date and datetime.now() < expiration_date:
        return True
    else:
        print(f"Подписка пользователя {user_id} истекла или отсутствует.")

    return False

def handle_payment_update(payload):
    try:
        print(f"Получен payload: {payload}") 
        user_id = int(payload['payload'])
        period = payload['description'].split()[-1]
        periods_map = {'day': 1, 'week': 7, 'month': 30, 'year': 365}
        duration_days = periods_map.get(period, 1)
        expiration_date = datetime.now() + timedelta(days=duration_days)  
        user_subscriptions[user_id] = expiration_date
        print(f"Обновлена подписка для пользователя {user_id}: до {expiration_date}")
    except Exception as e:
        print(f"Ошибка при обновлении подписки: {str(e)}")

@bot.message_handler(commands=['subscribe'])
def subscribe(msg: types.Message):
    kb = types.InlineKeyboardMarkup(row_width=2)
    btn_day = types.InlineKeyboardButton(text='1 день', callback_data='pay_day')
    btn_week = types.InlineKeyboardButton(text='1 неделя', callback_data='pay_week')
    btn_month = types.InlineKeyboardButton(text='1 месяц', callback_data='pay_month')
    btn_year = types.InlineKeyboardButton(text='1 год', callback_data='pay_year')
    kb.add(btn_day, btn_week, btn_month, btn_year)
    bot.send_message(msg.chat.id, 'Выберите период подписки:', reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data.startswith('pay_'))
def process_payment(call: types.CallbackQuery):
    period = call.data.split('_')[1]
    user_id = call.from_user.id
    payment_response = create_payment(user_id, period)

    
    if payment_response.get("ok"):
        pay_url = payment_response["result"]["pay_url"]
        bot.send_message(call.message.chat.id, f'Оплатите подписку по ссылке: {pay_url}')
    else:
        
        error_description = payment_response.get("description", "Неизвестная ошибка")
        bot.send_message(call.message.chat.id, f'Ошибка при создании платежа: {error_description}. Попробуйте позже.')
