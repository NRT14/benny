import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import datetime

class HoursCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hours", description="📊 Afișează orele acumulate")
    async def hours(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        file_path = "data/pontaj_data.json"
        now = datetime.datetime.now().strftime("%H:%M")
        log_channel = interaction.client.get_channel(1355983254175486014)

        if not os.path.exists(file_path):
            embed = discord.Embed(
                title="☂️ Nicio activitate găsită",
                description="Nu ai înregistrat nicio activitate până acum.",
                color=discord.Colour.from_str("#FFA500")
            )
            embed.set_footer(text="Benny's Service • Designed for NRT")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            await log_channel.send(f"📊 /hours → {interaction.user} — fără date — {now}")
            return

        with open(file_path, "r") as f:
            data = json.load(f)

        total_minutes = data.get(user_id, {}).get("total", 0)
        hours = total_minutes // 60
        minutes = total_minutes % 60

        embed = discord.Embed(
            title="☂️ Ore acumulate",
            description=f"🕓 Ai acumulat un total de **{hours} ore și {minutes} minute**.",
            color=discord.Colour.from_str("#FFA500")
        )
        embed.set_footer(text="Benny's Service • Designed for NRT")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await log_channel.send(f"📊 /hours → {interaction.user} — {hours}h {minutes}m — {now}")

async def setup(bot):
    await bot.add_cog(HoursCommand(bot))