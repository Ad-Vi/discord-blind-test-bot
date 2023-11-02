import discord
from discord.ext import commands
from discord.utils import get
import asyncio
from music_acquisition import Music, new_music, playlist, full_discography

prefix= "$"
intents = discord.Intents.all() 
intents.message_content = True
bot=commands.Bot(command_prefix=prefix, intents=intents)
 
@bot.command()
async def newmusic(ctx, link=None, title=None, author=None, playlist=None):
    if link == None or len(link) == 0 :
        await ctx.send("You need to pass at least the youtube link of the music \n use : $newmusic <link> <title> <author> <playlist>")
        pass
    new_music(link, title, author, playlist)
    print(link, title, author, playlist)
    await ctx.send(f'Music {title} created with the link {link}')
    
@bot.command()
async def test(ctx, arg):
    print("test")
    await ctx.send(arg)

@bot.command(
    name='vuvuzela',
    description='Plays an awful vuvuzela in the voice channel',
    pass_context=True,
)
async def vuvuzela(ctxt):
    # grab the user who sent the command
    user=ctxt.message.author
    voice_channel=user.voice.channel
    channel=None
    # only play music if user is in a voice channel
    # grab user's voice channel
    channel=voice_channel
    print(('User is in channel: '+ str(channel)))
    if not channel:
        await ctxt.send("You are not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctxt.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    
    voice.play(discord.FFmpegPCMAudio(executable='/usr/bin/ffmpeg', source="./audios/vuvuzela.mp4"))
    await asyncio.sleep(10)  # play for 10 seconds
    if voice.is_playing():
        voice.stop()
    await voice.disconnect()

@bot.command(
    name='blindtest',
    description='Launch the blindtest',
    pass_context=True,
)
async def blindtest(ctxt, playlist_name=None, nb_music=10):
    # grab the user who sent the command
    user=ctxt.message.author
    voice_channel=user.voice.channel
    channel=None
    # only play music if user is in a voice channel
    # grab user's voice channel
    channel=voice_channel
    print(('User is in channel: '+ str(channel)))
    if not channel:
        await ctxt.send("You are not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctxt.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    
    await ctxt.send("Let's go for the blind test !")
    #get playlist
    if playlist_name == None:
        discography = full_discography()
    else:
        discography = playlist(playlist_name)
    
    i = 0
    l = discography.get_length()
    while i < nb_music and i < l:
        # get one random music
        music = discography.get_one_music()
        print(music.title)
        voice.play(discord.FFmpegPCMAudio(executable='/usr/bin/ffmpeg', source=music.path))
        await asyncio.sleep(10)
        if voice.is_playing():
            voice.stop()
        i += 1
    await voice.disconnect()

@bot.command(
    name='fin_blindtest',
    description='End the blindtest',
    pass_context=True,
)
async def fin_blindtest(ctxt):
    # Disconnect the bot from voice channel
    voice = get(bot.voice_clients, guild=ctxt.guild)
    if voice and voice.is_connected():
        if voice.is_playing():
            voice.stop()
    await voice.disconnect()
 
 
@bot.event
async def on_ready():
    print("Le blind Test est prêt !")
    await bot.change_presence(activity=discord.Game(name="Blind Test"))
    

@bot.event
async def on_message(message):
    if message.content == "Ping":
        await message.channel.send("Pong")
    print(message.content)
    await bot.process_commands(message)
        
bot.run('MTE2ODU2Njk4OTA2MTYyMzkzOA.G4s-Xa.wx8GNcJz2a6K_30-6669pe_oLwG_ZjKxjn8Eeo')