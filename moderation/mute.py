import discord
import re
from discord.ext import commands
from datetime import timedelta

class MuteCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="mute")
  @commands.has_permissions(moderate_members=True)
  @commands.cooldown(1, 3, commands.BucketType.user)
  async def mute(self, ctx, member: discord.Member, duration: str, *, reason=None):
    time_converter = {
      "m": 60,
      "h": 3600,
      "d": 86400,
    }
    match = re.match(r"(\d+)([mhdMHD])", duration)
    if not match:
      await ctx.send("❓ Invalid duration format. Use `<number><m/h/d>`.")
      return
    amount, unit = match.groups()
    seconds = int(amount) * time_converter[unit.lower()]
    await member.timeout(discord.utils.utcnow() + timedelta(seconds=seconds), reason=reason or "No reason provided.")
    await ctx.send(f"{member.mention} has been muted for {duration} due to {reason or 'No reason provided.'}.")
    embed = discord.Embed(title="Penalty Details", color=discord.Color.blue())
    embed.add_field(name="Reason", value=reason, inline=True)
    embed.add_field(name="Duration", value=duration, inline=True)
    embed.add_field(name="Issuer", value=ctx.author, inline=True) 
    await ctx.send("✌ What's up? Just wanted to send this:")
    embed = discord.Embed(title="Penalty Details", color=discord.Color.blue(), embed=embed)

  @commands.command(name="unmute")
  @commands.has_permissions(moderate_members=True)
  @commands.cooldown(1, 3, commands.BucketType.user)
  async def unmute(self, ctx, member: discord.Member):
    await member.edit(timed_out_until=None)
    await ctx.send(f"{member.mention} has been unmuted.")
################ FOR INIT ###############
async def setup(bot):
  await bot.add_cog(MuteCommands(bot))
