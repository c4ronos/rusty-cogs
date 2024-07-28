import discord
from redbot.core import commands, app_commands
from typing import Optional

class Echo(commands.Cog):
    """Makes the bot say something in the specified channel."""

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="echo")
    @commands.has_permissions(administrator=True)
    @app_commands.describe(message="Input Message", channel="Input Channel")
    @commands.guild_only()
    async def echo(self, ctx: commands.Context, channel: Optional[discord.TextChannel] = None, *, message: str):
        """Makes the bot say something in the specified channel.
        
        - [documentation](<https://github.com/rusty-man/rusty-cogs/tree/main/echo>)
        """

        # Send the message without letting others know who ran the command
        if ctx.interaction:
            await ctx.send("Sent!", ephemeral=True)
        else:
            await ctx.message.add_reaction("✅")

        target_channel = channel or ctx.channel
        await target_channel.send(message)

    async def red_delete_data_for_user(self, **kwargs):
        pass
