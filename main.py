import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")

@bot.event
async def on_member_join(member):
    guild = member.guild

    role_names = ["Citoyens", "-----Citoyens-----"]
    
    for role_name in role_names:
        role = discord.utils.get(guild.roles, name=role_name)
        if role:
            await member.add_roles(role)
        else:
            print(f"⚠️ Rôle '{role_name}' non trouvé sur le serveur.")


bot.run(os.getenv("DISCORD_TOKEN"))
