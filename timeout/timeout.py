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
            return False
        return True
    

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
        color = discord.Color(0x3ACEFF)
        desc_reason = "Purpose" if reason=="Timeout addition." else "Reason"
        description = f"- ⏳ **Ending On:** <t:{timestamp}:f>\n- 🔒 **{desc_reason}:** {reason or 'No Reason.'}\n- 🔑 **Moderator:** {ctx.author.mention}"
        embed = discord.Embed(color=color, title=title, description=description)
        embed.add_field(name="> **Target Memberㅤㅤ**", value=f"ㅤ`{target.name}`")
        embed.add_field(name="> **Durationㅤㅤㅤㅤㅤ** ", value=f"ㅤ`{duration}`")
        await ctx.send(embed=embed)


    async def create_untimeout_embed(self, ctx, title, target=None):
        color = discord.Color(0x3ACEFF)
        description = f"- ⏳ **Ending On:** Timeout was removed.\n- 🔑 **Moderator:** {ctx.author.mention}"
        embed = discord.Embed(color=color, title=title, description=description)
        embed.add_field(name="> **Target Memberㅤㅤ**", value=f"ㅤ`{target.name}`")
        embed.add_field(name="> **Durationㅤㅤㅤㅤㅤ** ", value=f"ㅤ`None`")
        await ctx.send(embed=embed)


    async def create_error_embed(self, ctx, description):
        color = discord.Color(0xFF1A1A)
        title = "Unsuccessful Operation"
        docs = "- 📜 [Cog documentation](https://github.com/rusty-man/rusty-cogs/tree/main/timeout)"
        if description == "user_not_found":
            description = f"- ❌ User not found. Try again.ㅤㅤㅤㅤㅤㅤㅤㅤ\n{docs}"
        elif description == "not_timed_out":
            description = f"- ❌ User is currently not timed out.ㅤㅤㅤㅤㅤ\n{docs}"
        elif description == "timeout_duration":
            description = f"- ❌ Timeout duration cannot be `< 1m` / `> 28d`.\n{docs}"
        elif description == "invalid_duration":
            description = f"- ❌ That is not a valid time format.ㅤㅤㅤㅤㅤ\n{docs}"

        embed = discord.Embed(color=color, title=title, description=description)
        await ctx.send(embed=embed)


    @commands.hybrid_command(name="timeout")
    @app_commands.describe(member="the member to be timed out. (can be mention/id/username)", duration="[optional] the duration of timeout e.g. 2d3h30m", reason="[optional] the reason for timeout")
    @commands.has_permissions(moderate_members=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.guild_only()
    async def timeout(self, ctx: commands.Context, member: str, duration: str ="30m", *, reason: str =None):
        """Times out a member for a specified duration."""

        member_obj = await self.get_member(ctx, member)
        if not member_obj:
            await self.create_error_embed(ctx, "user_not_found")
            return
        if not self.check_hierarchy(ctx, member_obj):
            await ctx.send("Insufficient permissions (bot/author hierarchy)")
            return
        if not self.validate_duration(duration):
            await self.create_error_embed(ctx, "invalid_duration")
            return

        seconds = self.parse_duration(duration)
        min_seconds = 60
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
        except Exception:
            await ctx.send(f"Failed to timeout member. Try again. [{Exception}]")
        

    @commands.hybrid_command(name="untimeout")
    @app_commands.describe(member="the member to be timed out. (can be mention/id/username)")
    @commands.has_permissions(moderate_members=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.guild_only()
    async def untimeout(self, ctx: commands.Context, member: str):
        """Removes timeout from a member."""

        member_obj = await self.get_member(ctx, member)
        if not member_obj:
            await self.create_error_embed(ctx, "user_not_found")
            return
        if not self.check_hierarchy(ctx, member_obj):
            await ctx.send("Insufficient permissions (bot/author hierarchy)")
            return
        
        if not member_obj.is_timed_out():
            await self.create_error_embed(ctx, "not_timed_out")
            return
        else:
            try:
                await member_obj.timeout(None)
                await self.create_untimeout_embed(ctx, "Timeout Removal", member_obj)
            except Exception:
                await ctx.send(f"Failed to untimeout member. Try again. [{Exception}]")


    @commands.hybrid_command(name="extendtimeout")
    @app_commands.describe(member="the member to be timed out. (can be mention/id/username)", duration="[optional] the duration of timeout e.g. 2d3h30m")
    @commands.has_permissions(moderate_members=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.guild_only()
    async def extendtimeout(self, ctx: commands.Context, member: str, duration="30m"):
        """Extends the timeout duration for a member."""
        
        member_obj = await self.get_member(ctx, member)
        if not member_obj:
            await self.create_error_embed(ctx, "user_not_found")
            return
        if not self.check_hierarchy(ctx, member_obj):
            await ctx.send("Insufficient permissions (bot/author hierarchy)")
            return
        if not self.validate_duration(duration):
            await self.create_error_embed(ctx, "invalid_duration")
            return
        
        if not member_obj.is_timed_out():
            await self.create_error_embed(ctx, "not_timed_out")
            return
        else:
            seconds = self.parse_duration(duration)
            current = member_obj.timed_out_until

            min_seconds = 60
            max_seconds = 28 * 86400 - (current - discord.utils.utcnow()).total_seconds()
            if seconds < min_seconds or seconds > max_seconds:
                await self.create_error_embed(ctx, "timeout_duration")
                return

            new = current + datetime.timedelta(seconds=seconds)
            timestamp = int(new.timestamp())
            try:
                await member_obj.timeout(None)
                await member_obj.timeout(new)
                await self.create_timeout_embed(ctx, "Timeout Result", duration, timestamp, "Timeout addition.", member_obj)
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
