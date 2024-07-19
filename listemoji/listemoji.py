import discord
import time
from redbot.core import commands, checks
from redbot.core.utils.chat_formatting import pagify

__author__ = ["kennnyshiwa", "rusty-man"]


class ListEmoji(commands.Cog):
    """List all available emojis in a server"""

    async def red_delete_data_for_user(self, **kwargs):
        """ Nothing to delete """
        return
    

    @commands.command()
    @commands.guild_only()
    @checks.has_permissions(manage_emojis=True)
    async def listemoji(self, ctx: commands.Context, ids: bool = False):
        """Lists all available emojis in a server, perfect for an emoji channel"""

        if not ids:
            text = "\n".join(
                [
                    f"{emoji} ⟶ `:{emoji.name}:`" for emoji in ctx.guild.emojis
                ]
            )
        else:
            text = "\n".join(
                [
                    f"{emoji} ⟶ `<{'a' if emoji.animated else ''}:{emoji.name}:{emoji.id}>`"
                    for emoji in ctx.guild.emojis
                ]
            )
        
        # separate title to allow for its deletion
        await ctx.send(f"Emojis for: **{ctx.guild.name}**\n_ _")

        for page in pagify(text):
            time.sleep(0.5)             # prevent rate limit in servers with lots of emojis
            await ctx.send(page)
