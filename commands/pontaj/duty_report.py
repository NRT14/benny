import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from datetime import datetime

CHANNEL_ID = 1106207655002898514  # Conducere Service

class DutyReport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="duty-report", description="Raport pontaj zilnic")
    async def duty_report(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.manage_guild:
            await interaction.response.send_message("⛔ Nu ai acces la această comandă.", ephemeral=True)
            return

        file_path = "data/pontaj_data.json"
        if not os.path.exists(file_path):
            await interaction.response.send_message("⚠️ Nu există date salvate.", ephemeral=True)
            return

        with open(file_path, "r") as f:
            data = json.load(f)

        embed = discord.Embed(title="📋 Raport Pontaj Zilnic", color=discord.Color.orange())

        for user_id, info in data.items():
            user = await self.bot.fetch_user(int(user_id))
            total = info.get("total", 0)
            hours = total // 60
            mins = total % 60
            status = "🟢 ON" if info.get("on") else "🔴 OFF"
            embed.add_field(name=user.display_name, value=f"{status} – {hours}h {mins}m", inline=False)

        channel = self.bot.get_channel(CHANNEL_ID)
        await channel.send(embed=embed)
        await interaction.response.send_message("✅ Raport trimis cu succes.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(DutyReport(bot))