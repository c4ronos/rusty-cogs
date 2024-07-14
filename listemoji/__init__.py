from redbot.core.bot import Red

from .listemoji import ListEmoji

__red_end_user_data_statement__ = (
    "This cog does not persistently store data or metadata about users."
)

async def setup(bot: Red) -> None:
    await bot.add_cog(ListEmoji())
