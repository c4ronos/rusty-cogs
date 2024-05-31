from .waifuim import WaifuIM

async def setup(bot):
	await bot.add_cog(WaifuIM(bot))
