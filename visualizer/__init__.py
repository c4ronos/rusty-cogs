from redbot.core.bot import Red

from .visualizer import Visualizer

async def setup(bot: Red) -> None:
    await bot.add_cog(Visualizer())
