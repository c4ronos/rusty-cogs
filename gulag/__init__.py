from redbot.core.bot import Red

from .gulag import Gulag

async def setup(bot: Red) -> None:
    await bot.add_cog(Gulag())
