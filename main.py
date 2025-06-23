import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.initial_extensions = ["cogs.tickets", "cogs.welcome"]

    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)
        print("✅ Extensions chargées")

    async def on_ready(self):
        print(f"🟢 Connecté en tant que {self.user}")
        await self.tree.sync()
        print("✅ Commandes slash synchronisées")

    async def on_member_join(self, member):
        guild = member.guild
        role_names = ["Citoyens", "-----Citoyens-----"]
        for role_name in role_names:
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                await member.add_roles(role)
            else:
                print(f"⚠️ Rôle '{role_name}' non trouvé sur le serveur.")

bot = MyBot()
bot.run(os.getenv("DISCORD_TOKEN"))
