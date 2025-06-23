import discord
from discord.ext import commands

RECRUTEMENT_CHANNEL_ID = 1386403956271340678  # ID de ton salon recrutements
LOGO_URL = "https://i.postimg.cc/vb07tycs/Chat-GPT-Image-22-juin-2025-22-29-02.png"

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_recruitment_message(self):
        channel = self.bot.get_channel(RECRUTEMENT_CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                title="📩 Ouvre ton Ticket de Recrutement",
                description=(
                    "📌 Sélectionne une option ci-dessous pour postuler à un poste dans le **Groupe Osborne** :\n\n"
                    "🏢 **Osborne Real Estate**\n"
                    "🍸 **Bahamas**\n"
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
            discord.SelectOption(label="Recrutement Osborne Real Estate", value="ore", emoji="🏢"),
            discord.SelectOption(label="Recrutement Bahamas", value="bahamas", emoji="🍸"),
            discord.SelectOption(label="Demande de partenariats", value="partenariats", emoji="🤝"),
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        choice = select.values[0]

        if choice == "ore":
            category_name = "Osborne Real Estate - équipe"
            role_ids = [111, 222]  # Remplace par les bons rôles
        elif choice == "bahamas":
            category_name = "Bahamas - Équipe"
            role_ids = [333, 444]
        elif choice == "partenariats":
            category_name = "Relation Externes"
            role_ids = [555, 666]
        else:
            await interaction.response.send_message("❌ Erreur dans la sélection.", ephemeral=True)
            return

        # Crée ton ticket ici...

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Ticket.select_callback)

async def setup(bot):
    ticket_cog = Ticket(bot)
    await bot.add_cog(ticket_cog)
    await ticket_cog.send_recruitment_message()
