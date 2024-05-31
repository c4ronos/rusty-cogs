from redbot.core.bot import Red

from .avatar import Avatar

async def setup(bot: Red) -> None:
    await bot.add_cog(Avatar())
