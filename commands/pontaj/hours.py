import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class HoursCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hours", description="Show your total hours")
    async def hours(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        file_path = "data/pontaj_data.json"

        if not os.path.exists(file_path):
            await interaction.response.send_message("⛔ Nu ai ore salvate.", ephemeral=True)
            return

        with open(file_path, "r") as f:
            data = json.load(f)

        total = data.get(user_id, {}).get("total", 0)
        hours = total // 60
        mins = total % 60

        await interaction.response.send_message(f"🕒 Ai acumulat: {hours}h {mins}m.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(HoursCommand(bot))