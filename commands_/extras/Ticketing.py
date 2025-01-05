import discord
from discord.ext import commands
from discord.ui import Button, View

class TicketCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command(name="ticketsetup")
  @commands.cooldown(1, 3, commands.BucketType.user)  
  async def ticket_setup(self, ctx):
    embed = discord.Embed(
      title="Create a Ticket",
      description="Click the button below to create a ticket.",
      color=discord.Color.green()
    )
    button = Button(label="Create Ticket", style=discord.ButtonStyle.primary, custom_id="create_ticket")
    View().add_item(button)
    await ctx.send(embed=embed, view=View())

  @commands.Cog.listener()
  async def on_interaction(self, interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component and interaction.data['custom_id'] == 'create_ticket':
      category = discord.utils.get(interaction.guild.categories, name="Tickets")
      if not category:
        category = await interaction.guild.create_category("Tickets")
      overwrites = {
        interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        interaction.user: discord.PermissionOverwrite(read_messages=True)
      }
      channel = await category.create_text_channel(f"ticket-{interaction.user.name}", overwrites=overwrites)
      await channel.send(f"👋 Hello {interaction.user.mention}, your ticket has been created! How can we assist you?")
      await interaction.response.send_message("👌 Your ticket has been created.", ephemeral=True)
      
################ FOR INIT ###############
async def setup(bot):
  await bot.add_cog(TicketCommands(bot))
