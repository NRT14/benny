import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from datetime import datetime

class DutyCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="duty", description="Check if a user is on duty")
    async def duty(self, interaction: discord.Interaction, user: discord.Member):
        user_id = str(user.id)
        file_path = "data/pontaj_data.json"

        if not os.path.exists(file_path):
            await interaction.response.send_message("⛔ Nicio informație despre pontaj.", ephemeral=True)
            return

        with open(file_path, "r") as f:
            data = json.load(f)

        if user_id not in data or not data[user_id].get("on", False):
            await interaction.response.send_message(f"🔴 {user.display_name} este OFF.", ephemeral=True)
            return

        start_time = datetime.fromisoformat(data[user_id]["start"])
        now = datetime.utcnow()
        duration = now - start_time
        minutes = int(duration.total_seconds() / 60)
        hours = minutes // 60
        mins = minutes % 60

        await interaction.response.send_message(f"🟢 {user.display_name} este ON de {hours}h {mins}m.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(DutyCommand(bot))