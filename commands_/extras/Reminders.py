import asyncio
from discord.ext import commands
from ..utils.messages import MessageUtils

class ReminderCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.utils = MessageUtils(self.bot)
    
  @commands.command(name="remind")
  @commands.cooldown(1, 3, commands.BucketType.user) 
  async def remind(self, ctx, time: int, *, message: str):
    await self.utils.sendtemp(ctx=ctx, content=f"Reminder set for {time} seconds.")
    await asyncio.sleep(time)
    await self.utils.sendtemp(ctx=ctx, content=f":bangbang: Reminder: {message}")
################ FOR INIT ###############
async def setup(bot):
  await bot.add_cog(ReminderCommands(bot))
