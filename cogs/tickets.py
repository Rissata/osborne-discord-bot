import discord
from discord.ext import commands

RECRUTEMENT_CHANNEL_ID = 1386469356271304768  # ID de 📩・recrutements
LOGO_URL = "https://i.postimg.cc/vb07tycS/Chat-GPT-Image-22-juin-2025-22-29-02.png"  # URL du logo

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Module Ticket prêt.")

    channel = self.bot.get_channel(RECRUTEMENT_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="🎟️ Ouvre ton Ticket de Recrutement",
            description=(
                "Sélectionne une option ci-dessous pour postuler à un poste dans le **Groupe Osborne** :\n\n"
                "🏠 **Osborne Real Estate**\n"
                "🍹 **Bahamas**\n"
                "🤝 **Demande de partenariat**"
            ),
            color=0x2F3136
        )
        embed.set_thumbnail(url=LOGO_URL)
        embed.set_footer(text="Groupe Osborne • Vice City")

        view = TicketView()
        await channel.purge(limit=5)
        await channel.send(embed=embed, view=view)

    @discord.ui.select(
        placeholder="Choisissez une option de recrutement...",
        options=[
            discord.SelectOption(label="Recrutement Osborne Real Estate", value="ore", emoji="🧱"),
            discord.SelectOption(label="Recrutement Bahamas", value="bahamas", emoji="🍸"),
            discord.SelectOption(label="Demande de partenariats", value="partenariats", emoji="🤝")
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        choice = select.values[0]

        if choice == "ore":
            category_name = "Osborne Real Estate - Équipe"
            role_ids = [111, 222]  # Remplace par les vrais ID des rôles ORE
        elif choice == "bahamas":
            category_name = "Bahamas - Équipe"
            role_ids = [333, 444]  # Remplace par les vrais ID des rôles Bahamas
        elif choice == "partenariats":
            category_name = "Relation Externes"
            role_ids = [555, 666]  # Remplace par les vrais ID des rôles partenariat
        else:
            await interaction.response.send_message("❌ Erreur dans la sélection.", ephemeral=True)
            return

        guild = interaction.guild
        category = discord.u
