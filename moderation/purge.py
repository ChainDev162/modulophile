import discord  # noqa: F401
from discord.ext import commands

class PurgeCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="purge")
  @commands.has_permissions(manage_messages=True)
  @commands.cooldown(1, 2, commands.BucketType.user) 
  async def purge(self, ctx, amount: int):
    if amount < 1:
      await ctx.send("🤔 Please specify a number of messages to delete (1 or more).")
      return

    await ctx.channel.purge(limit=amount, bulk=True)  # for speed
    await ctx.send(f"Deleted {amount} messages.", delete_after=3)  

################ FOR INIT ###############
async def setup(bot):
  await bot.add_cog(PurgeCommands(bot))
