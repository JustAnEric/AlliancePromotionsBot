from discord.ext import commands, tasks
import discord
from discord.ext.commands import has_permissions

class MSCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot