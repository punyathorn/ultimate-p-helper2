from datetime import datetime
from discord.ext.commands.core import *
from discord.ext.commands import *
from discord_buttons_plugin import *
import discord
import os
from discord.utils import get
from discord import Member
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.ext.commands import has_permissions, BotMissingAnyRole
import nacl
from songs import songAPI 
import time
import random
import asyncio
import pandas as pd
import json
import pytz
import gtts
import youtube_dl
from keep_alive import keep_alive

bot = commands.Bot(command_prefix = "[]")
songsInstance = songAPI()
buttons = ButtonsClient(bot)

@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="[]help"))
  print(f"{bot.user} logged in now!")

@bot.event
async def on_voice_state_update(member, before, after):
  try:
    before_chan = before.channel
    after_chan = after.channel
    # print(before_chan, after_chan)
    if before_chan == None:
      after = member.guild.get_channel(after_chan.id)
      role_after = discord.utils.get(member.guild.roles,name=after.name)
      await member.add_roles(role_after)
      print(after.name)
    elif after_chan == None:
      before = member.guild.get_channel(before_chan.id)
      role_before = discord.utils.get(member.guild.roles,name=before.name)
      await member.remove_roles(role_before)
      print(before.name)
    else:
      after = member.guild.get_channel(after_chan.id)
      before = member.guild.get_channel(before_chan.id)
      role_after = discord.utils.get(member.guild.roles,name=after.name)
      await member.add_roles(role_after)
      role_before = discord.utils.get(member.guild.roles,name=before.name)
      await member.remove_roles(role_before)
      print(before.name, after.name)
  except Exception as error:
    print(error)

@bot.command()
async def role_vc_make(ctx):
  await ctx.send("role_vc_make")
  for vc in ctx.guild.voice_channels:
    role = get(ctx.guild.roles, name=f"{vc}")
    if role == None:
      await ctx.guild.create_role(name=f"{vc}")
      await ctx.send(f"Made role name {vc}")

@bot.command()
async def invite(ctx):
    embed = discord.Embed(title=f"Invite {bot.user.name}", color=0xff0000, description=f"Wanna invite {bot.user.name}, then [click here](https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot)")
    await buttons.send(
    content = None,
    embed = embed,
    channel = ctx.channel.id,
    components = [
      ActionRow([
        Button(
          style = ButtonType().Link,
          label = "Invite",
          url = f"https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot"
        )
      ])
    ]
  )

@bot.command(pass_context=True)
@commands.has_any_role(958223119359811665,983256812964950076)
async def giverole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    if ctx.author.name == user.name:
      await ctx.send(f"hey {ctx.author.name} was given {role.name}")
    else:
      await ctx.send(f"hey {ctx.author.name}, {user.name} was given {role.name}")

@giverole.error
async def giverole_error(ctx, error):
  if isinstance(error, MissingAnyRole):
    embed = discord.Embed(title="Error Missing Role", color= 0xff0000)
    embed.add_field(name="Missing Ultimate P Helper Privilege Commands", value="Giving role is a privilege feature, you need to have role Ultimate P Helper Privilege Commands", inline=False)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
@commands.has_any_role(958223119359811665,983256812964950076)
async def unrole(ctx, user: discord.Member, role: discord.Role):
        await user.remove_roles(role)
        if ctx.author.name == user.name:
          await ctx.send(f"hey {ctx.author.name} was removed from {role.name}")
        else:
          await ctx.send(f"hey {ctx.author.name}, {user.name} was removed from {role.name}")

@unrole.error
async def unrole_error(ctx, error):
  if isinstance(error, MissingAnyRole):
    embed = discord.Embed(title="Error Missing Role", color= 0xff0000)
    embed.add_field(name="Missing Ultimate P Helper Privilege Commands", value="Unrole is a privilege feature, you need to have role Ultimate P Helper Privilege Commands", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def all_alias(ctx):
  embed = discord.Embed(title="All Alias", description=f"All alias in alias.json", colour=discord.Colour.light_gray())
  with open('alias.json', 'r') as openfile:
      json_read = json.load(openfile)
  for i in json_read:
    embed.add_field(name=f"Alias ID: {i}", value=json_read[i], inline=False)
  await ctx.send(embed=embed)

@bot.command()
@commands.has_any_role(958223119359811665,983256812964950076)
async def set_alias(ctx, member: discord.Member, alias):
  id = member.id
  dictionary = {f"{id}" : f"{alias}"}
  with open('alias.json', 'r') as openfile:
    json_read = json.load(openfile)
    dictionary.update(json_read)
  json_object = json.dumps(dictionary, indent = 4)
  with open("alias.json", "w") as outfile:
    outfile.write(json_object)
  await ctx.send(f"Alias {alias} for {member.mention} has been saved in alias.json")

@set_alias.error
async def set_alias_error(ctx, error):
  if isinstance(error, MissingAnyRole):
    embed = discord.Embed(title="Error Missing Role", color= 0xff0000)
    embed.add_field(name="Missing Ultimate P Helper Privilege Commands", value="Set Alias is a privilege feature, you need to have role Ultimate P Helper Privilege Commands", inline=False)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_any_role(958223119359811665,983256812964950076)
async def edit_alias(ctx, member: discord.Member, new_alias):
  with open('alias.json', 'r+') as f:
      data = json.load(f)
      data[f'{member.id}'] = new_alias # <--- add `id` value.
      f.seek(0)        # <--- should reset file position to the beginning.
      json.dump(data, f, indent=4)
      f.truncate()     # remove remaining part
  await ctx.send(f"Alias for {member.mention} has been changed to {new_alias}")

@edit_alias.error
async def edit_alias_error(ctx, error):
  if isinstance(error, MissingAnyRole):
    embed = discord.Embed(title="Error Missing Role", color= 0xff0000)
    embed.add_field(name="Missing Ultimate P Helper Privilege Commands", value="Editing an Alias is a privilege feature, you need to have role Ultimate P Helper Privilege Commands", inline=False)
    await ctx.send(embed=embed)

@bot.command(pass_context= True)
async def info(ctx, member: discord.Member):
  role1 = "".join([str(r.name) for r in member.roles[1:][-1::1]])
  role2 = "".join([str(r.name) for r in member.roles[1:][-2::2]])
  #print(role1, role2, member.created_at)
  embed = discord.Embed(title="User Information", description=f"{member.mention}'s Information", colour=discord.Colour.light_gray())
  embed.set_author(name=member.display_name, icon_url=member.avatar_url)
  embed.add_field(name="Highest Role 1", value=role1, inline=False)
  embed.add_field(name="Highest Role 2", value=role2, inline=False)
  embed.add_field(name="Created at", value=member.created_at, inline=False)
  with open('alias.json', 'r') as openfile:
    json_read = json.load(openfile)
  try:
    alias = json_read[f'{member.id}']
  except:
    alias = "No alias found"
  embed.add_field(name="Alias", value=alias, inline=False)
  embed.timestamp = datetime.now(pytz.timezone('Asia/Bangkok'))
  await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def say(ctx, *, text):
    try:
        channel = ctx.author.voice.channel
        await channel.connect()
    except:
        pass

    tts = gtts.gTTS(text=text, lang="en")
    tts.save(f'speech.mp3')
    channel = ctx.author.voice.channel
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client == None:
        await channel.connect()
        voice_client = get(bot.voice_clients, guild=ctx.guild)

    audio_source = discord.FFmpegPCMAudio(f'speech.mp3')
    if not voice_client.is_playing():
        voice_client.play(audio_source, after=None)
        await asyncio.sleep(25)
        os.remove(f"speech.mp3")

@bot.command(pass_context=True)
@commands.has_any_role(958223119359811665,983256812964950076)
async def makechan(ctx, name, channeltype):
  guild = ctx.message.guild
  if channeltype.lower() == 'text':
    await guild.create_text_channel(name)
    await ctx.send(f"{ctx.author.mention} Text channel name {name} was created!")
  elif channeltype.lower() == 'voice' or channeltype.lower() == 'vc':
    await guild.create_voice_channel(name)
    await ctx.send(f"{ctx.author.mention} Voice channel name {name} was created!")

@makechan.error
async def makechan_error(ctx, error):
  if isinstance(error, MissingAnyRole):
    embed = discord.Embed(title="Error Missing Role", color= 0xff0000)
    embed.add_field(name="Missing Ultimate P Helper Privilege Commands", value="Making a channel is a privilege feature, you need to have role Ultimate P Helper Privilege Commands", inline=False)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
@commands.has_any_role(958223119359811665,983256812964950076)
async def deltextchan(ctx, channel: discord.TextChannel):
  await channel.delete()
  await ctx.send("Successfully deleted the channel!")

@deltextchan.error
async def deltextchan_error(ctx, error):
  if isinstance(error, MissingAnyRole):
    embed = discord.Embed(title="Error Missing Role", color= 0xff0000)
    embed.add_field(name="Missing Ultimate P Helper Privilege Commands", value="Deleting a text channel is a privilege feature, you need to have role Ultimate P Helper Privilege Commands", inline=False)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_any_role(958223119359811665,983256812964950076)
async def removechannel(ctx, channel_id: int):
    channel = bot.get_channel(channel_id)
    await channel.delete()
    await ctx.send("Successfully deleted the channel!")

@removechannel.error
async def removechannel_error(ctx, error):
  if isinstance(error, MissingAnyRole):
    embed = discord.Embed(title="Error Missing Role", color= 0xff0000)
    embed.add_field(name="Missing Ultimate P Helper Privilege Commands", value="Removing a channel is a privilege feature, you need to have role Ultimate P Helper Privilege Commands", inline=False)
    await ctx.send(embed=embed)

@bot.command(pass_context= True,aliases=["m", "M", "Mute"])
@commands.has_any_role(958223119359811665)
async def vcmem(ctx, status, member: discord.Member):
  if status.lower() == 'm':
    await member.edit(mute=True)
    await ctx.send(f"Muted 1 user {member.mention}")
  if status.lower() == 'um':
    await member.edit(mute=False)
    await ctx.send(f"Unmuted 1 user {member.mention}")
  if status.lower() == 'd':
    await member.edit(deafen=True)
    await ctx.send(f"Deafened 1 user {member.mention}")
  if status.lower() == 'ud':
    await member.edit(deafen=False)
    await ctx.send(f"Undeafened 1 user {member.mention}")

@vcmem.error
async def vcmem_error(ctx, error):
  if isinstance(error, MissingAnyRole):
    embed = discord.Embed(title="Error Missing Role", color= 0xff0000)
    embed.add_field(name="Missing Ultimate P Helper Privilege Commands", value="VC member controls are privilege features, you need to have role Ultimate P Helper Privilege Commands", inline=False)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
@commands.has_any_role(958223119359811665,983256812964950076)
async def chnick(ctx, member: discord.Member,*, nickname):
  if nickname.lower() == 'none':
      nick_change = ''
  else:
      nick_change = nickname
  if str(member.nick) != str(nickname):
    await ctx.send(f'Nickname was changed to {nickname} ')
    await member.edit(nick=nick_change)     
  else:
      await ctx.send(f"{member.mention} currently has this nickname!")

@chnick.error
async def chnick_error(ctx, error):
  if isinstance(error, MissingAnyRole):
    embed = discord.Embed(title="Error Missing Role", color= 0xff0000)
    embed.add_field(name="Missing Ultimate P Helper Privilege Commands", value="Changing nicknames are privilege features, you need to have role Ultimate P Helper Privilege Commands", inline=False)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
@commands.has_any_role(958223119359811665,983256812964950076)
async def troll(ctx, member: discord.Member):
  data = pd.read_csv('nicknames.csv')
  DATA = data['Names'].unique()
  for i in range(10):
    r = random.randint(0,18)
    await member.edit(nick=DATA[r])
    time.sleep(1)
  await ctx.send(f"""Troll Complete\nChanged nickname of {member.mention} 10 times
  """)

@troll.error
async def troll_error(ctx, error):
  if isinstance(error, MissingAnyRole):
    embed = discord.Embed(title="Error Missing Role", color= 0xff0000)
    embed.add_field(name="Missing Ultimate P Helper Privilege Commands", value="Nickname trolling is a privilege feature, you need to have role Ultimate P Helper Privilege Commands", inline=False)
    await ctx.send(embed=embed)

@bot.command()
@has_permissions(kick_members=True)
@commands.has_any_role(958223119359811665,983256812964950076)
async def kick(ctx, member: discord.Member, *, reason=None):
  await member.kick(reason=reason)
  await ctx.send(f"User {member} has been kicked")

@kick.error
async def kick_error(ctx, error):
  if isinstance(error, MissingAnyRole):
    embed = discord.Embed(title="Error Missing Role", color= 0xff0000)
    embed.add_field(name="Missing Ultimate P Helper Privilege Commands", value="Kicking members is a privilege feature, you need to have role Ultimate P Helper Privilege Commands", inline=False)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_any_role(958223119359811665)
async def kickmem(ctx, par):
  if par == "all":
    for members in ctx.author.voice.channel.members:
      await members.move_to(None)

@kickmem.error
async def kickmem_error(ctx, error):
  if isinstance(error, MissingAnyRole):
    embed = discord.Embed(title="Error Missing Role", color= 0xff0000)
    embed.add_field(name="Missing Ultimate P Helper Privilege Commands", value="Kicking all VC members is a privilege feature, you need to have role Ultimate P Helper Privilege Commands", inline=False)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def ping(ctx, member: discord.Member, times, *, par):
  if int(times) >= 25:
    await ctx.send("Ping more than 25 times are not allowed")
  else:
    for i in range(int(times)):
      await ctx.send(f"{member.mention} {par}")

@bot.command(pass_context= True)
@commands.has_any_role(958223119359811665)
async def logout(ctx):
  try:
    await ctx.send("Logging out")
    await ctx.send("Log out successful")
    await bot.logout()
  except:
    await ctx.send("Logout unsuccessful")

@logout.error
async def logout_error(ctx, error):
  if isinstance(error, MissingAnyRole):
    embed = discord.Embed(title="Error Missing Role", color= 0xff0000)
    embed.add_field(name="Missing Ultimate P Helper Privilege Commands", value="Bot logout is a privilege feature, you need to have role Ultimate P Helper Privilege Commands", inline=False)
    await ctx.send(embed=embed)

@bot.command(pass_context= True)
async def spamgif(ctx,url ,times):
  if int(times) >= 35:
    await ctx.send("No more than 35 times!")
  else:
    for i in range(int(times)):
      await ctx.send(url)

@bot.command(pass_context=True)
async def avatar(ctx, member: discord.Member):
  await ctx.send(member.avatar_url)

@bot.command(pass_context=True)
async def purge(ctx, *, amount):
  await ctx.channel.purge(limit= int(amount)+1)

# @bot.command() 
# async def play(ctx,* ,search: str):
#     await songsInstance.play(ctx, search)

# @bot.command() 
# async def stream(ctx,* ,url):
#     await songsInstance.stream(ctx, url)

# @bot.command()
# async def stop(ctx):
#     await songsInstance.stop(ctx)

# @bot.command()
# async def pause(ctx):
#     await songsInstance.pause(ctx)

# @bot.command()
# async def resume(ctx):
#     await songsInstance.resume(ctx)

# @bot.command()
# async def leave(ctx):
#     await songsInstance.leave(ctx)

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename


@bot.command(name='play_song', help='To play song')
async def play(ctx,url):
    # try :
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))
    # except Exception as e:
    #     await ctx.send(str(e))


@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")



@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


@bot.command()
async def queueList(ctx):
    await songsInstance.queueList(ctx)

@bot.command()
async def skip(ctx):
    await songsInstance.skip(ctx)



@bot.command()
async def gif(ctx):
  data = pd.read_csv('gif.csv')
  DATA = data['Links'].unique()
  Number_of_link = len(DATA)
  r = random.randint(0, Number_of_link)
  await ctx.send(DATA[r])

@bot.command(pass_context= True)
@commands.has_any_role(958223119359811665)
async def move(ctx, member: discord.Member, *,channel: discord.VoiceChannel=None):
  await member.move_to(channel)

@move.error
async def move_error(ctx, error):
  if isinstance(error, MissingAnyRole):
    embed = discord.Embed(title="Error Missing Role", color= 0xff0000)
    embed.add_field(name="Missing Ultimate P Helper Privilege Commands", value="Moving VC members is a privilege feature, you need to have role Ultimate P Helper Privilege Commands", inline=False)
    await ctx.send(embed=embed)

@bot.command(pass_context= True)
@commands.has_any_role(958223119359811665)
async def kickout(ctx, member: discord.Member):
  await member.move_to(None)

@kickout.error
async def kickout_error(ctx, error):
  if isinstance(error, MissingAnyRole):
    embed = discord.Embed(title="Error Missing Role", color= 0xff0000)
    embed.add_field(name="Missing Ultimate P Helper Privilege Commands", value="Kicking a VC member is a privilege feature, you need to have role Ultimate P Helper Privilege Commands", inline=False)
    await ctx.send(embed=embed)

@bot.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
@commands.has_any_role(958223119359811665)
async def mute(ctx, member: discord.Member= None, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    if mutedRole not in member.roles:
      embed = discord.Embed(title="Muted", description=f"{member.mention} was muted ", color= 0xff0000)
      embed.add_field(name="Reason:", value=reason, inline=False)
      await member.add_roles(mutedRole, reason=reason)
      await ctx.send(embed=embed)
      embed2 = discord.Embed(title="Muted", description=f"Sorry, you were muted.", color= 0xff0000)
      embed2.add_field(name="Reason: ", value=reason, inline=False)
      await member.send(embed=embed2)
    else:
      embed3 = discord.Embed(title="Already Muted", description=f"{member.mention} was already muted. No need to mute again!", color= 0xffff00)
      await ctx.send(embed=embed3)

@mute.error
async def mute_error(ctx, error):
  if isinstance(error, MissingAnyRole):
    embed = discord.Embed(title="Error Missing Role", color= 0xff0000)
    embed.add_field(name="Missing Ultimate P Helper Privilege Commands", value="Muting a member is a privilege feature, you need to have role Ultimate P Helper Privilege Commands", inline=False)
    await ctx.send(embed=embed)

@bot.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
@commands.has_any_role(958223119359811665)
async def unmute(ctx, member: discord.Member= None):
  mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
  if mutedRole not in member.roles:
    embed3 = discord.Embed(title="Not muted", description=f"{member.mention} isn't muted. No need to unmute!",colour=0xffff00)
    await ctx.send(embed=embed3)
  else:
    embed = discord.Embed(title="Unmute", description=f"Unmuted {member.mention}",colour=0x00ff00)
    await ctx.send(embed=embed)
    await member.remove_roles(mutedRole)
    embed2 = discord.Embed(title="Unmute", description=f"Congrats, You are unmuted!",colour=0x00ff00)
    await member.send(embed=embed2)

@unmute.error
async def unmute_error(ctx, error):
  if isinstance(error, MissingAnyRole):
    embed = discord.Embed(title="Error Missing Role", color= 0xff0000)
    embed.add_field(name="Missing Ultimate P Helper Privilege Commands", value="Unmuting a member is a privilege feature, you need to have role Ultimate P Helper Privilege Commands", inline=False)
    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
  Crosschat1 = bot.get_channel(957865189729001513)
  Crosschat2 = bot.get_channel(957865299598790656)
  if message.author.id == 865470330998358066:
      return
  elif message.channel.id == 957865189729001513:
      embed = discord.Embed(title="Message from Crosschat1", description=f"**{message.content}**", color=discord.Colour.random())
      embed.set_author(name=message.author, icon_url=message.author.avatar_url)
      embed.set_footer(text="Inspired from nextcord server")
      embed.timestamp = datetime.now(pytz.timezone('Asia/Bangkok'))
      await Crosschat2.send(embed=embed)
  elif message.channel.id == 957865299598790656:
      embed = discord.Embed(title="Message from Crosschat2", description=f"**{message.content}**", color=discord.Colour.random())
      embed.set_author(name=message.author, icon_url=message.author.avatar_url)
      embed.set_footer(text="Inspired from nextcord server")
      embed.timestamp = datetime.now(pytz.timezone('Asia/Bangkok'))
      await Crosschat1.send(embed=embed)
  await bot.process_commands(message)

ffmpeg_options = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5" ## song will end if no this line
}

@bot.command()
async def supported_intents(ctx):
    Patterns = []
    f = open('intents.json')
    data = json.load(f)
    intents = data["intents"]
    for i in range(len(intents)):
        patterns = data["intents"][i]["patterns"]
        Patterns.append(patterns)
    r =  Patterns[0]+Patterns[1]+Patterns[2]
    res = " ".join(r)
    #print(res)
    embed = discord.Embed(title="The Intents (Commands)", description=f"The commands to talk to the bot using <@!865470330998358066>", colour=0xffff00)
    embed.add_field(name="Commands", value="Including Initialized Capital Letters: {}".format(res), inline=False)
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      await ctx.send(f"the command is in cooldown wait for {round(error.retry_after, 2)} seconds ")
      
keep_alive()
secret = os.environ['TOKEN']

bot.run(secret)