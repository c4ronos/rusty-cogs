import discord
from typing import Literal
from redbot.core import app_commands, commands


class Banana(commands.Cog):
    """Show someone your banana or eat theirs"""

    
    @commands.hybrid_command(name="banana")
    @app_commands.describe(user="The user you wish to show your banana or eat theirs", action="show or eat")
    @commands.guild_only()
    async def banana(self, ctx: commands.Context, user: discord.Member, action: Literal["show","eat"]):
        """Show someone your banana or eat theirs
        
        > Example: `banana 792305160149 show`
        """

        embed_description = "Should we be surprised? 🤔"
        embed_color = discord.Color(0xFFFF00)

        embedTitle_1 = f"🍌 `{ctx.author.display_name}` looked at their own banana.. what? ..!"
        embedTitle_2 = f"🍌 `{ctx.author.display_name}` showed `{user.display_name}` their banana..!"
        embedTitle_3 = f"🍌 `{ctx.author.display_name}` ate their own banana.. what? ..!"
        embedTitle_4 = f"🍌 `{ctx.author.display_name}` ate the banana of `{user.display_name}`..!"

        bananaShow_image = "https://i.ibb.co/jVTCHRr/banana-show.gif"
        bananaEat_image = "https://i.ibb.co/Pwm2wKW/banana-eat.gif"


        if action == "show":
            banana_image = bananaShow_image
            embed_title = embedTitle_1 if (user == ctx.author) else embedTitle_2
        else:
            banana_image = bananaEat_image
            embed_title = embedTitle_3 if (user == ctx.author) else embedTitle_4

        embed = discord.Embed(title=embed_title, description=embed_description, color=embed_color)
        embed.set_image(url=banana_image)


        await ctx.send(content=user.mention, embed=embed)
