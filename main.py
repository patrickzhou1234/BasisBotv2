import os
import discord
from discord.ext import commands

TOKEN = 'token'

bot = commands.Bot(command_prefix='!')

@bot.command()
async def delete(ctx, arg):
    limit = int(arg)
    await ctx.channel.purge(limit=limit)

@bot.command()
async def nickname(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)

@bot.event
async def on_message_delete(message):
  await message.channel.send(str(message.author)+" deleted his message '"+message.content+"'")

@bot.event
async def on_message_edit(message_before, message_after):
        author = message_before.author
        guild = message_before.guild.name
        channel = message_before.channel
        if channel.id == 1009605535647146055 and author.id!=270904126974590976:
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
