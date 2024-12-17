import asyncio

TRASHCAN_EMOJI = "🗑️"  # Trashcan emoji

async def sendtemp(channel, content, timeout=60):
  bot_message = await channel.send(content)
  await bot_message.add_reaction(TRASHCAN_EMOJI)
  def check_reaction(reaction, user):
    return (
      str(reaction.emoji) == TRASHCAN_EMOJI
      and reaction.message.id == bot_message.id
      and not user.bot  
    )
  try:
    await bot_message.bot.wait_for("reaction_add", timeout=timeout, check=check_reaction)
    await bot_message.delete()
  except asyncio.TimeoutError:
    await bot_message.delete()