import discord
from discord.ext import commands
from discord import app_commands
import json
import datetime
import os
import pytz

class OnCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="on", description="🟠 Activează pontajul")
    async def on(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=False, ephemeral=False)  # Ascunde inputul și face outputul public

        user_id = str(interaction.user.id)
        file_path = "data/pontaj_data.json"
        log_channel = interaction.client.get_channel(1355983254175486014)
        garage_channel = interaction.client.get_channel(1355951493458427985)  # canal BENNY'S-GARAGE

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
            await garage_channel.send(embed=embed)
            return

        # Ora în funcție de regiunea utilizatorului (fallback România)
        user_time = datetime.datetime.now(datetime.timezone.utc).astimezone(pytz.timezone("Europe/Bucharest"))
        ora = user_time.strftime("%H:%M")

        data[user_id] = {
            "on": True,
            "start": datetime.datetime.utcnow().isoformat(),
            "total": data.get(user_id, {}).get("total", 0)
        }

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

        embed = discord.Embed(
            title="☂️ Începere pontaj",
            description=f"🟢 {interaction.user.mention} a intrat pe pontaj la {ora}.",
            color=discord.Colour.from_str("#FFA500")
        )
        embed.set_footer(text="Benny's Service • Designed for NRT")
        await garage_channel.send(embed=embed)

        log_embed = discord.Embed(
            title="☂️ Log Pontaj",
            description=f"📝 {interaction.user.mention} → /on — ora {ora}",
            color=discord.Colour.from_str("#FFA500")
        )
        log_embed.set_footer(text="Benny's Service • Designed for NRT")
        await log_channel.send(embed=log_embed)

async def setup(bot):
    await bot.add_cog(OnCommand(bot))