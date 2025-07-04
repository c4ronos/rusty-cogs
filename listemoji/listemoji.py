import discord
import time
from redbot.core import app_commands, commands
from redbot.core.utils.chat_formatting import pagify

class ListEmoji(commands.Cog):
    """List all available emojis in a server"""

    async def red_delete_data_for_user(self, **kwargs):
        """ Nothing to delete """
        return
    

    @commands.hybrid_command(name="listemoji", usage="[ids=false]")
    @app_commands.describe(ids="whether to send emoji name+id (true) or only emoji name (false)")
    @commands.has_permissions(manage_emojis=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    async def listemoji(self, ctx: commands.Context, ids: bool = False):
        """Lists all available emojis in a server, perfect for an emoji channel.
        
        > Use `listemoji` to display the emojis as {emoji} → {emoji_name}
        > Use `listemoji true` to display the emojis as {emoji} → {emoji_name+id}
        """

        if not ids:
            text = "\n".join(
                [
                    f"{emoji} [:{emoji.name}:](<{emoji.url}>)" for emoji in ctx.guild.emojis
                ]
            )
        else:
            text = "\n".join(
                [
                    f"{emoji} `<{'a' if emoji.animated else ''}:{emoji.name}:{emoji.id}>`"
                    for emoji in ctx.guild.emojis
                ]
            )

        if ctx.interaction:
            await ctx.send("Sent!", ephemeral=True)
        # separate title to allow for its deletion
        await ctx.channel.send(f"Emojis for: **{ctx.guild.name}**\n_ _")

        for page in pagify(text):
            time.sleep(0.5)             # prevent rate limit in servers with lots of emojis
            if ctx.interaction:
                await ctx.channel.send(page)
            else:
                await ctx.send(page)
