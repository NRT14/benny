import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

# Încarcă variabilele din .env (inclusiv tokenul botului)
load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} este online și slash commands sunt sincronizate!")

# Încarcă toate comenzile din folderul commands/pontaj/
async def load():
    for filename in os.listdir("./commands/pontaj"):
        if filename.endswith(".py"):
            await bot.load_extension(f"commands.pontaj.{filename[:-3]}")

async def main():
    await load()
    await bot.start(TOKEN)

asyncio.run(main())
