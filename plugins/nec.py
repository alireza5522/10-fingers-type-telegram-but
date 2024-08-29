from collections import defaultdict
from pyrogram import Client,filters
from pyrogram.types import Message , ReplyKeyboardMarkup , ReplyKeyboardRemove , InlineKeyboardMarkup , InlineKeyboardButton , CallbackQuery , KeyboardButton
import json
from datetime import datetime
import pytz
import os
import sys

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
    
# if getattr(sys, 'frozen', False):
#     application_path = os.path.dirname(sys.executable)
# else:
#     application_path = os.path.dirname(os.path.abspath(__file__))


