from collections import defaultdict
from pyrogram import Client,filters,enums
from pyrogram.types import Message , ReplyKeyboardMarkup , ReplyKeyboardRemove , InlineKeyboardMarkup , InlineKeyboardButton , CallbackQuery , KeyboardButton
from .functions import *
from .levelproccess import *
import random
import json

async def pre_proccess(client, callback_query, level):
    ...

async def start_level(client, message, level,stage):
    print(level,stage)
    data = {}
    with open("plugins/teachpath.json","r",encoding="utf-8") as file:
        data = json.load(file)
    
    data = data[level]

    if data["text_format"] == "word":
        keyboard = InlineKeyboardMarkup([
               [InlineKeyboardButton("برگشت", callback_data="stoplesson")]
               ])

        words = list(data["text"])
        text = "".join(words[random.randint(0,1)])+"".join(words[random.randint(0,1)])+"".join(words[random.randint(0,1)])+"".join(words[random.randint(0,1)])
        text_show = " ".join(f"[{char}]" for char in text)
        if stage == "0":
            await message.edit_text(text=f"**{text_show}**",reply_markup=ReplyKeyboardRemove())
        elif stage == "5":
            await message.reply_text(text=f"**awli**")
        else:
            await message.reply_text(text=f"**{text_show}**")


async def begin_level(client, callback_query, level):
    data = {}
    with open("plugins/teachpath.json","r",encoding="utf-8") as file:
        data = json.load(file)
    
    data = data[level]

    if data["text_format"] == "word":
        keyboard = InlineKeyboardMarkup([
               [InlineKeyboardButton("شروع", callback_data="start")],
               [InlineKeyboardButton("برگشت", callback_data="stop")]
               ])

        words = list(data["text"])
        text = "".join(words[random.randint(0,1)])+"".join(words[random.randint(0,1)])+"".join(words[random.randint(0,1)])+"".join(words[random.randint(0,1)])
        print(text)
        text_show = " ".join(f"[{char}]" for char in text)

        await callback_query.message.edit_text(text=f"در ادامه چند متن به شما نمایش داده میشه مثل این متن\n\n**{" ".join(f"[{char}]" for char in text)}**\n\nشما نیاز نیست کروشه هارو تایپ کنید فقط **{text}** رو تایپ کنید\nوقتی آماده بودید شروع رو بزنید",reply_markup=keyboard)

    




