from collections import defaultdict
from pyrogram import Client,filters
from pyrogram.types import Message , ReplyKeyboardMarkup , ReplyKeyboardRemove , InlineKeyboardMarkup , InlineKeyboardButton , CallbackQuery , KeyboardButton
from .nec import *
import time

@Client.on_message(filters.command("start") & filters.private)
async def start_handel(c:Client,m:Message): 
     # mycursor.execute("SELECT * FROM users WHERE id = %s",(m.from_user.id,))
     check_user(m)

     mycursor.execute(f'UPDATE users SET stats = "start" WHERE id = {str(m.from_user.id)};')
     db.commit()
     
     keyboard = create_keyboard([["تست تایپ ده انگشتی"]])
     await m.reply_text(text="خوش امدید",reply_markup=keyboard)

@Client.on_message(filters.regex("تست تایپ ده انگشتی") & filters.private)
async def button_handel(c:Client,m:Message):
     mycursor.execute(f'UPDATE users SET stats = "test_type" WHERE id = {str(m.from_user.id)};')
     db.commit()
     keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("شروع", callback_data="start")],
     ])

     await m.reply_text(text="Hello! Choose an option:",reply_markup=keyboard)
     

@Client.on_callback_query()
async def callback_query(client, callback_query):
     mycursor.execute("SELECT stats FROM users WHERE id = %s",(callback_query.message.chat.id,))
     stats = mycursor.fetchone()[0]

     if stats == "test_type":

          if callback_query.data == "start":
               keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("توقف/برگشت", callback_data="stop")],
               ])
               text = read_fact()

               await callback_query.message.edit_text(f"تست تایپ شما شروع شد این متن رو تایپ کنید\n\n**{text}**\n.",reply_markup=keyboard)

               mycursor.execute(f'UPDATE users SET stats = "typing" WHERE id = {str(callback_query.message.chat.id)};')
               mycursor.execute(f'UPDATE typing SET start_time = \"{str(time.time())}\",text_type = \"{text}\" WHERE user_id = {str(callback_query.message.chat.id)};')
               db.commit()
          
     elif stats == "typing":

          if callback_query.data == "stop":
               mycursor.execute(f'UPDATE users SET stats = "test_type" WHERE id = {str(callback_query.message.chat.id)};')
               db.commit()
          
               keyboard = InlineKeyboardMarkup([
               [InlineKeyboardButton("شروع", callback_data="start")],
               ])

               await callback_query.message.edit_text(text="Hello! Choose an option:",reply_markup=keyboard)





@Client.on_message((~filters.command("start") | ~filters.regex("تست تایپ ده انگشتی")) & filters.private)
async def message_handel(c:Client,m:Message):
     mycursor.execute("SELECT stats FROM users WHERE id = %s",(m.from_user.id,))
     stats = mycursor.fetchone()[0]

     if stats == "start":
          ...
     elif stats == "typing":
          mycursor.execute("SELECT start_time,text_type FROM typing WHERE user_id = %s",(m.from_user.id,))

          start_time,text = mycursor.fetchone()
          end_time = time.time()

          time_seconds = end_time - start_time
          wpm, accuracy, errors, stars, highlight_text = calculate_typing_metrics(text, m.text, time_seconds)

          mycursor.execute(f'UPDATE users SET stats = "test_type" WHERE id = {str(m.from_user.id)};')
          db.commit()

          keyboard = InlineKeyboardMarkup([
          [InlineKeyboardButton("شروع", callback_data="start")],
          ])

          await m.reply_text(text=f"سرعت تایپ (کلمه بر دقیقه): **{wpm:.1f}**\nدقت تایپ: **{accuracy:.1f}%**\nتعداد غلط: **{errors}**\n\n{"⭐️"*stars}\n\n{highlight_text}\n\nبرای شروع متن بعدی دکمه شروع رو بزنید",reply_markup=keyboard)



# ([["تست تایپ ده انگشتی","رقابت زنده"],["دعوت دوستان","اموزش ها"],["ارتباط با ما","پروفایل شما"]])