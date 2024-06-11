import discord
from redbot.core import commands, Config, checks
from redbot.core.bot import Red
import asyncio

class VoteMod(commands.Cog):
    """
    Fun vote-based moderation commands for banning or kicking users.
    """

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=167470521189)
        self.config.register_guild(required_votes=5)
        self.active_votes = {}

    @commands.command(name="voteban")
    @checks.admin_or_permissions(administrator=True)
    @commands.guild_only()
    async def voteban(self, ctx: commands.Context, member: discord.Member):
        """Start a vote to ban a user."""
        await self.start_vote(ctx, member, "ban")

    @commands.command(name="votekick")
    @checks.admin_or_permissions(administrator=True)
    @commands.guild_only()
    async def votekick(self, ctx: commands.Context, member: discord.Member):
        """Start a vote to kick a user."""
        await self.start_vote(ctx, member, "kick")

    @commands.command(name="voteset")
    @checks.admin_or_permissions(administrator=True)
    @commands.guild_only()
    async def voteset(self, ctx: commands.Context, votes: int):
        """Set the number of votes required for votemod."""
        await self.config.guild(ctx.guild).required_votes.set(votes)
        await ctx.send(f"Required votes for voteban and votekick set to {votes}.")

    async def start_vote(self, ctx: commands.Context, member: discord.Member, action: str):
        required_votes = await self.config.guild(ctx.guild).required_votes()

        embed = discord.Embed(
            title=f"Vote to {action} {member}",
            description=f"React with ✅ to {action}, ❌ to stop this vote.",
            color=discord.Color.red() if action == "ban" else discord.Color.orange()
        )
        embed.set_footer(text=f"{required_votes} reactions required to execute / cancel this action.")
        
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        self.active_votes[msg.id] = {
            "guild": ctx.guild.id,
            "channel": ctx.channel.id,
            "target": member.id,
            "action": action,
            "yes": 0,
            "no": 0
        }

        await asyncio.sleep(300)  # 5 minutes
        if msg.id in self.active_votes:
            await self.end_vote(msg.id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id not in self.active_votes:
            return

        vote = self.active_votes[payload.message_id]
        if payload.emoji.name == "✅":
            vote["yes"] += 1
        elif payload.emoji.name == "❌":
            vote["no"] += 1

        required_votes = await self.config.guild(self.bot.get_guild(vote["guild"])).required_votes()
        if vote["yes"] >= required_votes or vote["no"] >= required_votes:
            await self.end_vote(payload.message_id)

    async def end_vote(self, message_id: int):
        vote = self.active_votes.pop(message_id, None)
        if not vote:
            return

        guild = self.bot.get_guild(vote["guild"])
        channel = guild.get_channel(vote["channel"])
        member = guild.get_member(vote["target"])
        msg = await channel.fetch_message(message_id)

        if vote["yes"] >= await self.config.guild(guild).required_votes():
            action_text = "banned" if vote["action"] == "ban" else "kicked"
            try:
                if vote["action"] == "ban":
                    await member.ban(reason="Vote ban passed.")
                else:
                    await member.kick(reason="Vote kick passed.")
                result = f"{member.mention} has been {action_text}."
                color = discord.Color.red() if vote["action"] == "ban" else discord.Color.orange()
            except Exception as e:
                result = f"Failed to {vote['action']} {member.mention}: {e}"
                color = discord.Color.red()
        else:
            result = f"Vote to {vote['action']} {member.mention} has failed."
            color = discord.Color.green()

        embed = discord.Embed(
            title=f"Vote {vote['action'].capitalize()} Result",
            description=result,
            color=color
        )
        await msg.edit(embed=embed)

        # Remove reactions
        await msg.clear_reactions()
