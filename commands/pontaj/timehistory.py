import discord
from discord.ext import commands
from discord import app_commands
import json
import datetime
import os

class TimeHistoryCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="timehistory", description="📅 Istoric ore pentru un membru")
    @app_commands.describe(user="Membrul pentru care vrei să vezi istoricul")
    async def timehistory(self, interaction: discord.Interaction, user: discord.User):
        user_id = str(user.id)
        file_path = "data/pontaj_data.json"

        if not os.path.exists(file_path):
            embed = discord.Embed(
                title="☂️ Fără date disponibile",
                description="Nu există înregistrări pentru acest membru.",
                color=discord.Colour.from_str("#FFA500")
            )
            embed.set_footer(text="Benny's Service • Designed for NRT")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        with open(file_path, "r") as f:
            data = json.load(f)

        total = data.get(user_id, {}).get("total", 0)
        if total == 0:
            message = f"<@{user_id}> nu are nicio oră înregistrată."
        else:
            ore = total // 60
            minute = total % 60
            message = f"<@{user_id}> a acumulat **{ore} ore și {minute} minute** în total."

        embed = discord.Embed(
            title="☂️ Istoric pontaj membru",
            description=message,
            color=discord.Colour.from_str("#FFA500")
        )
        embed.set_footer(text="Benny's Service • Designed for NRT")
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(TimeHistoryCommand(bot))