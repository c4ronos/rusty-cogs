import discord
import re
import datetime
from redbot.core import app_commands, commands


class Timeout(commands.Cog):
    """Cog to manage timeouts of a user."""


    async def get_member(self, ctx, member_str):
        try:
            member_id = int(member_str)
            member = ctx.guild.get_member(member_id)
        except ValueError:
            member = discord.utils.find(lambda m: m.name == member_str or m.mention == member_str, ctx.guild.members)
        return member


    def check_hierarchy(self, ctx, member: discord.Member):
        bot_member = ctx.guild.get_member(ctx.bot.user.id)
        if member.top_role >= bot_member.top_role or member.top_role >= ctx.author.top_role:
            return False, "role_heirarchy"
        elif member.guild_permissions.moderate_members:
            return False, "user_mod"
        return True, None
    

    def validate_duration(self, duration):
        pattern = re.compile(r"^(\d+d)?(\d+h)?(\d+m)?(\d+s)?$")
        return bool(pattern.match(duration))


    def parse_duration(self, duration):
        """Parses a duration string into seconds."""
        seconds = 0
        chunk = ""
        for char in duration:
            if char.isdigit():                      # * if argument is a digit, take it as minutes
                chunk += char
            elif char in "dhms":
                seconds += int(chunk) * {"d": 86400, "h": 3600, "m": 60, "s": 1}[char]
                chunk = ""
        if chunk:
            seconds += int(chunk) * 60              # *
        return seconds
    

    async def create_timeout_embed(self, ctx, title, duration, timestamp, reason, target=None):
        color = discord.Color(0xFFFFFF)
        if title == "Timeout Result":
            description = f"- `{target.name}` has been muted for `{duration}`. Ends: <t:{timestamp}:R>\n> **Reason:** {reason or 'No Reason'}"
        else:
            description = f"- `{target.name}`'s mute extended by `{duration}`. Ends: <t:{timestamp}:R>\n> **Reason:** {reason or 'No Reason'}"

        embed = discord.Embed(color=color, title=title, description=description)
        await ctx.send(embed=embed)


    async def create_untimeout_embed(self, ctx, title, target=None):
        color = discord.Color(0xFFFFFF)
        description = f"- `{target.name}`'s mute has been removed."
        embed = discord.Embed(color=color, title=title, description=description)
        await ctx.send(embed=embed)


    async def create_error_embed(self, ctx, description):
        color = discord.Color(0xFF1A1A)
        title = "Unsuccessful Operation"
        docs = "- [Cog documentation](https://github.com/rusty-man/rusty-cogs/tree/main/timeout)"
        if description == "user_not_found":
            description = f"- User not found. Try again.ㅤㅤㅤㅤㅤㅤㅤㅤ\n{docs}"
        elif description == "not_timed_out":
            description = f"- User is currently not timed out.ㅤㅤㅤㅤㅤ\n{docs}"
        elif description == "timeout_duration":
            description = f"- Timeout duration cannot be `< 30s` / `> 28d`.\n{docs}"
        elif description == "invalid_duration":
            description = f"- That is not a valid time format.ㅤㅤㅤㅤㅤ\n{docs}"
        elif description == "role_heirarchy":
            description = f"- Insufficient permissions (bot/author hierarchy).\n{docs}"
        elif description == "user_mod":
            description = f"- Cannot timeout members with timeout permissions.\n{docs}"

        embed = discord.Embed(color=color, title=title, description=description)
        await ctx.send(embed=embed)


    @commands.hybrid_command(name="timeout", usage="<member> [duration] [reason]")
    @app_commands.describe(member="the member to be timed out. (can be mention/id/username)", duration="[optional] the duration of timeout e.g. 2d3h30m", reason="[optional] the reason for timeout")
    @commands.has_permissions(moderate_members=True)
    @commands.guild_only()
    async def timeout(self, ctx: commands.Context, member: str, duration: str ="10m", *, reason: str =None):
        """Times out a member for a specified duration.
        
        > example: `[p]timeout @yapper 1h30m talks too much`
        > [duration] is optional. default is 10m.
        > Timeout duration cannot exceed 28days.
        """

        member_obj = await self.get_member(ctx, member)
        if not member_obj:
            await self.create_error_embed(ctx, "user_not_found")
            return
        is_valid, error_message = self.check_hierarchy(ctx, member_obj)
        if not is_valid:
            await self.create_error_embed(ctx, error_message)
            return
        if not self.validate_duration(duration):
            await self.create_error_embed(ctx, "invalid_duration")
            return

        #await ctx.message.delete()

        seconds = self.parse_duration(duration)
        min_seconds = 30
        max_seconds = 28 * 86400
        if seconds < min_seconds or seconds > max_seconds:
            await self.create_error_embed(ctx, "timeout_duration")
            return
        
        td = datetime.timedelta(seconds=seconds)
        end = discord.utils.utcnow() + td
        timestamp = int(end.timestamp())
        try:
            await member_obj.timeout(td, reason=reason)
            await self.create_timeout_embed(ctx, "Timeout Result", duration, timestamp, reason, member_obj)
        except:
            await ctx.send(f"Failed to timeout member. Try again.")
        

    @commands.hybrid_command(name="untimeout", usage="<member>")
    @app_commands.describe(member="the member to be timed out. (can be mention/id/username)")
    @commands.has_permissions(moderate_members=True)
    @commands.guild_only()
    async def untimeout(self, ctx: commands.Context, member: str):
        """Removes timeout from a member.
        
        > example: `[p]untimeout @yapper`
        """

        member_obj = await self.get_member(ctx, member)
        if not member_obj:
            await self.create_error_embed(ctx, "user_not_found")
            return
        is_valid, error_message = self.check_hierarchy(ctx, member_obj)
        if not is_valid:
            await self.create_error_embed(ctx, error_message)
            return
        
        #await ctx.message.delete()
        
        if not member_obj.is_timed_out():
            await self.create_error_embed(ctx, "not_timed_out")
            return
        else:
            try:
                await member_obj.timeout(None)
                await self.create_untimeout_embed(ctx, "Timeout Removal", member_obj)
            except Exception:
                await ctx.send(f"Failed to untimeout member. Try again. [{Exception}]")


    @commands.hybrid_command(name="extendtimeout", usage="<member> [duration] [reason]")
    @app_commands.describe(member="the member to be timed out. (can be mention/id/username)", duration="[optional] the duration of timeout e.g. 2d3h30m", reason="[optional] the reason for timeout")
    @commands.has_permissions(moderate_members=True)
    @commands.guild_only()
    async def extendtimeout(self, ctx: commands.Context, member: str, duration: str ="10m", *, reason: str =None):
        """Extends the timeout duration for a member.
        
        > example: `[p]extendtimeout @yapper 1h30m talks too much`
        > Total timeout duration cannot exceed 28days
        """
        
        member_obj = await self.get_member(ctx, member)
        if not member_obj:
            await self.create_error_embed(ctx, "user_not_found")
            return
        is_valid, error_message = self.check_hierarchy(ctx, member_obj)
        if not is_valid:
            await self.create_error_embed(ctx, error_message)
            return
        if not self.validate_duration(duration):
            await self.create_error_embed(ctx, "invalid_duration")
            return
        
        #await ctx.message.delete()
        
        if not member_obj.is_timed_out():
            await self.create_error_embed(ctx, "not_timed_out")
            return
        else:
            seconds = self.parse_duration(duration)
            current = member_obj.timed_out_until

            min_seconds = 30
            max_seconds = 28 * 86400 - (current - discord.utils.utcnow()).total_seconds()
            if seconds < min_seconds or seconds > max_seconds:
                await self.create_error_embed(ctx, "timeout_duration")
                return

            new = current + datetime.timedelta(seconds=seconds)
            timestamp = int(new.timestamp())
            try:
                await member_obj.timeout(None)
                await member_obj.timeout(new, reason=reason)
                await self.create_timeout_embed(ctx, "Timeout Extension", duration, timestamp, reason, member_obj)
            except Exception:
                await ctx.send(f"Failed to extend timeout. Try again. [{Exception}]")


"""         LEGACY - TEXT

This is useful for usage outside embeds. In future, might add an option to choose between embeds and normal text.

-- timeout :: await ctx.send(f"Timed out **{member.name}** for **{self.format_duration(seconds)}** ~ <t:{timestamp}:t>. Reason: {reason or 'No reason.'}")
-- untimeout :: await ctx.send(f"**{member.name}** has been removed from timeout.")
-- extendtimeout :: await ctx.send(f"Added **{self.format_duration(seconds)}** timeout to **{member.name}**. Remaining time: <t:{timestamp}:t>")

    def format_duration(self, time):
        days, remaining = divmod(time, 86400)       # remaining seconds
        hours, remaining = divmod(remaining, 3600)
        minutes, seconds = divmod(remaining, 60)
        formatted = ""
        if days > 0:
            formatted += f"{days}day{'s' if days != 1 else ''}, "
        if hours > 0:
            formatted += f"{hours}hour{'s' if hours != 1 else ''}, "
        if minutes > 0:
            formatted += f"{minutes}minute{'s' if minutes != 1 else ''}, "
        if seconds > 0 or (days == 0 and hours == 0 and minutes == 0):
            formatted += f"{seconds}second{'s' if seconds != 1 else ''}"
        return formatted.rstrip(", ")

"""
