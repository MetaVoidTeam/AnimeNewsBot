"""
MIT License
Copyright (C) 2021-2022 MetaVoid (MoeZilla) 
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from pyrogram import Client, filters
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os


API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")



bot = Client(
    "AnimeNews" ,
    api_id = API_ID ,
    api_hash = API_HASH ,
    bot_token = BOT_TOKEN
)


@bot.on_message(filters.command("animenews")
async def animenews(_, message): 

    new_page = urlopen("https://myanimelist.net/news")
    soup = BeautifulSoup(new_page, "html.parser")

    AnimeNews = soup.findAll(
        "div", {"class": "news-unit clearfix rect"}
    )

    title, image, description, newlink = [], [], [], []

    for x in AnimeNews:

        text = x.findChildren("p")[0]
        a = text.find("a", href=True)
        text = a.get_text()

        newslinkx = a["href"]

        images = x.find("img")
        imagex = images["src"]

        descriptionx = x.findChildren("div", {"class": "text"})[0]

        title.append(text)
        image.append(imagex)      
        description.append(" ".join(descriptionx.text.split()))
        newlink.append(newslinkx)

    description = description
    title = title
    buttons = [[
        InlineKeyboardButton("Read More", url=f"{newlink[0]}")
    ]]

    photo = f"{image[0]}"
    
    await message.reply_photo(photo=photo, caption=f"**Title:** {title[0]}\n**Description:** {description[0]}", reply_markup=InlineKeyboardMarkup(buttons))



bot.run()
