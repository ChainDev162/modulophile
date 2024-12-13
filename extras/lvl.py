import discord
import json
import os 
from discord.ext import commands

class LevelingCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.level_roles = {} 
    self.load_xp_data()

  def load_xp_data(self):
    if os.path.exists("xp_data.json"):
      with open("xp_data.json", "r") as f:
        self.xp_data = json.load(f)
    else:
      self.xp_data = {}

  def save_xp_data(self):
    with open("xp_data.json", "w") as f:
      json.dump(self.xp_data, f, indent=4)

  def calculate_level(self, xp):
    return int(xp ** 0.5) 

  def get_user_data(self, user_id):
    if str(user_id) not in self.xp_data:
      self.xp_data[str(user_id)] = {"xp": 0, "level": 0}
    return self.xp_data[str(user_id)]

  def update_xp(self, user_id, xp_per_msg):
    user_data = self.get_user_data(user_id)
    user_data["xp"] += xp_per_msg
    new_level = self.calculate_level(user_data["xp"])
    leveled_up = new_level > user_data["level"]
    user_data["level"] = new_level
    self.save_xp_data()
    return leveled_up, new_level

  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author.bot:
      return

    user_id = message.author.id
    leveled_up, new_level = self.update_xp(user_id, xp_per_msg=5)

    if leveled_up:
      await message.channel.send(f"🥳 Congratulations {message.author.mention}, you've reached level {new_level}!")
      await self.assign_role_based_on_level(message.author, new_level)

  async def assign_role_based_on_level(self, member, level):
    guild = member.guild
    if level in self.level_roles:
      role_id = self.level_roles[level]
      role = guild.get_role(role_id)
      if role:
        await member.add_roles(role)
        await member.send(f"✔ You've been assigned the role: {role.name} for reaching level {level}!")

  @commands.command(name="setlevelrole")
  @commands.has_permissions(administrator=True)
  async def set_level_role(self, ctx, level: int, role: discord.Role):
    self.level_roles[level] = role.id
    await ctx.send(f"ℹ Role {role.name} will now be assigned at level {level}.")
    self.save_level_roles()

  def save_level_roles(self):
    with open("level_roles.json", "w") as f:
      json.dump(self.level_roles, f, indent=4)

  @commands.command(name="level")
  async def check_level(self, ctx, member: discord.Member = None):
    if member is None:
      member = ctx.author

    user_data = self.get_user_data(member.id)
    level = user_data["level"]
    xp = user_data["xp"]
    await ctx.send(f"{member.mention} is at level {level} with {xp} XP.")

################ FOR INIT ###############
async def setup(bot):                     
  await bot.add_cog(LevelingCommands(bot))
