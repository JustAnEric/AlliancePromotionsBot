from discord.ext import commands
import os, json, discord, sys, dotenv, asyncio
from structure.cogs import load
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
dotenv.load_dotenv("./.env")
asyncio.run(load.__loader__(bot))
@bot.command(name="sync")
async def sync_all_dev_commands(ctx):
    sync = await bot.tree.sync()
    await ctx.send(f"Synced {len(sync)} command(s)")
bot.run(os.environ.get("TOKEN"))