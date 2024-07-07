from redbot.core import app_commands, commands, Config
import discord


class Gulag(commands.Cog):
    """Gulag users by restricting them to a channel"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=238013889107)
        self.config.register_guild(gulag_role=None, gulag_channel=None)
        self.original_roles = {}

    @commands.hybrid_command(name="gulag")
    @app_commands.describe(member="The member to send to the gulag")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def gulag_member(self, ctx: commands.Context, member: discord.Member):
        """Sends a member to the gulag."""
        guild_config = self.config.guild(ctx.guild)
        gulag_role_id = await guild_config.gulag_role()
        gulag_channel_id = await guild_config.gulag_channel()

        if not gulag_role_id:
            await ctx.send("Gulag role is not configured for this guild.")
            return
        if not gulag_channel_id:
            await ctx.send("Gulag channel is not configured for this guild.")
            return

        gulag_role = ctx.guild.get_role(gulag_role_id)
        if not gulag_role:
            await ctx.send("Gulag role not found.")
            return
        gulag_channel = ctx.guild.get_channel(gulag_channel_id)
        if not gulag_channel:
            await ctx.send("Gulag channel not found.")
            return

        # Check if the bot has the required permissions
        bot_member = ctx.guild.get_member(ctx.bot.user.id)
        if not bot_member.top_role > member.top_role:
            await ctx.send("The bot does not have sufficient permissions to gulag this member.")
            return

        removable_roles = [role for role in member.roles[1:] if role.id != member.guild.premium_subscriber_role.id]  # Exclude @everyone
        self.original_roles[member.id] = removable_roles
        await member.remove_roles(*self.original_roles[member.id])
        await member.add_roles(gulag_role)
        await self.update_channel_permissions(ctx.guild, gulag_role, gulag_channel)
        await ctx.send(f"{member.mention} has been sent to the gulag.")
        await gulag_channel.send(f"{member.mention} [-](https://tenor.com/view/gulag-survive-welcome-to-the-gulag-gif-27052296)")


    @commands.hybrid_command(name="bail")
    @app_commands.describe(member="The member to be released from the gulag")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def bail_member(self, ctx: commands.Context, member: discord.Member):
        """Releases a member from the gulag."""
        guild_config = self.config.guild(ctx.guild)
        gulag_role_id = await guild_config.gulag_role()

        if not gulag_role_id:
            await ctx.send("Gulag role is not configured for this guild.")
            return

        gulag_role = ctx.guild.get_role(gulag_role_id)
        if not gulag_role:
            await ctx.send("Gulag role not found.")
            return

        if gulag_role in member.roles:
            # Member is in the gulag
            if member.id in self.original_roles:
                await member.remove_roles(gulag_role)
                await member.add_roles(*self.original_roles[member.id], atomic=True)
                del self.original_roles[member.id]
                await ctx.send(f"{member.mention} has been released from the gulag.")
            else:
                # Handle the case where the member is in the gulag but original roles are missing
                # You might want to log this or handle it differently
                await ctx.send(f"An error occurred while releasing {member.display_name} from the gulag.")
        else:
            await ctx.send(f"{member.display_name} is not currently in the gulag.")


    @commands.group()
    @commands.has_permissions(administrator=True)
    async def gulagset(self, ctx: commands.Context):
        """Commands for gulag management."""
        return


    @gulagset.command(name="channel")
    async def set_gulag_channel(self, ctx: commands.Context, channel: discord.TextChannel):
        """Configures the gulag channel."""
        guild = ctx.guild
        if not channel:
            await ctx.send("Channel not found.")
            return

        await self.config.guild(guild).gulag_channel.set(channel.id)
        await ctx.send(f"Gulag channel configured as {channel.mention}.")


    @gulagset.command(name="role")
    async def set_gulag_role(self, ctx: commands.Context, role: discord.Role):
        """Configures the gulag role."""
        guild = ctx.guild
        gulag_channel_id = await self.config.guild(guild).gulag_channel()

        if not gulag_channel_id:
            await ctx.send("Gulag channel is not configured for this guild.")
            return

        if not role:
            await ctx.send("Role not found.")
            return

        gulag_channel = guild.get_channel(gulag_channel_id)
        if not gulag_channel:
            await ctx.send("Gulag channel not found.")
            return

        # Set permissions for gulag role in gulag channel
        await gulag_channel.set_permissions(role, read_messages=True, send_messages=True)
        await self.update_channel_permissions(guild, role, gulag_channel)

        await self.config.guild(guild).gulag_role.set(role.id)
        await ctx.send(f"Gulag role configured as {role.name}.")


    @gulagset.command(name="clear")
    async def clear_gulag(self, ctx: commands.Context):
        """Resets and deletes the gulag role and channel."""
        guild = ctx.guild
        guild_config = self.config.guild(guild)
        gulag_role_id = await guild_config.gulag_role()
        gulag_channel_id = await guild_config.gulag_channel()

        if not gulag_role_id and not gulag_channel_id:
            await ctx.send("Gulag role and channel is not configured for this guild.")
            return

        gulag_role = guild.get_role(gulag_role_id)
        gulag_channel = guild.get_channel(gulag_channel_id)
        if gulag_role:
            await gulag_role.delete()
        if gulag_channel:
            await gulag_channel.delete()

        await guild_config.gulag_role.set(None)
        await guild_config.gulag_channel.set(None)
        await ctx.send("Gulag role and channel cleared.")


    async def update_channel_permissions(self, guild, gulag_role, gulag_channel):
        """Updates the channel permissions for a gulag role."""
        for channel in guild.channels:
            if channel != gulag_channel:
                await channel.set_permissions(gulag_role, read_messages=False, send_messages=False)
        await gulag_channel.set_permissions(guild.default_role, view_channel=False)
