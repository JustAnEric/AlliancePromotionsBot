from discord.ext import commands
import os, json, discord, sys
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
@bot.command(name="adwarn")