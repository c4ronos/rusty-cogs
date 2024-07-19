from redbot.core.bot import Red

from .banana import Banana

async def setup(bot: Red) -> None:
    await bot.add_cog(Banana())
