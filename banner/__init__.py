from .banner import Banner


async def setup(bot):
    await bot.add_cog(Banner(bot))