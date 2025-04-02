import discord
from discord.ext import commands
from discord import app_commands
import json
import datetime
import os

class OffCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="off", description="🔻 Oprește pontajul")
    async def off(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        file_path = "data/pontaj_data.json"

        if not os.path.exists(file_path):
            embed = discord.Embed(
                title="☂️ Nu ai fost niciodată ON!",
                description="Încearcă să folosești comanda /on mai întâi.",
                color=discord.Colour.from_str("#FFA500")
            )
            embed.set_footer(text="Benny's Service • Designed for NRT")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        with open(file_path, "r") as f:
            data = json.load(f)

        if user_id not in data or not data[user_id].get("on", False):
            embed = discord.Embed(
                title="☂️ Nu ești ON acum",
                description="Folosirea comenzii /off necesită să fii ON.",
                color=discord.Colour.from_str("#FFA500")
            )
            embed.set_footer(text="Benny's Service • Designed for NRT")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        start_time = datetime.datetime.fromisoformat(data[user_id]["start"])
        end_time = datetime.datetime.utcnow()
        minutes = int((end_time - start_time).total_seconds() / 60)

        data[user_id]["on"] = False
        data[user_id]["total"] += minutes

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

        embed = discord.Embed(
            title="☂️ Pontaj oprit cu succes",
            description=f"🕒 Ai acumulat {minutes} minute în această sesiune.",
            color=discord.Colour.from_str("#FFA500")
        )
        embed.set_footer(text="Benny's Service • Designed for NRT")
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(OffCommand(bot))