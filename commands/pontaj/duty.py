import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class DutyCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="duty", description="📍 Verifică dacă ești ON sau OFF")
    async def duty(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        file_path = "data/pontaj_data.json"

        if not os.path.exists(file_path):
            embed = discord.Embed(
                title="☂️ Pontaj inexistent",
                description="Nu ai fost niciodată ON până acum.",
                color=discord.Colour.from_str("#FFA500")
            )
            embed.set_footer(text="Benny's Service • Designed for NRT")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        with open(file_path, "r") as f:
            data = json.load(f)

        status = data.get(user_id, {}).get("on", False)
        embed = discord.Embed(
            title="☂️ Status pontaj",
            description=f"🔘 Ești {'🟢 ON' if status else '🔴 OFF'} în acest moment.",
            color=discord.Colour.from_str("#FFA500")
        )
        embed.set_footer(text="Benny's Service • Designed for NRT")
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(DutyCommand(bot))