from collections import defaultdict
from pyrogram import Client,filters
from pyrogram.types import Message , ReplyKeyboardMarkup , ReplyKeyboardRemove , InlineKeyboardMarkup , InlineKeyboardButton , CallbackQuery , KeyboardButton
from .nec import *

@Client.on_message(filters.command("start") & filters.private)
async def start_handel(c:Client,m:Message):
     keyboard = create_keyboard([["تست تایپ ده انگشتی"]])
     await m.reply_text(text="خوش امدید",reply_markup=keyboard)

@Client.on_message(filters.text & filters.private)
async def start_handel(c:Client,m:Message):
     ...





# ([["تست تایپ ده انگشتی","رقابت زنده"],["دعوت دوستان","اموزش ها"],["ارتباط با ما","پروفایل شما"]])