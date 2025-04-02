import discord
from discord.ext import commands
from discord import app_commands
import json
import datetime
import os

class OffCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="off", description="Stop duty (pontaj)")
    async def off(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        file_path = "data/pontaj_data.json"

        if not os.path.exists(file_path):
            await interaction.response.send_message("⛔ Nu ai fost niciodată ON!", ephemeral=True)
            return

        with open(file_path, "r") as f:
            data = json.load(f)

        if user_id not in data or not data[user_id].get("on", False):
            await interaction.response.send_message("⛔ Nu ești ON acum.", ephemeral=True)
            return

        start_time = datetime.datetime.fromisoformat(data[user_id]["start"])
        end_time = datetime.datetime.utcnow()
        minutes = int((end_time - start_time).total_seconds() / 60)

        data[user_id]["total"] += minutes
        data[user_id]["on"] = False
        data[user_id].pop("start", None)

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

        hours = minutes // 60
        mins = minutes % 60
        await interaction.response.send_message(f"⏱️ Timp adăugat: {hours}h {mins}m. Pontaj oprit cu succes.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(OffCommand(bot))