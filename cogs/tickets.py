import discord
from discord.ext import commands

RECRUTEMENT_CHANNEL_ID = 113864693566271304768  # Remplace par l'ID de ton salon recrutements
LOGO_URL = "https://i.postimg.cc/vb07tycs/Chat-GPT-Image-22-juin-2025-22-29-02.png"  # Lien du logo

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_recruitment_message(self):
        channel = self.bot.get_channel(RECRUTEMENT_CHANNEL_ID)
        if not channel:
            print(f"❌ Salon non trouvé avec l'ID ({RECRUTEMENT_CHANNEL_ID})")
            return
        else:
            print(f"✅ Salon trouvé : {channel.name}")

        embed = discord.Embed(
            title="📩 Ouvre ton Ticket de Recrutement",
            description=(
                "Sélectionne une option ci-dessous pour postuler à un poste dans le **Groupe Osborne** :\n\n"
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

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

class TicketSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Recrutement Osborne Real Estate", value="ore", emoji="🏢"),
            discord.SelectOption(label="Recrutement Bahamas", value="bahamas", emoji="🍸"),
            discord.SelectOption(label="Demande de partenariats", value="partenariats", emoji="🤝"),
        ]
        super().__init__(placeholder="Choisissez une option de recrutement...", options=options)

    async def callback(self, interaction: discord.Interaction):
        choice = self.values[0]

        if choice == "ore":
            category_name = "Osborne Real Estate - équipe"
            role_ids = [1386403996842426570, 1386457371451160881]  # remplace avec les bons IDs
        elif choice == "bahamas":
            category_name = "Bahamas - équipe"
            role_ids = [1386403996812582882, 1386448000239812718]
        elif choice == "partenariats":
            category_name = "Relation Externes"
            role_ids = [1386463997731366779, 1386468089233624596]
        else:
            await interaction.response.send_message("❌ Erreur dans la sélection.", ephemeral=True)
            return

        # 💡 Ici tu peux créer dynamiquement un salon ou ouvrir un ticket
        await interaction.response.send_message(
            f"✅ Ticket pour **{category_name}** créé avec les rôles {role_ids} ! (code à compléter)", ephemeral=True
        )

async def setup(bot):
    print("📩 Chargement du module Ticket...")
    ticket_cog = Ticket(bot)
    await bot.add_cog(ticket_cog)
    await ticket_cog.send_recruitment_message()  # Appel direct ici

