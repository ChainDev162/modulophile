import discord
import json  # noqa: F401
from discord.ext import commands

class BanCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="ban")
  @commands.has_permissions(ban_members=True)
  @commands.cooldown(1, 3, commands.BucketType.user)
  async def ban(self, ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} has been banned for {reason}.")

  @commands.command(name="unban")
  @commands.has_permissions(ban_members=True)
  @commands.cooldown(1, 3, commands.BucketType.user)
  async def unban(self, ctx, user_id: int):
    user = await self.bot.fetch_user(user_id)
    await ctx.guild.unban(user)
    await ctx.send(f"{user.mention} has been unbanned.")
################ FOR INIT ###############
async def setup(bot):
  await bot.add_cog(BanCommands(bot))
