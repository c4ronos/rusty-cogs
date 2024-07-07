import discord
from redbot.core import commands, app_commands
from typing import Optional

class Echo(commands.Cog):
    """Makes the bot say something in the specified channel."""

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="echo")
    @commands.guild_only()
    @commands.admin_or_permissions(administrator=True)
    @app_commands.describe(
        message="Input Message",
        channel="Input Channel"
    )
    async def echo(self, ctx: commands.Context, channel: Optional[discord.TextChannel] = None, *, message: str):
        """Makes the bot say something in the specified channel."""

        # Send an ephemeral confirmation
        if ctx.interaction:
            await ctx.send("Sent!", ephemeral=True)
        else:
            await ctx.message.add_reaction("✅")

        # Determine the channel to send the message to
        target_channel = channel or ctx.channel

        # Send the echoed message
        await target_channel.send(message)

    async def red_delete_data_for_user(self, **kwargs):
        pass
