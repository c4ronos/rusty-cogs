import discord
from redbot.core import app_commands, commands

class Banner(commands.Cog):
    """Get a user's banner."""

    @commands.hybrid_command(name="banner", description="Get a user's banner")
    @app_commands.describe(user="The user you wish to retrieve the banner of")
    @app_commands.guild_only()
    async def banner(self, ctx: commands.Context, user: discord.Member = None):
        """Returns a user's banner as an embed.

        The user argument can be a user mention, nickname, username, or user ID.
        Defaults to the requester when no argument is supplied.
        """

        user = user or ctx.author
        embed = discord.Embed(color=0xFFFFFF, description="### Banner")

        try:
            # Attempt to fetch the banner URL (may raise exceptions)
            banner_url = user.banner.url
        except discord.HTTPException:
            # Handle potential exceptions (e.g. user has no banner)
            embed.description = "No banner found for this user."
            await ctx.send(embed=embed)
            return

        # Detect animated banners (might need sometime)
        is_animated = banner_url.endswith(".gif")

        embed.set_image(url=banner_url)

        embed.set_author(name=user.display_name, icon_url=user.avatar.url)

        if ctx.channel.permissions_for(ctx.guild.me).embed_links:
            await ctx.send(embed=embed)
        else:
            await ctx.send("I do not have permission to send embeds in this channel.", ephemeral=True)

    async def red_delete_data_for_user(self, **kwargs):
        pass