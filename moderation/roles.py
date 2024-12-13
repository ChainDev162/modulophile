import discord
import json  # noqa: F401
from discord.ext import commands

class RoleCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="ar")
  @commands.has_permissions(manage_roles=True)
  @commands.cooldown(1, 3, commands.BucketType.user) 
  async def add_role(self, ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"{role.name} role added to {member.mention}.")

  @commands.command(name="rr")
  @commands.has_permissions(manage_roles=True)
  @commands.cooldown(1, 3, commands.BucketType.user) 
  async def remove_role(self, ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"{role.name} role removed from {member.mention}.")
################ FOR INIT ###############
async def setup(bot):
  await bot.add_cog(RoleCommands(bot))
