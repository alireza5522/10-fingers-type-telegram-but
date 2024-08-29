from collections import defaultdict
from pyrogram import Client,filters
from pyrogram.types import Message , ReplyKeyboardMarkup , ReplyKeyboardRemove , InlineKeyboardMarkup , InlineKeyboardButton , CallbackQuery , KeyboardButton
from datetime import datetime
from keys.keys import *
import pytz
import mysql.connector
import json
import random


db = mysql.connector.connect(
    host = HOST,
    user = USER,
    password = PASSWORD,
    database = DATABASE
)

mycursor = db.cursor()

def Tree():
    return defaultdict(Tree)

User_pucket = Tree()

def create_keyboard(buttons):
    return ReplyKeyboardMarkup(
        [[KeyboardButton(button) for button in row] for row in buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    
def date_time():
    iran_tz = pytz.timezone('Asia/Tehran')
    iran_time = datetime.now(iran_tz)
    return iran_time.strftime('%Y-%m-%d %H:%M:%S')

def check_user(m):
    mycursor.execute("SELECT COUNT(*) FROM users WHERE id = %s;",(m.from_user.id,))
    user_exist = mycursor.fetchone()[0]
    if user_exist:
        return
    else:
        mycursor.execute("INSERT iNTO users VALUES (%s,%s,%s,%s,%s);",(m.from_user.id,m.from_user.username,m.from_user.first_name,date_time(),"start"))
        db.commit()

def read_fact():
    with open("texts.txt", 'r', encoding='utf-8') as file:
        lines = file.readlines()
        random_line = random.choice(lines).strip()
    return random_line

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def calculate_typing_metrics(original_text, user_input, time_seconds):
    # محاسبه تعداد کاراکترهای صحیح
    correct_chars = levenshtein_distance(original_text, user_input)
    # محاسبه تعداد کل کاراکترهای تایپ شده
    total_chars = len(user_input)
    
    # محاسبه زمان تایپ به دقیقه
    time_minutes = time_seconds / 60
    
    # محاسبه WPM
    summ = 0
    for i in user_input.split(" "):
        summ += len(i)
    yo = summ/len(user_input.split(" "))

    wpm = (total_chars / yo) / time_minutes

    # محاسبه دقت تایپ
    accuracy = (correct_chars / total_chars) * 100
    accuracy = 100 - accuracy
    
    return wpm, accuracy


