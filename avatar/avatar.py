import discord
from typing import Optional, Union
from redbot.core import app_commands, commands

class Avatar(commands.Cog):
    """Get a user's avatar."""

    @commands.hybrid_command(name="avatar", description="Get a user's avatar")
    @app_commands.describe(user="The user you wish to retrieve the avatar of (optional)")
    @app_commands.guild_only()
    async def avatar(self, ctx: commands.Context, *, user: Optional[Union[discord.Member, discord.User]]) -> None:
        """Returns a user's avatar as an embed.

        The user argument can be a user mention, nickname, username, or user ID.
        Defaults to the requester when no argument is supplied.
        """

        user = user or ctx.author
        embed = discord.Embed(color=await ctx.embed_color(), title="Avatar")

        try:
            # Attempt to fetch the avatar URL
            avatar_url = user.avatar.url
        except discord.HTTPException:
            # Handle potential exceptions
            embed.description = "No avatar found for this user."
            await ctx.send(embed=embed)
            return

        # - Detect animated banners (might need sometime) -
        #is_animated = avatar_url.endswith(".gif")

        embed.set_image(url=avatar_url)

        embed.set_author(name=user.display_name, icon_url=user.avatar.url)

        if ctx.channel.permissions_for(ctx.guild.me).embed_links:
            await ctx.send(embed=embed)
        else:
            await ctx.send("I do not have permission to send embeds in this channel.", ephemeral=True)

    async def red_delete_data_for_user(self, **kwargs) -> None:
	    pass
