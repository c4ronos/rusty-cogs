import discord
from redbot.core import app_commands, commands, Config


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
        """Sends a member to the gulag.
        
        > This will take away all roles of a member and give them the gulag role.
        """
        guild_config = self.config.guild(ctx.guild)
        gulag_role_id = await guild_config.gulag_role()
        gulag_channel_id = await guild_config.gulag_channel()

        # Checks
        gulag_role = ctx.guild.get_role(gulag_role_id)
        if not gulag_role:
            await ctx.send("Gulag role not found.")
            return
        gulag_channel = ctx.guild.get_channel(gulag_channel_id)
        if not gulag_channel:
            await ctx.send("Gulag channel not found.")
            return

        bot_member = ctx.guild.get_member(ctx.bot.user.id)
        if member.top_role >= bot_member.top_role or member.top_role >= ctx.author.top_role:
            await ctx.send("Insufficient permissions (bot/author heirarchy)")
            return

        booster_role = None
        if ctx.guild.premium_subscriber_role:
            booster_role = ctx.guild.premium_subscriber_role.id

        removable_roles = [role for role in member.roles[1:] if role.id != booster_role and role.managed == False]
        self.original_roles[member.id] = removable_roles

        async with ctx.typing():
            await member.remove_roles(*removable_roles)
            await member.add_roles(gulag_role)

        await ctx.send(f"{member.mention} has been sent to the gulag.")
        await gulag_channel.send(f"{member.mention} [-](https://tenor.com/view/gulag-survive-welcome-to-the-gulag-gif-27052296)")


    @commands.hybrid_command(name="bail")
    @app_commands.describe(member="The member to be released from the gulag")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def bail_member(self, ctx: commands.Context, member: discord.Member):
        """Releases a member from the gulag.
        
        > This will take away gulag role and give back the roles the member previously had.
        """
        guild_config = self.config.guild(ctx.guild)
        gulag_role_id = await guild_config.gulag_role()
        gulag_role = ctx.guild.get_role(gulag_role_id)

        if not gulag_role_id:
            await ctx.send("Gulag role not found.")
            return

        if gulag_role in member.roles:
            async with ctx.typing():
                await member.remove_roles(gulag_role)

                if member.id in self.original_roles:
                    await member.add_roles(*self.original_roles[member.id], atomic=True)
                    del self.original_roles[member.id]
                else:           # Member not in bot's list
                    await ctx.send(f"User's original roles were not found and cannot be added back. You will have to add them manually.")

            await ctx.send(f"{member.mention} has been released from the gulag.")
        else:
            await ctx.send(f"{member.display_name} is not currently in the gulag.")

    
    @commands.hybrid_command(name="gulaglist")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def gulag_list(self, ctx: commands.Context):
        """Lists all users currently in the gulag."""

        guild_config = self.config.guild(ctx.guild)
        gulag_role_id = await guild_config.gulag_role()

        if not gulag_role_id:
            await ctx.send("Gulag role hasn't been configured.")
            return

        gulag_role = ctx.guild.get_role(gulag_role_id)
        members = [f"{member.name} \|| {member.id}" for member in gulag_role.members]

        if not members:
            await ctx.send("No members are currently in the gulag.")
            return

        message = "**Current Gulag Members:**\n\n" + "\n".join(members)
        await ctx.send(message)


    @commands.group()
    @commands.has_permissions(administrator=True)
    async def gulagset(self, ctx: commands.Context):
        """Commands for gulag management."""
        return


    @gulagset.command(name="channel")
    async def set_gulag_channel(self, ctx: commands.Context, channel: discord.TextChannel):
        """Configures the gulag channel."""
        if not channel:
            await ctx.send("Channel not found.")
            return

        await self.config.guild(ctx.guild).gulag_channel.set(channel.id)
        await ctx.send(f"Gulag channel configured as {channel.mention}.")


    @gulagset.command(name="role")
    async def set_gulag_role(self, ctx: commands.Context, role: discord.Role):
        """Configures the gulag role."""
        gulag_channel_id = await self.config.guild(ctx.guild).gulag_channel()
        gulag_channel = ctx.guild.get_channel(gulag_channel_id)

        if not gulag_channel:
            await ctx.send("Gulag channel is not configured for this guild.")
            return

        if not role:
            await ctx.send("Role not found.")
            return

        # Set permissions across server after channel and role are set.
        async with ctx.typing():
            try:
                await self.update_channel_permissions(ctx.guild, role, gulag_channel)
            except Exception:
                await ctx.send("Error. Please try again.")

        await self.config.guild(ctx.guild).gulag_role.set(role.id)
        await ctx.send(f"Gulag role configured as {role.name}.")


    @gulagset.command(name="clear")
    async def clear_gulag(self, ctx: commands.Context):
        """Resets the gulag role and channel."""
        guild_config = self.config.guild(ctx.guild)
        gulag_role_id = await guild_config.gulag_role()
        gulag_channel_id = await guild_config.gulag_channel()

        gulag_role = ctx.guild.get_role(gulag_role_id)
        gulag_channel = ctx.guild.get_channel(gulag_channel_id)

        await guild_config.gulag_role.set(None)
        await guild_config.gulag_channel.set(None)
        await ctx.send("Gulag role and channel cleared.")


    async def update_channel_permissions(self, guild, gulag_role, gulag_channel):
        """Updates the channel permissions for a gulag role."""
        for channel in guild.channels:
            if channel != gulag_channel:
                await channel.set_permissions(gulag_role, view_channel=False, send_messages=False)

        await gulag_channel.set_permissions(guild.default_role, view_channel=False)
        await gulag_channel.set_permissions(gulag_role, view_channel=True, send_messages=True)


    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        """Automatically update permissions for new channels created."""
        guild = channel.guild
        guild_config = self.config.guild(guild)
        gulag_role_id = await guild_config.gulag_role()

        if not gulag_role_id:
            return

        gulag_role = guild.get_role(gulag_role_id)
        gulag_channel_id = await guild_config.gulag_channel()
        gulag_channel = guild.get_channel(gulag_channel_id)

        if gulag_channel and channel.id == gulag_channel.id:
            return

        await channel.set_permissions(gulag_role, view_channel=False, send_messages=False)
