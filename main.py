import discord
from discord.ext import commands
from discord import app_commands, SelectOption, Interaction
from discord.ui import View, Select

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Commandes slash synchronisées : {len(synced)}")
    except Exception as e:
        print(f"Erreur de sync : {e}")

@bot.event
async def on_member_join(member):
    # Donne les rôles
    role_names = ["Citoyens", "-----Citoyens-----"]
    for role_name in role_names:
        role = discord.utils.get(member.guild.roles, name=role_name)
        if role:
            await member.add_roles(role)

    # Message de bienvenue
    channel = discord.utils.get(member.guild.text_channels, name="📝-bienvenue")
    if channel:
        embed = discord.Embed(
            title="Bienvenue !",
            description=f"Bienvenue {member.mention} sur le serveur !",
            color=discord.Color.blue()
        )
        embed.set_image(url="https://link.to/your/banner.jpg")  # Mets ici ton URL de bannière
        await channel.send(embed=embed)


# Système de tickets
class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

class TicketSelect(Select):
    def __init__(self):
        options = [
            SelectOption(label="Recrutement Osborne Real Estate", value="osborne"),
            SelectOption(label="Recrutement Bahamas", value="bahamas"),
            SelectOption(label="Demande de Partenariat", value="partenariat")
        ]
        super().__init__(placeholder="Sélectionnez une option", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        user = interaction.user
        guild = interaction.guild

        config = {
            "osborne": {
                "cat_name": "🏢・𝗢𝗦𝗕𝗢𝗥𝗡𝗘 𝗥𝗘𝗔𝗟 𝗘𝗦𝗧𝗔𝗧𝗘 — 𝗘𝗤𝗨𝗜𝗣𝗘",
                "allowed_roles": ["PDG", "Direction"]
            },
            "bahamas": {
                "cat_name": "🍸・𝗕𝗔𝗛𝗔𝗠𝗔𝗦 — 𝗘𝗤𝗨𝗜𝗣𝗘",
                "allowed_roles": ["PDG", "Direction"]
            },
            "partenariat": {
                "cat_name": "🤝・𝗥𝗲𝗹𝗮𝘁𝗶𝗼𝗻𝘀 𝗘𝘅𝘁𝗲𝗿𝗻𝗲𝘀",
                "allowed_roles": ["Direction Général", "Famille"]
            }
        }

        data = config[self.values[0]]
        category = discord.utils.get(guild.categories, name=data["cat_name"])
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }

        for role_name in data["allowed_roles"]:
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True)

        channel = await guild.create_text_channel(f"ticket-{user.name}", category=category, overwrites=overwrites)
        await interaction.response.send_message(f"Ticket créé dans {channel.mention}", ephemeral=True)

# Slash command pour setup le menu
@bot.tree.command(name="setup_ticket", description="Affiche le menu de tickets")
async def setup_ticket(interaction: discord.Interaction):
    await interaction.channel.send("Choisissez une option ci-dessous :", view=TicketView())
    await interaction.response.send_message("Menu envoyé", ephemeral=True)

bot.run("DISCORD_TOKEN")  # 🔴 Mets ici ton token
