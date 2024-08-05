from redbot.core.bot import Red

from .regexsearch import RegexSearch

async def setup(bot: Red) -> None:
    await bot.add_cog(RegexSearch())
