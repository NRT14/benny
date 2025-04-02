import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} este online și slash commands sunt sincronizate!")
    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} comenzi slash au fost sincronizate.")
    except Exception as e:
        print(f"❌ Eroare la sincronizarea comenzilor: {e}")

async def load():
    for folder in os.listdir("commands"):
        for filename in os.listdir(f"commands/{folder}"):
            if filename.endswith(".py"):
                await bot.load_extension(f"commands.{folder}.{filename[:-3]}")

async def main():
    await load()
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
