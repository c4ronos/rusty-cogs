import discord
from typing import Optional, Union
from redbot.core import app_commands, commands, Config

class Banner(commands.Cog):
    """Get a user's banner."""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=245189443860)
        default_global = {"embed_color": None}
        self.config.register_global(**default_global)


    @commands.hybrid_command(name="banner", description="Get a user's banner")
    @app_commands.describe(user="The user you wish to retrieve the banner of (optional)")
    @app_commands.guild_only()
    async def banner(self, ctx: commands.Context, *, user: Optional[Union[discord.Member, discord.User]]) -> None:
        """Returns a user's banner as an embed.

        The user argument can be a user mention, nickname, username, or user ID.
        Defaults to the requester when no argument is supplied.
        """

        user = user or ctx.author
        embed_color = await self.config.embed_color() or user.color
        embed = discord.Embed(color=embed_color, title="Banner")

        
        try:
        # cannot get banner without fetch_user or get_user
            user = await ctx.bot.fetch_user(user.id)

            if user.banner:
                banner_url = user.banner.url
                embed.set_image(url=banner_url)

                embed.set_author(name=f"{user.name} ~ {user.display_name}", icon_url=user.avatar.url)

            else:
                embed.description = "This user doesn't have a banner."

        except discord.HTTPException:
            embed.description = "No banner found for this user."

        if ctx.channel.permissions_for(ctx.guild.me).embed_links:
            await ctx.send(embed=embed)
        else:
            await ctx.send("I do not have permission to send embeds in this channel.", ephemeral=True)


    @commands.command(name="banner_embed", description="Embed color for banner (defaults to role color)")
    @commands.guild_only()
    @commands.is_owner()
    async def banner_embed(self, ctx: commands.Context, color: str) -> None:
        """Embed color for banner (defaults to role color)

        Use a hex color code or 'clear' to reset to the default color.
        """

        if color.lower() == "clear":
            await self.config.embed_color.set(None)
            await ctx.send("Embed color has been reset to default.")
        else:
            try:
                # Only accept hex (and `clear`)
                embed_color = discord.Color(int(color.lstrip("#"), 16))
                await self.config.embed_color.set(embed_color.value)
                await ctx.send(f"Embed color has been set to {color}.")
            except ValueError:
                await ctx.send("Invalid hex color code. Please provide a valid hex color code or 'clear'.")


    async def red_delete_data_for_user(self, **kwargs) -> None:
        pass
