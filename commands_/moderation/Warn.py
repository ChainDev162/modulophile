import discord
import os
import json
from discord.ext import commands
from commands_.utils.messages import MessageUtils

class WarnCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.warn_file = 'warnings.json'
    self.load_warnings()

  def load_warnings(self):
    if os.path.exists(self.warn_file):
      with open(self.warn_file, 'r') as f:
          self.warn_counts = json.load(f)
    else:
      self.warn_counts = {}

  def save_warnings(self):
    with open(self.warn_file, 'w') as f:
      json.dump(self.warn_counts, f, indent=4)

  @commands.command(name="warn")
  @commands.cooldown(1, 3, commands.BucketType.user)  
  async def warn(self, ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.manage_messages:
      user_id = str(member.id)
      if user_id not in self.warn_counts:
        self.warn_counts[user_id] = []
      self.warn_counts[user_id].append(reason or "No reason provided.")
      self.save_warnings()
      await member.send(f"You have been warned in {ctx.guild.name} for: {reason or 'No reason provided.'}")
      await MessageUtils.sendtemp(f"{member.mention} has been warned for: {reason or 'No reason provided.'}", ctx=ctx)

  @commands.command(name="wcs")
  @commands.cooldown(1, 3, commands.BucketType.user)  
  async def warn_counts(self, ctx, member: discord.Member):
    user_id = str(member.id)
    if user_id in self.warn_counts and self.warn_counts[user_id]:
      embed = discord.Embed(
        title=f"Warnings for {member.display_name} ({member.name})",
        color=discord.Color.orange()
        )
      for i, warning in enumerate(self.warn_counts[user_id], start=1):
        embed.add_field(name=f"Warning {i}", value=warning, inline=False)
        await ctx.author.send(embed=embed)
    else:
      await ctx.send(f"No warnings found for {member.mention}.")

################ FOR INIT ###############
async def setup(bot):
  await bot.add_cog(WarnCommands(bot))
