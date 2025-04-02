import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import datetime

class DutyCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="duty", description="🟠 👁️ Verifică dacă ești ON sau OFF")
    async def duty(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        file_path = "data/pontaj_data.json"
        now = datetime.datetime.now().strftime("%H:%M")
        log_channel = interaction.client.get_channel(1355983254175486014)

        if not os.path.exists(file_path):
            embed = discord.Embed(
                title="☂️ Pontaj inexistent",
                description="Nu ai fost niciodată ON până acum.",
                color=discord.Colour.from_str("#FFA500")
            )
            embed.set_footer(text="Benny's Service • Designed for NRT")
            await interaction.response.send_message(embed=embed)
            log_embed = discord.Embed(
                title="☂️ Log Pontaj",
                description=f"📝 {interaction.user.mention} → /duty — fără fișier — {now}",
                color=discord.Colour.from_str("#FFA500")
            )
            log_embed.set_footer(text="Benny's Service • Designed for NRT")
            await log_channel.send(embed=log_embed)
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
        await interaction.response.send_message(embed=embed)

        log_embed = discord.Embed(
            title="☂️ Log Pontaj",
            description=f"📝 {interaction.user.mention} → /duty — {'ON' if status else 'OFF'} — {now}",
            color=discord.Colour.from_str("#FFA500")
        )
        log_embed.set_footer(text="Benny's Service • Designed for NRT")
        await log_channel.send(embed=log_embed)

async def setup(bot):
    await bot.add_cog(DutyCommand(bot))