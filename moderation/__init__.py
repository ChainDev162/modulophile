import discord # leave as is
from moderation.ban import BanCommands
from moderation.mute import MuteCommands
from moderation.warn import WarnCommands
from moderation.roles import RoleCommands
from moderation.purge import PurgeCommands

async def setup(bot):
  await bot.add_cog(BanCommands(bot))
  await bot.add_cog(MuteCommands(bot))
  await bot.add_cog(WarnCommands(bot))
  await bot.add_cog(RoleCommands(bot))
  await bot.add_cog(PurgeCommands(bot))