import discord
from typing import Optional, Union, Literal
from redbot.core import app_commands, commands, Config
import aiohttp
import subprocess
import os
from io import BytesIO

class Avatar(commands.Cog):
    """Get a user's global/guild avatar in an embed, with settings to manage the embed."""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=524188088840)
        default_global = {"embed_color": None, "use_embed": True}
        self.config.register_global(**default_global)

    async def convert_apng_to_gif(self, url: str) -> BytesIO:
        async with aiohttp.ClientSession() as session, session.get(url) as resp:
            if resp.status != 200:
                return None
            img_data = await resp.read()
        
        input_file = "temp.apng"
        output_file = "temp.gif"
        
        with open(input_file, "wb") as f:
            f.write(img_data)
        
        subprocess.run([
            "ffmpeg", "-i", input_file, "-vf", "split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
            "-y", output_file
        ], check=True)
        
        with open(output_file, "rb") as f:
            gif_data = BytesIO(f.read())
        
        os.remove(input_file)
        os.remove(output_file)
        
        return gif_data

    @commands.hybrid_command(name="avatar", usage="[user] [type]")
    @app_commands.describe(user="The user you wish to retrieve the avatar of (optional)", type="Global avatar or guild avatar or avatar decoration (optional)")
    @commands.guild_only()
    async def avatar(self, ctx: commands.Context, user: Optional[Union[discord.Member, discord.User]], type: Optional[Literal["global", "guild", "deco"]]) -> None:
        """Returns a user's avatar assets as an embed. (see help)

        > optional - [user] = `@mention` / `username` / `id`
        > optional - [type] = `global` / `guild` / `deco` (default=global)
        """

        user = user or ctx.author
        embed_color = await self.config.embed_color() or user.color
        use_embed = await self.config.use_embed()

        if type is None:
            avatar_url = user.display_avatar.url
            type = "global"
        elif type.lower() == "guild":
            try:
                avatar_url = user.guild_avatar.url if user.guild_avatar else user.display_avatar.url
            except AttributeError:
                await ctx.send("Cannot access guild avatar as user is not in this guild.")
                return
        elif type.lower() == "deco":
            avatar_url = user.avatar_decoration.url if user.avatar_decoration else user.display_avatar.url
            gif_data = await self.convert_apng_to_gif(avatar_url)
            if gif_data:
                await ctx.send(file=discord.File(gif_data, filename="converted.gif"))
            else:
                await ctx.send("Failed to convert image.")
            return
        else:
            avatar_url = user.display_avatar.url

        if use_embed:
            embed = discord.Embed(color=embed_color, description=f"**[Avatar]({avatar_url})**")
            embed.set_author(name=f"{user.name} ~ {user.display_name}", icon_url=avatar_url)
            embed.set_image(url=avatar_url)

            if ctx.channel.permissions_for(ctx.guild.me).embed_links:
                await ctx.send(embed=embed)
            else:
                await ctx.send("I do not have permission to send embeds in this channel.")
        else:
            await ctx.send(avatar_url)

    @commands.group(name="avatar_embed")
    @commands.is_owner()
    @commands.guild_only()
    async def avatar_embed(self, ctx: commands.Context) -> None:
        """Avatar embed settings for bot owner.
        
        > With this, you have the ability to change embed color or disable the embed altogether.
        """
        return

    @avatar_embed.command(name="color")
    @commands.is_owner()
    @commands.guild_only()
    async def avatar_embed_color(self, ctx: commands.Context, color: str) -> None:
        """Set embed color for avatar (defaults to role color)

        > Use a hex color code or 'clear' to reset to the default color.
        """

        if color.lower() == "clear":
            await self.config.embed_color.set(None)
            await ctx.send("Embed color has been reset to default.")
        else:
            try:
                embed_color = discord.Color(int(color.lstrip("#"), 16))
                await self.config.embed_color.set(embed_color.value)
                await ctx.send(f"Embed color has been set to {color}.")
            except ValueError:
                await ctx.send("Invalid hex color code. Please provide a valid hex color code or 'clear'.")

    @avatar_embed.command(name="show")
    @commands.guild_only()
    @commands.is_owner()
    async def avatar_embed_show(self, ctx: commands.Context, show: bool) -> None:
        """Enable or disable avatar embed.

        > Use `true` to enable embed or `false` to disable embed.
        """

        await self.config.use_embed.set(show)
        await ctx.send(f"Avatar embed has been {'enabled' if show else 'disabled'}.")

    async def red_delete_data_for_user(self, **kwargs) -> None:
        pass 
