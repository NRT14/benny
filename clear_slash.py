import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Conectat ca {bot.user}")
    
    # Șterge comenzile globale
    await bot.tree.sync()  # sincronizează ce are deja
    await bot.tree.clear_commands(guild=None)  # șterge toate comenzile globale
    await bot.tree.sync()  # aplică ștergerea

    print("✅ Comenzile globale au fost șterse.")
    await bot.close()

asyncio.run(bot.start(TOKEN))
