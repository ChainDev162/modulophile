import discord
from discord.ext import commands

class AvatarCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="av")
  @commands.cooldown(1, 3, commands.BucketType.user) 
  async def avatar(self, ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member.display_name}'s Avatar", color=discord.Color.blurple())
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)
################ FOR INIT ###############
async def setup(bot):
  await bot.add_cog(AvatarCommands(bot))
