import json
import os 
from discord.ext import commands
from commands_.utils.messages import MessageUtils

def load_aliases():
  if os.path.exists('aliases.json'):
    with open('aliases.json', 'r') as f:
      return json.load(f)
  return {}

def save_aliases(aliases):
  with open('aliases.json', 'w') as f:
    json.dump(aliases, f, indent=2)

aliases = load_aliases()

class AliasCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.utils = MessageUtils(self.bot)
    
  @commands.command(name='alias')
  @commands.is_owner()
  async def create_alias(self, ctx, alias_name: str, actual_command: str):
    command = self.bot.get_command(actual_command)
    if command is None:
      await self.utils.sendtemp(ctx=ctx, content=f"❓ The command `{actual_command}` does not exist.")
      return

    aliases[alias_name] = actual_command
    save_aliases(aliases) 
    await self.utils.sendtemp(ctx=ctx, content=f"👌 Alias `{alias_name}` created for `{actual_command}`.")

  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author.bot:
      return
    if message.content.startswith(self.bot.command_prefix):
      command_name = message.content[len(self.bot.command_prefix):].split()[0]
      if command_name in aliases:
        actual_command_name = aliases[command_name]
        command = self.bot.get_command(actual_command_name)
        if command:
          ctx = await self.bot.get_context(message)
          await command(ctx, *message.content[len(self.bot.command_prefix) + len(command_name):].split())
          return
################ FOR INIT ###############
async def setup(bot):
  await bot.add_cog(AliasCommands(bot))