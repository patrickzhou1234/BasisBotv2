import discord
from discord.ext import commands

TOKEN = 'token lol'

bot = commands.Bot(command_prefix='!')
cont = ""
reactmsg = ""
rolemsg = ""

@bot.command()
async def delete(ctx, arg):
    limit = int(arg)
    await ctx.channel.purge(limit=limit)

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
async def on_message_delete(message):
  await message.channel.send(str(message.author)+" deleted his message '"+message.content+"'")

@bot.event
async def on_message_edit(message_before, message_after):
        author = message_before.author
        guild = message_before.guild.name
        channel = message_before.channel
        if author.id!=270904126974590976 and author.id!=1009665998397390869:
            await channel.send(f"""{author} edited his original message: '{message_before.content}' to an Edited Message: '{message_after.content}'""")

@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        await message.channel.send('Dont ping me or.')

    await bot.process_commands(message)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you when you're awake :("))

bot.run(TOKEN)
