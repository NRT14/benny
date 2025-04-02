import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()  # Încarcă variabilele din fișierul .env

TOKEN = os.getenv("TOKEN")  # Ia tokenul

# Verifică dacă a fost citit corect
if TOKEN is None:
    raise ValueError("TOKEN is missing! Check your .env file or environment variables.")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

bot.run(TOKEN)
