import discord
from datetime import datetime
import discord.utils
from discord.ext import commands
import json
import os
bot = commands.Bot(command_prefix=';', intents=discord.Intents.all())
bot.remove_command('help')
data = json.load(open("data.json"))
def get_list(dictionary, key):
  output = []
  for k, v in dictionary.items():
    output.append(v[key])
  return output
def remove_list(li):
  return " ".join(li)
@bot.event
async def on_ready():
  global me
  me = bot.user
  print(f'startup at {datetime.now()} using @{me.name}#{me.discriminator}')
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

@bot.command()
async def dm(ctx, victims, *content):
  content = remove_list(content)
  if victims == 'all':
    victims = ctx.guild.members
  else:
    victims = victims.split(',')
    victims = [discord.utils.get(bot.get_all_members(), name=i) for i in victims]
  for i in victims:
    if not i.bot:
      try:
        chan = await i.create_dm()
        await chan.send(content)
        await ctx.channel.send("oki!!! I just sent `"+i.name+"` this:\n`"+content+"`")
      except:
        await ctx.channel.send("`"+i.name+"` probably disabled their dm's (bitch)")
    


# connect token
@bot.event
async def on_message(message):
    if not message.guild and not message.content.startswith(';') and not message.author.id == me.id:
        print(message.author.name+": "+message.content)
    else:
      await bot.process_commands(message)
with open('token.env') as f:
  token = f.read()
bot.run(token)