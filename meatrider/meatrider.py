import discord
import random
from redbot.core import app_commands, commands


class MeatRider(commands.Cog):
    """Send a random meatrider image pointed at someone"""


    @commands.hybrid_command(name="meatrider", usage="<user> [delete]")
    @app_commands.describe(user="The user who is meatriding", delete="[Optional] Whether to hide who ran the command or not")
    @commands.guild_only()
    async def meatrider(self, ctx: commands.Context, user: discord.Member, delete: bool=False):
        """Send a random meatrider image pointed at someone.
        
        > example: `meatrider @dream` / `meatrider @dream true`
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
            "https://i.ibb.co/d4tkhPC/meatrider-15.jpg",
            "https://i.ibb.co/2d8qQv1/meatrider-16.jpg",
            "https://i.ibb.co/287nX8n/meatrider-18.jpg",
            "https://i.ibb.co/q73cZ2c/meatrider-19.png",
            "https://i.ibb.co/hR7t9Qz4/meatrider-20.jpg",
            "https://i.ibb.co/Q7s11Q7H/meatrider-21.jpg"
        )

        url = random.choice(urls)
        color = await ctx.embed_color()

        if user == ctx.author:
            embed = discord.Embed(title="Imagine meatriding yourself LOL", color=color)
        else:
            embed = discord.Embed(title="#Stop meatriding", color=color)

        embed.set_image(url=url)

        # handle deletions for normal commands and app commands
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
