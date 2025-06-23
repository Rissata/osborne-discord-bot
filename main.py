import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

initial_extensions = ["cogs.welcome", "cogs.tickets"]

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.initial_extensions = initial_extensions

    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)
        print("✅ Extensions chargées")

    async def on_ready(self):
        print(f"🤖 Connecté en tant que {self.user}")
        await self.tree.sync()
        print("✅ Commandes slash synchronisées")

        # Envoi du message de recrutement automatiquement
        from cogs.tickets import Ticket
        ticket_cog = Ticket(self)
        await ticket_cog.send_recruitment_message()

    async def on_member_join(self, member):
        guild = member.guild
        role_names = ["Citoyens", "------Citoyens-----"]
        for role_name in role_names:
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                await member.add_roles(role)
            else:
                print(f"⚠️ Rôle '{role_name}' non trouvé sur le serveur.")

bot = MyBot()
bot.run(os.getenv("DISCORD_TOKEN"))
