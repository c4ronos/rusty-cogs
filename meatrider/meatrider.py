import discord
import random
from redbot.core import app_commands, commands


class MeatRider(commands.Cog):
    """Send a random meatrider image pointed at someone"""


    @commands.hybrid_command(name="meatrider")
    @app_commands.describe(user="The user who is meatriding", delete="[Optional] Whether to hide who ran the command or not")
    @commands.guild_only()
    async def meatrider(self, ctx: commands.Context, user: discord.Member, delete: bool=False):
        """Send a random meatrider image pointed at someone
        
        Example: `meatrider 829031830138 true`
        """

        urls = (
            "https://i.ibb.co/71Tg2sG/meatrider-1.jpg",
            "https://i.ibb.co/wYcgBZQ/meatrider-2.jpg",
            "https://i.ibb.co/Q8jMP02/meatrider-3.jpg",
            "https://i.ibb.co/NN0qjCj/meatrider-4.jpg",
            "https://i.ibb.co/PM7q2p8/meatrider-5.jpg",
            "https://i.ibb.co/qs5DMHs/meatrider-6.jpg",
            "https://i.ibb.co/9wVCyTy/meatrider-8.jpg",
            "https://i.ibb.co/x7jxM8H/meatrider-10.jpg",
            "https://i.ibb.co/ccML0Ks/meatrider-11.jpg",
            "https://i.ibb.co/0myvdy7/meatrider-12.jpg",
            "https://i.ibb.co/TKPRv5t/meatrider-13.jpg",
            "https://i.ibb.co/d4tkhPC/meatrider-15.jpg"
        )

        url = random.choice(urls)
        color = await ctx.embed_color()

        if user == ctx.author:
            embed = discord.Embed(title="Imagine MeatRiding yourself LMAO", color=color)
        else:
            embed = discord.Embed(title="#Stop MeatRiding", color=color)

        embed.set_image(url=url)


        if ctx.interaction:
            if delete:
                await ctx.send("Sent!", ephemeral=True)
                await ctx.channel.send(content=user.mention, embed=embed)
            else:
                await ctx.send(content=user.mention, embed=embed)

        else:
            await ctx.send(content=user.mention, embed=embed)
            if delete:
                await ctx.message.delete()
