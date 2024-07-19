from redbot.core.bot import Red

from .meatrider import MeatRider

async def setup(bot: Red) -> None:
    await bot.add_cog(MeatRider())
