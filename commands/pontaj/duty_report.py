import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class DutyReportCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="duty-report", description="📄 Raport complet cu orele tuturor")
    async def duty_report(self, interaction: discord.Interaction):
        file_path = "data/pontaj_data.json"
        if not os.path.exists(file_path):
            embed = discord.Embed(
                title="☂️ Nicio înregistrare",
                description="Nu există date de pontaj înregistrate momentan.",
                color=discord.Colour.from_str("#FFA500")
            )
            embed.set_footer(text="Benny's Service • Designed for NRT")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        with open(file_path, "r") as f:
            data = json.load(f)

        lines = []
        for user_id, info in data.items():
            total = info.get("total", 0)
            ore = total // 60
            minute = total % 60
            lines.append(f"<@{user_id}> — **{ore}h {minute}m**")

        report = "\n".join(lines) or "Nu există membri înregistrați."
        embed = discord.Embed(
            title="☂️ Raport complet pontaj",
            description=report,
            color=discord.Colour.from_str("#FFA500")
        )
        embed.set_footer(text="Benny's Service • Designed for NRT")

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(DutyReportCommand(bot))