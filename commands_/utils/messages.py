import discord
from discord.ext import commands
import asyncio

TRASHCAN_EMOJI = "🗑️"  # Trashcan emoji

class MessageUtils(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_reaction_add(self, reaction, user):
    """
    Deletes a message when the trashcan emoji is added by a user (not a bot).
    """
    if (
      str(reaction.emoji) == TRASHCAN_EMOJI
      and not user.bot
      and reaction.message.author == self.bot.user
    ):
      try:
        await reaction.message.delete()
        print(f"Deleted message: {reaction.message.content}")
      except discord.Forbidden:
        print("Bot doesn't have permission to delete messages.")
      except discord.HTTPException as e:
        print(f"Failed to delete message: {e}")

  async def sendtemp(self, ctx, content, timeout=60):
    if isinstance(content, discord.Embed):
      bot_message = await ctx.send(embed=content)
    else:
      bot_message = await ctx.send(content)
    
    bot_message = await ctx.send(content)
    await bot_message.add_reaction(TRASHCAN_EMOJI)

    def check_reaction(reaction, user):
      return (
        str(reaction.emoji) == TRASHCAN_EMOJI
        and reaction.message.id == bot_message.id
        and not user.bot
      )

    try:
      await self.bot.wait_for("reaction_add", timeout=timeout, check=check_reaction)
      await bot_message.delete()
    except discord.Forbidden:
      print("Bot doesn't have permission to delete messages.")
    except discord.HTTPException as e:
      print(f"Failed to delete message: {e}")
    except asyncio.TimeoutError:
      await bot_message.delete()

async def setup(bot):
  await bot.add_cog(MessageUtils(bot))