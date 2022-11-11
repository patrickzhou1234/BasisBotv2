import discord
from discord.ext import commands
import time

TOKEN = 'token lol'

bot = commands.Bot(command_prefix='!')
cont = ""
reactmsg = ""
rolemsg = ""

@bot.command()
async def nickname(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)

@bot.command()
async def reaction_roles(message):
    if message.author.guild_permissions.administrator:
        embedVar = discord.Embed(title="Role", description="undefined", color=0x00ff00)
        embedVar.add_field(name="Emoji to add", value="undefined", inline=False)
        embedVar.add_field(name="Channel", value="undefined", inline=False)
        await message.channel.send("Please provide the following information separated with space")
        await message.channel.send(embed=embedVar)
        def check(m):
            return m.content and m.channel == message.channel and m.author == message.author
        msg = await bot.wait_for('message', check=check)
        global cont
        cont = msg.content.split()
        embedVar2 = discord.Embed(title="Role", description=cont[0], color=0x00ff00)
        embedVar2.add_field(name="Emoji to add", value=cont[1], inline=False)
        embedVar2.add_field(name="Channel", value=cont[2], inline=False)
        await message.channel.send(embed=embedVar2)
        global reactmsg
        reactmsg = await message.channel.send("Does this seem right?")
        await reactmsg.add_reaction("✅")
        await reactmsg.add_reaction("❌")
    else:
        await message.channel.send("Lmao u thought")

@bot.command(name="Do-My-Homework")
async def doMyHomework(ctx):
    await ctx.channel.send("Search it up on https://google.com lmao like r u dumb or stupid")

@bot.command(name="spam-arunachalam")
async def skillIssue(ctx):
    arunachalam = bot.fetch_user(726151990228549705)
    await ctx.channel.send("On it...")
    try:
        for i in range(25):
            await arunachalam.send("I THINK theres an issue in ur skill!")
            time.sleep(2)
        await ctx.channel.send("SUCCESSFULLY SPAMMED ARUNACHALAM")
    except:
        await ctx.channel.send(":( I think he blocked me :cry:")

@bot.event
async def on_reaction_add(reaction, user):
  if reaction.emoji == '✅' and user.id!=1009665998397390869 and reaction.message == reactmsg:
      channel = bot.get_channel(int(cont[2][2:-1]))
      global rolemsg
      rolemsg = await channel.send("If you want the "+cont[0]+" role, please react with "+cont[1]+" to this message.")
      await rolemsg.add_reaction(cont[1])
      await reactmsg.remove_reaction("❌", reactmsg.author)
  elif reaction.emoji == '❌' and user.id!=1009665998397390869 and reaction.message == reactmsg:
      await reaction.message.channel.send("Ok, Cancelled")
      await reactmsg.remove_reaction("✅", reactmsg.author)
  elif reaction.emoji == cont[1] and user.id!=1009665998397390869 and reaction.message == rolemsg:
      role = discord.utils.get(user.guild.roles, name=cont[0])
      await user.add_roles(role)

@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        await message.channel.send('Dont ping me or.')

    await bot.process_commands(message)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you when you're awake :("))
    
@bot.command()
@commands.has_permissions(administrator=True)
async def delete(ctx, arg):
    limit = int(arg)
    await ctx.channel.purge(limit=limit)

bot.run(TOKEN)
