import asyncio
from discord.ext import commands

class ReminderCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="remind")
  @commands.cooldown(1, 3, commands.BucketType.user) 
  async def remind(self, ctx, time: int, *, message: str):
    await ctx.send(f"ℹ Reminder set for {time} seconds.")
    await asyncio.sleep(time)
    await ctx.send(f":bangbang: Reminder: {message}")
################ FOR INIT ###############
async def setup(bot):
  await bot.add_cog(ReminderCommands(bot))
