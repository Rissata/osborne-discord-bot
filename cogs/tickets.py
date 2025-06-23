import discord
from discord.ext import commands

RECRUTEMENT_CHANNEL_ID = 1386469356271380478  # ID de 📥・recrutements
LOGO_URL = "https://i.postimg.cc/vb07tysc/Chat-GPT-Image-22-juin-2025-22-29-02.png"  # URL du logo

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Module Ticket prêt.")

        channel = self.bot.get_channel(RECRUTEMENT_CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                title="📥 Ouvre ton Ticket de Recrutement",
                description=(
                    "👋 Sélectionne une option ci-dessous pour postuler à un poste dans le **Groupe Osborne** :\n\n"
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
            discord.SelectOption(label="Demande de partenariats", value="partenariats", emoji="🤝")
        ]
        super().__init__(placeholder="Choisissez une option de recrutement...", options=options)

    async def callback(self, interaction: discord.Interaction):
        choice = self.values[0]

        if choice == "ore":
            category_name = "Osborne Real Estate - équipe"
            role_ids = [111, 222]  # Remplace par les vrais IDs
        elif choice == "bahamas":
            category_name = "Bahamas - Équipe"
            role_ids = [333, 444]  # Remplace par les vrais IDs
        elif choice == "partenariats":
            category_name = "Relation Externes"
            role_ids = [555, 666]  # Remplace par les vrais IDs
        else:
            await interaction.response.send_message("❌ Erreur dans la sélection.", ephemeral=True)
            return

        await interaction.response.send_message(
            f"🎟️ Création de ton ticket dans la catégorie **{category_name}** en cours...", ephemeral=True
        )
        # Tu peux ajouter ici la logique de création du ticket

async def setup(bot):
    await bot.add_cog(Ticket(bot))

