from redbot.core.bot import Red

from .timeout import Timeout

async def setup(bot: Red) -> None:
    await bot.add_cog(Timeout())
