import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class ActiveCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="active", description="Show all users currently on duty")
    async def active(self, interaction: discord.Interaction):
        file_path = "data/pontaj_data.json"
        if not os.path.exists(file_path):
            await interaction.response.send_message("⚠️ Nicio activitate ON salvată.", ephemeral=True)
            return

        with open(file_path, "r") as f:
            data = json.load(f)

        active_users = []
        for user_id, info in data.items():
            if info.get("on"):
                user = await self.bot.fetch_user(int(user_id))
                active_users.append(user.mention)

        if not active_users:
            await interaction.response.send_message("🔴 Nimeni nu este ON acum.", ephemeral=True)
            return

        await interaction.response.send_message(f"🟢 Utilizatori activi: {', '.join(active_users)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ActiveCommand(bot))