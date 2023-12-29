from discord.ext import commands, tasks
import discord
from discord.ext.commands import has_permissions

class SSCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

        @bot.tree.command(name="promote", description="Promote user to a specific role.")
        @has_permissions(manage_roles=True)
        async def promote(interaction:discord.Interaction, user:discord.Member, role:discord.Role):
            await interaction.response.defer(thinking=True)
            if role.is_assignable():
                await user.add_roles(role)
                return await interaction.followup.send(content=f"Promoted **{user.name}** to **{role.name}**")
            else: return await interaction.followup.send(content=f"Unfortunately, I am unable to promote **{user.name}** to **{role.name}** because of my ***insufficient permissions***.")
        
        @promote.error
        async def _promote_error(interaction:discord.Interaction, error):
            return await interaction.followup.send(f"You are not allowed to promote because of your **insufficient permissions**.")
        
        @bot.tree.command(name="fire", description="Fire someone from the staff team. This removes all roles and rights from the user.")
        @has_permissions(manage_roles=True)
        async def fire(interaction:discord.Interaction, user:discord.Member):
            await interaction.response.defer(thinking=True)
            try: await user.edit(roles=[], reason="User was fired/removed completely.")
            except: return await interaction.followup.send("Unfortunately, we were unable to fire the user specified. Please make sure the bot role is higher than the user.", ephemeral=True)
            return await interaction.followup.send("User was completely fired.", ephemeral=False)
        
        @fire.error
        async def _fire_error(interaction:discord.Interaction, error):
            return await interaction.followup.send(f"You are not allowed to fire because of your **insufficient permissions**.")
        
        @bot.tree.command(name="demote", description="Demotes a user from a specified role. The bot will remove the highest role if no role was specified.")
        @has_permissions(manage_roles=True)
        async def demote(interaction:discord.Interaction, user:discord.Member, position:discord.Role=None):
            await interaction.response.defer(thinking=True)
            if position is None:
                roleToRemove = user.top_role
                await user.remove_roles(roleToRemove)
                return await interaction.followup.send(f"Removed **{roleToRemove.name}** from **{user.name}**\nUsage: .demote [user:server-member] [position:role|optional]")
            else:
                await user.remove_roles(position)
                return await interaction.followup.send(f"Removed **{roleToRemove.name}** from **{user.name}**")
            
        @demote.error
        async def _demote_error(interaction:discord.Interaction, error):
            return await interaction.followup.send(f"You are not allowed to demote because of your **insufficient permissions**.")

        @bot.command(name="promote", brief="Promote user to a specific role.")
        @has_permissions(manage_roles=True)
        async def raw_promote(ctx:commands.Context, user:discord.Member, role:discord.Role):
            default = await ctx.send("**Alliance Promotions Utilities** is thinking...")
            if role.is_assignable():
                await user.add_roles(role)
                return await default.edit(content=f"Promoted **{user.name}** to **{role.name}**")
            else: return await default.edit(content=f"Unfortunately, I am unable to promote **{user.name}** to **{role.name}** because of my ***insufficient permissions***.")
        
        @raw_promote.error
        async def _raw_promote_error(ctx:commands.Context, error):
            return await ctx.send(f"You are not allowed to promote because of your **insufficient permissions**.")
        
        @bot.command(name="fire", brief="Fire someone from the staff team. This removes all roles and rights from the user.")
        @has_permissions(manage_roles=True)
        async def raw_fire(ctx:commands.Context, user:discord.Member):
            default = await ctx.send("**Alliance Promotions Utilities** is thinking...")
            try: await user.edit(roles=[], reason="User was fired/removed completely.")
            except: return await default.edit(content="Unfortunately, we were unable to fire the user specified. Please make sure the bot role is higher than the user.")
            return await default.edit(content="User was completely fired.")
        
        @raw_fire.error
        async def _raw_fire_error(ctx:commands.Context, error):
            return await ctx.send(f"You are not allowed to fire because of your **insufficient permissions**.")
        
        @bot.command(name="demote", brief="Demotes a user from a specified role. The bot will remove the highest role if no role was specified.")
        @has_permissions(manage_roles=True)
        async def raw_demote(ctx:commands.Context, user:discord.Member, position:discord.Role=None):
            default = await ctx.send("**Alliance Promotions Utilities** is thinking...")
            if position is None:
                roleToRemove = user.top_role
                await user.remove_roles(roleToRemove)
                return await default.edit(content=f"Removed **{roleToRemove.name}** from **{user.name}**\nUsage: .demote [user:server-member] [position:role|optional]")
            else:
                await user.remove_roles(position)
                return await default.edit(content=f"Removed **{position.name}** from **{user.name}**")
            
        @raw_demote.error
        async def _raw_demote_error(ctx:commands.Context, error):
            return await ctx.send(f"You are not allowed to demote because of your **insufficient permissions**.")
        
        @bot.tree.command(name="strikes", description="See the strikes a user has.")
        async def _strikes(intr:discord.Interaction, user:discord.User):
            send = intr.response.send_message
            author = intr.user
            if user.bot:
                return await send("You are unable to see the strikes for this user as they are a robot.")
