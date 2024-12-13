import discord # leave as is
from .avatar import AvatarCommands
from .reminders import ReminderCommands
from .serverinfo import ServerInfoCommands
from .ticket import TicketCommands
from .aliasing import AliasCommands

async def setup(bot):
  await bot.add_cog(AvatarCommands(bot))
  await bot.add_cog(ReminderCommands(bot))
  await bot.add_cog(ServerInfoCommands(bot))
  await bot.add_cog(TicketCommands(bot))
  await bot.add_cog(AliasCommands(bot))