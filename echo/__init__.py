from .echo import Echo


async def setup(bot):
    await bot.add_cog(Echo(bot))