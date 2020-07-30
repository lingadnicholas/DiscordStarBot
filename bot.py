import discord
from discord.ext import commands
from discord.utils import find
import pytz 

client = commands.Bot(command_prefix = 's!')

#Get token
file = open("token.txt")
token = file.read()
file.close()

local_tz = pytz.timezone('America/Los_Angeles')
reacts_required = 2

@client.event
async def on_ready():
    print("Bot is online.")

@client.event 
async def on_guild_join(guild):
    create_starboard(guild)
    starboard = find(lambda x: x.name == 'starboard', guild.text_channels)
    if not starboard:
        await guild.create_text_channel('starboard')


@client.event
async def on_raw_reaction_add(payload):
    if str(payload.emoji) == "⭐":
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

        #Check # of star reactions. If more than reacts_required, return
        reaction = None
        for react in message.reactions:
            if str(react.emoji) == "⭐":
                reaction = react
        if not reaction:
            return
        if reaction.count < reacts_required or reaction.count > reacts_required: 
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
        embed=discord.Embed(color=0xffc23d)
        embed.set_thumbnail(url=pfp)
        embed.add_field(name = "Author", value= author.mention, inline=True)
        embed.add_field(name = "Channel", value = channel.mention, inline = True)
        if message.content:
            embed.add_field(name="Message", value=message.content, inline = False)
        if attached:
            embed.set_image(url=attached)
        embed.add_field(name = "Message", value = f"[Jump to]({message.jump_url})", inline = False)

        embed.set_footer(text=f"⭐ | {message_id} • {timestamp} (PDT)")
        await starboard.send(embed=embed)

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

                            

client.run(token)