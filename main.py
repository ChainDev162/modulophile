import discord
import asyncio
import os
import json
import sys
import dotenv
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

@bot.event
async def on_ready():
	print(f'Logged in as {bot.user.name}')
	if not bot.guilds:
		print("Not on any servers.")
	else:
		print("Connected to servers:")
	for guild in bot.guilds:
		print(f'- {guild.name} (ID: {guild.id})')
	await load_cogs()

async def load_cogs():
  for folder in ['moderation', 'extras']:
    for filename in os.listdir(folder):
      if filename.endswith('.py') and filename != '__init__.py':
        try:
          await bot.load_extension(f'{folder}.{filename}')
          print(f'Loaded {folder}.{filename} successfully')
        except Exception as e:
          print(f'Failed to load {folder}.{filename}: {e}')

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
  else:
    await ctx.send(f"An error occurred while processing the command.`{error}`")
    print(f"Error: {error}")

@bot.command(name='reboot')
@commands.is_owner()
async def reboot(ctx):
  await ctx.send("🔄 Rebooting bot...")
  os.execv(sys.executable, ['python'] + sys.argv)

async def main():    
  await bot.start(TOKEN)

asyncio.run(main())
# somebody make this entire bot use sqlite3 im too lazy to learn sql