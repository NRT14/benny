import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import datetime

class ActiveCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="active", description="🟠 👥 Vezi cine este ON acum")
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
            log_embed = discord.Embed(
                title="☂️ Log Pontaj",
                description=f"📝 {interaction.user.mention} → /active — fără fișier — {now}",
                color=discord.Colour.from_str("#FFA500")
            )
            log_embed.set_footer(text="Benny's Service • Designed for NRT")
            await log_channel.send(embed=log_embed)
            return

        with open(file_path, "r") as f:
            data = json.load(f)

        on_users = []
        for uid, val in data.items():
            if val.get("on"):
                start_time = datetime.datetime.fromisoformat(val.get("start"))
                now_time = datetime.datetime.utcnow()
                minutes_on = int((now_time - start_time).total_seconds() / 60)
                on_users.append(f"<@{uid}> — **{minutes_on}m ON**")

        if not on_users:
            embed = discord.Embed(
                title="☂️ Niciun membru ON",
                description="Toți membrii sunt OFF în acest moment.",
                color=discord.Colour.from_str("#FFA500")
            )
            embed.set_footer(text="Benny's Service • Designed for NRT")
            await interaction.response.send_message(embed=embed)
            log_embed = discord.Embed(
                title="☂️ Log Pontaj",
                description=f"📝 {interaction.user.mention} → /active — nimeni ON — {now}",
                color=discord.Colour.from_str("#FFA500")
            )
            log_embed.set_footer(text="Benny's Service • Designed for NRT")
            await log_channel.send(embed=log_embed)
            return

        embed = discord.Embed(
            title="☂️ Membri activi",
            description="✅ Următorii membri sunt ON:" + "".join(on_users),
            color=discord.Colour.from_str("#FFA500")
        )
        embed.set_footer(text="Benny's Service • Designed for NRT")
        await interaction.response.send_message(embed=embed)

        log_embed = discord.Embed(
            title="☂️ Log Pontaj",
            description=f"📝 {interaction.user.mention} → /active — {len(on_users)} membri ON — {now}",
            color=discord.Colour.from_str("#FFA500")
        )
        log_embed.set_footer(text="Benny's Service • Designed for NRT")
        await log_channel.send(embed=log_embed)

async def setup(bot):
    await bot.add_cog(ActiveCommand(bot))