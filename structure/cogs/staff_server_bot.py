from discord.ext import commands, tasks
import discord
from discord.ext.commands import has_permissions

class SSCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

        @bot.tree.command(name="promote", description="Promote user to a specific role.")
        @has_permissions(manage_roles=True)
        async def promote(interaction:discord.Interaction, user:discord.Member, role:discord.Role):
            interaction.response.defer(thinking=True)
            if role.is_assignable():
                return await interaction.response.send_message(content=f"Promoted **{user.name}** to **{role.name}**")
            else: return await interaction.response.send_message(content=f"Unfortunately, I am unable to promote **{user.name}** to **{role.name}** because of my ***sufficient permissions***.")
        
        @promote.error
        async def _promote_error(error, interaction:discord.Interaction, user:discord.Member, role:discord.Role):
            return await interaction.response.send_message(f"You are not allowed to promote **{user.name}** because of your **sufficient permissions**.")
        
        @bot.tree.command(name="fire", description="Fire someone from the staff team. This removes all roles and rights from the user.")
        async def fire(interaction:discord.Interaction, user:discord.Member):
            interaction.response.defer(thinking=True)
            try: await user.edit(roles=[], reason="User was fired/removed completely.")
            except: return await interaction.response.send_message("Unfortunately, we were unable to fire the user specified. Please make sure the bot role is higher than the user.", ephemeral=True)
            return await interaction.response.send_message("User was completely fired.", ephemeral=False)