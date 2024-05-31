import discord
from typing import Optional, Union
from redbot.core import app_commands, commands

class Banner(commands.Cog):
    """Get a user's banner."""

    @commands.hybrid_command(name="banner", description="Get a user's banner")
    @app_commands.describe(user="The user you wish to retrieve the banner of")
    @app_commands.guild_only()
    async def banner(self, ctx: commands.Context, *, user: Optional[Union[discord.Member, discord.User]]) -> None:
        """Returns a user's banner as an embed.

        The user argument can be a user mention, nickname, username, or user ID.
        Defaults to the requester when no argument is supplied.
        """

        user = user or ctx.author
        embed = discord.Embed(color=0xFFFFFF, title="Banner")

        
        try:
        # cannot get banner without fetch_user or get_user
            user = await ctx.bot.fetch_user(user.id)

            if user.banner:
                banner_url = user.banner.url
                embed.set_image(url=banner_url)

            else:
                embed.description = "This user doesn't have a banner."

        except discord.HTTPException:
            embed.description = "No banner found for this user."

        # - Detect animated banners (might need sometime) -
        #is_animated = banner_url.endswith(".gif")

        embed.set_author(name=user.display_name, icon_url=user.avatar.url)

        if ctx.channel.permissions_for(ctx.guild.me).embed_links:
            await ctx.send(embed=embed)
        else:
            await ctx.send("I do not have permission to send embeds in this channel.", ephemeral=True)

    async def red_delete_data_for_user(self, **kwargs) -> None:
        pass
