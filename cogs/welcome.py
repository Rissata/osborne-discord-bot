import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Module Welcome prêt.")

        channel_id = 1386469270778675220  # ← Remplace par l'ID du salon 'Bienvenue'
        banner_url = "https://cdn.discordapp.com/attachments/958369489492258876/1386750033466097855/ChatGPT_Image_22_juin_2025_22_29_02.png?ex=685ad71c&is=6859859c&hm=dee11832d64d12e76e678c34dcf7b8319f9a0634e5c7eac4f53cc65cb6941f34&"  # ← Remplace par l'URL de ta bannière

        channel = self.bot.get_channel(channel_id)
        if channel:
            embed = discord.Embed(
                title="# Bienvenue sur le serveur du Groupe Osborne",
                description=(
                    "## 🎩 Le Groupe Osborne regroupe nos entreprises civiles et institutions familiales.\n\n"
                    "## 🧾 Vous trouverez ici des services de qualité, une équipe compétente et une vision ambitieuse pour San Andreas.\n"
                    "## 📬 En cas de besoin, utilisez les tickets correspondants à vos demandes."
                ),
                color=0x3498db
            )
            embed.set_image(url=banner_url)
            embed.set_footer(text="### Nous vous souhaitons la bienvenue.")

            await channel.purge(limit=10)
            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Welcome(bot))
