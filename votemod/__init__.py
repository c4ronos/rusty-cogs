from .votemod import VoteMod

async def setup(bot):
    await bot.add_cog(VoteMod(bot))