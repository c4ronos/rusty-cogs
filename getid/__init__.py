from redbot.core.bot import Red

from .getid import GetID

async def setup(bot: Red) -> None:
    await bot.add_cog(GetID())
