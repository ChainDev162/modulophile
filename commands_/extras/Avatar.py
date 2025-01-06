import discord
from discord.ext import commands
from commands_.utils.messages import MessageUtils

class AvatarCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.utils = MessageUtils(self.bot)

  @commands.command(name="av")
  @commands.cooldown(1, 3, commands.BucketType.user) 
  async def avatar(self, ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member.display_name}'s Avatar", color=discord.Color.blurple())
    embed.set_image(url=member.avatar.url)
    await self.utils.sendtemp(ctx=ctx, content=embed)
################ FOR INIT ###############
async def setup(bot):
  await bot.add_cog(AvatarCommands(bot))
