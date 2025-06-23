import discord
from discord import app_commands
from discord.ext import commands

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Module Ticket prêt.")

    @app_commands.command(name="recrutement", description="Ouvre un ticket de recrutement.")
    async def open_ticket(self, interaction: discord.Interaction):
        view = TicketView()
        await interaction.response.send_message("Choisissez une option de recrutement :", view=view, ephemeral=True)


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        placeholder="Sélectionnez une option...",
        options=[
            discord.SelectOption(label="Recrutement Osborne Real Estate", value="ore"),
            discord.SelectOption(label="Recrutement Bahamas", value="bahamas"),
            discord.SelectOption(label="Demande de partenariats", value="partenariats"),
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        choice = select.values[0]

        if choice == "ore":
            category_name = "Osborne Real Estate - Équipe"
            role_ids = [1386443996842426570, 1386457473145110688]  # ← Remplace par les vrais ID des rôles PDG & direction ORE

        elif choice == "bahamas":
            category_name = "Bahamas - Équipe"
            role_ids = [1386443996871528582, 1386444000239812718]  # ← Remplace par les vrais ID des rôles PDG & direction Bahamas

        elif choice == "partenariats":
            category_name = "Relation Externes"
            role_ids = [1386443997731360779, 1386460894233624596]  # ← Remplace par les ID famille & direction générale

        else:
            await interaction.response.send_message("❌ Erreur dans la sélection.", ephemeral=True)
            return

        guild = interaction.guild
        category = discord.utils.get(guild.categories, name=category_name)

        if not category:
            await interaction.response.send_message("❌ Catégorie introuvable.", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        for role_id in role_ids:
            role = guild.get_role(role_id)
            if role:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        ticket_channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=category,
            overwrites=overwrites,
            topic=f"Ticket ouvert par {interaction.user.display_name}"
        )

        await ticket_channel.send(f"🎫 Ticket créé par {interaction.user.mention} — merci de patienter.")
        await interaction.response.send_message("✅ Ticket créé avec succès !", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Ticket(bot))
