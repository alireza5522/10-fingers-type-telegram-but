from collections import defaultdict
from pyrogram import Client,filters,enums
from pyrogram.types import Message , ReplyKeyboardMarkup , ReplyKeyboardRemove , InlineKeyboardMarkup , InlineKeyboardButton , CallbackQuery , KeyboardButton
from .functions import *
from .levelproccess import *
import random
import json
import time

async def pre_proccess(client, callback_query, level):
    ...

async def start_level(client, message, level,stage):
    data = {}
    with open("plugins/teachpath.json","r",encoding="utf-8") as file:
        data = json.load(file)
    
    data = data[level]

    if data["before"]:
        pre_proccess()

    if data["text_format"] == "word":
        keyboard = InlineKeyboardMarkup([
               [InlineKeyboardButton("برگشت", callback_data="stoplesson")]
               ])
        
        pass_ = data["pass"]
        pass_level = {}
        for key, value in pass_.items():
            key_tuple = tuple(map(int, key.split(',')))
            pass_level[key_tuple] = value

        words = list(data["text"])
        text = "".join(words[random.randint(0,1)])+"".join(words[random.randint(0,1)])+"".join(words[random.randint(0,1)])+"".join(words[random.randint(0,1)])
        text_show = " ".join(f"[{char}]" for char in text)
        if stage == "0":
            mycursor.execute(f'UPDATE users SET stats = "learning_{level}_{1}" WHERE id = {str(message.chat.id)};')
            db.commit()
            User_pucket[str(message.chat.id)]["temp_text"] = ""
            User_pucket[str(message.chat.id)]["bots_text"] = text + " "
            User_pucket[str(message.chat.id)]["start_time"] = time.time()
            await message.edit_text(text=f"**{text_show}**",reply_markup=ReplyKeyboardRemove())
        elif stage == "6":
            end_time = time.time()
            time_seconds = end_time - User_pucket[str(message.chat.id)]["start_time"]
            wpm, accuracy, errors, stars, highlight_text, enc = calculate_typing_metrics(User_pucket[str(message.chat.id)]["bots_text"], User_pucket[str(message.chat.id)]["temp_text"], time_seconds,pass_level)
            
            mycursor.execute(f'UPDATE users SET stats = "learning" WHERE id = {str(message.from_user.id)};')
            mycursor.execute(f'UPDATE learn SET lesson = lesson + 1 WHERE user_id = {str(message.from_user.id)};')

            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("شروع", callback_data="start")],
                [InlineKeyboardButton("برگشت", callback_data="stop")]
                ])

            await message.reply_text(text=f"سرعت تایپ (کلمه بر دقیقه): **{wpm:.1f}**\nدقت تایپ: **{accuracy:.1f}%**\nتعداد غلط: **{errors}**\n\n{"⭐️"*stars}\n\n{highlight_text}\n\n{enc}\n\nبرای شروع متن بعدی دکمه شروع رو بزنید",reply_markup=keyboard)
        
        else:
            User_pucket[str(message.chat.id)]["bots_text"] += text + " "
            await message.reply_text(text=f"**{text_show}**")

    if data["text_format"] == "word_random":

        words = list(data["text"])
        text_show = ""
        for i in range(random.randint(12,20)):
            for j in range(random.randint(3,5)):
                text_show += "".join(words[random.randint(1,len(words))-1])
            text_show += " "

        pass_ = data["pass"]
        pass_level = {}
        for key, value in pass_.items():
            key_tuple = tuple(map(int, key.split(',')))
            pass_level[key_tuple] = value

        if stage == "0":
            mycursor.execute(f'UPDATE users SET stats = "learning_{level}_{1}" WHERE id = {str(message.chat.id)};')
            db.commit()
            User_pucket[str(message.chat.id)]["temp_text"] = ""
            User_pucket[str(message.chat.id)]["bots_text"] = text_show
            User_pucket[str(message.chat.id)]["start_time"] = time.time()
            await message.edit_text(text=f"**{text_show}**",reply_markup=ReplyKeyboardRemove())
        elif stage == "2":
            end_time = time.time()
            time_seconds = end_time - User_pucket[str(message.chat.id)]["start_time"]
            wpm, accuracy, errors, stars, highlight_text, enc = calculate_typing_metrics(User_pucket[str(message.chat.id)]["bots_text"], User_pucket[str(message.chat.id)]["temp_text"], time_seconds,pass_level)
            
            mycursor.execute(f'UPDATE users SET stats = "learning" WHERE id = {str(message.from_user.id)};')
            mycursor.execute(f'UPDATE learn SET lesson = lesson + 1 WHERE user_id = {str(message.from_user.id)};')

            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("شروع", callback_data="start")],
                [InlineKeyboardButton("برگشت", callback_data="stop")]
                ])

            await message.reply_text(text=f"سرعت تایپ (کلمه بر دقیقه): **{wpm:.1f}**\nدقت تایپ: **{accuracy:.1f}%**\nتعداد غلط: **{errors}**\n\n{"⭐️"*stars}\n\n{highlight_text}\n\n{enc}\n\nبرای شروع متن بعدی دکمه شروع رو بزنید",reply_markup=keyboard)

    elif data["text_format"] == "sentence":
        words = data["text"]

        pass_ = data["pass"]
        pass_level = {}
        for key, value in pass_.items():
            key_tuple = tuple(map(int, key.split(',')))
            pass_level[key_tuple] = value

        if stage == "0":
            mycursor.execute(f'UPDATE users SET stats = "learning_{level}_{1}" WHERE id = {str(message.chat.id)};')
            db.commit()
            User_pucket[str(message.chat.id)]["temp_text"] = ""
            User_pucket[str(message.chat.id)]["bots_text"] = words
            User_pucket[str(message.chat.id)]["start_time"] = time.time()
            await message.edit_text(text=f"**{words}**",reply_markup=ReplyKeyboardRemove())
        elif stage == "2":
            end_time = time.time()
            time_seconds = end_time - User_pucket[str(message.chat.id)]["start_time"]
            wpm, accuracy, errors, stars, highlight_text, enc = calculate_typing_metrics(User_pucket[str(message.chat.id)]["bots_text"], User_pucket[str(message.chat.id)]["temp_text"].rstrip(), time_seconds,pass_level)
            
            mycursor.execute(f'UPDATE users SET stats = "learning" WHERE id = {str(message.from_user.id)};')
            mycursor.execute(f'UPDATE learn SET lesson = lesson + 1 WHERE user_id = {str(message.from_user.id)};')

            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("شروع", callback_data="start")],
                [InlineKeyboardButton("برگشت", callback_data="stop")]
                ])

            await message.reply_text(text=f"سرعت تایپ (کلمه بر دقیقه): **{wpm:.1f}**\nدقت تایپ: **{accuracy:.1f}%**\nتعداد غلط: **{errors}**\n\n{"⭐️"*stars}\n\n{highlight_text}\n\n{enc}\n\nبرای شروع متن بعدی دکمه شروع رو بزنید",reply_markup=keyboard)

    db.commit()

        

async def begin_level(client, callback_query, level):
    data = {}
    with open("plugins/teachpath.json","r",encoding="utf-8") as file:
        data = json.load(file)
    
    data = data[level]

    keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("شروع", callback_data="start")],
            [InlineKeyboardButton("برگشت", callback_data="stop")]
            ])
    if data["text_format"] == "word":
        words = list(data["text"])

        text = "".join(words[random.randint(0,1)])+"".join(words[random.randint(0,1)])+"".join(words[random.randint(0,1)])+"".join(words[random.randint(0,1)])
        await callback_query.message.edit_text(text=f"""
**{data["header"]}**
در ادامه چند متن به شما نمایش داده میشه مثل این متن

**{" ".join(f"[{char}]" for char in text)}**

شما نیاز نیست کروشه هارو تایپ کنید فقط **{text}** رو تایپ کنید
وقتی آماده بودید شروع رو بزنید
""",reply_markup=keyboard)
        
    elif data["text_format"] == "word_random":
        await callback_query.message.edit_text(text=f"""
**{data["header"]}**
در ادامه یک جمله با کلمات تصادفی که تا الان بهتون تدریس شده بهتون نمایش داده میشه سعی کنید اونهارو با دقت تایپ کنید
هرموقع آماده بودید شروع رو بزنید
""",reply_markup=keyboard)
    elif data["text_format"] == "sentence":
        await callback_query.message.edit_text(text=f"""
**{data["header"]}**
در ادامه یک جمله بهتون نمایش داده میشه سعی کنید اونرو با دقت تایپ کنید
هرموقع آماده بودید شروع رو بزنید
""",reply_markup=keyboard)



