import asyncio 
import discord
import os
from discord.ext import commands
from discord.utils import find
import random
import pytz 
from keep_alive import keep_alive
from datetime import datetime, time, timedelta

nico_id = 186680853131165696
client = commands.Bot(command_prefix = 'a!')
client.remove_command('help')

local_tz = pytz.timezone('America/Los_Angeles')
reacts_required = 2

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.online, activity=discord.Streaming(name = "Permission To Dance", url = "https://www.youtube.com/watch?v=CuklIb9d3fI"))
    print("Bot is online.")


@client.event 
async def on_guild_join(guild):
    starboard = find(lambda x: x.name == 'starboard', guild.text_channels)
    if not starboard:
        await guild.create_text_channel('starboard')

@client.event
async def on_raw_reaction_add(payload):
    emote = str(payload.emoji)
    if emote == "⭐":
        #Gather all data: the message the user reacted to, the server it's in, the channel it's in, etc.
        #All data necessary to create the embed.
        channel = client.get_channel(payload.channel_id)
        message_id = payload.message_id
        guild = client.get_guild(payload.guild_id)
        message = await channel.fetch_message(message_id)
        author = message.author
        pfp = str(author.avatar_url)
        attached = None
        if message.attachments:
            attached = message.attachments[0].url

        #Check # of star reactions. If more than reacts_required, return. (But I still need to check if it needs to be added. There has been a problem where if people happen to react at the same time, it won't get added to #starboard.)
        reaction = None
        for react in message.reactions:
            if str(react.emoji) == "⭐":
                reaction = react
        if not reaction:
            return
        
        if reaction.count < reacts_required or reaction.count > reacts_required: 
          message_id = payload.message_id
          str_id = str(message_id)
          starboard = find(lambda x: x.name == 'starboard', guild.text_channels)
          message = None


          async for msg in starboard.history(limit=20):
              embed = msg.embeds
              if msg.author != client.user: 
                  continue
              if not embed:
                  continue
              embed = embed[0]
              if str_id in str(embed.footer):
                  message = msg
                  break
          if message != None:
              return

        #Get date
        timestamp = message.created_at
        local_dt = timestamp.replace(tzinfo=pytz.utc).astimezone(local_tz)
        local_tz.normalize(local_dt)
        timestamp = str(local_dt)[:10]

        #Create starboard channel if not already created
        starboard = find(lambda x: x.name == 'starboard', guild.text_channels)
        if not starboard:
            starboard = await guild.create_text_channel('starboard')

        #Create embed
        nico = f"{(await client.fetch_user(nico_id)).name}#{str((await client.fetch_user(nico_id)).discriminator)}"
        embed=discord.Embed(color=0xffc23d)
        embed.set_thumbnail(url=pfp)
        embed.add_field(name = "Author", value= author.mention, inline=True)
        embed.add_field(name = "Channel", value = channel.mention, inline = True)
        if message.content:
            embed.add_field(name="Message", value=message.content, inline = False)
        if attached:
            embed.set_image(url=attached)
        embed.add_field(name = "Message", value = f"[Jump to]({message.jump_url})", inline = False)

        embed.set_footer(text=f"⭐ | {message_id} • {timestamp} (PDT) | {nico}")
        await starboard.send(embed=embed)
    elif emote == "😡": 
      channel = client.get_channel(payload.channel_id)
      message_id = payload.message_id
      message = await channel.fetch_message(message_id)
      reaction = None
      for react in message.reactions:
        if str(react.emoji) == "😡":
          reaction = react
      if not reaction:
        return
      if reaction.count == 2:
        await channel.send("HAJIMA :rage:")
        return 


@client.event
async def on_raw_reaction_remove(payload):
    if str(payload.emoji) == "⭐":
        #Gather message data: the message the user reacted to, the server it's in, the channel it's in, etc.
        #All data necessary to create the embed.
        channel = client.get_channel(payload.channel_id)
        message_id = payload.message_id
        str_id = str(message_id)
        guild = client.get_guild(payload.guild_id)
        message = await channel.fetch_message(message_id)
        #Check # of star reactions. If less than reacts_required, 
        reaction = None
        starboard = find(lambda x: x.name == 'starboard', guild.text_channels)
        if not starboard:
            starboard = await guild.create_text_channel('starboard')
        for react in message.reactions:
            if str(react.emoji) == "⭐":
                reaction = react
        #Find the message to remove
        if not reaction or reaction.count < reacts_required:
            message = None
            async for msg in starboard.history(limit=200):
                embed = msg.embeds
                if msg.author != client.user: 
                    continue
                if not embed:
                    continue
                embed = embed[0]
                if str_id in str(embed.footer):
                    message = msg
                    break
            if not message:
                return
            await message.delete()


#####################
#This stuff is just for fun. Ignore these commands. 
######################
@client.command()
async def ram(ctx): 
  if ctx.author.id == 145308906887839744: 
    await ctx.send("")

@client.command()
async def celine(ctx): 
  if ctx.author.id == 196442874999603201: 
    await ctx.send("Jungkook misses you Celine! :revolving_hearts:")
  else: 
    await ctx.send("Do you know where Celine is? Jungkook is looking for her :(")

@client.command()
async def cameron(ctx):
  if ctx.author.id == 144624264836808704: 
    responses = [
                'stan us cameron we know you want to :)',
                'JUNGKOOK LOVES U MORE THAN CELINE'
                ]
    await ctx.send(f'{random.choice(responses)}')
  else: 
    await ctx.send("When is Cameron gonna stan :rage:")

@client.command()
#Command use: a!deline
async def deline(ctx):
  if ctx.author.id == 186998666546905088:
    responses = [
                'You can do it, Adeline! :)',
                'May Firestar be with you, Adeline.',
                "https://cdn.discordapp.com/attachments/194265532285976578/751672737176748102/Egw3elHWsAM38U4.png",
                "I want to be ur best friend Adeline :-)",
                ]
    await ctx.send(f'{random.choice(responses)}')
  else: 
    await ctx.send("Please tell Adeline she's doing a good job :))")

@client.command()
async def mir(ctx):
  if ctx.author.id == 183679553556840448:
    await ctx.send("fart")

@client.command()
async def noah(ctx):
  if ctx.author.id == 369273450814111753:
    responses = [
                'Hi Noah :revolving_hearts:',
                'Yes baby? :heart:',
                "I'll go get Namjoon for you ;)",
                "I love you Noah :heart:",
                "Wanna :basketball: together? :)",
                "Hope u have a good day :revolving_hearts:",
                "Have you been drinking enough water Noah?? :)",
                "Bro I just feel so empty and I wish that I could just feel some love for once in my life. Nothing feels like it's worth it anymore and there's nothing that makes me happy anymore :sob: - Neeko :heart: No I'm not ok x"
                ]
    await ctx.send(f'{random.choice(responses)}')
  else: 
    await ctx.send("You're not Noah. :rage: I want to talk to Noah :heart:")

@client.command()
async def neeko(ctx):
  if ctx.author.id == 186680853131165696:
    await ctx.send("test")
  
@client.command()
async def dom(ctx):
  if ctx.author.id == 263798100064337920:
    await ctx.send("Hey! Want to collab on Paper Planes 2?")
  else: 
    await ctx.send("https://open.spotify.com/album/0byPMLxKOQ9G0r9sbaJNFw?si=BcifDbR8SRmTzA2GdlU-rQ")

@client.command()
async def hayden(ctx):
  if ctx.author.id == 146425316313661441: 
    responses = [
                "Get your toes out I'm getting Celine :)",
                "I'll tell Dubchaeng you said hi :)"
                ]
    await ctx.send(f'{random.choice(responses)}')
  else: 
    await ctx.send("where's my white boy :(")

@client.command()
async def james(ctx):
  if ctx.author.id == 188171146552672256: 
    await ctx.send("uhhh dm nico what u want me to put")

@client.command() 
async def msg(ctx, arg1, *, txt): 
  #527584900757454883 BANGER
  #746917955069018184 FISHELL GENERAL
  if ctx.author.id == 186680853131165696: 
    channel = client.get_channel(int(arg1)) 
    await channel.send(txt)

voice_client = 0
@client.command()
async def join(ctx, arg1):
    if ctx.author.id == 186680853131165696: 
      channel = client.get_channel(int(arg1))
      global voice_client 
      voice_client = await channel.connect()

@client.command()
async def leave(ctx):
    if ctx.author.id == 186680853131165696: 
      global voice_client
      await voice_client.disconnect()
    

#CHANGE AT DAYLIGHT SAVINGS
WHEN = time(16, 0, 0)  # 09:00 AM PDT
daily_id = 820870366896717824 # Put your channel id here
async def called_once_a_day():  # Fired every day
    await client.wait_until_ready()  # Make sure your guild cache is ready so the channel can be found via get_channel
    channel = client.get_channel(daily_id) # Note: It's more efficient to do bot.get_guild(guild_id).get_channel(daily_id) as there's less looping involved, but just get_channel still works fine
    await channel.send("<@186680853131165696> <@299354510583922690> <@691761097140731986> Daily https://webstatic-sea.mihoyo.com/ys/event/signin-sea/index.html?act_id=e202102251931481&lang=en-us")


async def background_task():
    now = datetime.utcnow()
    if now.time() > WHEN:  # Make sure loop doesn't start after {WHEN} as then it will send immediately the first time as negative seconds will make the sleep yield instantly
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start 
    while True:
        now = datetime.utcnow() # You can do now() or a specific timezone if that matters, but I'll leave it with utcnow
        target_time = datetime.combine(now.date(), WHEN)  # 6:00 PM today (In UTC)
        seconds_until_target = (target_time - now).total_seconds()
        await asyncio.sleep(seconds_until_target)  # Sleep until we hit the target time
        await called_once_a_day()  # Call the helper function that sends the message
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start a new iteration


#####################
#End of fun# 
######################
keep_alive()
client.loop.create_task(background_task())        
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
