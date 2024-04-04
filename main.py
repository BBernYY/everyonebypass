import discord
from datetime import datetime
import discord.utils
from discord.ext import commands
import json
import os
bot = commands.Bot(command_prefix='!')
bot.remove_command('help')
data = json.load(open("data.json"))
def get_list(dictionary, key):
  output = []
  for k, v in dictionary.items():
    output.append(v[key])
  return output
@bot.event
async def on_ready():
  print(f'startup at {datetime.now()}')
@bot.command()
async def help(ctx, command=None):
    if command:
      embed=discord.Embed(title=command, description=data["commands"][command]["description"])
      embed.add_field(name="usage", value=data["commands"][command]["usage"])
    else:
      embed=discord.Embed(title='Help', description='commands and the description', color=0xFF5733)
      embed.add_field(name="command", value="\n".join(list(data["commands"].keys())))
      embed.add_field(name="description", value="\n".join(get_list(data["commands"], "description")))
      embed.add_field(name="usage", value="\n".join(get_list(data["commands"], "usage")))
    await ctx.channel.send("I'm glad to help!", embed=embed)
# connect token
bot.run(TOKEN)