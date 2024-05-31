from redbot.core.bot import Red

from .banner import Banner

async def setup(bot: Red) -> None:
    await bot.add_cog(Banner())
