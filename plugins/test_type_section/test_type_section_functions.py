from collections import defaultdict
from pyrogram import Client,filters
from pyrogram.types import Message , ReplyKeyboardMarkup , ReplyKeyboardRemove , InlineKeyboardMarkup , InlineKeyboardButton , CallbackQuery , KeyboardButton
from datetime import datetime
from keys.keys import HOST,USER,PASSWORD,DATABASE
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
    with open("plugins/test_type_section/texts.txt", 'r', encoding='utf-8') as file:
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

def rate_typing(accuracy, speed):
    rating_criteria = {
        (95, 50): 5,
        (95, 30): 4,
        (90, 50): 4,
        (90, 30): 3,
        (80, 30): 2
    }
    
    for (acc_threshold, spd_threshold), stars in rating_criteria.items():
        if accuracy > acc_threshold and speed > spd_threshold:
            return stars
    return 1

def highlight_errors(original_text, user_input):
    original_words = original_text.split()
    user_words = user_input.split()
    len_original = len(original_words)
    len_user = len(user_words)
    dp = [[0] * (len_user + 1) for _ in range(len_original + 1)]

    for i in range(len_original + 1):
        for j in range(len_user + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif original_words[i - 1] == user_words[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1])

    result = []
    i, j = len_original, len_user
    while i > 0 and j > 0:
        if original_words[i - 1] == user_words[j - 1]:
            result.append(original_words[i - 1])
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i - 1][j - 1] + 1:
            result.append(f"--**{user_words[j - 1]}**--")
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i - 1][j] + 1:
            result.append(f"--**{original_words[i - 1]}**--")
            i -= 1
        else:
            result.append(f"--**{user_words[j - 1]}**--")
            j -= 1

    while i > 0:
        result.append(f"--**{original_words[i - 1]}**--")
        i -= 1

    while j > 0:
        result.append(f"--**{user_words[j - 1]}**--")
        j -= 1

    return ' '.join(result[::-1])

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

    text = highlight_errors(original_text,user_input)
    
    return wpm, accuracy,correct_chars,rate_typing(accuracy, wpm),text

def read_encorrage(stars):
    data1 = {}
    data2 = {}
    with open('plugins/test_type_section/file.json', mode='r', encoding='utf-8') as file:
        data1 = json.load(file)
    with open('plugins/test_type_section/emoji.json', mode='r', encoding='utf-8') as file:
        data2 = json.load(file)
    return data1[stars][random.randint(0,len(data1[stars]))] + data2[stars][random.randint(0,len(data2[stars]))]
