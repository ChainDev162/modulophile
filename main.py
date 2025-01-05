import discord
import asyncio
import os
import json
import sys
import dotenv
import pathlib
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  
intents.guilds = True

bot = commands.Bot(command_prefix="_", intents=intents)

OWNER_ID = 1170123796783583375

dotenv.load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

def load_warnings():
  if os.path.exists('warnings.json'):
    with open('warnings.json', 'r') as f:
      return json.load(f)
  return {}

def save_warnings(warnings):
  with open('warnings.json', 'w') as f:
    json.dump(warnings, f, indent=2)

warnings = load_warnings()

async def load_cogs():
  loaded_exts = []
  ext_dir = "commands_"
  
  def get_ignore_reason(file):
    with open(file, "r", encoding="utf-8") as f:
      first_line = f.readline().strip()
    if first_line == "#_ignore_" or file.stem.startswith("_"):
      return f"⏭ File {file} is marked as ignored, moving on!"
    return None 
  
  all_files = list(pathlib.Path(ext_dir).rglob("*.py"))
  
  for file in all_files:
    ignore_reason = get_ignore_reason(file)
    if ignore_reason:
      print(ignore_reason)
      continue
    
    try:
      await bot.load_extension(".".join(file.with_suffix("").parts))
      print(f"✅ Loaded {file}")
      loaded_exts.append(file.stem)
    except commands.ExtensionError as e:
      print(f"❌ Failed to load {file}: {e}")
  
  loaded_commands = ", ".join(loaded_exts)
  loaded_amt = len(loaded_exts) + len(all_files) # just for this next condition
  
  if len(loaded_exts) == len(all_files) and loaded_amt != 0:
    print("🔥 All extensions loaded!")
    print(loaded_exts)
  else:
    print(f"Loaded commands: {loaded_commands}")

tiplist = ["Pro tip: You can mark extensions to be ignored by setting the first line to `#_ignore_` or by appending an underscore to the beginning of the extension's filename!",
           "Pro tip: You can add your own conditions for the cog loading method!",
           """Pro tip: You can add your own commands/handlers in this bot! Just create a new file in the existing `commands_` directory and add your code there!
           Make sure to include the following:
           ```py
           async def setup(bot):
             await bot.add_cog(TicketCommands(bot))``` in your file!"""]
@bot.event
async def on_ready():
  
  print(f'Logged in as {bot.user.name}')
  if not bot.guilds:
    print("Not on any servers.")
  else:
    print("Connected to servers:")
  for guild in bot.guilds:
    print(f'- {guild.name} (ID: {guild.id})')
    
@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    await ctx.send("⁉ This command does not exist.")
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("🤔 You are missing an argument for this command.")
  elif isinstance(error, commands.CommandOnCooldown):
    await ctx.send(f"⏳ Command is on cooldown. Try again in {int(error.retry_after)} seconds.")
  elif isinstance(error, commands.MissingPermissions):
    await ctx.send("🙅‍♂️ You don't have the necessary permissions to use this command.")
  elif isinstance(error, discord.Forbidden):
    await ctx.send("❌ I don't have permissions for your requested command!")
  else:
    await ctx.send(f"An error occurred while processing the command.`{error}`")
    print(f"Error: {error}")

@bot.command(name='reboot')
@commands.is_owner()
async def reboot(ctx):
  await ctx.send("🔄 Rebooting bot...")
  os.execv(sys.executable, ['python'] + sys.argv)

async def main():  
  await load_cogs()
  await bot.start(TOKEN)

asyncio.run(main())
# somebody make this entire bot use sqlite3 instead of json im too lazy to learn sql