from discord.ext import commands
from commands_.utils.messages import MessageUtils

class PurgeCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    global utils
    utils = MessageUtils(self.bot)
    
  @commands.command(name="purge")
  @commands.has_permissions(manage_messages=True)
  @commands.cooldown(1, 2, commands.BucketType.user) 
  async def purge(self, ctx, amount: int):
    if amount < 1:
      await utils.sendtemp(ctx=ctx, content="🤔 Please specify a number of messages to delete (1 or more).")
      return

    await ctx.channel.purge(limit=amount, bulk=True)  # for speed
    await utils.sendtemp(ctx=ctx, content=f"Deleted {amount} messages.")  

################ FOR INIT ###############
async def setup(bot):
  await bot.add_cog(PurgeCommands(bot))
