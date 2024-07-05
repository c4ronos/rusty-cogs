import discord
from typing import Optional, Union
from redbot.core import app_commands, commands, Config

class Avatar(commands.Cog):
    """Get a user's avatar."""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=524188088840)
        default_global = {"embed_color": None}
        self.config.register_global(**default_global)

    @commands.hybrid_command(name="avatar", description="Get a user's avatar")
    @app_commands.describe(user="The user you wish to retrieve the avatar of (optional)")
    @app_commands.describe(type="Whether to return global avatar or guild (optional)")
    @app_commands.guild_only()
    async def avatar(self, ctx: commands.Context, user: Optional[Union[discord.Member, discord.User]] = None, type: Optional[str] = None) -> None:
        """Returns a user's global/guild avatar as an embed.

        > The user argument can be a user mention, nickname, username, or user ID. (optional)
        > The type argument can be either `global` or `guild` (defaults to guild).
        """

        type = type or "guild"

        if type.lower() not in ["global", "guild"]:
            await ctx.send("Invalid avatar type. Please use `global` or `guild` (or nothing).")
            return

        user = user or ctx.author
        embed_color = await self.config.embed_color() or user.color
        embed = discord.Embed(color=embed_color, title="Avatar")

        try:
            avatar_url = user.guild_avatar.url if type.lower() == "guild" and user.guild_avatar else user.avatar.url

            embed.set_author(name=f"{user.name} ~ {user.display_name}", icon_url=avatar_url)
            embed.set_image(url=avatar_url)

        except discord.HTTPException:
            embed.description = "No avatar found for this user."
            await ctx.send(embed=embed)
            return

        if ctx.channel.permissions_for(ctx.guild.me).embed_links:
            await ctx.send(embed=embed)
        else:
            await ctx.send("I do not have permission to send embeds in this channel.", ephemeral=True)


    @commands.command(name="avatar_embed", description="Embed color for avatar (defaults to role color)")
    @commands.guild_only()
    @commands.is_owner()
    async def avatar_embed(self, ctx: commands.Context, color: str) -> None:
        """Embed color for avatar (defaults to role color)

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
