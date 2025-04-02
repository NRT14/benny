import discord
from discord.ext import commands
from discord import app_commands
import json
import datetime
import os

class OnCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="on", description="🟠 Activează pontajul")
    async def on(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        file_path = "data/pontaj_data.json"
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                json.dump({}, f)

        with open(file_path, "r") as f:
            data = json.load(f)

        if user_id in data and data[user_id].get("on", False):
            embed = discord.Embed(
                title="☂️ Pontaj deja activ",
                description="Ești deja ON. Nu uita să folosești /off la final!",
                color=discord.Colour.from_str("#FFA500")
            )
            embed.set_footer(text="Benny's Service • Designed for NRT")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        data[user_id] = {
            "on": True,
            "start": datetime.datetime.utcnow().isoformat(),
            "total": data.get(user_id, {}).get("total", 0)
        }

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

        embed = discord.Embed(
            title="☂️ Pontaj pornit cu succes",
            description="🛠️ Pontajul este activ. Spor la muncă!",
            color=discord.Colour.from_str("#FFA500")
        )
        embed.set_footer(text="Benny's Service • Designed for NRT ")
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(OnCommand(bot))