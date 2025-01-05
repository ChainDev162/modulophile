import discord
import asyncio
import os
import json
import sys
import dotenv
import pathlib
from discord.ext import commands
from commands_.utils.messages import MessageUtils
import inquirer

intents = discord.Intents.default()
intents.message_content = True  
intents.guilds = True

BASE_DIR = os.path.dirname(os.path.abspath(__name__))
os.chdir(BASE_DIR)

_env = dotenv.load_dotenv()

if not _env:
  print("Must be your first time running this, eh? Let's get you set up!")
  questions = [
    inquirer.Text("TOKEN", message="Enter your bot's token", 
                  validate=lambda _, x: len(x) > 0 or "Token cannot be empty!"),
    
    inquirer.Text("PREFIX", message="Enter your bot's prefix"),
    
    inquirer.Text("OWNER_ID", message="Enter your Discord ID", 
                  validate=lambda _, x: len(x) == 18 and x.isdigit() or "ID is not valid!"),
    
    inquirer.Text("TESTING_GUILD", message="Enter the ID of the guild you want to test this bot in (optonal, but recommended)",
                  validate=lambda _, x: len(x) == 18 and x.isdigit() or "ID is not valid!"),
    
    inquirer.Text("MAIN_GUILD", message="Enter the ID of the main guild this bot will be used in (used in Leveling cog)",
                  validate=lambda _,x: len(x) == 18 and x.isdigit() or "ID is not valid!"),
  ]
  answers = inquirer.prompt(questions) 
  with open('.env', 'w') as fp:
    for key, value in answers.items():
      fp.write(f"{key}={value}\nFLAGS=None")
  dotenv.load_dotenv()

FLAGS = os.getenv('FLAGS')
if 'DEL_PYCACHE' in FLAGS:
  for pycache_dir in pathlib.Path('.').rglob('__pycache__'):
    if pycache_dir.is_dir():  
      import shutil
      shutil.rmtree(pycache_dir) 

bot = commands.Bot(command_prefix=answers['PREFIX'], intents=intents)

TOKEN = os.getenv('TOKEN')

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
    if file.stem.startswith("_"):
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
    await MessageUtils.sendtemp(ctx=ctx, content="⁉ This command does not exist.")
  elif isinstance(error, commands.MissingRequiredArgument):
    await MessageUtils.sendtemp(ctx=ctx, content="🤔 You are missing an argument for this command.")
  elif isinstance(error, commands.CommandOnCooldown):
    await MessageUtils.sendtemp(ctx=ctx, content=f"⏳ Command is on cooldown. Try again in {int(error.retry_after)} seconds.")
  elif isinstance(error, commands.MissingPermissions):
    await MessageUtils.sendtemp(ctx=ctx, content="🙅‍♂️ You don't have the necessary permissions to use this command.")
  elif isinstance(error, discord.Forbidden):
    await MessageUtils.sendtemp(ctx=ctx, content="❌ I don't have permissions for your requested command!")
  else:
    await MessageUtils.sendtemp(ctx=ctx, content=f"⚠ An error occurred while processing the command.`{error}`")
    print(f"Error: {error}")

@bot.command(name='reboot')
@commands.is_owner()
async def reboot(ctx):
  await MessageUtils.sendtemp(ctx=ctx, content="🔄 Rebooting bot...")
  os.execv(sys.executable, ['python'] + sys.argv)

async def main():  
  await load_cogs()
  await bot.start(TOKEN)

asyncio.run(main())
# somebody make this entire bot use sqlite3 instead of json im too lazy to learn sql