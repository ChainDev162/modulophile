import discord
from discord.ext import commands
from commands_.utils.messages import MessageUtils

class ServerInfoCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="serverinfo")
  @commands.cooldown(1, 3, commands.BucketType.user)
  async def server_info(self, ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Server Information", color=discord.Color.blue())
    embed.add_field(name="Server ID", value=ctx.guild.id, inline=True)
    embed.add_field(name="Owner", value=ctx.guild.owner, inline=True)
    embed.add_field(name="Members", value=ctx.guild.member_count, inline=True)
    await MessageUtils.sendtemp(ctx=ctx, content=embed)
################ FOR INIT ###############
async def setup(bot):
  await bot.add_cog(ServerInfoCommands(bot))
