import discord
from discord.ext import commands
import pytesseract
from PIL import Image
import requests
from io import BytesIO
import os
from flask import Flask
import threading

# ---- KEEP ALIVE (Replit + UptimeRobot) ----
app = Flask('')


@app.route('/')
def home():
    return "Futok fasz"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = threading.Thread(target=run)
    t.start()


# ---- DISCORD BOT ----
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# IDE ÍRD BE a role ID-t és a channel ID-t
VERIFY_CHANNEL_ID = 1404392228981571634  # ide a verify szoba ID
ROLE_ID = 1396795922070896772  # ide a rang ID amit adni szeretnél


@bot.event
async def on_ready():
    print(f"Bejelentkezve mint: {bot.user}")


@bot.event
async def on_message(message):
    if message.channel.id != VERIFY_CHANNEL_ID:
        return

    if len(message.attachments) > 0:  # ha képet küldtek
        for attachment in message.attachments:
            if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg")):
                response = requests.get(attachment.url)
                img = Image.open(BytesIO(response.content))

                text = pytesseract.image_to_string(img, lang="eng+hun")
                print("Felismert szöveg:", text)

                if "Feliratkozva" in text:
                    role = message.guild.get_role(ROLE_ID)
                    if role:
                        await message.author.add_roles(role)
                        await message.channel.send(
                            f" {message.author.mention} grat a rangho ocs!")
                else:
                    await message.channel.send(
                        f" {message.author.mention}, anyad megrakom, iratkozza fe!"
                    )

    await bot.process_commands(message)


# Keep bot alive
keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
