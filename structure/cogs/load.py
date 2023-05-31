from . import main_server_bot
from . import staff_server_bot
from discord.ext.commands import Bot

cogs = [
    main_server_bot.MSCog,
    staff_server_bot.SSCog
]

async def __loader__(bot:Bot):
    for i in cogs:
        await bot.add_cog(i(bot))
    print("Loaded cogs.")