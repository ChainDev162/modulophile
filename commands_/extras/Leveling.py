#_ignore_
# thanks to Defxult/discordLevelingSystem for this system, really helped a lot
from discordLevelingSystem import DiscordLevelingSystem, LevelUpAnnouncement, RoleAward
import dotenv
import os
from main import bot 
from discord.ext import commands
import pathlib

dotenv.load_dotenv()

LVLDB_PATH = os.getenv("LVDB_PATH")
MAIN_GUILD = os.getenv("MAIN_GUILD")
LEVELDB_NAME = os.getenv("LEVELDB_NAME")

class LevelingCommands(commands.Cog):
  global lvl
  lvl = DiscordLevelingSystem(stack_awards=False, bot=bot)
  
  if pathlib.Path('../../data/').exists():
    pass 
  else:
    pathlib.Path("../../data/").mkdir(exist_ok=True)
    
  if pathlib.Path(f"../../data/{LEVELDB_NAME}.db").exists():
    lvl.connect_to_database_file(LVLDB_PATH)
  else:
    lvl.create_database_file(LVLDB_PATH, LEVELDB_NAME)

  my_awards = {
    MAIN_GUILD: [
      RoleAward(role_id=831672678586777601, level_requirement=1, role_name='Rookie'),
      RoleAward(role_id=831672730583171073, level_requirement=2, role_name='Associate'),
      RoleAward(role_id=831672814419050526, level_requirement=3, role_name='Legend')
    ]
    # add other guilds here with the same format or expand this one
  }
  
  @bot.event
  async def on_message(message):
    await lvl.award_xp(amount=15, message=message)

  announcement = LevelUpAnnouncement(f'{LevelUpAnnouncement.Member.mention} just leveled up to level {LevelUpAnnouncement.LEVEL} 😎')

################ FOR INIT ###############
async def setup(bot):
  await bot.add_cog(LevelingCommands(bot))