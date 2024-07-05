import discord
from typing import Optional, Union
from redbot.core import app_commands, commands, Config

class Banner(commands.Cog):
    """Get a user's banner."""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=245189443860)
        default_global = {"embed_color": None, "use_embed": True}
        self.config.register_global(**default_global)

    @commands.hybrid_command(name="banner", description="Get a user's banner")
    @app_commands.describe(user="The user you wish to retrieve the banner of (optional)")
    @app_commands.guild_only()
    async def banner(self, ctx: commands.Context, user: Optional[Union[discord.Member, discord.User]] = None) -> None:
        """Returns a user's banner as an embed.

        The user argument can be a user mention, nickname, username, or user ID.
        Defaults to the requester when no argument is supplied.
        """

        user = user or ctx.author
        embed_color = await self.config.embed_color() or user.color
        use_embed = await self.config.use_embed()

        try:
            # cannot get banner without fetch_user or get_user
            user = await ctx.bot.fetch_user(user.id)
            banner_url = user.banner.url if user.banner else None

            if use_embed:
                embed = discord.Embed(color=embed_color, title="Banner")
                if banner_url:
                    embed.set_image(url=banner_url)
                    embed.set_author(name=f"{user.name} ~ {user.display_name}", icon_url=user.avatar.url)
                else:
                    embed.description = "This user doesn't have a banner."

                if ctx.channel.permissions_for(ctx.guild.me).embed_links:
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("I do not have permission to send embeds in this channel.", ephemeral=True)
            else:
                await ctx.send(banner_url or "This user doesn't have a banner.")

        except discord.HTTPException:
            if use_embed:
                embed = discord.Embed(color=embed_color, description="No banner found for this user.")
                await ctx.send(embed=embed)
            else:
                await ctx.send("No banner found for this user.")

    @commands.group(name="banner_embed", description="Banner embed settings for bot owner")
    @commands.guild_only()
    @commands.is_owner()
    async def banner_embed(self, ctx: commands.Context) -> None:
        """Banner embed settings."""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @banner_embed.command(name="color", description="Set embed color for banner (defaults to role color)")
    @commands.guild_only()
    @commands.is_owner()
    async def banner_embed_color(self, ctx: commands.Context, color: str) -> None:
        """Set embed color for banner (defaults to role color)

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

    @banner_embed.command(name="show", description="Enable or disable banner embed")
    @commands.guild_only()
    @commands.is_owner()
    async def banner_embed_show(self, ctx: commands.Context, show: bool) -> None:
        """Enable or disable banner embed.

        Use `true` to enable embed or `false` to disable embed.
        """

        await self.config.use_embed.set(show)
        await ctx.send(f"Banner embed has been {'enabled' if show else 'disabled'}.")

    async def red_delete_data_for_user(self, **kwargs) -> None:
        pass
