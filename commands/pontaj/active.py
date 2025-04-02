import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import datetime

class ActiveCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="active", description="👥 Vezi cine este ON acum")
    async def active(self, interaction: discord.Interaction):
        file_path = "data/pontaj_data.json"
        now = datetime.datetime.now().strftime("%H:%M")
        log_channel = interaction.client.get_channel(1355983254175486014)

        if not os.path.exists(file_path):
            embed = discord.Embed(
                title="☂️ Niciun pontaj activ",
                description="Nu există date înregistrate momentan.",
                color=discord.Colour.from_str("#FFA500")
            )
            embed.set_footer(text="Benny's Service • Designed for NRT")
            await interaction.response.send_message(embed=embed)
            await log_channel.send(f"👥 /active → {interaction.user} — fără fișier — {now}")
            return

        with open(file_path, "r") as f:
            data = json.load(f)

        on_users = [f"<@{uid}>" for uid, val in data.items() if val.get("on")]
        if not on_users:
            embed = discord.Embed(
                title="☂️ Niciun membru ON",
                description="Toți membrii sunt OFF în acest moment.",
                color=discord.Colour.from_str("#FFA500")
            )
            embed.set_footer(text="Benny's Service • Designed for NRT")
            await interaction.response.send_message(embed=embed)
            await log_channel.send(f"👥 /active → {interaction.user} — nimeni ON — {now}")
            return

        embed = discord.Embed(
            title="☂️ Membri activi",
            description="✅ Următorii membri sunt ON:\n" + "\n".join(on_users),
            color=discord.Colour.from_str("#FFA500")
        )
        embed.set_footer(text="Benny's Service • Designed for NRT")
        await interaction.response.send_message(embed=embed)
        await log_channel.send(f"👥 /active → {interaction.user} — {len(on_users)} membri ON — {now}")

async def setup(bot):
    await bot.add_cog(ActiveCommand(bot))